---
tags:
  - #organon
  - #workflow
type: concept
---
# Obsidian Sync Gate

The Organon pattern: *every knowledge artifact a skill produces is offered to
the user for sync into this vault*. Not silent — explicit, one prompt per
artifact.

## What gets offered

- Paper summaries from [[concepts/host-response-paradigm|literature-research]] → `paper-notes/`
- Hypothesis designs → `experiments/`
- Data observations from `sci-data-analysis` → `data-notes/`
- Manuscript drafts from `sci-writing` → `drafts/`
- Daily session summaries from `meta-wrap-up` → `daily/`

## What doesn't get offered

- Binary files (PDFs, CSVs, PNGs) — those go via the Drive Push Gate, not here.
- Organon framework files (memory/, .planning/, cron status) — those stay in
  Organon, not Obsidian.

## Why the gate matters

The graph view is only useful if the cluster is *connected*. The gate exists to
prompt the researcher to write a one-paragraph summary at write-time, with
explicit `[[wikilinks]]` to related notes — so the next time they search the
graph, the structure they expect is there.

Related: [[README]], [[identity/research-interests]].
