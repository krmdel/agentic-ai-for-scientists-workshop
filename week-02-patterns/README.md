# Week 2 — AI Agents Fundamentals I: Patterns

**Series:** Agentic AI for Scientists (6-week workshop)
**This week:** a LangChain primer, function calling, ReAct (+ CoT & ToT), and RAG. From CRUD app to control loop.
**Duration:** 120 min
**Format:** Instructor drives Colab notebooks live; attendees fork and re-run after class.

---

## Open notebooks in Colab (one click)

| Notebook | Open in Colab | What it does |
|---|---|---|
| 00 — LangChain in 15 Minutes | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/krmdel/agentic-ai-for-scientists-workshop/blob/main/week-02-patterns/notebooks/00_langchain_intro.ipynb) | Warm-up: model wrapper, messages, prompt templates, output parsers, the LCEL `|` pipe, and a first look at `@tool`. The vocabulary every later notebook uses. |
| 01 — Tool Use & Function Calling | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/krmdel/agentic-ai-for-scientists-workshop/blob/main/week-02-patterns/notebooks/01_tool_use.ipynb) | The smallest agent built three ways: hand-rolled loop → Gemini native function-calling → LangChain **tool-calling agent** — plus **structured output** (Pydantic `with_structured_output`). |
| 02 — ReAct, CoT & ToT | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/krmdel/agentic-ai-for-scientists-workshop/blob/main/week-02-patterns/notebooks/02_react_agent.ipynb) | Chain-of-Thought → hand-built ReAct loop → `create_react_agent` → Tree-of-Thoughts → the **function-calling vs ReAct** contrast (who owns tool selection). |
| 03 — RAG End-to-End | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/krmdel/agentic-ai-for-scientists-workshop/blob/main/week-02-patterns/notebooks/03_rag_pipeline.ipynb) | LangChain-native: `PyPDFLoader` → splitter → embeddings → **FAISS + Chroma** → BM25 → `EnsembleRetriever` → compare on 5 questions → citation RAG chain. |
| 04 — Elasticsearch Appendix (optional) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/krmdel/agentic-ai-for-scientists-workshop/blob/main/week-02-patterns/notebooks/04_rag_elasticsearch_appendix.ipynb) | Same RAG pipeline on a real Elastic Cloud trial cluster with native RRF. Homework only — not run in class. |

> **First time on Colab?** Click any badge above, then `File → Save a copy in Drive` so your edits persist.

---

## Slides

**Final deck:** [`slides/agentic-ai-workshop-week2.pptx`](slides/agentic-ai-workshop-week2.pptx) · [`slides/agentic-ai-workshop-week2.pdf`](slides/agentic-ai-workshop-week2.pdf) — the deck used in the workshop. Open the `.pptx` and **Open with → Google Slides** for a browser-editable copy.

---

## Resources

Curated companion material — the FC-vs-ReAct reference video, LangChain docs, key papers, and more: **[`resources.md`](resources.md)**.

---

## Pre-class prep (≤ 5 min)

Do this once before the workshop. You can skip everything if you're only watching.

1. **Google Gemini API key (free)** — get one at https://aistudio.google.com/apikey (no credit card). In Colab, add it as **GOOGLE_API_KEY** under the 🔑 *Secrets* panel (left sidebar). The free tier covers all four notebooks. Full guide: **[API_KEYS.md](API_KEYS.md)**.
2. *(optional)* **OpenAI API key** — only if you want to swap embeddings to `text-embedding-3-small` instead of the free local model. Skippable.
3. *(optional)* **Elastic Cloud free trial** — only for Notebook 04. Sign up at https://cloud.elastic.co (14-day trial, no card). Note your `Cloud ID` and create a `Data API key`. Skippable for in-class.

No local install needed for Colab. If you want to run locally, see **Local run** below.

---

## Block schedule (live, 120 min)

| Part | Min | What | Notebook |
|---|---|---|---|
| 0 | 5 | Hook + Week 1 callback | — |
| 1 | 18 | **Why LLMs work** — next-token, attention, scaling, System 1/2 | — |
| 2 | 25 | **The agentic ladder** — L0 bare → L1 tools → L2 reasoning (CoT/ToT/ReAct) | — |
| 3 | 40 | **LangChain + hands-on** | ▶ 00, 01, 02 |
| 4 | 27 | **RAG end-to-end** (FAISS + Chroma + hybrid) | ▶ 03 |
| 5 | 10 | Week 3 bridge + Q&A + close | — |

Soft 90-second stretch at the 65-min mark, no formal break.

---

## Local run (optional)

```bash
git clone https://github.com/krmdel/agentic-ai-for-scientists-workshop.git ~/Projects/agentic-ai-for-scientists-workshop
cd ~/Projects/agentic-ai-for-scientists-workshop/week-02-patterns
./setup.sh                       # creates .venv, installs pinned deps
cp .env.example .env             # fill in GOOGLE_API_KEY at minimum
.venv/bin/jupyter lab notebooks/ # opens in browser
```

Tested on macOS 14 (Apple Silicon) and Ubuntu 22.04. Python 3.10–3.12.

---

## Sample articles

`sample_articles/` is empty in the repo by design — the notebooks download papers on first run (~7 MB total, takes ~30 s). The corpus is five public ML/AI papers:

1. **ReAct: Synergizing Reasoning and Acting in Language Models** — Yao et al. 2022 (arXiv:2210.03629)
2. **Attention Is All You Need** — Vaswani et al. 2017 (arXiv:1706.03762)
3. **Training Compute-Optimal Large Language Models (Chinchilla)** — Hoffmann et al. 2022 (arXiv:2203.15556)
4. **Constitutional AI: Harmlessness from AI Feedback** — Bai et al. 2022 (arXiv:2212.08073)
5. **Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks** — Lewis et al. 2020 (arXiv:2005.11401)

If you want to drop in your own corpus, replace `sample_articles/*.pdf` and re-run Notebook 03 from cell 1.

---

## Eval data

The five test queries for Notebook 03's comparison cell are **inlined directly in the notebook** (each annotated with the paper + section that holds the ground-truth answer), so the dense-vs-BM25-vs-hybrid comparison runs identically in Colab and locally with no external download. `eval/rag_questions.json` keeps the same set on disk for reference.

---

## After class

- All Colab links above are persistent. Fork into your own Drive (`File → Save a copy in Drive`) to keep your edits.
- Week 1 materials: [`../week-01-foundations/`](../week-01-foundations/)
- Week 3 preview: multi-agent systems with LangGraph. Notebook 03's retriever becomes a tool node in next week's deep-research triagent.

---

## Honesty contract

Every notebook builds the primitive (manual loop, raw prompt template, hand-built retriever) before collapsing to a framework. If you only see the framework call, you'll think the magic is in the framework. The magic is in the loop.

CoT and ToT are demonstrated live in Notebook 02 alongside ReAct. Reflexion is a one-slide mention only — the honest hands-on scope for one 120-min session is a LangChain primer + function calling + ReAct (with CoT/ToT) + RAG.

---

*Built with [Organon](https://github.com/krmdel/organon). Questions? Open an issue at github.com/krmdel/agentic-ai-for-scientists-workshop.*
