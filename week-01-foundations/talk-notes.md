# Speaker Notes — GenAI Foundations for Scientists

90 min · in-person + Zoom + recorded · bold-opinion voice on vibe coding

> Voice rules: American spelling. No marketing fluff. The Idea Inbox is **never** called an agent. Attribution gets named (Ivakhnenko, Hochreiter, Ciresan) at least once each.

---

## Block 0 · Hook + roadmap (5 min)

**Slide 1 — Title slide**

Land softly. Walk people in.

> "Welcome to Week 1 of *Agentic AI for Scientists*. Today is foundations. By the end of these 90 minutes, three things will be true:
> one, you'll know the actual history of how we got here;
> two, you'll have a strong opinion about a thing called vibe coding;
> three, you'll be holding your phone and looking at a real URL — for an app you watched me build with Claude in 35 minutes, deployed live to the internet."

**Slide 2 — Roadmap**

> "Here's the shape of the next 90 minutes. History first — short, but not shallow. Then a paradigm question. Then the build. Then a teaser of where this all goes if you keep pulling the thread."

Set the rule: questions held to the end except for clarifying questions during the build.

---

## Block 1 · A short history (12 min)

**Posture:** This block earns scientific respect or loses it. Be precise with names and years. Don't editorialize Schmidhuber's polemic; just credit the real inventors and let the audience draw conclusions.

**Slide — "Three threads"**

> "Most pop-history of AI sounds like: rules in the 50s, neural nets in the 80s, deep learning in 2012, ChatGPT, the end. That story is wrong. The real story has three threads — math, algorithms, hardware — and each one waited decades for the next."

**Slide — "Math came first"**

> "Leibniz, 1676. The chain rule of calculus. That's how you propagate credit through a network — every neural net trained since uses Leibniz's chain rule. Then Gauss and Legendre, 1795 to 1805 — least squares. That's a linear neural network. It's the same math you use when you fit a regression today."

**Slide — "Algorithms came before you were born"**

> "Ivakhnenko, USSR, 1965 — first deep multi-layer perceptron. Trained, layer by layer, on real data. This is twenty years before what most people call the start of deep learning."
>
> "Amari, 1967, deep stochastic gradient descent. Linnainmaa, 1970, backpropagation — published as reverse-mode automatic differentiation. Fukushima, 1979, convolutional networks. He'd published the ReLU activation in 1969. Most of what you call deep learning was solved before you were born. It just didn't scale."

**Slide — "1991 was the year"**

> "Sepp Hochreiter, diploma thesis, 1991. He identifies why deep nets stop learning — vanishing gradients — and the same year, with Schmidhuber, publishes LSTM. Now the most cited AI paper of the 20th century. Same year, the Neural History Compressor — self-supervised pretraining. The 'P' in ChatGPT, in 1991. Same year, fast weights with key-value patterns — mathematically equivalent to the Transformer attention block, twenty-six years before the Transformer paper."

**Slide — "Hardware finally arrived"**

> "And then nothing happens for nineteen years. Why? Compute is too expensive."
>
> "2010 — Ciresan, GPU, MNIST. New record. Then DanNet — superhuman traffic-sign recognition, five months before AlexNet. Same algorithms from the 60s. Same gradient descent. Just GPUs."

**Slide — "Everything since is rescaled"**

> "ResNet, 2015 — that's an unfolded LSTM. Transformer, 2017 — that's 1991 fast weights with a softmax. The architecture revolution was 1991. The hardware revolution was 2010. Everything since is engineering."

**Slide — "Models to agents"**

> "What ChatGPT showed us in 2022 is that next-token prediction at scale is shockingly good. But notice what it doesn't have. No memory beyond a context window. No identity that persists. Can describe a Bash command but can't run one. Doesn't update from your last conversation."
>
> "Add those four atoms — memory, identity, tools, learnings — and you get something different. You get an agent. That's the new layer."

**Slide — "Throughline"**

> "Math waited 290 years for algorithms. Algorithms waited 45 for hardware. Hardware waited 14 for architecture. We're at the architecture moment. Unlike the prior three, you don't have to wait — you can build in this layer this afternoon."

---

## Block 2 · What makes an agent (10 min)

**Posture:** Concrete, not abstract. Show real files from this repo, on screen. Let the audience see that "agents" are not magic — they're files plus a loop.

**Slide — "Function vs. system"**

> "An LLM call is a function. Input goes in, output comes out, the function forgets you exist. An agent is a loop. Read memory. Check tools. Act. Write memory. Loop. The loop is the difference."

**Slide — "Memory"**

Open a real `context/memory/2026-05-10.md` snippet on the screen.

> "This is a real file from this morning. When the agent wakes up tomorrow, it reads this. It picks up where it left off. Open threads, deliverables, decisions — all there. This is not Slack history. It's a written record the system maintains for itself."

**Slide — "Identity"**

