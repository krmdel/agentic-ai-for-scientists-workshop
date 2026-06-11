# Week 3 — From Loops to Graphs (LangGraph)

**Agentic AI for Scientists** · Week 3 · *AI Agents Fundamentals II*

Week 2 ended with a hard truth: **the control loop is the agent**. But that hand-rolled `while` loop couldn't pause, couldn't branch cleanly, and forgot everything when the cell ended. Week 3 earns the next abstraction — **LangGraph**: agents as **stateful graphs** (nodes = steps, edges = control flow, a typed state threaded through), so the loop becomes inspectable, resumable, and persistent.

Everything runs on **Google Gemini's free tier** (`gemini-2.5-flash`) — no credit card.

> **Version note.** Week 2 pinned *classic* LangChain **0.3.x** (for `AgentExecutor` / `create_react_agent`). Week 3 is the cutover to the **LangChain / LangGraph 1.0 GA** line. The concepts carry over; the imports change. See [resources.md](resources.md) for the map.

## Open notebooks in Colab (one click)

Each notebook's first cell installs its dependencies and reads your `GOOGLE_API_KEY` from Colab Secrets. Open in order:

| Notebook | Open in Colab | What it does |
|---|---|---|
| 00 — LangGraph Core | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/krmdel/agentic-ai-for-scientists-workshop/blob/main/week-03-multi-agent/notebooks/00_langgraph_intro.ipynb) | State, nodes, edges, **conditional-edge cycles**, `stream()` — a graph is a loop you can pause. |
| 01 — Reflexion Agent | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/krmdel/agentic-ai-for-scientists-workshop/blob/main/week-03-multi-agent/notebooks/01_reflexion_agent.ipynb) | generate → **reflect** → revise; a self-improving paper abstract. |
| 02 — Agentic RAG | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/krmdel/agentic-ai-for-scientists-workshop/blob/main/week-03-multi-agent/notebooks/02_agentic_rag.ipynb) | retrieve → **grade** → web-search fallback (CRAG / Self-RAG / Adaptive). |
| 03 — Production Graph | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/krmdel/agentic-ai-for-scientists-workshop/blob/main/week-03-multi-agent/notebooks/03_production_graph.ipynb) | `ToolNode` + **memory** + **human-in-the-loop** + `SqliteSaver` + async fan-out. |
| 04 — Multi-Agent Deep Research | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/krmdel/agentic-ai-for-scientists-workshop/blob/main/week-03-multi-agent/notebooks/04_multiagent_deep_research.ipynb) | **supervisor → worker** deep research, mapped onto `open_deep_research` + TriAgent. |

> **First time on Colab?** Click any badge above, then `File → Save a copy in Drive` so your edits persist.

## Recording

📹 **[Week 3 — Multi-Agent Systems (full session)](https://youtu.be/ditHGU1hauU)** — unlisted YouTube; anyone with the link can watch.

## API keys

| Key | Required? | Free | Used by |
|-----|-----------|------|---------|
| `GOOGLE_API_KEY` | **Yes** | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) | every notebook (the LLM) |
| `TAVILY_API_KEY` | Optional | [app.tavily.com](https://app.tavily.com) (1,000/mo) | NB02 web-search fallback (mock runs without it) |
| `LANGSMITH_API_KEY` | Optional | [smith.langchain.com](https://smith.langchain.com) | NB01–04 tracing — **use `LANGSMITH_*` names** (1.x), not `LANGCHAIN_*` |

In Colab: add each under the 🔑 **Secrets** panel (left sidebar) with *Notebook access* on. Locally: `cp .env.example .env` and fill it in.

## Run locally

```bash
bash setup.sh            # installs the LangGraph 1.x stack (Python 3.10+; use a fresh venv)
cp .env.example .env     # add your GOOGLE_API_KEY
jupyter lab              # open notebooks/
```

## Slides

**Final deck:** [`slides/agentic-ai-workshop-week3.pdf`](slides/agentic-ai-workshop-week3.pdf), the deck used in the workshop.

## The arc

```
00  LangGraph core ........ a graph is a loop you can pause
01  Reflexion ............. generate → reflect → revise, until good enough
02  Agentic RAG ........... retrieval that grades itself and web-searches the gaps
03  Production ............ memory, human-in-the-loop, durable state, parallelism
04  Multi-agent ........... supervisor + workers → the shape behind real deep-research systems
```

## What's next

Week 4 builds on these graphs toward evaluation and domain agents. The capstone (NB04) maps directly onto production systems — [`open_deep_research`](https://github.com/langchain-ai/open_deep_research), [GPT-Researcher](https://github.com/assafelovic/gpt-researcher), and the instructor's own [TriAgent](https://github.com/krmdel/TriAgent) (clinical biomarker discovery + literature validation).

## License

Course materials: **CC BY 4.0**. Code cells: MIT (reuse freely with attribution).
