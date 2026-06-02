---
title: Buell 2024 — ML for early detection of untreated infection
journal: Critical Care Explorations
year: 2024
doi: 10.1097/CCE.0000000000001165
tags:
  - #paper
  - #ML
  - #antibiotic-timing
type: paper-note
---
Develops and validates a machine-learning model for early detection of
*untreated* infection — the bedside problem that gates antibiotic timing.

## Two-failure-mode framing
- Delayed antibiotics in infected patients → mortality.
- Unnecessary antibiotics in non-infected patients → resistance, harm.
- A good model has to be calibrated on *both* failure modes, not just AUROC.

## Why it's in the bibliography
- Anchors the *clinical relevance* of the timing question for the
  [[experiments/hyp-cbc-vitals-antibiotic-response|active hypothesis]] — it's not
  enough to predict response, the model must drive earlier intervention or
  earlier de-escalation.

## Connections
- [[concepts/antibiotic-stewardship]] is the downstream consumer.
- [[paper-notes/hernandez-2025-sepsis-ML-living-review]] surveys this class of model.
