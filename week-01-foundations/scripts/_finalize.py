#!/usr/bin/env python3
"""Move the nano-banana figure into the figure subfolder, register it,
update the manuscript + hypothesis to link to it."""
from __future__ import annotations
import hashlib
import json
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SLUG = "agentic-ai-workshop"
PROJ = REPO / "projects" / SLUG
NOW_ISO = "2026-05-19T04:20:00.000Z"

# 1. Figure folder + relocate
fig_id = f"fig-20260519-{hashlib.sha1(b'bone-marrow-stress').hexdigest()[:6]}"
fig_dir = PROJ / "figures" / fig_id
fig_dir.mkdir(parents=True, exist_ok=True)

src = REPO / "v1.png"
dst = fig_dir / "v1.png"
shutil.move(str(src), str(dst))

idx = {
    "_artifact": "figure",
    "schema_version": 1,
    "id": fig_id,
    "project_slug": SLUG,
    "kind": "illustration",
    "version": 1,
    "format": "png",
    "data_source": None,
    "params": {
        "backend": "nano-banana",
        "model": "gemini-3-pro-image",
        "style": "scientific",
        "sub_style": "mechanism-schematic",
        "resolution": "2K",
        "aspect_ratio": "4:3",
    },
    "caption": "Bone marrow stress response in bacterial infection. Cross-section view: (1) immature granulocyte spillover from the hematopoietic niche into peripheral blood (IG% rise), (2) neutrophilia as mature and band-form neutrophils accumulate in circulation, and (3) eosinophil sequestration from blood to lymph node under cortisol drive.",
    "alt_text": "Diagram with two halves. Left: bone marrow with myeloid precursors and band cells. Right: a blood vessel cross-section with mature and immature neutrophils, and below it a lymph node icon. Three labeled arrows show IG% spillover, neutrophilia, and eosinophil sequestration.",
    "code_path": None,
    "png_path": f"projects/{SLUG}/figures/{fig_id}/v1.png",
    "svg_path": None,
    "thumbnail_path": f"projects/{SLUG}/figures/{fig_id}/v1.png",
    "library_path": f"projects/{SLUG}/figures/{fig_id}/index.json",
    "backend": "nano-banana",
    "cost_cents": 0,
    "parent_version": None,
    "created_at": NOW_ISO,
}
(fig_dir / "index.json").write_text(json.dumps(idx, indent=2) + "\n", encoding="utf-8")

# 2. Patch manuscript: append fig id to linked_figure_ids
manu_dir = PROJ / "manuscripts" / "cbc-vitals-antibiotic-response"
manu_json = manu_dir / "manuscript.json"
manu = json.loads(manu_json.read_text())
if fig_id not in manu["linked_figure_ids"]:
    manu["linked_figure_ids"].append(fig_id)
manu["updated_at"] = NOW_ISO
manu_json.write_text(json.dumps(manu, indent=2) + "\n", encoding="utf-8")

# 3. Patch results section: add a Figure-1 reference at the P1 paragraph + add to linked_figure_ids
results_md_path = manu_dir / "sections" / "results.md"
results_json_path = manu_dir / "sections" / "results.json"
results_md = results_md_path.read_text()
results_md = results_md.replace(
    "**P1 — IG% at admission stratifies outcome (Figure 1).**",
    f"**P1 — IG% at admission stratifies outcome (Figure 1; [`{fig_id}`]).**",
)
# append the figure callout as a markdown block at end
fig_block = (
    f"\n\n![Bone marrow stress response in bacterial infection](../../figures/{fig_id}/v1.png)\n"
    f"*Figure 1. Stylised mechanism. Immature granulocyte spillover (IG% rise), neutrophilia, "
    f"and eosinophil sequestration to lymphoid tissue. Figure id `{fig_id}`.*\n"
)
if "![Bone marrow stress response" not in results_md:
    results_md += fig_block
results_md_path.write_text(results_md, encoding="utf-8")

results_json = json.loads(results_json_path.read_text())
if fig_id not in results_json["linked_figure_ids"]:
    results_json["linked_figure_ids"].append(fig_id)
results_json["content_md"] = results_md
results_json["updated_at"] = NOW_ISO
results_json["version"] = 2
results_json_path.write_text(json.dumps(results_json, indent=2) + "\n", encoding="utf-8")

# 4. Patch hypothesis: surface the figure in tags + notes
hyp_dir = PROJ / "hypotheses"
for h in hyp_dir.glob("hyp-*"):
    if (h / "hypothesis.json").exists():
        hyp = json.loads((h / "hypothesis.json").read_text())
        if hyp["claim_short"].startswith("Sequential CBC"):
            hyp.setdefault("linked_figure_ids", []).append(fig_id)
            hyp["updated_at"] = NOW_ISO
            (h / "hypothesis.json").write_text(json.dumps(hyp, indent=2) + "\n", encoding="utf-8")
        break

# 5. Bone marrow figure also belongs in the obsidian vault as an attachment-ish note
vault = REPO / "projects" / "briefs" / SLUG / "obsidian-vault"
vault_fig = vault / "_attachments" / f"{fig_id}-bone-marrow-stress.png"
vault_fig.parent.mkdir(parents=True, exist_ok=True)
shutil.copy(str(dst), str(vault_fig))

# add a figure-note in the vault that references it
(vault / "concepts" / "fig-bone-marrow-stress-response.md").write_text(
    f"""---
tags: ["#figure", "#bone-marrow", "#mechanism"]
type: figure
---
# Figure — Bone marrow stress response in bacterial infection

![[_attachments/{fig_id}-bone-marrow-stress.png]]

Generated via the `viz-nano-banana` skill (scientific style, mechanism-schematic
sub-style). Lives in the dashboard at:

```
projects/{SLUG}/figures/{fig_id}/v1.png
```

## What it shows

Three coupled events under bacterial infection:

1. **IG% spillover** — [[concepts/immature-granulocytes|immature granulocytes]]
   leave the bone marrow ahead of the peripheral neutrophilia peak.
2. **Neutrophilia** — mature and band-form neutrophils accumulate in circulation;
   the classic [[concepts/neutrophil-left-shift|left shift]].
3. **Eosinophil sequestration** — cortisol-driven movement of eosinophils from
   blood to lymphoid tissue, the cellular substrate of
   [[concepts/eosinopenia-of-stress|eosinopenia of stress]].

## Where it lands

- Manuscript Results section P1 — see [[drafts/manuscript-cbc-antibiotic-response]].
- Hypothesis [[experiments/hyp-cbc-vitals-antibiotic-response]] — primary
  mechanism schematic.

## Regeneration

```bash
uv run .claude/skills/viz-nano-banana/scripts/generate_image.py \\
  --prompt "..." \\
  --filename "v1.png" --resolution "2K" --aspect-ratio "4:3"
```

(See the original prompt in `projects/{SLUG}/figures/{fig_id}/index.json`.)
""", encoding="utf-8",
)

print(f"Figure {fig_id} registered + wired into manuscript + vault.")
print(f"   PNG: {dst}")
print(f"   Index: {fig_dir / 'index.json'}")
print(f"   Vault copy: {vault_fig}")
