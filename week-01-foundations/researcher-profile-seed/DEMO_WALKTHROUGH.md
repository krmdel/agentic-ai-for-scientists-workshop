# Week 1 demo walkthrough — `/lets-go` from scratch

Step-by-step script for the **live demo** in Block 5 of Week 1. Total run time
on stage: **3–4 minutes**. Read this once before the talk; you won't reference
it live.

## Dry-run before the workshop — pick one of two paths

You should run the full demo end-to-end at least once before going live.
There are two ways to do it; pick based on whether you want to touch your
real Organon install.

### Path A — Isolated clone (recommended, zero risk)

Clones a second Organon to a separate path. Your real
`~/Projects/organon/` is **not touched** at any point.

```bash
# 1. Fresh clone to a separate path
git clone https://github.com/krmdel/organon.git ~/Projects/organon-demo
cd ~/Projects/organon-demo && bash scripts/install.sh

# 2. Seed it via the workshop setup, targeting the isolated clone
ORGANON_ROOT=~/Projects/organon-demo \
  bash ~/Projects/agentic-ai-workshop/setup.sh

# 3. Run /lets-go from inside the isolated clone
cd ~/Projects/organon-demo && claude
# (then in the Claude prompt, type:)  /lets-go
```

When the agent shows the welcome screen, type `ready`. The agent will
ingest, classify, and build `research_context/research-profile.md`.

**Cleanup when you're done:**
```bash
rm -rf ~/Projects/organon-demo
```

This is the path to use on the **actual demo laptop** as well — set
`ORGANON_ROOT` to wherever Organon is cloned on that machine and the
seed pipes through correctly.

### Path B — In-place on your main Organon (only if you accept the cleanup)

If you'd rather dry-run against `~/Projects/organon/` directly,
back up the bits that `/lets-go` will mutate first, then run, then
restore.

```bash
# Snapshot the only file that might exist + can be reverted
cp ~/Projects/organon/context/.lets-go-onboarded /tmp/lgmark-backup 2>/dev/null || true

# Run the demo flow
bash ~/Projects/agentic-ai-workshop/setup.sh
cd ~/Projects/organon && claude
# /lets-go → say "ready" when prompted

# Rollback after the dry-run:
cp /tmp/lgmark-backup ~/Projects/organon/context/.lets-go-onboarded 2>/dev/null || true
rm -rf ~/Projects/organon/research_artifacts/
rm -rf ~/Projects/organon/research_context/
```

Risks of Path B (not catastrophic, but messy):
- `research_artifacts/` will be created with 12 demo files. Removable.
- `research_context/research-profile.md` will be written. Removable.
- `context/memory/{today}.md` and `context/learnings.md` will get a
  "just onboarded" entry that's awkward to see in your real timeline
  later. Reversible by hand-editing those files.

**Use Path A.** It's the same end-to-end test with no cleanup.

---

## Pre-flight (do this before the workshop starts)

On the demo laptop:

```bash
# 1. Workshop repo cloned and set up
cd ~/Projects/agentic-ai-workshop
git pull
./setup.sh

# 2. Confirm research_artifacts is pre-populated
ls ~/Projects/organon/research_artifacts/
# Expect 12 files: cv-kerem-delikoyun.{md,docx}, linkedin-profile.pdf,
# research-statement-{1..4}.docx, rt-had-paper.pdf, triagent-paper.pdf,
# article-digest.md, kerem-research-notes.md, kerem-academic-links.md

# 3. Confirm Organon is in first-run state
ls ~/Projects/organon/context/.lets-go-onboarded 2>&1
# Expect: "No such file or directory" — that's good, means /lets-go will run first-run mode.

# 4. Confirm dashboard is ready
ls ~/Projects/organon/projects/briefs/organon-dashboard
```

**If `.lets-go-onboarded` exists**, the demo will skip onboarding and you won't see the live build. To reset:

```bash
rm ~/Projects/organon/context/.lets-go-onboarded
rm -f ~/Projects/organon/research_context/research-profile.md
# (Leave research_artifacts/ alone — the seed is what gets ingested.)
```

## On stage

### 1. Open a clean Claude Code session
```bash
cd ~/Projects/organon
claude
```

Wait for the heartbeat to finish (CLAUDE.md + SOUL.md + USER.md loaded). The
session will auto-run `/lets-go` because the marker file is missing.

