# Week 2 — Talk Notes

**Format:** part-by-part speaker notes plus backup Q&A. Read top-to-bottom; it mirrors `slides/slides.md` slide order.

**The arc in one line:** open the box (why LLMs work) → climb the ladder (bare model → tools → reasoning) → pick up LangChain → give it memory (RAG). The notebooks are clustered after the LangChain intro, because every notebook uses LangChain.

**Discipline:** the four Colab notebooks open in **separate** tabs *before* the room sits down, with all setup cells already run. Don't switch tabs in front of the audience — alt-tab between the deck and the relevant notebook.

**Timing (120 min):**

| Part | Min | Slides | Notebook |
|---|---|---|---|
| 0 · Hook + W1 recap | 5 | 1–3 | — |
| 1 · Why LLMs work | 18 | 4–10 | — |
| 2 · The agentic ladder | 25 | 11–21 | — |
| 3 · LangChain + hands-on | 40 | 22–27 | ▶ 00, 01, 02 |
| 4 · RAG | 27 | 28–34 | ▶ 03 |
| 5 · W3 bridge + wrap + Q&A | 5 | 35–42 | — |

Soft 90-second stretch at the ~65-min mark (start of Part 3, before the first notebook).

---

## Part 0 — Hook + Week 1 callback (5 min)

**Slides 1–3** (title → "Where we left off" → Week 1 recap)

### Narration

Open standing. Wait for the room to settle.

> *"Last week we traced how we got here — punch cards to natural language — and met Claude Code and Organon: working agents, built as plain files on disk. We landed on one equation: an agent is an LLM plus four primitives — memory, identity, tools, learnings."*

(Beat.)

> *"What we did NOT do is open the hood. Why does the model work at all? And what actually turns a bare model into something that uses tools, reasons, and remembers? That's today.*
>
> *We do two things. First we open the box — why a language model works. Then we climb a ladder: take that bare model and add one capability at a time until it's a reasoning, tool-using agent with memory. By the end you'll have run five notebooks and you'll never again think 'agent' is magic."*

Click to the Week 1 recap slide.

> *"Quick recap on the left — what we shipped. On the right is the shape of today: open the box, climb the ladder, pick up LangChain, add RAG. Five Colab notebooks back the right-hand column. You'll run them as we go."*

### Backup answers

- **"Is the loop just async / streaming?"** No. Streaming returns one response in pieces. An agent runs multiple full LLM calls with tool results between them.
- **"Is GitHub Copilot an agent?"** Inline completion isn't. Copilot Chat with file edits + terminal access is — tools and a loop.
- **"Do we need Week 1 to follow today?"** No. Everything is rebuilt from first principles.

---

## Part 1 — Why LLMs work (18 min)

**Slides 4–10** (opener → the unlock → next-token → tokens/embeddings → attention → scaling/emergence → cognitive fit)

This is the part most agent workshops skip. Don't. If people understand *why* the model is good at language, "tools" and "reasoning" stop feeling like magic stacked on magic.

### Narration

**Opener ("Opening the box").**

> *"Six slides on what a language model actually is. I'm not going to make you derive backprop — I want you to leave with a working mental model, because every pattern later today is a small twist on it."*

**"The unlock: one architecture, three exponentials."**

> *"For sixty years language AI was hand-written rules and narrow models. Three things changed at once. One: the architecture — the Transformer, 2017, the 'Attention Is All You Need' paper, which is literally one of the five papers in today's RAG corpus. Two: scale — parameters went from millions to hundreds of billions. Three: data and compute — train on much of the public web."*
>
> *"The deep point is the 'bitter lesson': general methods that scale with compute beat clever hand-crafted ones. The Transformer was the first language architecture that just kept getting better the more you fed it."*

**"One dumb objective: predict the next token."**