> "This file is the constitution. It's the first thing the agent re-reads at every session. 'Be genuinely helpful, not performatively helpful.' 'Have scientific opinions.' This is what stops it from being a chatbot. Models without an identity file will say whatever you want; agents with one push back."

**Slide — "Tools"**

> "Sixty-plus skills, each in a folder. Each has a contract — what it triggers on, what it produces. The agent matches the user's words to the right skill. That's tool use."

**Slide — "Learnings"**

> "This is the part that compounds. Every time the agent gets feedback — 'no, don't do it that way', 'yes that worked' — it writes it here. The next session reads this *before* attacking a similar problem. That's how you get an agent that gets sharper, not one that resets every Monday."

**Slide — "Take one away"**

> "Take memory away — it's a chatbot. Take identity away — it's a wrapper around an API. Take tools away — it's a summarizer. Take learnings away — it's a demo. The LLM is the engine. The four atoms are the car."

---

## Block 3 · Vibe coding (8 min)

**Posture:** Bold. This is the section where you have an opinion and defend it. Use the word "honestly" twice — once at the start, once at the end. Acknowledge the tradeoff at the end so the bold opinion lands as considered, not glib.

**Slide — "A new rung on the ladder"**

> "We've been climbing this ladder for seventy years. Machine code in the 50s. Assembly in the 60s. C in the 70s. Python in the 90s. English in 2024. Each rung up: fewer lines you write, more abstraction you trust."
>
> "Vibe coding is the next rung. That's not a slogan. That's the trajectory."

**Slide — "What changes / what doesn't"**

> "What changes: you write paragraphs of intent, not lines of syntax. You ship in 35 minutes what used to take a week."
>
> "What doesn't change: the architecture is still your call. The tests are still your contract. The judgment is still yours. The work didn't disappear — it moved to where it always should have been."

**Slide — "The new contract"**

> "If you can describe the architecture clearly, and you have an end-to-end test suite that catches what matters, you don't need to read every line. This is not radical. Python developers don't read CPython source. You don't audit `numpy.dot` before using it. The abstraction has just moved one rung up."

**Slide — "Honest failure mode"**

This is the slide where you earn the bold opinion. Don't skip it.

> "Here's where this fails. Vibe-coded code that passes the vibe but breaks the tests. Looks right. Demo works. Fails on the second user. If you don't have tests, vibe coding is a foot-gun. The bolder your vibe coding, the stricter your test suite must be. That is not optional."

**Slide — "What you trade"**

> "You give up reading every line. You give up knowing each commit personally. You give up the romance of authorship. You get leverage — shipping in hours, iterating on architecture instead of syntax."
>
> "Some scientists love this trade. Some don't. Both positions are honest. I'm in the love-it camp. Let me show you why."

Cut to Block 4.

---

## Block 4 · Live build (35 min)

**Posture:** Confident, narrate every prompt before you type it. The audience is watching *you* drive Claude — they should hear the *intent* first, then watch Claude execute it. That's the lesson.

**Discipline:** never call the Idea Inbox an agent. Use "the app", "the build", "the LLM call", "the vibe-coded tool". Save "agent" for Block 5.

**Sub-block 1 (3 min) — premise**

(See `WORKSHOP_PROMPTS.md` for the literal opening line.)

> "Real Supabase, real auth, real Vercel deploy. About thirty minutes. I'm going to type prompts in plain English. Watch what I do versus what Claude does."

**Sub-block 2 (8 min) — scaffold + landing page**

Before typing, narrate the intent:

> "I want a landing page. Hero, textarea, save button, list of saved ideas. shadcn for the components — that's a design-system choice I made. Dark mode by default — that's an aesthetic call I'm making. Monospace headings — scientist aesthetic, no marketing fluff."

Type the prompt. Watch Claude work.

If it overshoots: refine *once*, no more. Show the refinement loop on screen.

**Sub-block 3 (7 min) — Supabase**

> "Now backend. The schema is already in Supabase — I created it before this session because we have 30 minutes, not an hour. I'm telling Claude the schema, telling it which package to use — `@supabase/ssr` — and asking it to wire insert and fetch."

After Claude runs: switch to the Supabase Table Editor tab, save an idea live, show the row landing in the table.

**Sub-block 4 (5 min) — auth**

> "Auth. Supabase magic-link — that's an architecture call. RLS — that's the security model. Sign-out button in the header — that's a UX call."

Sign in with your own email live. Show the Supabase Auth → Users tab where your user just appeared. This always lands well.

**Sub-block 5 (6 min) — AI feature**

> "Now the AI. Expand button per idea. Vercel AI SDK — that's a stack call. Claude Haiku 4.5 — that's a cost call, fast and cheap. Stream the response — that's a UX call. Save the result back to the row."

When the expansion streams in: pause, let the audience watch it appear. That's the magic moment.

**Sub-block 6 (4 min) — deploy**

While `vercel deploy --prod` runs, fill the time:

