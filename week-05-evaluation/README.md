# Week 5: Evaluation and Benchmarking of AI Agents

**Agentic AI for Scientists** · Week 5 · *A model you can't measure is a model you can't trust*

Week 4 produced models, full SFT, LoRA, QLoRA fine-tunes of `Qwen3-0.6B` on MedQuAD. Week 5 answers the question that decides whether any of it mattered: **are they actually good?** We measure against held-out ground truth, recruit a model as a judge (and learn how much to trust it), run a real published benchmark honestly, and build a reusable regression suite for your own system.

> Same thread as Week 4: one dataset, one model. **Week 4 makes → Week 5 measures → Week 6 deploys.**

Evaluation runs on a **free Colab T4**; judging uses **Gemini's free tier**.

## Run in Colab (nothing to install)

Run in order. NB00 picks up the models you trained in Week 4 (falling back to the base model so every notebook runs standalone). **Set the runtime to GPU** first.

| # | Notebook | What you build | Colab |
|---|----------|----------------|-------|
| 00 | `00_eval_vs_groundtruth.ipynb` | field-level metrics (JSON validity, disease acc, symptom/treatment F1), **base vs fine-tuned** | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/krmdel/agentic-ai-for-scientists-workshop/blob/main/week-05-evaluation/notebooks/00_eval_vs_groundtruth.ipynb) |
| 01 | `01_llm_as_judge.ipynb` | pointwise + pairwise judges, **position-bias defense**, human calibration | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/krmdel/agentic-ai-for-scientists-workshop/blob/main/week-05-evaluation/notebooks/01_llm_as_judge.ipynb) |
| 02 | `02_benchmarks.ipynb` | run **PubMedQA** honestly + map the agent-benchmark landscape (SWE-bench/GAIA/AgentBench) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/krmdel/agentic-ai-for-scientists-workshop/blob/main/week-05-evaluation/notebooks/02_benchmarks.ipynb) |
| 03 | `03_custom_eval_harness.ipynb` | an assertion-based **regression suite** with a real safety check → a CI gate | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/krmdel/agentic-ai-for-scientists-workshop/blob/main/week-05-evaluation/notebooks/03_custom_eval_harness.ipynb) |

## API keys

| Key | Required? | Free | Used by |
|-----|-----------|------|---------|
| `GOOGLE_API_KEY` | **Yes (NB01)** | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) | the LLM-as-judge in NB01 |

NB00, NB02, NB03 need only the GPU. NB01 (model-graded eval) needs the Gemini key.

## Run locally

```bash
bash setup.sh            # eval stack: unsloth (inference), datasets, rouge-score, gemini
cp .env.example .env     # add GOOGLE_API_KEY (only NB01 needs it)
jupyter lab              # open notebooks/ and run 00 → 03
```

## The arc

```
00  Ground truth ........ held-out metrics; the base-vs-fine-tuned delta is the proof
01  LLM as judge ........ score the unmeasurable, and neutralize the judge's biases
02  Benchmarks .......... run PubMedQA honestly; read agent-benchmark claims critically
03  Custom harness ...... your own regression suite = eval-driven development
```

## What's in this folder

```
week-05-evaluation/
├── README.md                  ← this file
├── setup.sh                   ← local install of the eval stack
├── .env.example               ← GOOGLE_API_KEY (NB01 judge)
├── notebooks/                 ← 00–03 (Colab-first)
└── slides/                    ← the talk deck (PDF)
```

## Slides

**Final deck:** [`slides/agentic-ai-workshop-week5.pdf`](slides/agentic-ai-workshop-week5.pdf), the deck used in the workshop.

## Notes & honesty

- **Reference numbers.** NB00's base-vs-fine-tuned table ships representative reference scores so the comparison is visible even if you only evaluated one model this session. Point `CANDIDATES` at your Week 4 models and rerun for your real numbers.
- **Subset benchmarking is labeled as such.** NB02 runs `PubMedQA[:50]` and says so, and compares against the majority-class baseline, the habit that catches most misleading benchmark claims.
- **A judge is an instrument.** NB01 deliberately spends time on bias and calibration; an unvalidated LLM judge is a vibe, not a metric.

## What's next

**Week 6, Towards Full Autonomy:** take a model that *passed* its evals and let it run a research chore on its own as an **Organon skill**. The suite you build this week stops being a report card and becomes the **safety harness** for autonomy.

## License

Course materials: **CC BY 4.0**. Code cells: MIT (reuse freely with attribution).