> *"Here's the training objective, and it's almost insultingly simple: guess the next token. 'The capital of France is' — and the model puts 91% on ' Paris.' That's it. No labels, no human annotation — the text is its own answer key, which is why you can train on trillions of tokens."*
>
> *"Why is that enough? Because to predict the next token across ALL of human text, you're forced to learn grammar, facts, translation, arithmetic, a bit of reasoning. Compression is understanding — squeezing the web into a fixed set of weights forces useful abstractions to fall out."*

**"How text becomes math: tokens → embeddings."**

> *"Two steps to turn text into something math can touch. Tokenisation splits text into sub-word pieces — 'agentic' becomes 'agent' + 'ic'. Then each token becomes a vector in a few-hundred-dimensional space. And meaning becomes geometry: 'king minus man plus woman' lands near 'queen.' Hold onto this slide — the SAME embedding idea is exactly how RAG retrieval works in Notebook 03."*

**"The engine: attention as learned relevance."**

> *"This is the one mechanism worth knowing by name. 'The scientist read the paper because IT was…' — what does 'it' refer to? Attention lets each token look at every other token and weight them by learned relevance. 'It' attends strongly to 'paper.' Stack that operation a few dozen times and you get rich, context-aware meaning."*
>
> *"Two properties changed everything. It's parallel — the whole sequence at once, where the old RNNs went word by word, and that parallelism is what made web-scale training possible. And it's long-range — a token can attend to anything in the window, not just its neighbours."*

**"Scaling laws & emergence."**

> *"Two ideas. First, scaling laws: performance improves PREDICTABLY with size, data, and compute — smooth power-law curves. The Chinchilla paper — paper #3 in today's corpus — found the compute-optimal recipe is about 20 training tokens per parameter, and that most early models were badly under-trained. You'll literally retrieve this exact claim in Notebook 03."*
>
> *"Second, emergence: some abilities are just ABSENT in small models and appear fairly abruptly past a scale threshold — in-context learning, multi-step arithmetic, instruction following, and chain-of-thought reasoning. Everything we build today emerged from scale. Nobody hand-coded it."*

**"Why this architecture fits us so well."** Slow down here — this is the bridge into agents.

> *"Why does this particular technology feel so natural to work with? Two reasons. Language is humanity's API — we already encode knowledge and intent in text, so a model fluent in text plugs straight into how we work. And in-context learning is like working memory — put facts in the prompt and behaviour adapts on the spot, the way you hold instructions in mind for one task."*
>
> *"Now the idea that powers the rest of the day. Kahneman: System 1 is fast, automatic, intuitive; System 2 is slow, deliberate, step-by-step. A raw next-token answer is System-1-like — one fluent pass. And the entire trick of 'reasoning' that we're about to build is just: make the fast model slow down and deliberate. That's chain-of-thought. That's ReAct. Hold that thought."*

(Flag the disclaimer line.) *"This is an analogy, not a claim that the model literally thinks — but it's a genuinely useful map for why the patterns work."*

### Backup answers