> "While this builds — about 60 seconds — notice what just happened. I described what I wanted in five paragraphs of English. Claude wrote about 600 lines of TypeScript. I made the architecture calls. I didn't write any of the code. That's the new contract."

When the URL prints: open it on your phone. Walk to the front of the room if in-person. Show it to the audience. *Tell them they can visit it too — read the URL out loud.*

**Sub-block 7 (2 min) — reflection**

This is the bridge. Read it carefully — it's the load-bearing line.

> "What you just watched is an LLM-powered CRUD app. It is not an agent. It has no memory across sessions — the database stores rows, not context. It has no identity — there's no soul file. It has no tools beyond a single API call. It has no learnings — it won't be sharper tomorrow."
>
> "It's the engine. Not the car. The car is what the next 15 minutes is about."

---

## Block 5 · Organon teaser (15 min)

**Posture:** This is a teaser, not a feature tour. Show one researcher journey end to end. Don't get lost in any single panel. Set up future weeks.

**Slide — "Same kernel, scaled"**

> "What we just built — paste, store, expand — is one prompt, one model call, one row. Organon is the same kernel taken seriously. One research question. Sixty-plus skills. Memory. Learnings. A council of personas. A citation graph. A manuscript draft. Same idea, different scale."

**Slide — "Architecture"**

Show the SOUL/USER/memory/learnings + skills sketch. Then say:

> "These are the four atoms from Block 2, made real. Files on disk. The agent reads them at every session. The skills are real folders, real code. There's no magic."

**(switch to dashboard)**

Walk through one journey:

1. Type a research question
2. Run literature search → 8 papers, scored
3. Generate a hypothesis from one paper, send to council, 3 personas critique
4. Drop in the bacterial cohort CSV → t-test + plot
5. Drop both into a manuscript section → draft writes itself
6. Pop the citation graph → "and this is the artifact substrate"

> "Eighteen minutes ago, we built an LLM call. Now you're looking at a hypothesis being critiqued by three personas with different epistemic styles, against a literature corpus the system pulled itself, with a draft section being written from the result. Same paradigm, an order of magnitude more agency."

**Slide — "Where the series goes"**

> "This is Week 1. Week 2 we build *your* first agent — skills, memory, soul. Week 3 we put it to work on a real scientific workflow. Week 4 we go further — cost, safety, when *not* to use this. Each week stacks on the last."

---

## Block 6 · Close (5 min)

**Slide — "Homework"**

> "If you want homework — and only if you want it — install Claude Code, clone the Idea Inbox starter from the workshop folder in the Organon repo, and *break* one thing. Replace the theme. Swap the model. Try a different deploy target. Bring what broke to Week 2. The fastest way to learn this is to break something on purpose."

**Slide — "Resources"**

Read the four URLs.

> "Questions?"

---

## Q&A backup script

| If asked | Answer with |
|---|---|
| "Didn't [famous person] invent X?" | Backup slide. Stay neutral on Schmidhuber's polemic; just credit the real inventors. "He's pointed about attribution. The dates are correct." |
| "How much does this cost?" | Backup slide. Total today: ~$3. Real Organon project: ~$5–15 per finished manuscript. |
| "What about hallucinations?" | Backup slide. "LLMs hallucinate. So do graduate students. The discipline that catches both is tests + citation gates + human review + reproducibility checks. Vibe coding fails when there are no tests." |
| "Is this just hype?" | Backup slide. "Possibly. Some of this stack will look quaint in 2030. What won't look quaint: knowing how to specify intent, write good tests, and know what a system *should* do." |
| "How does this compare to AI-Scientist / AlphaEvolve?" | "Different trade. They optimize for autonomy — the human is mostly out of the loop. I optimize for catchability — every step is something a researcher can read, redirect, or override. Both are valid; my read is that catchability is the more durable shape for science." |
| "Can I use this for [specific domain]?" | "If your domain has scientists writing papers, analyzing data, and reading literature — yes. If it's purely wet-lab, partly. Bring it to Week 3, that's the workflow week." |

---

## If the live build snags

| Symptom | Action | Filler line |
|---|---|---|
| Claude misreads a prompt | Cancel, restate more concretely | "I'm being too vague. Watch what specificity does." |
| `npm run dev` won't compile | Show error to Claude; if not fixed in 30s, switch to fallback recording | "And this is what an honest live demo looks like — let me cut to the recording while I debug offline." |
| Supabase RLS blocks reads | Re-run the schema from the SQL editor | "Row-level security is doing its job — almost too well. Re-applying the policies." |
| Vercel deploy >2 min | Filler: walk through the file Claude just wrote | "While Vercel builds, let me show you what's actually in this file." |
| Anthropic rate limit | Switch to Sonnet 4.6 in code, restart | "Rate limit. Swapping models — this is also a real-world skill." |

---

## Closing energy

End on the homework prompt, not the resources slide. Energy higher → audience walks out wanting to try it tonight. Resources can be on the recap email.

The line that should be the last thing they hear:

> "Break something on purpose. See you next week."
