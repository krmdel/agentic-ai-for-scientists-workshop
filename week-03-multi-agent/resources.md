# Week 3 — Resources

Curated companion material for **Week 3: From Loops to Graphs** — LangGraph, reflexion, agentic retrieval-augmented generation (RAG), persistence/human-in-the-loop, and multi-agent deep research. Suggestions welcome via an issue or pull request.

> **Version note.** Week 3 runs on the **LangChain / LangGraph 1.0** general-availability line (`langgraph>=1.2.4`, `langchain-core>=1.4.0`) — the cutover from Week 2's pinned classic 0.3.x. Where Week 2 used `AgentExecutor` / `create_react_agent`, Week 3 uses `StateGraph` + `ToolNode`. Most docs below are already on the 1.x API.

---

## 🧑‍💻 The course this builds on

- **[emarco177/langgraph-course](https://github.com/emarco177/langgraph-course)** — Eden Marco · the project-based LangGraph course these notebooks adapt (reflection, reflexion, agentic RAG, ReAct-in-LangGraph, persistence/human-in-the-loop, deployment, multi-agent). The section list is captured in [`scripts/SOURCE_CURRICULUM.md`](scripts/SOURCE_CURRICULUM.md). *(The course uses Anthropic/OpenAI; our notebooks run the same patterns on free Gemini.)*

---

## 📄 Official documentation

- **[LangGraph docs](https://langchain-ai.github.io/langgraph/)** — the framework reference: `StateGraph`, nodes/edges, conditional edges, persistence, streaming.
- **[LangGraph — Persistence & checkpointers](https://langchain-ai.github.io/langgraph/concepts/persistence/)** — `MemorySaver`, `SqliteSaver`, `thread_id`, time-travel.
- **[LangGraph — Human-in-the-loop](https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/)** — `interrupt` / `interrupt_before`, approve / edit / resume.
- **[LangGraph — `ToolNode` & prebuilt](https://langchain-ai.github.io/langgraph/reference/prebuilt/)** — the ReAct tool loop in two nodes.
- **[Adaptive RAG tutorial](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_adaptive_rag/)** — wires corrective RAG, self-RAG, and a query router into one graph (the full version of Notebook 02).
- **[Trace with Google Gemini (LangSmith)](https://docs.langchain.com/langsmith/trace-with-google-gemini)** — on the 1.x line, environment variables alone turn tracing on.

---

## ✍️ Essential reading

- **[Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)** — Anthropic Engineering. The workflows-vs-agents map; re-read now that you're composing graphs.
- **[Self-Reflective RAG with LangGraph](https://blog.langchain.com/agentic-rag-with-langgraph/)** — LangChain blog walking corrective RAG + self-RAG as graphs (the basis for Notebook 02).

---

## 📚 Foundational papers (the patterns, in order)

- **Reflexion: Language Agents with Verbal Reinforcement Learning** — Shinn et al., 2023 · arXiv 2303.11366
  Persist verbal self-reflection in memory; revise against it. The Notebook 01 loop.
- **Corrective Retrieval-Augmented Generation (CRAG)** — Yan et al., 2024 · arXiv 2401.15884
  Grade retrieved docs; fall back to web search when they're weak. The Notebook 02 spine.
- **Self-RAG: Learning to Retrieve, Generate, and Critique** — Asai et al., 2023 · arXiv 2310.11511
  Reflection tokens that grade grounding and usefulness of the generation.
- **Adaptive-RAG** — Jeong et al., 2024 · arXiv 2403.14403
  A router that picks the retrieval strategy per query.
- **ReAct: Synergizing Reasoning and Acting** — Yao et al., 2022 · arXiv 2210.03629
  The loop from Week 2, now a two-node graph (Notebook 03).

---

## 🔬 Real-world multi-agent systems (the Notebook 04 capstone)

- **[langchain-ai/open_deep_research](https://github.com/langchain-ai/open_deep_research)** — single-iterative *and* plan-execute *and* supervisor-researcher reference architectures; per-role model routing via `init_chat_model()`. The clearest production reference for Notebook 04's pattern.
- **[assafelovic/gpt-researcher](https://github.com/assafelovic/gpt-researcher)** — planner → parallel executors → publisher; report generation in the STORM style (Synthesis of Topic Outlines through Retrieval and Multi-perspective question asking).
- **[krmdel/TriAgent](https://github.com/krmdel/TriAgent)** — the instructor's framework: a four-node LangGraph pipeline (Scoping → Data Analysis + H2O AutoML → **supervisor/worker Deep Research** → Report) that discovers clinical biomarkers and validates them against literature (established vs novel candidate) for acute-care risk stratification. Every box in its Deep-Research node is a node you build in Notebook 04.

---

## How to use this list

Run the notebooks first — they *are* the lesson. Keep the **LangGraph docs** open while you do (especially persistence + human-in-the-loop). Skim **figure 1 plus the abstract** of each paper; they're short and map one-to-one onto a node in the notebooks. When you want the production version, read **open_deep_research**'s three architectures side by side, then **TriAgent** to see the pattern applied to a real clinical-research problem.
