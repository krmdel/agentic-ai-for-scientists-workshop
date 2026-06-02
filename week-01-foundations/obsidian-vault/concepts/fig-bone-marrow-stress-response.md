---
tags: ["#figure", "#bone-marrow", "#mechanism"]
type: figure
---
# Figure — Bone marrow stress response in bacterial infection

![[_attachments/fig-20260519-9a4a07-bone-marrow-stress.png]]

Generated via the `viz-nano-banana` skill (scientific style, mechanism-schematic
sub-style). Lives in the dashboard at:

```
projects/agentic-ai-workshop/figures/fig-20260519-9a4a07/v1.png
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
uv run .claude/skills/viz-nano-banana/scripts/generate_image.py \
  --prompt "..." \
  --filename "v1.png" --resolution "2K" --aspect-ratio "4:3"
```

(See the original prompt in `projects/agentic-ai-workshop/figures/fig-20260519-9a4a07/index.json`.)
