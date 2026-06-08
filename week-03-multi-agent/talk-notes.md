# Week 3 — Talk Notes (block-by-block narration)

**From Loops to Graphs.** 120 min. You drive the notebooks; the room re-runs later. Colab links land in chat at the close. Slide deck: `slides.pptx` (25 slides).

---

## Block 0 · Recap + "the loop you can't pause" (8 min) — slides 2–6

- **Open with the callback.** "Last week the honest punchline was: the control loop *is* the agent. You hand-rolled ReAct before importing anything." Don't re-teach it — one slide.
- **The pivot (slide 4).** Walk the four things a `while` loop can't do cleanly: cycles-with-state, conditional routing, pause/resume/persist, parallel fan-out. Land it as: "each is awkward-to-impossible by hand; all four fall out if you model the agent as a *graph*."
- **Slide 5 (the graph diagram).** Point at it: "Nodes are functions. Edges are control flow. `add_edge` is a line, `add_conditional_edges` is an `if`, an edge pointing back is a `while`." That sentence is the whole framework.
- **Slide 6 (version cutover).** Two beats: (1) Week 3 leaves classic 0.3.x for LangGraph 1.0 — concepts carry, imports change. (2) Relief: LangSmith *just works* via env vars now; the Colab silent-failure from last week was a 0.3.x artifact. (If anyone fought it last week, this lands.)

## Block 1 · NB00 LangGraph core (17 min) — slide 8

- **Drive `00_langgraph_intro`.** Run the pure-Python graphs FIRST (no LLM): `shout → tag`, then the conditional-edge cycle that loops until `count >= 3`. "This is a graph — and it's just a script you can inspect."
- The payoff cell is the **conditional edge + back-edge**. Say out loud: "the graph owns the stop condition — that's what lets us later pause it, checkpoint it, hand it to a human."
- Then the minimal LLM chatbot (`add_messages` reducer) — "this three-line graph is the template under every notebook today." End on `.stream()` (watch each node fire).

## Block 2 · NB01 Reflexion (22 min) — slides 10–11

- **Diagram first (slide 10).** generate → reflect → revise. The key idea: *the critique is persisted in state*, so revisions converge instead of wander.
- **Drive `01_reflexion_agent`.** Show the structured `Critique` (score + suggestions) — "we branch on a *number*, not prose." Run the loop on the sepsis-ML abstract; narrate the score climbing 1→… toward the bar.
- Turn on LangSmith (env-var cell) and re-run — "the whole loop is one trace tree." If it doesn't appear instantly, it's the background flush, not a failure (give it a few seconds). *Backup:* if no LangSmith key in the room, skip — the loop still runs.

## Block 3 · NB02 Agentic RAG (30 min) — slides 13–14

- **Diagram (slide 13).** Corrective RAG: retrieve → grade docs → (ok → generate | weak → web_search → generate). "The grader is the agentic part."
- **Drive `02_agentic_rag`.** Note the corpus is small *on purpose* (free embedding tier is rate-limited — flag this; it's the one quota to respect). Run the two questions: the in-corpus one passes the grader straight to generate; the out-of-corpus one trips the grader → web-search fallback. That contrast *is* the lesson.
- **Slide 14 (three patterns table).** CRAG / Self-RAG / Adaptive are three points on the same graph — a grader and a conditional edge, composed differently. Show the Self-RAG generation-grader cell briefly; describe Adaptive's front router. Don't build all three live.
- *Backup:* if embeddings 429, the notebook falls back to a tiny corpus; if it still stalls, talk to the diagram — the graph is the point, not the corpus size.

## Block 4 · NB03 Production (23 min) — slides 16–18

- **Diagram (slide 16).** Week 2's ReAct loop as two nodes: `agent ↔ tools` (ToolNode), `tools_condition` closes or continues.
- **Drive `03_production_graph`** as four small additive steps:
  1. The 2-node ReAct graph runs.
  2. `MemorySaver` + `thread_id` — the follow-up with a pronoun ("how many years before *that*?") resolves only because it remembered. Switch `thread_id` → it forgets. That's the memory boundary, made visible.
  3. `interrupt_before=["tools"]` — the graph *pauses* before acting; inspect `pending.tool_calls`; resume with `invoke(None, cfg)`. "This is impossible with a plain loop."
  4. `SqliteSaver` (durable) + the async fan-out (3 nodes concurrently, reducer accumulates).
- **Scientist framing (slide 17 card):** "an assistant that remembers your last question and asks permission before it writes to a DB or kicks off a long job."

## Block 5 · NB04 Capstone + deployment (15 min) — slides 20–23

- **Diagram (slide 20).** Supervisor → {researcher, writer}. "Multi-agent is *specialisation, not headcount*."
- **Drive `04_multiagent_deep_research`** as a *tour* (don't type along). Run the supervisor→researcher↺→writer graph once on a clinical-reliability question; show the planned subtopics + the synthesised brief.
- **Slide 21 (real systems table)** then **slide 22 (TriAgent diagram).** Land the capstone line: "every box in TriAgent's Deep-Research node — supervisor, retrieval sub-agents, findings-synthesis — is a node you just built. Multi-agent isn't a new framework; it's these primitives, composed for a real clinical-research problem." (Tie to your own work.)
- **Slide 23 (deployment).** 60-second tour: Studio (visual IDE), Cloud/Platform (graph as API), LangSmith (trace + eval). "Everything today is a compiled graph object; deployment wraps it — the graph doesn't change."

## Close (5 min) — slides 24–25

- Five notebooks recap; Colab links into chat (`week-03-multi-agent/notebooks`). "Fork them, break them." One-line Week 4 tease: evaluation + domain agents.

---

## Backup Q&A

- **"Why not just use `create_react_agent` from last week?"** — You can, for a plain tool loop. The moment you need memory, a human pause, branching, or parallelism, you need a graph. LangGraph's prebuilt `create_react_agent` is itself a compiled graph.
- **"LangGraph vs CrewAI / AutoGen?"** — LangGraph is lower-level and explicit (you draw the graph); CrewAI/AutoGen are higher-level role abstractions. LangGraph gives you the control production needs (checkpoints, interrupts, streaming). open_deep_research and TriAgent are LangGraph.
- **"Is this free?"** — Yes: gemini-2.5-flash + gemini-embedding-001 free tier. The one limit to respect is the embedding rate cap (hence the small corpus in NB02).
- **"Does LangSmith cost?"** — Free Developer plan. Optional — every notebook runs without it.
- **"Can it call real tools / PubMed?"** — Yes; swap the mock `web_search` for Tavily (key in NB02), or wire any function as a `@tool` (NB03). The graph doesn't change.
