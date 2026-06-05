# Week 01 · Foundations of Gen AI

90-minute session covering the 200-year abstraction arc + Claude Code primitives + Organon as an agentic OS for scientists. Live build of an Idea Inbox CRUD app. Demo of the workshop's pre-populated dashboard project and Obsidian vault.

## Slides

**Final deck:** [`slides/agentic-ai-workshop-week1.pdf`](slides/agentic-ai-workshop-week1.pdf) — the version used in the workshop.

## Resources

Curated companion material — videos, official docs, and reading for this week: **[`resources.md`](resources.md)**.

## What's in this folder

```
week-01-foundations/
├── README.md                          ← this file
├── brief.md                           ← Workshop brief (goal, audience, time budget)
├── talk-notes.md                      ← Speaker notes per block
├── WORKSHOP_PROMPTS.md                ← The 5–6 Claude Code prompts for Block 4 (live build)
├── PORTABILITY.md                     ← (Legacy — pre-repo-split portability notes)
├── WORKSHOP-DESCRIPTION.md            ← Original brief description (kept for reference)
├── slides/                            ← Final workshop deck
│   └── agentic-ai-workshop-week1.pdf
├── resources.md                       ← Curated videos, docs & reading for Week 1
├── dashboard-project/                 ← Drop-in for Organon's projects/briefs/agentic-ai-workshop/
│   ├── papers/                        ← 20 real PubMed papers as paperclip-*.json
│   ├── hypotheses/                    ← hyp-20260519-…/ + personas.json
│   │   ├── personas.json              ← 4 active personas (incl. Biostatistician)
│   │   └── hyp-20260519-8e8d0d/
│   │       ├── hypothesis.json
│   │       └── critiques/             ← skeptic, methodologist, domain-expert, biostatistician
│   ├── data/                          ← cohort_cbc_vitals.csv + analyze_cohort.py + preview JSON
│   ├── figures/                       ← fig-20260519-…/ (bone marrow stress response)
│   ├── manuscripts/                   ← cbc-vitals-antibiotic-response/ (6 sections)
│   └── .organon/runs/                 ← 10 simulated workflow entries
├── obsidian-vault/                    ← 43-note pre-populated knowledge graph
│   ├── .obsidian/                     ← Pre-configured graph.json (8 colour groups)
│   ├── README.md                      ← Vault gateway note
│   ├── identity/                      ← 3 notes (profile, interests, lab context)
│   ├── concepts/                      ← 11 concept notes
│   ├── paper-notes/                   ← 13 paper notes
│   ├── experiments/                   ← 3 hypothesis notes
│   ├── data-notes/                    ← 3 data observation notes
│   ├── drafts/                        ← 2 draft pointers
│   ├── daily/                         ← 4 daily session logs
│   ├── inbox/                         ← 5 quick-capture notes
│   └── _attachments/                  ← Figure copies for vault embedding
└── assets/                            ← Static figures for the deck
```

## Block-by-block (90 min)

| Block | Min | What | Lives in |
|---|---|---|---|
| 0. Hook + roadmap | 5 | Two arcs converged in 2024 | `slides/agentic-ai-workshop-week1.pdf` slides 1–5 |
| 1. History | 12 | Jacquard → Ada → assembly → compilers → Python → AI milestones → Transformer → ChatGPT → 2024 | slides 6–18 |
| 2. Agent atoms | 10 | Memory, identity, tools, learnings as real files on disk | slides 19–22 |
| 3. Vibe coding | 8 | Bold opinion + honest caveats | slides 23–24 |
| 4. Live build: Idea Inbox | 35 | Next.js + Supabase + Auth + Vercel via Claude Code | `WORKSHOP_PROMPTS.md` |
| 5. Organon teaser | 15 | Walk through the pre-populated dashboard + Obsidian vault | `dashboard-project/`, `obsidian-vault/` |
| 6. Q&A + close | 5 | — | — |

## Demo content (Block 5)

Theme: **CBC + vital-sign trajectories as real-time indicators of antibiotic-response trajectory in bacterial infection.**

Hypothesis ID `hyp-20260519-8e8d0d`. Claim drawn from real research interest at TUMCREATE; cohort is synthetic but shaped against published outcome distributions. The four-persona council (Skeptic / Methodologist / Domain-expert / Biostatistician) is fully populated with critique + counter-evidence + suggested experiments + a synthesised research plan.

Figure: bone marrow stress response (`fig-20260519-9a4a07`) — IG% spillover, neutrophilia, eosinophil sequestration. Generated via `viz-nano-banana` (scientific style, mechanism-schematic sub-style).

## Linking to Organon

The repo's top-level `setup.sh` creates symlinks from `~/Projects/organon/projects/briefs/agentic-ai-workshop/{papers,hypotheses,data,figures,manuscripts,.organon,obsidian-vault,…}` into this folder. Edit either location; both reflect changes.

To verify the dashboard sees this content:

```bash
curl -s 'http://localhost:8769/api/lit/library?project=agentic-ai-workshop' | jq '.total'
# → 20
```
