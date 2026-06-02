# Organon Dashboard setup

The dashboard is a Next.js 16 app that ships with Organon at `projects/briefs/organon-dashboard/`. After this repo's `setup.sh` runs, the dashboard will resolve the `Agentic Ai Workshop` project via symlinks.

## First run

```bash
cd ~/Projects/organon/projects/briefs/organon-dashboard
npm install        # only first time
npm run dev        # → http://localhost:8769
```

The first `npm install` takes 30–60 s. The dev server boots in <1 s after that.

## Selecting the workshop project

1. Open http://localhost:8769 in Chrome.
2. Top-left **PROJECT** dropdown → select **Agentic Ai Workshop**.
3. Each tab on the left rail (Literature / Hypothesis / Data / Figures / Draft / Tools / Runs) should populate.

If a tab is empty:
- Reload the page (Cmd+R).
- Switch project away and back (this resets cached client state).
- Check the symlinks: `ls -la ~/Projects/organon/projects/briefs/agentic-ai-workshop/` — every entry should show as a `lrwxr-xr-x` symlink.

## Project workspaces explained

| Workspace | What it shows | Source folder (symlinked) |
|---|---|---|
| **Literature** | 20 paper cards with abstracts, citation counts, BibTeX export | `dashboard-project/papers/*.json` |
| **Hypothesis** | The claim + four persona critique tabs + synthesis | `dashboard-project/hypotheses/hyp-*/` |
| **Data** | The cohort CSV preview with per-column stats and a chart picker | `dashboard-project/data/cohort_cbc_vitals.csv` + `*.preview.json` |
| **Figures** | The bone marrow stress response illustration with caption | `dashboard-project/figures/fig-*/v1.png` |
| **Draft** | The manuscript with 6 sections (open `cbc-vitals-antibiotic-response` from the list) | `dashboard-project/manuscripts/cbc-vitals-antibiotic-response/` |
| **Runs** | 10 simulated workflow entries (the timeline view) | `dashboard-project/.organon/runs/*.jsonl` |
| **Tools** | Catalog of installed skills | (Organon-managed, not workshop-specific) |
| **Crons** | Scheduled jobs | (Organon-managed) |

## Suppressing the orange "Compiling…" indicator (capture mode)

For screen recordings or screenshots, the Next.js dev indicator can be distracting. Add to `projects/briefs/organon-dashboard/next.config.ts`:

```ts
const nextConfig: NextConfig = {
  devIndicators: false,   // suppress orange compile indicator
  // ...
};
```

Revert after the capture session.

## Common operations

**Search literature** — type a query into the Literature search bar and hit Search. The skill picks up the active project slug from the URL and writes new papers into the symlinked `papers/` folder.

**Generate a new hypothesis** — Hypothesis tab → New → enter a claim → Generate via Council. The skill spawns four parallel critique agents.

**Plot a column** — Data tab → click a column header → choose a plot type. Plots land in `figures/` with a new `fig-…` id.

**Run a skill via CLI** — Tools tab → pick a skill → fill the form → submit. Output streams to the Runs tab in real time.

## Restarting the dashboard

```bash
# Stop:  Ctrl+C in the npm-run-dev terminal
# Restart:
cd ~/Projects/organon/projects/briefs/organon-dashboard
npm run dev
```

## When the symlinks break

If the workshop repo dir gets renamed or moved, the symlinks in Organon will dangle. Fix by re-running `setup.sh` from the workshop repo.
