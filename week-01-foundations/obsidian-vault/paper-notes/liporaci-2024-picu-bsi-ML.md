---
title: Liporaci 2024 — ML for early BSI detection in PICU
journal: PLoS ONE
year: 2024
doi: 10.1371/journal.pone.0299884
tags:
  - #paper
  - #PICU
  - #BSI
  - #machine-learning
type: paper-note
---
Retrospective PICU cohort, 76 patients, 8816 records. Combines CBC differentials, CRP,
and vital signs (HR, RR, BP, temperature, SpO2) 72 h before and on blood-culture day.
Machine-committee model: accuracy 99.33%, precision 98.89%, sensitivity 100%,
specificity 98.46%.

## Why it's important
- *Combines* CBC + CRP + vitals in a longitudinal model — closest published precedent
  for the [[experiments/hyp-cbc-vitals-antibiotic-response|active hypothesis]].
- Demonstrates that 72-h pre-culture data carry signal for blood-stream infection.

## Methodologist concern
- n = 76 is below the variance floor for the reported 99%+ point estimates.
  Confidence intervals are not reported in the abstract — at this n, even small CI
  expansion could flip the headline.

## Connections
- [[concepts/immature-granulocytes]] — CBC differentials include IG-class features.
- [[paper-notes/hernandez-2025-sepsis-ML-living-review]] — situates this in the
  ML-for-sepsis living review.
