# Week 4: Post-Training & Deployment of AI Agents

**Agentic AI for Scientists** · Week 4 · *How to make a model behave, then put it to work*

Weeks 2–3 used models *as they shipped*. Week 4 is where you **change** one. We take a tiny open model (`Qwen/Qwen3-0.6B`) and a real medical Q&A corpus (**MedQuAD**, 47k NIH clinician answers), build a structured fine-tuning dataset, train the model three ways, **full SFT → LoRA → QLoRA**, and then look at how a trained model actually **serves** (local, endpoint, on-device).

> One dataset, one model, threaded across the whole back half of the course. Week 4 *produces* the models, **Week 5** *evaluates* them, **Week 6** *deploys* one as an Organon skill.

Everything runs on a **free Colab T4 GPU**. Labeling uses **Gemini's free tier**.

## Run in Colab (nothing to install)

Each notebook's first cell installs its own dependencies. Run them **in order**, `00` builds the dataset the rest depend on. **Set the runtime to GPU** first (`Runtime → Change runtime type → T4 GPU`).

| # | Notebook | What you build | Colab |
|---|----------|----------------|-------|
| 00 | `00_dataset_prep.ipynb` | MedQuAD → **Gemini entity labeler** → chat-format JSONL (disease/symptoms/treatment) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/krmdel/agentic-ai-for-scientists-workshop/blob/main/week-04-post-training/notebooks/00_dataset_prep.ipynb) |
| 01 | `01_full_sft.ipynb` | **Full** supervised fine-tune, update 100% of the weights | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/krmdel/agentic-ai-for-scientists-workshop/blob/main/week-04-post-training/notebooks/01_full_sft.ipynb) |
| 02 | `02_lora.ipynb` | **LoRA**, train <1% of params, MB-sized adapter | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/krmdel/agentic-ai-for-scientists-workshop/blob/main/week-04-post-training/notebooks/02_lora.ipynb) |
| 03 | `03_qlora.ipynb` | **QLoRA**, 4-bit NF4 base + LoRA → quantization + the 3-way comparison | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/krmdel/agentic-ai-for-scientists-workshop/blob/main/week-04-post-training/notebooks/03_qlora.ipynb) |
| 04 | `04_deploy_inference.ipynb` | Serve the tuned model: local / endpoint / on-device, latency vs cost vs privacy | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/krmdel/agentic-ai-for-scientists-workshop/blob/main/week-04-post-training/notebooks/04_deploy_inference.ipynb) |

## API keys

| Key | Required? | Free | Used by |
|-----|-----------|------|---------|
| `GOOGLE_API_KEY` | **Yes (NB00)** | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) | the Gemini labeler in NB00 |
| `HF_TOKEN` | Optional | [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) | pushing datasets/models to the Hub |
| `ANTHROPIC_API_KEY` | Optional | n/a | swap the NB00 labeler to Claude (one cell) |

In Colab: add each under the 🔑 **Secrets** panel (left sidebar), *Notebook access* on. Locally: `cp .env.example .env` and fill it in. NB01–04 (training) need **no key**, only the GPU.

## Run locally

```bash
bash setup.sh            # installs the Unsloth + TRL fine-tuning stack (Python 3.10–3.12, a CUDA GPU)
cp .env.example .env     # add GOOGLE_API_KEY (only NB00 needs it)
jupyter lab              # open notebooks/ and run 00 → 04
```

> Local training needs an NVIDIA GPU (Ampere+ ideal; T4 works). No GPU? Use Colab, it's the intended path.

## The arc

```
00  Dataset prep ......... the model is easy; the dataset is the project
01  Full SFT ............. update every weight, best quality, heaviest cost
02  LoRA ................. freeze the base, train tiny adapters, ~1% of params
03  QLoRA ............... 4-bit base + LoRA, lowest VRAM, the consumer-GPU unlock
04  Deployment .......... local vs endpoint vs on-device, latency, cost, privacy
```

## What's in this folder

```
week-04-post-training/
├── README.md                  ← this file
├── setup.sh                   ← local install of the fine-tuning stack
├── .env.example               ← GOOGLE_API_KEY (NB00) + optional HF_TOKEN / ANTHROPIC
├── notebooks/                 ← 00–04 (Colab-first)
├── jobs/                      ← the REAL training run on Hugging Face Jobs (train.py, infer_batch.py)
├── AGENT_DRIVEN.md            ← drive train/eval/infer from Claude Code via HF Agent Skills
├── data/                      ← a small pre-baked structured sample + your generated splits
└── slides/                    ← the talk deck (PDF)
```

## Three ways to train (escalating in agency)

| | **Colab** (`notebooks/`) | **HF Jobs** (`jobs/`) | **Claude Code skill** ([`AGENT_DRIVEN.md`](AGENT_DRIVEN.md)) |
|---|---|---|---|
| You... | do it by hand | script it, headless | **tell the agent** in plain English |
| Cost | free, no account | [Pro](https://huggingface.co/pro) + per-min compute | Pro (same; the skill uses HF Jobs) |
| For | learning the mechanics | a real run | the agentic way, the course thesis |

All three train the same model on the same MedQuAD data; the only difference is how much you
delegate. The notebooks stay the **free in-class default**. The other two produce a real
model on the **Hub**, the shared artifact the eval (Week 5) and deploy (Week 6) notebooks
point at (set `MODEL_PATH` to your Hub id).

- **`jobs/`**: `hf jobs uv run` with our `train.py` / `infer_batch.py`. See [`jobs/README.md`](jobs/README.md).
- **`AGENT_DRIVEN.md`**: install HF's `hf-llm-trainer` Agent Skill and let Claude Code run the whole lifecycle. HF Skills use the *same* `SKILL.md` format as the `sci-clinical-assistant` skill you build in Week 6, so your agent ends up owning both training and deployment.

## Slides

**Final deck:** [`slides/agentic-ai-workshop-week4.pdf`](slides/agentic-ai-workshop-week4.pdf), the deck used in the workshop.

## Notes & honesty

- **Demo budgets.** Training notebooks use `max_steps=60` so each finishes in a few minutes on a T4. Set `max_steps=-1` + the full dataset for a real (multi-hour) run.
- **Pre-baked labels.** A full Gemini label pass over thousands of rows costs time + quota, so `data/medquad_structured.jsonl` ships as a small offline-labeled **sample seed** and NB00 only labels a few rows live to show the mechanism. Replace it with your own full run for a serious fine-tune.
- **Reference comparison numbers.** NB03's comparison table falls back to reference VRAM/loss figures when you haven't run NB01/NB02 in the same session: re-run them to populate your own.

## What's next

**Week 5, Evaluation & Benchmarking:** measure the models you just trained against ground truth (entity F1), build an LLM-as-judge, and run a published benchmark. **Week 6, Towards Full Autonomy:** deploy one of these models as an **Organon skill** that runs a daily research chore on its own.

## License

Course materials: **CC BY 4.0**. Code cells: MIT (reuse freely with attribution).
