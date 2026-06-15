# Week 4: the agent-driven path: train/eval/infer from Claude Code

This is the third (and most on-theme) way to run the pipeline. Instead of clicking through
a notebook or typing `hf jobs` commands, you **tell Claude Code what you want** and an
installed **Agent Skill** does the whole thing: validates the dataset, picks hardware,
generates the TRL script, submits the job to HF infrastructure, monitors it, converts to
GGUF, and pushes the model to the Hub.

> This *is* the course thesis. Weeks 1–3 taught you that an agent is skills + tools + a loop.
> Here the agent fine-tunes a model for you. And the punchline for Week 6: **HF Skills are
> the same `SKILL.md` Agent-Skill format as Organon's skills**, you install Hugging Face's
> `hf-llm-trainer` right next to the `sci-clinical-assistant` skill you build in Week 6, in
> the same Claude Code.

## Three paths, escalating in agency

```
   notebooks/  (Colab) ...... you do it by hand          -> learn the mechanics   (free)
   jobs/       (uv + CLI) .... you script it, headless    -> a real run            (Pro)
   THIS doc    (Agent Skills)  you TELL the agent          -> the agentic way       (Pro)
```

All three train the *same* model on the *same* MedQuAD data. Pick by how much you want to
do yourself versus delegate.

## What Hugging Face shipped

[`huggingface/skills`](https://github.com/huggingface/skills) is a marketplace of ~19
Agent Skills that cover the whole loop. The ones that matter here:

| Stage | HF Skill | Does |
|---|---|---|
| **Data** | `huggingface-datasets` | explore / validate a dataset before training |
| **Train** | `hf-llm-trainer` (`trl-training`) | SFT / DPO / GRPO on HF Jobs, hardware + cost estimate, Trackio monitoring, GGUF, push to Hub |
| **Eval** | HF model-evaluation skill + [`upskill`](https://github.com/huggingface/upskill) | score a checkpoint; author + eval skills across models |
| **Inference** | `huggingface-local-models` | run a GGUF locally (the on-device path from Week 4 NB04 / Week 6) |
| **Hub** | `hf-cli` | repos, uploads, model cards |

Background: [hf.co/blog/hf-skills-training](https://huggingface.co/blog/hf-skills-training)
and [hf.co/blog/upskill](https://huggingface.co/blog/upskill).

## Install (Claude Code)

```text
/plugin marketplace add huggingface/skills
/plugin install hf-llm-trainer@huggingface/skills
```

Set a write-scope token in your shell before launching Claude Code (the skill uses HF Jobs,
so the same **Pro account** caveat from `jobs/README.md` applies):

```bash
export HF_TOKEN=hf_your_write_token   # https://huggingface.co/settings/tokens
```

Optionally add the data + local-inference skills:

```text
/plugin install huggingface-datasets@huggingface/skills
/plugin install huggingface-local-models@huggingface/skills
```

## Drive our pipeline in natural language

Once installed, you talk to the agent. These prompts run **our** workshop pipeline
(MedQuAD-structured dataset from NB00, Qwen3-0.6B):

**Data check**
> "Use the datasets skill to inspect `YOUR_USERNAME/medquad-structured`, confirm it has
> train/validation/test splits and a `messages` field, and show one example."

**Train (the agent estimates cost, submits the job, monitors it)**
> "Use the HF LLM trainer skill to fine-tune `Qwen/Qwen3-0.6B` on
> `YOUR_USERNAME/medquad-structured` with QLoRA for one epoch. Push the result to
> `YOUR_USERNAME/qwen3-medquad-qlora` and give me a cost estimate before you start."

The agent replies with hardware + cost (e.g. *"t4-small, ~20 min, ~$0.30"*), submits the
HF Job, and streams progress. Re-run with `SFT` or `DPO` to compare methods, the same
ladder as notebooks 01–03, now agent-operated.

**Convert for on-device use**
> "Convert `YOUR_USERNAME/qwen3-medquad-qlora` to GGUF (q4_k_m) and push it so I can run it
> with Ollama / the local-models skill."

**Inference (local, private)**
> "Use the local-models skill to load `YOUR_USERNAME/qwen3-medquad-qlora` and answer:
> what are the symptoms and treatment of Hashimoto's disease?"

**Evaluate**, point the Week 5 harness at the Hub model (set `MODEL_PATH` to your repo id),
or go fully agentic and let `upskill` evaluate a *skill* across models:
```bash
pip install upskill
export ANTHROPIC_API_KEY=sk-ant-...   # teacher
upskill eval ./skills/your-skill/ --model haiku --model sonnet
```

## Why this is the right capstone framing

- **It closes the loop with Week 1.** You went from *using* Claude Code to having it run a
  GPU training job for you, in plain English.
- **Same format, end to end.** HF's `hf-llm-trainer` and your Week-6 `sci-clinical-assistant`
  are both Agent Skills (`SKILL.md`). Installed side by side, one trains the model and the
  other deploys it, your agent now owns the whole lifecycle.
- **Honest cost line.** Like `jobs/`, the training skill uses HF Jobs and needs a **Pro
  account**. Keep free Colab as the in-class default; reach for the agent-driven path when
  you want the agent to do the real run for you.

## How it threads into Weeks 5 & 6

```
  Claude Code + hf-llm-trainer  ->  model on the Hub
                                        |
   Week 5  eval: MODEL_PATH = "YOUR_USERNAME/qwen3-medquad-qlora"  (or upskill eval for skills)
   Week 6  the agent that TRAINED the model is the same one that DEPLOYS it (sci-clinical-assistant)
```
