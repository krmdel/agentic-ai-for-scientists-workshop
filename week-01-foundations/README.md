# Week 01 · Foundations of Gen AI

90-minute session covering the 200-year abstraction arc + Claude Code primitives + Organon as an agentic OS for scientists. Live build of an Idea Inbox CRUD app. Demo of the workshop's pre-populated dashboard project and Obsidian vault.

> **Dry-running the demo before the workshop?** Use the isolated-clone path — it tests the full `/lets-go` flow without touching your real Organon install. Full instructions: [`researcher-profile-seed/DEMO_WALKTHROUGH.md`](researcher-profile-seed/DEMO_WALKTHROUGH.md) → "Path A — Isolated clone".

## Slides

- **Final deck (hand-edited):** [`slides/agentic-ai-workshop-week1.pptx`](slides/agentic-ai-workshop-week1.pptx) · [`agentic-ai-workshop-week1.pdf`](slides/agentic-ai-workshop-week1.pdf) — the version used in the workshop. PPTX is Google-Slides-compatible (macOS internal font references rewritten to Helvetica Neue so it renders correctly on import).
- **Google Drive:** [Week 01 folder ↗](https://drive.google.com/drive/folders/18H1ERTJ4yJIiTlpOGSdB4saM-vI5XJuT) — holds the same `agentic-ai-workshop-week1.pptx` + `agentic-ai-workshop-week1.pdf`. Right-click the `.pptx` → **Open with → Google Slides** for a browser-editable converted copy in the same folder.
- **Marp source:** [`slides/slides-v2.{md,pdf,pptx}`](slides/) — pre-edit Marp build retained for regeneration.
- **Updating slides:** Folder link is stable across updates. When you replace the deck, re-upload to the same Drive folder (drag-and-drop or replace via Drive Desktop sync). The link in this README does not need to change.

## What's in this folder

```
week-01-foundations/
├── README.md                          ← this file
├── brief.md                           ← Workshop brief (goal, audience, time budget)
├── talk-notes.md                      ← Speaker notes per block
├── WORKSHOP_PROMPTS.md                ← The 5–6 Claude Code prompts for Block 4 (live build)
├── PORTABILITY.md                     ← (Legacy — pre-repo-split portability notes)
├── WORKSHOP-DESCRIPTION.md            ← Original brief description (kept for reference)
├── supabase-schema.sql                ← DB schema for the live build
├── slides/                            ← Marp deck + exports
│   ├── slides-v2.md                   ← Current source (May 15 v2 + May 19 fact-check)
│   ├── slides-v2.pdf
│   ├── slides-v2.pptx
│   ├── slides.md                      ← Original v1 (May 12)
│   └── slides.{pdf,pptx}
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
├── idea-inbox-starter/                ← Next.js + Tailwind starter for the Block 4 live build
├── assets/                            ← Static figures for the deck
└── scripts/
    ├── _build_demo.py                 ← Regenerate papers + hypothesis + cohort + manuscript + runs
    ├── _build_vault.py                ← Regenerate the Obsidian vault
    ├── _finalize.py                   ← Wire generated figure into manuscript
    └── _finalize_data.py              ← Build DataframeArtifact preview JSON for Data workspace
```

## Block-by-block (90 min)

| Block | Min | What | Lives in |
|---|---|---|---|
| 0. Hook + roadmap | 5 | Two arcs converged in 2024 | `slides/slides-v2.{pdf,pptx}` slides 1–5 |
| 1. History | 12 | Jacquard → Ada → assembly → compilers → Python → AI milestones → Transformer → ChatGPT → 2024 | slides 6–18 |
| 2. Agent atoms | 10 | Memory, identity, tools, learnings as real files on disk | slides 19–22 |
| 3. Vibe coding | 8 | Bold opinion + honest caveats | slides 23–24 |
| 4. Live build: Idea Inbox | 35 | Next.js + Supabase + Auth + Vercel via Claude Code | `idea-inbox-starter/`, `WORKSHOP_PROMPTS.md`, `supabase-schema.sql` |
| 5. Organon teaser | 15 | Walk through the pre-populated dashboard + Obsidian vault | `dashboard-project/`, `obsidian-vault/` |
| 6. Q&A + close | 5 | — | — |

## Demo content (Block 5)

Theme: **CBC + vital-sign trajectories as real-time indicators of antibiotic-response trajectory in bacterial infection.**

Hypothesis ID `hyp-20260519-8e8d0d`. Claim drawn from real research interest at TUMCREATE; cohort is synthetic but shaped against published outcome distributions. The four-persona council (Skeptic / Methodologist / Domain-expert / Biostatistician) is fully populated with critique + counter-evidence + suggested experiments + a synthesised research plan.

Figure: bone marrow stress response (`fig-20260519-9a4a07`) — IG% spillover, neutrophilia, eosinophil sequestration. Generated via `viz-nano-banana` (scientific style, mechanism-schematic sub-style).

## Regenerating from scratch

The four scripts in `scripts/` produce everything in `dashboard-project/` deterministically (except the figure — Gemini outputs vary slightly each run).

```bash
cd ~/Projects/agentic-ai-workshop/week-01-foundations
python3 scripts/_build_demo.py            # papers + hypothesis + cohort + manuscript + runs
python3 scripts/_build_vault.py           # obsidian-vault/

# Figure (regenerate):
uv run ~/Projects/organon/.claude/skills/viz-nano-banana/scripts/generate_image.py \
  --prompt "$(jq -r '.params' dashboard-project/figures/fig-*/index.json | head)" \
  --filename "v1.png" --resolution "2K" --aspect-ratio "4:3"

python3 scripts/_finalize.py              # wire figure → manuscript
python3 scripts/_finalize_data.py         # rebuild dataframe preview
```

Note: the scripts were originally written assuming files under `projects/briefs/agentic-ai-workshop/` (Organon-relative). They still work if you run them from there via the symlinks. If you run them from this repo's `week-01-foundations/` directly, output lands here too (because the symlinks point both ways).

## Linking to Organon

The repo's top-level `setup.sh` creates symlinks from `~/Projects/organon/projects/briefs/agentic-ai-workshop/{papers,hypotheses,data,figures,manuscripts,.organon,obsidian-vault,…}` into this folder. Edit either location; both reflect changes.

To verify the dashboard sees this content:

```bash
curl -s 'http://localhost:8769/api/lit/library?project=agentic-ai-workshop' | jq '.total'
# → 20
```
