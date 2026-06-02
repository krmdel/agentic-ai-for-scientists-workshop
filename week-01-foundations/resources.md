# Week 1 — Resources

Curated companion material for **Week 1: GenAI Foundations** (how we got here, Claude Code, and Organon). Watch and read these alongside or after the session to go deeper. The list grows over time — suggestions welcome via an issue or PR.

---

## 📺 Videos

Ordered roughly from "watch first" (short, big-picture) to "deep dive" (long, hands-on).

1. **[Why Coding Is Solved, and What Comes Next](https://www.youtube.com/watch?v=SlGRN8jh2RI)** — Boris Cherny (Anthropic) · Sequoia Capital · 25 min
   The big-picture framing: where AI-assisted coding is heading and why agents — not just autocomplete — are the next step. Good to watch before the session.

2. **[Every Level of Claude Code Explained in 39 Minutes](https://www.youtube.com/watch?v=Y09u_S3w2c8)** — Simon Scrapes · 39 min
   A structured tour of Claude Code from the basics up to the advanced primitives. Maps directly onto Week 1's "agent = LLM + primitives (memory, identity, tools, learnings)" framing.

3. **[Vibe coding in prod | Code w/ Claude](https://www.youtube.com/watch?v=fHWFF_pnqDk)** — Anthropic · 31 min
   An official Anthropic session on using Claude Code for real, production-grade work — not just toy demos.

4. **[Claude Code for Beginners Tutorial — Full Course](https://www.youtube.com/watch?v=gh2_PhgZGsM)** — freeCodeCamp.org · 4h 28m
   The deep dive: a complete hands-on course. Work through it after the session to build real fluency with the tool.

5. **[Build & Sell a SaaS With Claude Code + n8n + GSD](https://youtu.be/KeeU-_bLIwY)** — Simon Scrapes · 4h 37m
   An end-to-end project build — watch Claude Code drive a complete application from zero. For when you want to see the full workflow in anger.

---

## 📄 Official documentation

- **[Claude Code — Overview](https://code.claude.com/docs/en/overview)** — the official docs: install, `CLAUDE.md`, tools, skills, sub-agents, hooks, MCP.
- **[Claude Code on GitHub](https://github.com/anthropics/claude-code)** — source, issues, and release notes.
- **[Model Context Protocol (MCP)](https://modelcontextprotocol.io/)** — the open standard for connecting agents to external tools and data (the "USB-C port for AI").
- **[Organon](https://github.com/krmdel/organon)** — the agent-first Claude Code template for scientists used throughout this workshop.

---

## ✍️ Essential reading

- **[Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)** — Anthropic Engineering. The canonical primer on agent patterns (workflows vs. agents). The mental model the whole series builds on.
- **[Claude Code: Best Practices](https://code.claude.com/docs/en/best-practices)** — Anthropic. Practical guidance on `CLAUDE.md`, context, and agentic workflows.
- **[The Bitter Lesson](http://www.incompleteideas.net/IncIdeas/BitterLesson.html)** — Rich Sutton. Why general methods that scale with compute beat clever hand-crafted ones — the idea behind the "AI road" in the Week 1 deck.

---

## 📚 Foundational papers (the "AI road")

- **Attention Is All You Need** — Vaswani et al., 2017 · [arXiv:1706.03762](https://arxiv.org/abs/1706.03762)
  The Transformer. The architecture under every modern LLM.
- **Language Models are Few-Shot Learners (GPT-3)** — Brown et al., 2020 · [arXiv:2005.14165](https://arxiv.org/abs/2005.14165)
  Scale + in-context learning — the moment language models became general-purpose.

---

## How to use this list

If you're new to Claude Code: watch **#1 → #2**, install the tool ([SETUP.md](../SETUP.md)), skim the **Overview** docs, then dip into the **freeCodeCamp** course as needed. The papers are optional depth for the curious — the workshop doesn't assume them.
