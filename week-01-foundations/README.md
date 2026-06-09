# Week 01 · Foundations of Gen AI

90-minute session covering the 200-year abstraction arc, Claude Code primitives, and Organon as an agentic OS for scientists. It closes with a live demo: running `/lets-go` from scratch, building a researcher profile, wiring an Obsidian vault, and walking the pre-populated dashboard project as the knowledge graph fills in.

## Slides

**Final deck:** [`slides/agentic-ai-workshop-week1.pdf`](slides/agentic-ai-workshop-week1.pdf) — the version used in the workshop.

## Recording

📹 **[Week 1 — Foundations (full session)](https://youtu.be/wNKf4KWJnLA)** — unlisted YouTube; anyone with the link can watch.

## Resources

Curated companion material — videos, official docs, and reading for this week: **[`resources.md`](resources.md)**.

## What's in this folder

```
week-01-foundations/
├── README.md                          ← this file
├── slides/                            ← Final workshop deck
│   └── agentic-ai-workshop-week1.pdf
├── resources.md                       ← Curated videos, docs & reading for Week 1
├── PORTABILITY.md                     ← Running the demo outside TUMCREATE
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

| Block | What | Slides |
|---|---|---|
| Intro · Hook + roadmap | Two arcs converge; the four parts of the session | 1–2 |
| Part 1 · How we got here | The 200-year abstraction staircase: Jacquard, Ada, machine code, compilers, Python, AI's long road, Transformer, ChatGPT. By 2024 English becomes the programming layer and the test suite is the new contract | 3–16 |
| Part 2 · CLI-based AI agents | Claude Code as a terminal-native colleague; the six primitives (CLAUDE.md, tools, skills, sub-agents, MCP, hooks) plus slash commands, ending on one full session | 17–28 |
| Part 3 · Organon | An agentic OS for scientists: the kernel, three-layer architecture, continuity (SOUL, memory, learnings), skills as a recipe, an end-to-end research journey, the Einstein Arena domain stretch | 29–38 |
| Live demo + roadmap | `/lets-go` from scratch, build a researcher profile, wire an Obsidian vault, watch the graph fill in; where weeks 2 to 6 go | 39 + live |

## Demo content (Part 3 + live demo)

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
