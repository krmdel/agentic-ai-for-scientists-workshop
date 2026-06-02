# Researcher-profile seed (template)

This folder feeds the live `/lets-go` demo in Week 1. When `setup.sh` runs, any
documents placed here are copied into `{Organon}/research_artifacts/` so that
`/lets-go` first-run mode builds a researcher profile from real content instead
of an empty folder.

> **Public-repo note.** The instructor's personal documents (CV, LinkedIn,
> research statements, and papers) are **not included** in this public repo.
> The structure below is a **template** — drop *your own* equivalent documents
> into these subfolders, then run `setup.sh`, to reproduce the demo with your
> own profile. `setup.sh` seeds whatever is present and skips gracefully when
> the folders are empty.

## What to put here

```
researcher-profile-seed/
├── README.md                ← this file
├── DEMO_WALKTHROUGH.md      ← how to dry-run the /lets-go demo
├── cv/                      ← your CV (cv.md / .docx) + an optional profile.yml
├── research-statements/     ← one or more narrative research statements
└── publications/            ← a few representative papers (PDF) + an article digest
```

Supported file types for seeding: `.md`, `.txt`, `.pdf`, `.docx`, `.csv`, `.xlsx`
(top-level files in each subfolder; `/lets-go` ingests them on first run).

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
