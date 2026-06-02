---
title: Xu 2026 — Burn sepsis biomarker trajectories
journal: Frontiers in Cellular and Infection Microbiology
year: 2026
doi: 10.3389/fcimb.2026.1710916
tags:
  - #paper
  - #trajectories
  - #growth-mixture-modeling
type: paper-note
---
Growth-mixture modeling of longitudinal biomarker trajectories in burn sepsis
identifies *phenotype clusters* by trajectory shape, not by admission value.

## Methodologist's love
- This is the right statistical machinery for the
  [[experiments/hyp-cbc-vitals-antibiotic-response|active hypothesis]] — recover
  latent trajectory phenotypes first, then regress phenotype on outcome. Avoids
  the "pick a feature, pick a timepoint" fishing problem.

## Limitations
- Burn sepsis is a unique population (predictable injury timing, intense ICU
  monitoring). External validity to community-acquired bacterial infection is not
  established.

## Connections
- [[concepts/host-response-paradigm]] — same family of methods.
- [[paper-notes/tertess-2026-lymphopenia-bacterial]] — adjacent trajectory work.