- **"Is next-token prediction really all it does?"** At training time, yes — that single objective. The richness is emergent: modelling the text well requires modelling the world that produced it.
- **"What's a token, exactly?"** A sub-word unit from a fixed vocabulary (~tens of thousands). Common words are one token; rare words split into several. Roughly ¾ of a word on average in English.
- **"Does attention 'understand' meaning?"** It computes weighted relevance between tokens. Whether that's "understanding" is philosophy; operationally it produces representations that support the behaviours we see.
- **"Are scaling laws still holding?"** Broadly yes, though the frontier has shifted toward data quality, post-training (RLHF/RLAIF — paper #4 today), and inference-time compute (reasoning models). Chinchilla's "scale data and params together" still holds.
- **"What's the context window?"** The max tokens the model can attend over at once. Bigger windows = more it can hold, at higher cost per call. Relevant later: RAG exists partly so you don't stuff everything into the window.

---

## Part 2 — The agentic ladder (25 min)

**Slides 11–21** (opener → ladder → anatomy → L0 → L1 → L2 intro → CoT → ToT → ReAct → ReAct trace → two ways to pick a tool)

### Narration

**Opener + "the ladder" slide.**

> *"Here's the spine of the next 25 minutes. A ladder. L0 is the bare model — one prompt, one answer. L1 adds tool use — the model can act on the world. L2 adds reasoning — chain-of-thought, tree-of-thought, ReAct. L3 is multi-agent systems, and we're deliberately NOT climbing that today — that's Week 3. Everything today is a single agent."*
>
> *"The key idea: each rung adds ONE capability to the rung below. Nothing here is a new model. It's the same LLM with more scaffolding. The agent is the loop you wrap around the model — not the model itself."*

**Anatomy slide.** Walk it with a pointer.

> *"Three components: tools give capability, memory gives state, the control loop gives agency. Take away the loop and you're back to a single model call. Take away tools and you've got a chatbot. Take away memory and the agent has amnesia."*

**L0 — the bare LLM.**

> *"Start at the bottom. A bare model is a brilliant improviser with no hands, no memory of today, and no scratchpad. It can't know anything after its training cut-off, can't look up a fact it didn't memorise, can't do anything in the world, and it'll happily get long arithmetic wrong with total confidence. Every rung above removes one of those limits."*

**L1 — tool use.**

> *"Rung one: give it hands. A tool is just a function the model can ask you to call. The loop is five steps — the model reads the question and the tool list, it says 'call calculator with this input,' YOU run the function, you feed the result back, and you loop until it's done. Crucial point: the model never runs anything. It requests; your code executes."*
>
> *"The modern version is 'function calling' — the model is fine-tuned to pick a tool and fill its arguments from a schema. And notice where the responsibility sits: the VENDOR trained the tool-picking skill; YOUR job is clear tool names and descriptions. Suddenly the model can fetch fresh facts and act — L0's ceiling is gone."*

**L2 intro — "make the fast model slow down."**

> *"Rung two is the System-1-to-System-2 jump from Part 1. Same model, but we change the prompt so it deliberates. Three flavours: chain-of-thought thinks in a straight line, tree-of-thought branches and searches, and ReAct couples reasoning to L1's tools. Let's take each."*

**Chain-of-Thought slide.**

> *"Five words change the answer: 'Let's think step by step.' The juggler problem — 16 balls, half golf balls, half of those blue. Asked directly, the model might just blurt a number. Asked to think step by step, it writes 16 → 8 golf → 4 blue, and the reasoning is visible and checkable. It's using its own intermediate tokens as a scratchpad. That's System 2, summoned by a prompt. CoT is the base; ReAct extends it."*

**Tree-of-Thoughts slide.**

> *"CoT commits to ONE line of reasoning. If step one is wrong, the whole chain is wrong. Tree-of-thought treats reasoning as search: propose several candidate thoughts, evaluate each as promising or dead, expand the good ones, backtrack out of dead ends. It buys accuracy on problems where a single chain routinely fails — planning, puzzles, proof search — by spending a lot more compute. Notebook 02 shows one propose-evaluate level live on the Game of 24."*

**ReAct slide + trace slide.** This is the heart of the day.

> *"ReAct: reason AND act. CoT thinks, L1 acts — ReAct interleaves them in one loop. Yao et al., 2022, the single most important agent paper to know. And the whole thing is a PROMPT. Read it: Thought, Action, Action Input, Observation, repeat, until Final Answer. There is no 'ReAct API.' It's English in a fixed format that the model produces and we parse."*
>
> *"One subtlety that makes it work" (point to the mechanism card) — *"we stop the model the instant it writes 'Action Input,' run the tool ourselves, and append the REAL observation. The model never gets to hallucinate the tool's output — it reads the one our code returned."*

Click to the trace slide.

> *"Here's a real trace. Thought: find the ReAct authors. Action: web_search. Observation: Yao et al. Thought: now the transformer year. Another search. Then calculator for the difference. Then Final Answer. Thought, Action, Observation, repeat — THAT loop is the agent. You'll build it by hand in Notebook 02."*

**"Two ways to pick a tool"** — the function-calling vs ReAct contrast.

> *"We've now seen two ways the model picks a tool, and the difference is genuinely important. The ReAct agent keeps tool choice in a PROMPT you write — high control, you can read and edit every step, but the parsing is brittle. The function-calling agent shifts tool choice to the VENDOR's native capability — structured, robust, no parsing, but you can't see or edit the selection logic."*
>
> *"The whole thing is a 'where do we put the responsibility' question. Most production agents use function calling. ReAct stays the clearest way to UNDERSTAND what an agent is — and the fallback when a model has no native tool-calling."*

### Backup answers

- **"Is CoT the same as a reasoning model (o-series / thinking models)?"** Same spirit, different delivery. CoT is prompt-elicited; reasoning models are post-trained to produce long internal chains by default. Both spend tokens before answering.
- **"When is ToT worth the cost?"** When one wrong early step dooms the answer and you can score partial states — puzzles, planning, search. For most Q&A it's overkill; CoT is enough.
- **"Why stop the model before the Observation in ReAct?"** Otherwise it cheerfully writes its own fake observation and reasons over fiction. The stop sequence forces it to wait for the real tool result.
- **"ReAct vs function calling — which should I use?"** Function calling on any modern model in production. Build ReAct by hand once to understand the loop; reach for it when you need full prompt control or a model without tool APIs.
- **"Where does Reflexion fit?"** It's "ReAct + a critique step fed back in" — the quality-first option. One-slide mention today; it composes on top of anything we build.

---

## Part 3 — LangChain + hands-on (40 min)

**Slides 22–27** (opener → what LangChain is → implements the ladder → structured output → demo-to-production → hands-on cluster) then **▶ Notebooks 00, 01, 02**

### Soft 90-second stretch (start of Part 3, ≈ 65-min mark)

> *"We're about two-thirds in and about to go hands-on. Stand up, stretch for 90 seconds, then we move to Colab for the rest."*

(Don't sit. Don't open a tab. Resume in exactly 90s.)

### Narration — the LangChain intro (slides 22–24, ~8 min)

> *"We've climbed the ladder BY HAND in our heads. LangChain is just the standard toolkit that implements every rung, so you don't re-write the loop each time. One sentence: it's a thin, vendor-neutral layer over 'call a model, give it a prompt, maybe tools, parse the output.' The exact same code runs on Anthropic, OpenAI, or Google."*

**"What LangChain is."** Point at the five-piece table + the LCEL code.

> *"Five pieces: a model wrapper, message types, prompt templates, output parsers, and tools. And one operator that ties them together — the pipe. 'prompt pipe llm pipe parser,' exactly like a Unix pipe, data flowing left to right. That's the whole mental model. And it isn't magic — everything we built by hand, the tool loop, the ReAct parse, LangChain wraps in one call. Because you built the primitive first, the abstraction is transparent."*

**"LangChain implements the ladder."** This slide is the payoff of Part 2.

> *"Read this table left to right — it's the whole day in one grid. L0 by hand was client-dot-models-dot-generate-content; in LangChain it's ChatGoogleGenerativeAI-dot-invoke. L1 was our for-loop and regex; in LangChain it's create_tool_calling_agent. L2 ReAct was our prompt and parser; it's create_react_agent. And RAG memory — manual chunk-embed-search — becomes loaders, splitters, vector stores, retrievers. We pin the classic LangChain 0.3 line, the last one with AgentExecutor. The newer LangGraph runtime is next week's reveal."*

**"Structured output" slide.**

> *"One more LangChain feature, and it's the twin of function calling. With the tool-calling agent, the model fills a schema to pick a TOOL. Here we point a schema at the ANSWER — define a Pydantic model with the exact fields you want, call with_structured_output, and the model hands you back a validated Python object. Not a string you parse — an object where result-dot-verdict is GUARANTEED to be one of your allowed values. This is how you make an agent's output safe to feed into the next step of a pipeline. Same machinery, aimed at the output instead of a tool. We run it live in Notebook 01."*

**"From demo to production" slide.** Quick, ~45 seconds — set expectations honestly.

> *"Two production notes so you're not surprised later. One: our notebooks MOCK the search tool so they run offline and the trace is reproducible. In production you drop in a real one — Tavily is built for agents — and the tool interface is identical, only the body changes. Two: observability. Set two environment variables and LangSmith traces every agent run — every Thought, every Action, tool latency, token counts — with zero code change. When a real agent misbehaves, you don't guess; you watch the trace."*

**"Hands-on: three notebooks."**

> *"Now we watch all of this run. Three notebooks back to back. Notebook 00 is LangChain in fifteen minutes. Notebook 01 is tool use, built three ways. Notebook 02 is reasoning — CoT, ReAct from scratch, ToT, and the function-calling-versus-ReAct contrast you just saw. Same model, same loops you saw on the slides — now step by step in code. Switch your eyes to Colab; don't type along, you'll fall behind. Links go in the chat at the end."*

### Notebook 00 — LangChain basics (~7 min)

Open the **Notebook 00 tab**. Setup cells already run.

1. **Model wrapper cell** — *"ChatGoogleGenerativeAI dot invoke. Notice it returns an AIMessage OBJECT, not a string — the text is in dot-content. That object-not-string detail matters the moment we start chaining."*
2. **Messages cell** — *"System sets behaviour, Human is the user turn. Same idea as the raw API, typed."*
3. **Prompt template cell** — *"A prompt with curly-brace slots you fill at call time."*
4. **LCEL chain cell** — the key one. *"prompt pipe llm pipe parser. The StrOutputParser pulls the text out so the chain returns a plain string. This three-piece chain is the spine of everything — a RAG chain is this with a retriever bolted on the front; an agent is this wrapped in a loop."*
5. **`@tool` cell** — *"The decorator reads the function's type hints and docstring to build the schema the model sees. Name, description, typed args — that's the entire contract behind function calling."*

> *"That's LangChain. Five pieces and a pipe. Everything else is built from these."*

### Notebook 01 — tool use, three ways (~10 min)

Switch to the **Notebook 01 tab**.

1. **Calculator + hand-built loop** — run, narrate the trace. *"The model emits 'CALL: calculator(...)' — that's just text. We parse it with a regex, run the function, append the result, re-prompt. Three turns, final answer."*
   - **The pause.** *"That is the entire idea of tool use. A for-loop, a function, and a way to recognise when the model wants the function. Frameworks add convenience, not new ideas."*
2. **Native tool-use cell** — *"Same control flow. The SDK gives typed tool_use blocks instead of regex — lower injection risk, type safety, identical loop."*
3. **LangChain tool-calling agent cell** — the third way. *"Now LangChain owns the loop. This is the function-calling agent: we hand it the tools, the VENDOR picks which to call. Watch the verbose trace — it called get_weather AND calc, then composed both answers, and we never wrote a loop. That loop is the same for-loop from the first two cells, now inside AgentExecutor."*
4. **Structured-output cell** (Section 5) — *"Same machinery, pointed at the answer. We define a Pydantic ClaimCheck with three fields, call with_structured_output, and ask it to check a claim. Look at the output — it's a ClaimCheck OBJECT, and result-dot-verdict is a guaranteed enum value. No parsing. This is the slide we just saw, running."*

> *"Three implementations of the loop, decreasing code, identical control flow — plus structured output as the function-calling twin. That's the takeaway."*

### Notebook 02 — reasoning (~15 min)

Switch to the **Notebook 02 tab**. This is the richest notebook. As you scroll, two short production callouts appear in the markdown — a **Tavily** note after the tools cell, a **LangSmith** note after the `create_react_agent` cell. Point at each for a beat ("real search drops in here", "tracing turns on here") and keep moving; they're the slides you just showed, in context.

1. **CoT cell** — *"Direct answer versus 'let's think step by step.' Watch the model lay out 16 → 8 → 4. Same model, the prompt summons the reasoning."*
2. **ReAct prompt + hand-built loop** — run, narrate the trace as it prints. *"Thought, Action: web_search, Action Input. We parsed it, called our mock, got 'Yao et al.', appended the Observation, re-prompted. Then the transformer year, then the calculator, then Final Answer. We built that loop — there's no framework here yet."*
3. **`create_react_agent` cell** — *"Same trace shape, same answer, one line. LangChain hides the loop in AgentExecutor-dot-invoke — but you just saw what's inside the box. And handle_parsing_errors=True is the seatbelt for when the model breaks format."*
4. **Live-add-a-tool cell** — the showpiece. *"I didn't touch the prompt. New tool in the list, the agent used it next iteration. The tool list IS the agent's vocabulary."*
5. **ToT cell** — *"Propose several first moves for Game of 24, then evaluate each as sure / maybe / impossible. That propose-evaluate-prune is the heart of tree-of-thought. The full algorithm recurses it; we show one level to keep it cheap."*
6. **FC-vs-ReAct contrast cell** — *"Same question through both agents. Same answer, two different mechanisms — ReAct parses text it wrote; the tool-calling agent gets a structured call from the model. Look back at the slide: it's the 'where's the responsibility' trade."*

### Backup answers

- **"Why pin LangChain 0.3 and not the latest?"** 0.3 is the last line with the classic AgentExecutor + create_react_agent. The newer 1.0 pushes everything to LangGraph, which is Week 3. Pinning keeps today stable and the abstractions readable.
- **"LangChain vs LlamaIndex vs Haystack vs DSPy?"** LangChain is the broadest and most common; LlamaIndex is RAG-first; Haystack is pipeline-first; DSPy treats prompts as programs you optimise. Pick one, learn the loop underneath — it's the same everywhere.
- **"`create_react_agent` raised an output-parser error — why?"** The model didn't follow the Action/Action-Input format. `handle_parsing_errors=True` feeds it a 'fix your format' nudge instead of crashing.
- **"Is the tool-calling output a string?"** On Gemini the tool-calling agent returns a plain string; the notebook keeps a tiny `as_text()` helper as a safe no-op in case a model ever returns content parts.
- **"How is structured output different from a tool?"** Same function-calling mechanism, opposite target. A tool's schema describes a *function to call*; `with_structured_output`'s schema describes the *answer's shape*. The model fills one or the other. Use structured output whenever the result feeds code that expects fixed fields.
- **"Is the Pydantic output guaranteed valid?"** The model is constrained to the schema and LangChain validates against the Pydantic model — if it can't conform, the call errors rather than handing you garbage. Far safer than 'respond in JSON' + a try/except.
- **"Do we need a Tavily / LangSmith key today?"** No. The search tool is mocked so the notebooks run offline, and the LangSmith snippet is commented out. Both are one-liners you enable in production — shown so you know they exist.
- **"Cost of a run?"** Each turn is one full LLM call — and these run on **Gemini's free tier**, so the whole session is free. (Free tier is rate-limited, so a heavy "Run all" may pause between calls; cell-by-cell live is smooth.)

---

## Part 4 — RAG (27 min)

**Slides 26–32** (opener → RAG diagram → build with LangChain pieces → three strategies → chunking → comparison → RAG vs raw LLM) then **▶ Notebook 03**

### Narration — the slides (~7 min)

**Opener + RAG-in-one-diagram.**

> *"Last rung's memory layer: RAG. Two halves. Retrieval finds the relevant chunks — using the exact embedding idea from Part 1. Augmentation stuffs them into the prompt. The model's job becomes 'answer from this context and cite it.' RAG isn't magic; it's grep with embeddings, plus 'show your sources.'"*

**"Build it with LangChain pieces."**

> *"Every stage is one LangChain class. PyPDFLoader to load, RecursiveCharacterTextSplitter to chunk, HuggingFaceEmbeddings to embed, FAISS or Chroma to store, BM25Retriever for keywords, EnsembleRetriever to fuse. FAISS is the fastest in-memory index; Chroma is a small persistent local DB — write once, reopen later, no re-embedding. Same retriever interface either way, so the rest of the pipeline doesn't care which you pick."*

**"Three retrieval strategies."**

> *"Dense embeds and compares — great for paraphrase, 'what does X mean.' Sparse is BM25 keyword scoring — great for exact terms like 'RLAIF.' Hybrid fuses both with reciprocal rank fusion and usually wins on getting the right SECTION, because it catches both query types."*

**"Chunking dominates."** The counterintuitive slide.

> *"People obsess over which embedding model to use. The bigger lever is usually chunking. 137 pages become 676 chunks at 800 characters with 100 overlap. Recursive splitting respects paragraph and sentence boundaries — the cheapest win in RAG. Sweep chunk size on your own corpus."*

**"Comparison" + "RAG vs raw LLM."**

> *"Two metrics — did we get the right PAPER, and did we get the right PART of it. On our clean 5-paper corpus all three retrievers nail both. On a big messy corpus, hybrid pulls ahead. And the punchline" (RAG-vs-raw slide) *"same question, with and without retrieval. Raw, the model answers from memory — no citation, possibly confidently wrong. With RAG, every claim points to a chunk you can re-read. Citations are the killer feature — not prompt magic, just retrieval plus 'cite your source.'"*

### Notebook 03 — RAG end-to-end (~20 min)

Switch to the **Notebook 03 tab**. **Skip cells 1–2 quickly** (download + load — scaffolding; pre-cached).

3. **Splitter cell** — *"676 chunks, each carrying its source and a chunk-id we can cite. split_documents keeps the metadata; that's how citations survive."*
4. **Embeddings cell** — *"Free local model, 384 dimensions, runs on Colab's CPU. Production: swap to OpenAI or Voyage — same interface."*
5. **FAISS cell** — *"from_documents embeds everything and builds the index in one call. as_retriever gives a standard query-to-documents component."*
6. **Chroma cell** — *"Same vectors, persistent on disk, identical retriever interface. Note: no .persist() needed in modern langchain-chroma — passing persist_directory auto-saves."*
7. **BM25 cell** — *"Keyword retriever from the same chunks."*
8. **EnsembleRetriever cell** — *"Fuse BM25 and FAISS with weights — reciprocal rank fusion under the hood, so no score-normalisation headache."*
9. **Comparison cell** — the punchline. Run, narrate the table. *"Right paper, and right section, for all three. On this corpus everyone wins; the honest test is a messy corpus where hybrid pulls ahead."*
10. **RAG chain cell** — *"The LCEL pipe: retriever-then-format into context, then prompt, llm, parser. The answer comes back with bracketed chunk-id citations — every claim grounded."*
11. **Raw-LLM cell** — *"Same question, no retrieval. Compare. No citations, and it can be confidently wrong on specifics."*

> *"Notebook 04 is optional homework — the same pipeline on real Elasticsearch with native RRF. Same recipe, production substrate."*

### Backup answers

- **"FAISS vs Chroma — which in production?"** FAISS for raw speed in-process; Chroma when you want persistence + metadata filtering without standing up a server. Past ~1M vectors, a managed store (Weaviate/Qdrant/Pinecone) or Elasticsearch.
- **"How often re-embed?"** Only when you change the embedding model. Same model = stable embeddings forever; new docs just get embedded and appended.
- **"Reranking (Cohere/BGE)?"** A reasonable extra step — retrieve top-50, rerank to top-5. Skipped for time; great next addition.
- **"Long-context models kill RAG?"** No. Long context is expensive per call and gives you no citations. RAG lets you keep a huge corpus and only send the relevant slice, with grounding.
- **"Graph RAG?"** For corpora with strong relational structure. Overkill for five papers; its own session.
- **"Why did the eval show 1.00 everywhere?"** Small, clean, well-separated corpus — the easy case, by design, so the pipeline is legible. The differences show up at scale and on noisier text.

---

## Part 5 — Week 3 bridge + wrap + Q&A (5 min)

**Slides 33–40** (opener → limits → retriever as W3 node → reading list → take-home → one sentence → questions)

### Narration

> *"A single ReAct-plus-RAG agent covers a huge amount of real work. So when do you actually need MORE? Four real limits — context overflow, no specialisation, sequential bottlenecks, hard-to-isolate failures. Those are the L3 rung we left off the ladder."*

Click to the W3-tool-node slide.

> *"And the punchline: the hybrid retriever you just built becomes a TOOL NODE in next week's LangGraph multi-agent researcher. We throw none of today's code away. The orchestrator changes; the building blocks don't. Same with your ReAct loop — it becomes a node in a graph."*

Reading-list slide, then take-home.

> *"Three things to read before Week 3 — the LangGraph quickstart, Anthropic's 'Building effective agents' post, and the GPT-Researcher repo. Five notebooks open in Colab from the repo — links going into chat now."*

(Paste links. Wait 10 seconds.)

One-sentence slide.

> *"One sentence to remember: a language model predicts the next token; an AGENT is the loop you wrap around it — tools give it hands, reasoning gives it a scratchpad, RAG gives it memory it can cite. Frameworks add ergonomics; they don't add the agency. Next week we wrap several of these into a graph. Thanks — I'll stay for office-hours Q&A at the front."*

### Backup answers

- **"Fine-tune vs RAG?"** Default RAG. Fine-tune only for style/format you can't prompt into, or proprietary language embeddings can't capture. Both rare.
- **"Simplest agent eval?"** Hit@k on a labelled retrieval set (we just did it) plus LLM-as-judge on grounded answers. Formalised in W5.
- **"What's a triagent?"** Planner decomposes, retriever runs RAG, writer composes with citations. The W3 demo.
- **"LangGraph vs the AgentExecutor we used?"** AgentExecutor is a single loop; LangGraph is a state machine of nodes and edges — multiple agents, branching, persistence. That's exactly why it's next week.

---

## Pre-stage prep (day-of, ~30 min before)

- [ ] **Four** Colab tabs open (00, 01, 02, 03), each on the first cell, all setup cells **already run** (saves 60–90s/notebook on stage). Tab 5 = Notebook 04 only if someone asks.
- [ ] `GOOGLE_API_KEY` set in each Colab via `userdata`; verify the setup cell prints **"Ready with model: gemini-2.5-flash"**
- [ ] Notebook 03: corpus PDFs downloaded **and** embeddings cell already run (don't make the room watch a download or a 676-chunk encode)
- [ ] Slides open in a **separate window** from the notebook tabs — never alt-tab between them
- [ ] Backup screen-recording of each notebook in case a cell fails live
- [ ] Chat tool ready with pre-typed Colab links to paste in Part 5
- [ ] Phone in pocket — open one Colab link from the phone in Part 5 to model the "fork and re-run" behaviour
- [ ] Glance the "▶ Switch to Colab" green markers in the deck — those are your tab-switch cues (end of Part 3 intro, end of Part 4)

---

## Risk handling on stage

- **Running long at the 100-min mark.** Cut in this order: ToT cell in NB02 (concept already on slides), the raw-LLM cell in NB03 (keep the comparison table + RAG chain — they're load-bearing), then trim Part 1 to the next-token + attention + cognitive-fit slides.
- **Running short.** Expand Part 1 (take questions on attention/scaling) and the reading-list slide.
- **A cell raises an exception.** Don't debug live. Click the deck forward, narrate what the cell *should* show, switch to the backup recording. (All four were validated end-to-end, so this is unlikely — most failures on the day are Colab disconnects, not code.)
- **Colab disconnects.** Reconnect, re-run setup cells (~30s; NB03 re-embed ~1 min). Narrate over the wait: "Colab times out aggressively; in production you'd use a persistent server."
- **Theory question derails Part 1 timing.** Park it: "Great question — holding it for Q&A so we get to the hands-on."
- **"This is too much theory, when do we code?"** *"Two more slides — I promise the model makes more sense once you know why it works."* Then move.