### 2. The agent shows the welcome screen
You'll see:

> Welcome to Scientific-OS. I've created a `research_artifacts/` folder at the repo root.
> Step 1 — get your research materials to me. Pick whichever is easiest:
> - Drop files into `research_artifacts/` …
> - Drag files into this chat …
> - Paste a path …
> - Paste text content …
>
> Say `ready` when you're done.

**Your line:** "Everything's already in `research_artifacts/` from the workshop seed — say `ready`."

Type: `ready`

### 3. The agent ingests (~ 60–90 sec)
You'll see it:

1. Glob `research_artifacts/*.{md,txt,pdf,docx,...}` → find 12 files
2. Read each one (PDF / DOCX / MD)
3. Classify each (CV → notes, papers → papers, research statements → notes, digest → notes)
4. Extract structured metadata
5. Move into `papers/`, `notes/`, etc.

**Talking points while it runs:**
- "Notice every file is being read first, not just listed by filename."
- "The classifier uses both content shape and filename hints."
- "Notes are the catch-all — CV and research statements land there because they don't have the paper structure (abstract/intro/methods)."

### 4. The agent asks for academic links (Step 0.25)
**Your line:** "Pull them from `kerem-academic-links.md` in `research_artifacts/`."

Or paste the URLs directly from `links.md` in the seed folder. Either works.

### 5. The agent asks 2–4 profile questions
Likely questions, with one-liner answers:

- **"What's your primary research field?"** → "AI for biomedical imaging and agentic AI systems for scientific workflows."
- **"Any active research questions?"** → "Sequential CBC features + vital-sign trends as real-time indicators of antibiotic-treatment efficacy. Beyond that, post-training of small LLMs for biomedical reasoning."
- **"Writing style preference?"** → "Direct, evidence-anchored, short paragraphs. Avoid em-dashes."

(Or just point at `kerem-research-notes.md` and say "all my preferences are in there.")

### 6. Profile builds
The agent writes `research_context/research-profile.md` and shows a summary.

**Show the file:** `cat ~/Projects/organon/research_context/research-profile.md | head -40`

Then segue to the dashboard:

> "Now watch what happens when I open the dashboard — the profile is already loaded."

### 7. Open the dashboard
```bash
# In a second terminal
cd ~/Projects/organon/projects/briefs/organon-dashboard
npm run dev
```

Browse to `http://localhost:8769`. Select "Agentic Ai Workshop" project. Show:
- Library: 20 PubMed papers (pre-seeded for the CBC/antibiotic theme)
- Hypothesis: 1 with 4-persona council critiques
- Data: 100-patient cohort with stats
- Figures: bone-marrow stress-response illustration
- Draft: 6-section manuscript
- Runs: 10 simulated workflow entries

### 8. Open Obsidian
```bash
# Already configured to point at the workshop vault
open -a Obsidian ~/Projects/agentic-ai-workshop/week-01-foundations/obsidian-vault/
```

Press **Cmd+G** for the graph view. Show the 43 cross-linked notes and the 8 colour-coded folders.

**Talking points:**
- "Same agent. Same identity. Same memory. Two surfaces — terminal + dashboard + knowledge graph."
- "Every file you saw the agent classify is now usable by every skill."

## Recovery if something breaks

| Symptom | Likely cause | Fix |
|---|---|---|
| `/lets-go` says "returning mode" | Marker file exists | `rm ~/Projects/organon/context/.lets-go-onboarded` and retry |
| Agent doesn't see seeded files | `research_artifacts/` empty | `bash ~/Projects/agentic-ai-workshop/setup.sh` to re-seed |
| Dashboard shows empty sections | Symlinks broken | `bash ~/Projects/agentic-ai-workshop/setup.sh` to re-link |
| Obsidian graph view empty | Wrong vault opened | Re-open the workshop's `obsidian-vault/` folder, not your personal one |

## Dry-run checklist (do once before the workshop)

- [ ] Reset Organon to first-run state (delete marker + research_context profile)
- [ ] Run `setup.sh` clean
- [ ] Time the full `/lets-go` flow end-to-end (target: ≤ 4 min)
- [ ] Verify dashboard auto-picks up the new profile
- [ ] Verify Obsidian graph view loads (Cmd+G)
- [ ] Verify all symlinks survived (`ls -la ~/Projects/organon/projects/briefs/agentic-ai-workshop/`)
