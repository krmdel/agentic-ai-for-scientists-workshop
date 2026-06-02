# Week 2 — Resources

Curated companion material for **Week 2: Agentic Patterns** — the agentic ladder (tool use, function calling, CoT/ToT, ReAct) and RAG. Watch and read these alongside or after the session. Suggestions welcome via an issue or PR.

> **Version note.** The notebooks pin **classic LangChain 0.3.x** (`AgentExecutor`, `create_react_agent`, `create_tool_calling_agent`) — the last line before the LangGraph-first rewrite. The latest LangChain docs and Eden Marco's course below now target **LangChain v1+ / LangGraph**, which is exactly **Week 3's** topic. The *concepts* map one-to-one; mostly the import paths differ.

---

## 📺 Videos

1. **[LangChain Function Calling Agents vs. ReAct Agents — What's Right for You?](https://www.youtube.com/watch?v=L6suEeJ3XXc)** — Eden Marco · 5 min
   The exact contrast Notebook 02 builds: who owns tool selection — the model's native function-calling, or your ReAct prompt? Short and to the point. This video is the basis for the FC-vs-ReAct section of the workshop.

---

## 🧑‍💻 Courses & code

- **[emarco177/langchain-course](https://github.com/emarco177/langchain-course)** — Eden Marco · Apache-2.0
  A project-based course repo: search agents, RAG systems, reflection agents, code interpreters. The companion code to his popular Udemy LangChain course. *(Now LangChain v1+/LangGraph — see the version note above; great for going deeper and previewing Week 3.)*

---

## 📄 Official documentation

- **[LangChain — Python docs](https://docs.langchain.com/oss/python/langchain/overview)** — the framework reference: models, prompts, output parsers, LCEL, agents, retrievers.
- **[Gemini — Function calling](https://ai.google.dev/gemini-api/docs/function-calling)** — how the model requests a tool call and you return the result. The mechanism under Notebook 01.
- **[LangSmith](https://docs.langchain.com/langsmith)** — tracing + observability for agents. Set two env vars and watch every Thought / Action / tool call step-by-step (the "From demo to production" slide).
- **[Tavily](https://docs.tavily.com/)** — a hosted search API built for agents — the real-tool drop-in for the mocked `web_search` in the notebooks.
- **[Pydantic](https://docs.pydantic.dev/latest/)** — the schema library behind structured output (`with_structured_output`) in Notebook 01.

---

## ✍️ Essential reading

- **[Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)** — Anthropic Engineering. The canonical map of agent patterns (workflows vs. agents); the backbone of the whole series. *(Also linked in Week 1 — re-read it now that you've built the patterns by hand.)*
- **[Prompt engineering — Chain-of-thought](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/chain-of-thought)** — Anthropic's practical guidance on eliciting step-by-step reasoning (the System-2 idea from Part 2).

---

## 📚 Foundational papers (the patterns, in order)

The Week 2 RAG corpus and the reasoning patterns come straight from these:

- **Chain-of-Thought Prompting** — Wei et al., 2022 · [arXiv:2201.11903](https://arxiv.org/abs/2201.11903)
  "Let's think step by step" — eliciting reasoning by writing intermediate steps.
- **ReAct: Synergizing Reasoning and Acting** — Yao et al., 2022 · [arXiv:2210.03629](https://arxiv.org/abs/2210.03629)
  Interleave Thought → Action → Observation. The loop Notebook 02 builds by hand.
- **Tree of Thoughts** — Yao et al., 2023 · [arXiv:2305.10601](https://arxiv.org/abs/2305.10601)
  Reasoning as search: propose, evaluate, expand the best, prune the dead.
- **Retrieval-Augmented Generation** — Lewis et al., 2020 · [arXiv:2005.11401](https://arxiv.org/abs/2005.11401)
  Ground the model in retrieved documents — the idea Notebook 03 implements end-to-end.

---

## How to use this list

Watch the **5-minute FC-vs-ReAct video** before (or right after) Notebook 02 — it crystallises the one idea the whole notebook is about. Keep the **LangChain docs** open while you run the notebooks. The **papers** are the original sources for each pattern; skim the abstract + figure 1 of each — they're short and very readable. When you're ready for more, the **`langchain-course`** repo is the natural bridge into Week 3's LangGraph material.
