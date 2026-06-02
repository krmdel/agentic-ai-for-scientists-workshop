---
tags:
  - #data
  - #cohort
  - #cbc
  - #vitals
type: data-note
---
# Demo cohort — 100 patients, CBC + vitals, 0–72 h

**File**: `projects/agentic-ai-workshop/data/cohort_cbc_vitals.csv`
**Analysis**: `projects/agentic-ai-workshop/data/analyze_cohort.py`
**Linked hypothesis**: [[experiments/hyp-cbc-vitals-antibiotic-response]]

## Shape

- 100 patients
- 36 columns (5 demographics + 7 features × 4 timepoints + outcome)
- Outcome distribution: improver 68, slow_responder 18, non_responder 9, died 5

## What the analysis showed

- IG% at admission rises *monotonically* across outcome strata (3.9 / 4.9 / 6.4 / 9.6).
- IG% gap *widens* by 48 h (1.4 / 3.2 / 6.0 / 11.8) — the bone-marrow stress
  response persists in non-responders.
- EOS% recovery slope is the discriminating feature for improvers vs
  non-responders, *not* admission EOS% (which is universally low).
- Temperature normalisation is attenuated in the $\geq 65$y subgroup, echoing
  [[paper-notes/grudzinska-2020-neutrophils-CAP|Grudzinska 2020]].

## Caveats — read before citing

- *Synthetic cohort.* Trajectories were generated with outcome-conditioned slopes,
  so the analysis recovers exactly what was put in. This is for the workshop demo
  — not evidence.
- See the manuscript [[drafts/manuscript-cbc-antibiotic-response|discussion
  section]] for the full limitations passage.

## Connections

- [[concepts/immature-granulocytes]]
- [[concepts/eosinopenia-of-stress]]
- [[concepts/neutrophil-left-shift]]
- [[concepts/sepsis-3-criteria]] — endpoint framing.
