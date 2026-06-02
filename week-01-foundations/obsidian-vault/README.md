# Organon Workshop Vault

This is a **standalone sample vault** built for the *Agentic AI for Scientists* workshop
(Week 1 — Foundations of Gen AI, 15 May 2026). It is **separate** from the user's main
iCloud Obsidian vault on purpose: nothing here touches personal notes.

## What you're looking at

Every note in this vault is the kind of artifact Organon writes into Obsidian over the
course of a researcher's day. Open the **Graph View** (Cmd+G) and you'll see the
seven artifact families colour-coded:

- 🟧 **identity** — who the researcher is (profile, interests, lab context)
- 🟦 **paper-notes** — one note per paper picked up by `sci-literature-research`
- 🟨 **concepts** — biological / methodological notions that show up across papers
- 🟥 **experiments** — hypothesis notes from `sci-hypothesis` (with council critiques inlined)
- 🟦 **data-notes** — observations and decisions from `sci-data-analysis`
- 🟨 **drafts** — manuscript pointers + blog drafts from `sci-writing` / `sci-communication`
- 🟪 **daily** — session summaries from `meta-wrap-up`
- ⬜ **inbox** — quick-capture ideas, brainstorms, meeting notes

The point of the graph view is to show that *every* artifact a researcher creates
through Organon lands as a node in this connected vault. The connections are the
[[wikilinks]] between notes; they are how the graph becomes the unit of recall.

## Starting points

- [[identity/profile-kerem]] — the researcher's profile
- [[experiments/hyp-cbc-vitals-antibiotic-response]] — the active hypothesis at the
  centre of the workshop demo
- [[drafts/manuscript-cbc-antibiotic-response]] — the manuscript-in-progress that
  the dashboard's Draft workspace is building

## How this vault was generated

A single Python script (`_build_vault.py`, sibling to this vault) wrote every note
in one pass. In a real Organon session, these notes accumulate one at a time as the
researcher works — each skill that produces a knowledge artifact prompts to also
write it here via the [[concepts/obsidian-sync-gate|Obsidian Sync Gate]].

## Portability

This vault travels with the workshop folder. To use it on another laptop:

```bash
# After cloning / pulling the Organon repo on the second laptop:
rsync -av projects/briefs/agentic-ai-workshop/obsidian-vault/ \
  <second-laptop>:/path/to/projects/briefs/agentic-ai-workshop/obsidian-vault/
# Then in Obsidian: File → Open folder as vault → select obsidian-vault/
```

See `../PORTABILITY.md` (one level up) for the full project-portability story.
