# Agentic AI for Scientists — Workshop Materials

Public materials and demos for a 6-week workshop series on Claude Code, [Organon](https://github.com/krmdel/organon), and agentic AI for scientific workflows. Each week's content lives in its own folder — slides, runnable notebooks, demo projects, and notes — so you can re-run everything on your own laptop or in Colab.

**Instructor:** Kerem Delikoyun (TUMCREATE)
**Substrate:** [Organon](https://github.com/krmdel/organon) — an agent-first Claude Code project template for scientists.

> Materials are published **after each session is delivered**. Weeks 1–5 are available now; the remaining weeks are added as the series runs.

📄 **[Workshop overview (PDF)](Agentic-AI-for-Scientists-Workshop-Overview.pdf)** — the full 6-week series description, learning outcomes, speaker bio, and logistics.

## Series overview

| Week | Title | Materials |
|---|---|---|
| 1 | GenAI Foundations for Scientists | [`week-01-foundations/`](week-01-foundations/) ✅ |
| 2 | AI Agents Fundamentals I — Patterns (tool use, function calling, CoT/ToT, ReAct, RAG) | [`week-02-patterns/`](week-02-patterns/) ✅ |
| 3 | AI Agents Fundamentals II — Multi-Agent Systems | [`week-03-multi-agent/`](week-03-multi-agent/) ✅ |
| 4 | Post-Training & Deployment of AI Agents | [`week-04-post-training/`](week-04-post-training/) ✅ |
| 5 | Evaluation and Benchmarking of AI Agents | [`week-05-evaluation/`](week-05-evaluation/) ✅ |
| 6 | Towards Full Autonomy | *upcoming* |

## Start here

**Weeks 2–5 are notebook-driven — open any notebook straight in Colab** (no install needed):

- **Week 2** — [`week-02-patterns/`](week-02-patterns/): LangChain in 15 minutes · tool use & function calling · ReAct, CoT & ToT · RAG end-to-end · Elasticsearch appendix *(optional)*
- **Week 3** — [`week-03-multi-agent/`](week-03-multi-agent/): LangGraph core · Reflexion · agentic RAG · production graph · multi-agent deep research
- **Week 4** — [`week-04-post-training/`](week-04-post-training/): dataset prep · full SFT · LoRA · QLoRA · deploy & inference *(open in Colab with a free GPU runtime)*
- **Week 5** — [`week-05-evaluation/`](week-05-evaluation/): eval vs ground truth · LLM-as-judge · benchmarks · custom eval harness *(open in Colab with a free GPU runtime)*

Weeks 2 and 3 run entirely on a free Google Gemini API key (get one at https://aistudio.google.com/apikey, no credit card). Weeks 4 and 5 run on a free Colab GPU and only need the Gemini key for one notebook each. Each week's README has the one-click Colab badges.

## Run the demos locally (optional)

```bash
git clone https://github.com/krmdel/agentic-ai-for-scientists-workshop.git ~/Projects/agentic-ai-for-scientists-workshop
cd ~/Projects/agentic-ai-for-scientists-workshop
./setup.sh
```

The bootstrap script verifies Claude Code is installed, points the demos at your [Organon](https://github.com/krmdel/organon) checkout, and copies `.env.example` → `.env` for you to fill in. Full walkthrough: [SETUP.md](SETUP.md).

## Repo structure

```
agentic-ai-for-scientists-workshop/
├── README.md                ← this file
├── SETUP.md                 ← full setup walkthrough
├── setup.sh                 ← one-command bootstrap
├── .env.example             ← API keys template
├── docs/                    ← Claude Code, dashboard, Obsidian, troubleshooting
├── week-01-foundations/     ← GenAI Foundations for Scientists
├── week-02-patterns/        ← AI Agents Fundamentals I — Patterns
├── week-03-multi-agent/     ← AI Agents Fundamentals II — Multi-Agent Systems
├── week-04-post-training/   ← Post-Training & Deployment
└── week-05-evaluation/      ← Evaluation & Benchmarking
```

Each week folder is self-contained: deck, scripts, demo project, and notes.

## Week 1 — GenAI Foundations (highlights)

- The 200-year **abstraction staircase** and the 80-year **AI road** converging at natural language.
- **Claude Code** and its primitives (`CLAUDE.md`, tools, skills, sub-agents, MCP, hooks).
- **Organon** — an agentic OS for scientists; memory, identity, and skills as plain files on disk.
- A live research-dashboard demo: a literature library, a 4-persona hypothesis critique, a **100-patient synthetic cohort** with an analysis script, a mechanism figure, a 6-section manuscript draft, and a 43-note Obsidian vault.

See [week-01-foundations/README.md](week-01-foundations/README.md).

## Week 2 — Agentic patterns (highlights)

- **The agentic ladder:** bare LLM → tool use → reasoning (CoT, ToT, ReAct).
- The smallest agent built three ways: hand-rolled loop → native tool-use → LangChain tool-calling agent, plus **structured output** (Pydantic).
- **ReAct** from scratch and via `create_react_agent`; **Tree-of-Thoughts**; the function-calling-vs-ReAct contrast.
- **RAG end-to-end** with LangChain: loaders → splitters → embeddings → **FAISS + Chroma** → BM25 → hybrid retrieval → citations.

See [week-02-patterns/README.md](week-02-patterns/README.md).

## Week 3 — Multi-agent systems (highlights)

- **From loops to graphs:** the hand-rolled `while` loop becomes a **LangGraph** stateful graph (nodes, edges, typed state) that is inspectable, resumable, and persistent.
- **Reflexion:** generate → reflect → revise, with the critique persisted in state so the output converges instead of drifting.
- **Agentic RAG:** retrieval that grades itself and web-searches the gaps (Corrective / Self / Adaptive RAG).
- **Production graph:** memory across turns, human-in-the-loop approval, durable `SqliteSaver` checkpoints, async fan-out.
- **Multi-agent deep research:** a supervisor → worker capstone, mapped onto `open_deep_research`, GPT-Researcher, and **TriAgent**.

See [week-03-multi-agent/README.md](week-03-multi-agent/README.md).

## Week 4 — Post-Training & Deployment (highlights)

- **Why fine-tune, and the post-training stages:** continued pretraining → supervised fine-tuning → alignment, and where full FT / LoRA / QLoRA each fit.
- **Three ways to fine-tune, one notebook each:** full SFT, **LoRA** (low-rank adapters), and **QLoRA** (4-bit base + adapters) — all on **Unsloth + TRL**, the same code with one flag flipped.
- **The data formats that teach behaviour:** chat templates, tool-use tokens (`<tool_call>` / `<tool_response>`), and reasoning traces (`<think>`).
- **Deployment:** serve what you trained — local `transformers`, **vLLM**, **Ollama** / llama.cpp, plus the cloud landscape (Ray Serve, HF Endpoints, SageMaker, Bedrock).
- Plus a **Hugging Face Jobs** path (real training and batch inference) and an **agent-driven** path that drives train / eval / infer from Claude Code.

See [week-04-post-training/README.md](week-04-post-training/README.md).

## Week 5 — Evaluation & Benchmarking (highlights)

- **Why eval is the hard part:** a model you can't measure is a model you can't trust — and a lower training loss does not mean better answers.
- **Ground truth first:** field-level metrics (JSON validity, disease accuracy, symptom/treatment F1) and the **base-vs-fine-tuned delta** that proves the Week 4 tuning worked.
- **LLM-as-judge, honestly:** pointwise and pairwise judging for what has no F1 (faithfulness, safety, tone), plus **position-bias defense** and human calibration — an unvalidated judge is a vibe, not a metric.
- **Benchmarks without fooling yourself:** run **PubMedQA** against its majority-class baseline, and learn to read agent-benchmark claims (SWE-bench, GAIA) critically.
- **Your own harness:** an assertion-based **regression suite** with a real safety check, turned into a CI gate — eval-driven development for models.

See [week-05-evaluation/README.md](week-05-evaluation/README.md).

## Prerequisites

- macOS (tested) / Linux / Windows WSL2
- Git, Node ≥ 20, Python ≥ 3.10
- Claude Code CLI: `npm install -g @anthropic-ai/claude-code`
- Organon (for the local Week 1 dashboard demo): `git clone https://github.com/krmdel/organon.git ~/Projects/organon`
- An `.env` with `ANTHROPIC_API_KEY` (and `GEMINI_API_KEY` for figure generation)

Detailed install order: [docs/claude-code-setup.md](docs/claude-code-setup.md).

## License

[Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE) © Kerem Delikoyun.
You may share and adapt these materials for any purpose, including commercially, as long as you give appropriate credit. Third-party papers, logos, and figures referenced in the demos remain the property of their respective owners.
