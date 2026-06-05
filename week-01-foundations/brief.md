---
project: agentic-ai-workshop
status: active
level: 2
created: 2026-05-10
---

# Brief: GenAI Foundations for Scientists (Week 1)

**Series:** Agentic AI for Scientists
**Week 1 title:** GenAI Foundations for Scientists
**Subtitle on slides:** none (kept clean)
**Subtitle on registration card / Substack:** *"A short history, a new paradigm, and one app you'll deploy live."*
**Duration:** 90 minutes
**Format:** In-person (primary) + Zoom + recorded for async
**Audience:** Mixed scientific backgrounds, varying technical proficiency
**Date:** This week (lock at scheduling time)

## Goal

Land three things on a mixed scientific audience in 90 minutes:
1. The intellectual arc from rules → ML → transformers → LLMs → agents — so the rest of the series shares vocabulary
2. A bold-opinion take on vibe coding as a paradigm shift, backed by an honest live build
3. A working, deployed app the audience watches happen in real time, plus a teaser of where this paradigm goes if pulled all the way (Organon)

## Honesty contract

The Idea Inbox we ship in 35 min is an LLM-powered CRUD app, not an agent. Block 4 narration must never call it "an agent" — the contrast (LLM app vs. agent system) is the bridge into the Organon teaser. Bold opinion only works if attribution and scope are clean.

## Deliverables

- `slides.md` — Marp deck, ~28 slides, dark theme, scientist-aesthetic
- `slides.pdf` — exported for screen-share, projector, async
- `talk-notes.md` — speaker notes per block, with the bold-opinion script for §3 and the honest narration for §4
- `idea-inbox-starter/` — empty Next.js + shadcn + Tailwind shell, `npm install`-d, `npm run dev` boots clean
- `WORKSHOP_PROMPTS.md` — exact 5–6 Claude Code prompts to run live during Block 4, timed
- `supabase-schema.sql` — schema + RLS policies, copy-paste into Supabase SQL editor
- `.env.example` — placeholder env vars (Supabase + Anthropic)
- `README.md` — how to do a dry-run before the workshop

## Acceptance criteria

- [ ] Deck renders cleanly to PDF; no overflowing slides; diagrams embed correctly
- [ ] Idea Inbox starter `npm run dev` boots on localhost:3000
- [ ] Workshop prompts execute end-to-end in <35 min in a dry-run (verified by user)
- [ ] Block 1 history slides credit Ivakhnenko 1965, Hochreiter 1991, Ciresan 2010 by name
- [ ] Block 4 narration never calls the deployed CRUD app "an agent"
- [ ] Block 5 Organon teaser stays under 15 min and previews future weeks
- [ ] One backup slide for "wait, didn't [famous person] invent X?" Q&A pushback

## Timeline

| Block | Min | Cumulative |
|---|---|---|
| 0. Hook + roadmap | 5 | 5 |
| 1. History — three threads (math/algorithms/hardware) → why agents are next | 12 | 17 |
| 2. Agent atoms — memory, identity, tools, learnings (with Organon files) | 10 | 27 |
| 3. Vibe coding — bold opinion | 8 | 35 |
| 4. Live build: Idea Inbox → Next.js + Supabase + Auth + Vercel | 35 | 70 |
| 5. Organon teaser + series preview | 15 | 85 |
| 6. Q&A + close | 5 | 90 |

## Source material

- Schmidhuber, deep learning history — https://people.idsia.ch/~juergen/deep-learning-history.html (Block 1 attribution rigor)
- Organon repo — https://github.com/krmdel/organon (Block 5 demo + Block 2 atom files)
- Substack post — https://keremdelikoyun.substack.com/p/an-ai-agent-built-for-scientific (Block 5 framing, Substack arc)
- Anthropic devs presentation — https://x.com/eng_khairallah1/status/2052763325105365066 (voice/structure inspiration)

## Out of scope (Week 1 non-goals)

- Building your own skill (Week 2 or 3)
- Deep dive into Organon internals (Week 2+)
- Audience coding-along during Block 4 (would explode the time budget)
- "Agentic patterns" theory (Week 3+)
- Cost / safety / governance discussion (later weeks)

## Risks + mitigations

| Risk | Mitigation |
|---|---|
| Live build snags during Block 4 | Pre-recorded fallback video; switch screen-share instantly |
| Anthropic rate limit during build | Console pre-loaded with credits; can swap to Haiku 4.5 on the fly |
| Supabase project lag | Schema applied + warm-cached pre-workshop |
| Vercel deploy >2 min | Start deploy early; "while that builds, here's…" filler |
| Tech-skeptical scientist Q in §3 | Cautionary backup slide; honest acknowledgment that vibe coding fails without architecture + tests |
| Audience drift during history block | Cap at 12 min, one slide per beat, attribution as the teaching device (resonates with scientific audience) |

---

*Status: planning locked 2026-05-10 (Session 2). Next step: scaffold + draft deck.*
