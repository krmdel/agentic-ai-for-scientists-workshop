# Week 4: `jobs/`: the real training run (Hugging Face Jobs)

The Colab notebooks (`01`–`03`) teach the mechanics on a tiny `max_steps` budget so they
finish in class. **This folder is the "do it for real" path:** run a full training job on
HF's managed GPUs, headless, and push a finished model to the Hub. That Hub model is the
shared artifact **Week 5** evaluates and **Week 6** deploys.

These are **PEP 723 uv scripts** (dependencies declared inline), the same format as the
neuralmaze finetuning reference. `hf jobs uv run` ships the script to an HF GPU, installs
the deps, runs it, and streams the logs back.

## Two paths, on purpose

| | **Free Colab T4** (notebooks) | **HF Jobs** (this folder) |
|---|---|---|
| Cost | free, no account | **Pro account ($9/mo) + pay-per-minute compute** |
| Best for | learning the mechanics in class | the real run that produces the Hub model |
| Budget | tiny `max_steps` | full epoch(s) |
| Output | local files, may expire | a model on the Hub, permanent |

> **HF Jobs is a paid feature.** It needs a [Pro / Team / Enterprise](https://huggingface.co/pro)
> account, then bills [per minute](https://huggingface.co/docs/hub/jobs-pricing) for the GPU.
> It is **not** the free in-class path, it's how the instructor (or a Pro participant)
> produces the real models. Keep Colab as the default for the room.

## Cost (it's small for a 0.6B model)

| flavor | GPU | $/hour | a real Qwen3-0.6B run |
|---|---|---|---|
| `t4-small` | T4 16GB | $0.40 | ~$0.20–0.40 |
| `a10g-small` | A10G 24GB | $1.00 | **~$0.50–1.00** (recommended) |
| `a100-large` | A100 80GB | $2.50 | fastest, overkill here |

Full list: `hf jobs hardware`.

## Prerequisites

```bash
pip install -U huggingface_hub
hf auth login                      # a token with WRITE scope
# Pro account required for Jobs: https://huggingface.co/pro
```

You also need the structured dataset on the Hub. In **Notebook 00**, uncomment the final
cell to `push_to_hub("YOUR_USERNAME/medquad-structured")`. The job trains on that. (If you
skip it, the script falls back to formatting raw `lavita/MedQuAD`, so it still runs, just
without your Gemini-labeled schema.)

## Train (one script, three methods)

```bash
# Full supervised fine-tuning
hf jobs uv run --flavor a10g-small --timeout 2h -s HF_TOKEN=$HF_TOKEN \
  train.py -- --method full \
  --dataset_name YOUR_USERNAME/medquad-structured \
  --hub_model_id YOUR_USERNAME/qwen3-medquad-full

# LoRA
hf jobs uv run --flavor a10g-small --timeout 2h -s HF_TOKEN=$HF_TOKEN \
  train.py -- --method lora \
  --dataset_name YOUR_USERNAME/medquad-structured \
  --hub_model_id YOUR_USERNAME/qwen3-medquad-lora

# QLoRA (4-bit base; merged to fp16 on push for easy deployment)
hf jobs uv run --flavor a10g-small --timeout 2h -s HF_TOKEN=$HF_TOKEN \
  train.py -- --method qlora \
  --dataset_name YOUR_USERNAME/medquad-structured \
  --hub_model_id YOUR_USERNAME/qwen3-medquad-qlora
```

Useful flags: `--max_steps 500` (shorter run), `--num_train_epochs 3`, `--batch_size 8`,
`--lora_r 64`. Defaults match the Colab notebooks.

## Inference

**Offline batch inference** (score the whole test set without a Colab session), push
predictions to the Hub so Week 5 can grade them:

```bash
hf jobs uv run --flavor t4-small --timeout 1h -s HF_TOKEN=$HF_TOKEN \
  infer_batch.py -- \
  --model_id YOUR_USERNAME/qwen3-medquad-qlora \
  --dataset_name YOUR_USERNAME/medquad-structured --split test \
  --out_repo YOUR_USERNAME/medquad-predictions
```

**Live serving (an API)**, Jobs is for *batch*; for a always-on endpoint use **HF Inference
Endpoints** instead: open your pushed model on the Hub → **Deploy → Inference Endpoints** →
pick a GPU. You get an OpenAI-compatible URL (this is Week 4 NB04 Pattern B):

```python
from openai import OpenAI
client = OpenAI(base_url="https://<your-endpoint>.endpoints.huggingface.cloud/v1/",
                api_key="hf_xxx")
r = client.chat.completions.create(model="qwen3-medquad",
        messages=[{"role": "user", "content": "Symptoms of anemia?"}], max_tokens=200)
```

## Monitor a running job

```bash
hf jobs ps                         # list running jobs
hf jobs logs <job_id>              # stream logs
hf jobs inspect <job_id>           # status + metrics
hf jobs cancel <job_id>            # stop it (billing stops too)
```

## Gotchas

- **Default timeout is 30 minutes.** Training will be killed mid-run unless you pass
  `--timeout 2h` (the value is the *job* wall clock, not a training arg).
- **`-s` for secrets, `-e` for env vars.** `-s HF_TOKEN=...` is encrypted server-side;
  unsloth/transformers read it automatically to push to the Hub.
- **Billing is per minute while Starting/Running**, pay-as-you-go. Cancel stuck jobs.
- **Pick `a10g-small`** for this model. T4 works but lacks Flash-Attention-2; A100 is wasted money on 0.6B.

## How this threads into Weeks 5 & 6

```
NB00 push dataset  ->  jobs/train.py (real run)  ->  model on the Hub
                                                          |
                          Week 5 eval: set CANDIDATES / MODEL_PATH = "YOUR_USERNAME/qwen3-medquad-qlora"
                          Week 6 deploy: pull the Hub model into the Organon skill (or export GGUF for Ollama)
```

The eval/deploy notebooks already accept a model path, point them at your Hub id and the
whole pipeline runs on real weights.
