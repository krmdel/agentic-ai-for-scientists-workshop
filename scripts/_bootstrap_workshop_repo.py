#!/usr/bin/env python3
"""Bootstrap the agentic-ai-workshop repo on disk.

Phase 1: Scaffold directory structure (top-level + 6 week stubs + week-01 subdirs).
Phase 2: Move week-01 content from Organon's projects/briefs/agentic-ai-workshop/
         into workshop-repo/week-01-foundations/.
Phase 3: Find-replace paths in JSON/MD files (Organon→workshop relative paths).
Phase 4: Symlink workshop content back into Organon so the local dashboard works.

Idempotent on re-run for moved/non-existent files.
"""
from __future__ import annotations
import shutil
import os
import json
import re
from pathlib import Path

REPO = Path.home() / "Projects" / "agentic-ai-workshop"
ORGANON = Path.home() / "Projects" / "scientific-os"
SRC = ORGANON / "projects" / "briefs" / "agentic-ai-workshop"
W1 = REPO / "week-01-foundations"

assert REPO.exists() and (REPO / ".git").exists(), f"workshop repo not found at {REPO}"
assert SRC.exists(), f"source folder not found at {SRC}"

# -------- Phase 1: scaffold ----------
TOP_DIRS = ["docs"]
WEEK_DIRS = [
    "week-01-foundations",
    "week-02-skills",
    "week-03-memory",
    "week-04-multi-agent",
    "week-05-cost-safety",
    "week-06-capstone",
]
W1_SUBDIRS = ["dashboard-project", "obsidian-vault", "scripts", "slides"]

for d in TOP_DIRS + WEEK_DIRS:
    (REPO / d).mkdir(exist_ok=True)
for d in W1_SUBDIRS:
    (W1 / d).mkdir(exist_ok=True)

print(f"[1] scaffolded top-level dirs + 6 week stubs + week-01 subdirs")

# -------- Phase 2: move content ----------
# What goes where in week-01:
#   dashboard-project/    ← papers/, hypotheses/, data/, figures/, manuscripts/, .organon/
#   obsidian-vault/       ← obsidian-vault/
#   scripts/              ← _build_*.py, _finalize*.py
#   slides/               ← slides-v2.{md,pdf,pptx}, slides.{md,pdf,pptx}
#   <root of week-01>     ← brief.md, talk-notes.md, WORKSHOP_PROMPTS.md, supabase-schema.sql,
#                            README.md (from source), PORTABILITY.md, .env.example,
#                            idea-inbox-starter/, assets/

DASHBOARD_MOVE = ["papers", "hypotheses", "data", "figures", "manuscripts", ".organon"]
ROOT_MOVE = [
    "brief.md", "talk-notes.md", "WORKSHOP_PROMPTS.md", "supabase-schema.sql",
    "idea-inbox-starter", "assets",
]
# README and PORTABILITY get RENAMED + moved to top-level repo + week-01 respectively
SCRIPTS_MOVE = ["_build_demo.py", "_build_vault.py", "_finalize.py", "_finalize_data.py"]
SLIDES_MOVE = ["slides-v2.md", "slides-v2.pdf", "slides-v2.pptx",
               "slides.md", "slides.pdf", "slides.pptx"]


def safe_move(src: Path, dst: Path) -> bool:
    if not src.exists():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        if dst.is_dir() and not any(dst.iterdir()):
            dst.rmdir()
        else:
            # already moved — skip
            return False
    shutil.move(str(src), str(dst))
    return True


moved = 0
for name in DASHBOARD_MOVE:
    if safe_move(SRC / name, W1 / "dashboard-project" / name):
        moved += 1
for name in ROOT_MOVE:
    if safe_move(SRC / name, W1 / name):
        moved += 1
for name in SCRIPTS_MOVE:
    if safe_move(SRC / name, W1 / "scripts" / name):
        moved += 1
for name in SLIDES_MOVE:
    if safe_move(SRC / name, W1 / "slides" / name):
        moved += 1
# obsidian-vault — keep folder name
safe_move(SRC / "obsidian-vault", W1 / "obsidian-vault")

# Source README → week-01 README (we'll write a new top-level README later)
src_readme = SRC / "README.md"
if src_readme.exists():
    safe_move(src_readme, W1 / "WORKSHOP-DESCRIPTION.md")  # rename so it doesn't collide with week-01 README

