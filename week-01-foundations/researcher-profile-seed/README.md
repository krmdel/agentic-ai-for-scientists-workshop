# Researcher-profile seed

Source materials for the live `/lets-go` demo during Week 1. When the
workshop's `setup.sh` runs, these files get copied into
`{Organon}/research_artifacts/` so that `/lets-go` first-run mode finds
real content instead of an empty folder.

## What's in here

```
researcher-profile-seed/
├── README.md                                  ← this file
├── notes.md                                   ← seeds research_artifacts/notes.md
├── links.md                                   ← seeds research_artifacts/links.md
├── cv/
│   ├── cv.md                                  ← curated markdown CV (most readable)
│   ├── profile.yml                            ← structured profile
│   ├── cv-kerem-delikoyun-website.docx        ← public website CV
│   └── linkedin-profile.pdf                   ← LinkedIn export
├── research-statements/
│   ├── research_statement-1.docx              ← four narrative research statements
│   ├── research_statement-2.docx
│   ├── research_statement-3.docx
│   └── research_statement-4.docx
└── publications/
    ├── rt-had.pdf                             ← RT-HAD paper (real-time DHM, CVPR 2025 W)
    ├── triagent.pdf                           ← TriAgent paper (LLM multi-agent, arXiv 2025)
    └── article-digest.md                      ← curated digest of all writings + talks
```

## Demo flow

On a fresh laptop:

1. `git clone https://github.com/krmdel/agentic-ai-for-scientists-workshop.git ~/Projects/agentic-ai-for-scientists-workshop`
2. `cd ~/Projects/agentic-ai-for-scientists-workshop && ./setup.sh` — this:
   - Symlinks the demo dashboard project into Organon
   - **Copies this seed folder into `{Organon}/research_artifacts/`** (only if not already populated; never overwrites existing user content)
3. `cd ~/Projects/organon && claude`
4. Type `/lets-go`
5. The heartbeat creates the `research_artifacts/` scaffold (no-op since files are already there), shows the welcome, and asks you to drop files or say `ready`.
6. Say **`ready`** — the agent ingests everything in the folder, classifies each file (CV, papers, research statements), and builds your full `research_context/research-profile.md`.
7. You'll be asked one or two clarifying questions about active research questions and writing style; everything else is extracted from the files.

End-to-end: roughly **3–4 minutes** from `claude` start to a populated profile.

## What lands in the dashboard

Once `/lets-go` finishes:

- `research_context/research-profile.md` — full identity + focus + tool ecosystem (populates the dashboard's profile card and tunes every `sci-*` skill).
- `context/.lets-go-onboarded` — marker file so you don't re-onboard next session.
- `research_artifacts/{papers,manuscripts,notebooks,datasets,references}/` — classified copies of the source files.

## Why this exists

The Week 1 live demo shows two things:
1. **/lets-go onboarding from scratch** — the magic moment of "type one command, get a fully populated agent."
2. **Drop-in research context** — pre-existing materials (your CV, papers, statements) auto-classified into a usable profile.

The seed is the second piece: it removes the "drop files and wait" step from the demo so the audience sees the ingestion + profile-build live, not file shuffling.

## Editing the seed

The seed evolves with the speaker (currently Kerem Delikoyun). If you fork this
workshop for a different instructor, regenerate the seed by:

1. Replace files in `cv/`, `research-statements/`, `publications/` with the new
   speaker's materials.
2. Rewrite `notes.md` to reflect their research focus and active questions.
3. Update `links.md` with their academic profiles.
4. Commit. The `setup.sh` step copies whatever's in the seed folder, no other
   changes needed.

The seed never gets ingested by Organon directly — it's the source of truth for
the **demo state**, copied at setup time into the runtime location
(`research_artifacts/`).
