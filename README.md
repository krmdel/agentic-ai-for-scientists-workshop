# Agentic AI for Scientists — Workshop Materials

Public materials and demos for a 6-week workshop series on Claude Code, [Organon](https://github.com/krmdel/organon), and agentic AI for scientific workflows. Each week's content lives in its own folder — slides, runnable notebooks, demo projects, and notes — so you can re-run everything on your own laptop or in Colab.

**Instructor:** Kerem Delikoyun (TUMCREATE)
**Substrate:** [Organon](https://github.com/krmdel/organon) — an agent-first Claude Code project template for scientists.

> Materials are published **after each session is delivered**. Weeks 1–2 are available now; the remaining weeks are added as the series runs.

## Series overview

| Week | Title | Materials |
|---|---|---|
| 1 | GenAI Foundations for Scientists | [`week-01-foundations/`](week-01-foundations/) ✅ |
| 2 | AI Agents Fundamentals I — Patterns (tool use, function calling, CoT/ToT, ReAct, RAG) | [`week-02-patterns/`](week-02-patterns/) ✅ |
| 3 | AI Agents Fundamentals II — Multi-Agent Systems | *upcoming* |
| 4 | Post-Training & Deployment of AI Agents | *upcoming* |
| 5 | Evaluation and Benchmarking of AI Agents | *upcoming* |
| 6 | Towards Full Autonomy | *upcoming* |

## Start here

**Week 2 is notebook-driven — open any notebook straight in Colab** (no install needed) from [`week-02-patterns/`](week-02-patterns/):

- **00 — LangChain in 15 minutes** · **01 — Tool use & function calling** · **02 — ReAct, CoT & ToT** · **03 — RAG end-to-end** · **04 — Elasticsearch appendix** *(optional)*

You only need a free Google Gemini API key — the free tier covers all the notebooks (get one at https://aistudio.google.com/apikey, no credit card). See [`week-02-patterns/README.md`](week-02-patterns/README.md) for the one-click Colab badges.

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
└── week-02-patterns/        ← AI Agents Fundamentals I — Patterns
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
