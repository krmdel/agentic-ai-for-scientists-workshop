---
tags:
  - #instrument
  - #imaging-flow-cytometry
  - #TUMCREATE
type: concept
---
# Label-free imaging flow cytometry

Single-cell imaging at flow-cytometry rates *without fluorescent staining*.
Brightfield + quantitative phase + deep-learning morphology classification.
The TUMCREATE flagship capability.

## Why it matters

The standard CBC differential is reductive: 5 classes (NEUT, LYMPH, MONO, EOS, BASO)
plus IG%. Imaging flow cytometry can resolve:
- [[concepts/neutrophil-left-shift|Band cells vs segmented neutrophils]] directly,
  without serial 5-part differentials.
- [[concepts/platelet-aggregation-activation|Platelet activation states]] in real time.
- Reticulocyte maturation stages (clinically relevant in
  [[experiments/hyp-bone-marrow-recovery-after-sepsis|post-sepsis recovery]]).

## How it ties to this work

[[experiments/hyp-imaging-flow-cytometry-platelets]] is the adjacent imaging
hypothesis — measuring platelet activation before classical CBC parameters move.
The same instrument can also direct-measure the band-cell fraction that
[[concepts/immature-granulocytes|IG%]] *infers*.

## Instrument logistics

- Throughput: ~3000 cells/s in current prototype #4
- Sample volume: 50 µL whole blood (heparinised)
- Turnaround: 5–10 min including sample prep
- Cost per run: $4–7 (consumables + GPU time)

Related: [[experiments/hyp-imaging-flow-cytometry-platelets]],
[[concepts/platelet-aggregation-activation]],
[[data-notes/TUMCREATE-imaging-flow-pilot]].