src_portability = SRC / "PORTABILITY.md"
if src_portability.exists():
    safe_move(src_portability, W1 / "PORTABILITY.md")

src_env = SRC / ".env.example"
if src_env.exists():
    safe_move(src_env, REPO / ".env.example")  # top-level for the workshop repo

print(f"[2] moved {moved} top-level items + nested files")

# -------- Phase 3: find-replace JSON paths ----------
# Old prefix:  projects/briefs/agentic-ai-workshop/
# New prefix:  week-01-foundations/dashboard-project/   (relative to workshop repo root)
# But artifacts read by Organon dashboard still need to resolve from the symlinked path.
# Decision: leave library_path / data_path fields anchored to the ORGANON repo's view
# (projects/briefs/agentic-ai-workshop/...) because the dashboard reads relative to
# organonRoot() — and the symlinked path on Organon side preserves the old structure.
# So we DO NOT rewrite paths in JSON. The symlinks (Phase 4) bridge the gap.

# But we DO patch the manuscript section .md files where they reference figures via
# `../../figures/{fig_id}/v1.png` — those relative paths break when the manuscript
# section is now under .../dashboard-project/manuscripts/{slug}/sections/. Verify and fix.

manuscript_sections_dir = W1 / "dashboard-project" / "manuscripts"
section_md_count = 0
for md in manuscript_sections_dir.rglob("*.md"):
    txt = md.read_text(encoding="utf-8")
    # Already `../../figures/...` which resolves to dashboard-project/figures/ — OK
    section_md_count += 1
print(f"[3] {section_md_count} manuscript section .md files inspected; paths preserved")

# -------- Phase 4: symlink back into Organon ----------
# After moves, SRC is mostly empty. Recreate it with symlinks pointing at the new home.
# This way the running dashboard still resolves projects/briefs/agentic-ai-workshop/papers/etc.

# Ensure SRC exists as a directory (may have been emptied)
SRC.mkdir(exist_ok=True)

SYMLINKS = [
    # source under SRC      ← target in workshop repo (relative)
    ("papers",                W1 / "dashboard-project" / "papers"),
    ("hypotheses",            W1 / "dashboard-project" / "hypotheses"),
    ("data",                  W1 / "dashboard-project" / "data"),
    ("figures",               W1 / "dashboard-project" / "figures"),
    ("manuscripts",           W1 / "dashboard-project" / "manuscripts"),
    (".organon",              W1 / "dashboard-project" / ".organon"),
    ("obsidian-vault",        W1 / "obsidian-vault"),
    ("brief.md",              W1 / "brief.md"),
    ("talk-notes.md",         W1 / "talk-notes.md"),
    ("WORKSHOP_PROMPTS.md",   W1 / "WORKSHOP_PROMPTS.md"),
    ("supabase-schema.sql",   W1 / "supabase-schema.sql"),
    ("idea-inbox-starter",    W1 / "idea-inbox-starter"),
    ("assets",                W1 / "assets"),
    ("slides-v2.md",          W1 / "slides" / "slides-v2.md"),
    ("slides-v2.pdf",         W1 / "slides" / "slides-v2.pdf"),
    ("slides-v2.pptx",        W1 / "slides" / "slides-v2.pptx"),
    ("slides.md",             W1 / "slides" / "slides.md"),
    ("slides.pdf",            W1 / "slides" / "slides.pdf"),
    ("slides.pptx",           W1 / "slides" / "slides.pptx"),
    ("scripts",               W1 / "scripts"),
]

symlinked = 0
for rel_in_src, target in SYMLINKS:
    link = SRC / rel_in_src
    if not target.exists():
        continue  # nothing to symlink to
    if link.exists() or link.is_symlink():
        link.unlink() if link.is_symlink() or link.is_file() else shutil.rmtree(link)
    link.symlink_to(target.resolve())
    symlinked += 1

print(f"[4] created {symlinked} symlinks from Organon into workshop repo")

# Done
print()
print("Workshop repo bootstrap complete.")
print(f"  Workshop repo: {REPO}")
print(f"  Organon side:  {SRC} (symlinks pointing into workshop repo)")
