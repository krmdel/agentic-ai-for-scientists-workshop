---
tags:
  - #hypothesis
  - #active
  - #CBC
  - #sepsis
  - #antibiotic-response
type: experiment
status: active
---
# Hypothesis — CBC + vital-sign trajectories as antibiotic-response indicators

**Status**: Active, council-critiqued, ready for prospective registration.

**Claim**. I want to investigate whether the sequential measurements of CBC-based
features ([[concepts/neutrophil-left-shift|neutrophil %]],
[[concepts/eosinopenia-of-stress|eosinophil %]], and
[[concepts/immature-granulocytes|immature granulocyte %]]) together with vital-sign
trends serve as real-time indicators of antibiotic treatment efficacy and clinical
improvement in bacterial infections.

## Council critique (4 personas, synthesised)

### Skeptic — confidence 0.7
- *Causation vs correlation*: CBC tracks host response, not the antibiotic's direct
  effect. "Efficacy" is unidentifiable from these signals alone.
- *Real-time is overclaimed*: routine CBC turnaround is 30–120 min; IG% requires
  automated 5-part differentials.
- Suggested: negative-control outcome test + viral / aseptic controls.

### Methodologist — confidence 0.65
- Two-stage design: retrospective hypothesis generation on MIMIC-IV, then
  prospective registration at TUMCREATE clinical partner.
- Use [[paper-notes/xu-2026-burn-sepsis-trajectories|growth-mixture modeling]] —
  trajectory phenotypes first, then regress on outcome.
- Pre-register endpoint, feature set, analysis plan on OSF.

### Domain-expert — confidence 0.85
- *Strongest leg*: IG% slope as bone-marrow stress signal — biology well-supported.
- *Plan for age-attenuated response* (Grudzinska 2020) — older adults run lower
  IG% for same severity. Stratify by age band ($<65$ / $\geq 65$y).
- Test EOS% *recovery slope*, not admission value.

### Biostatistician — confidence 0.60
- Mixed-effects logistic regression with patient-level random intercept + slope.
- BH-FDR within feature family.
- Minimum n = 600 (Bonferroni-equivalent power); n ≥ 1000 preferred.
- Report calibration (Brier, calibration slope) alongside AUROC.

## Synthesis

Three actionable refinements before measurement is meaningful:
1. *Re-scope* from "antibiotic efficacy" to "host-response trajectory associated
   with antibiotic response."
2. *Pre-register* a longitudinal design with locked feature set (NEUT%, EOS%, IG%,
   HR, Temp, RR, SpO2), locked endpoint ([[concepts/sepsis-3-criteria|48-h SOFA
   delta]] + 30-d mortality), held-out external-site test set.
3. *Stratify* by age band and antibiotic regimen class.

## Linked artifacts

- Data: [[data-notes/cohort-100-CBC-vitals]]
- Draft: [[drafts/manuscript-cbc-antibiotic-response]]
- Supporting papers: [[paper-notes/grudzinska-2020-neutrophils-CAP]],
  [[paper-notes/khanghah-2025-vital-signs-mrsa]],
  [[paper-notes/liporaci-2024-picu-bsi-ML]],
  [[paper-notes/buell-2024-early-untreated-infection]],
  [[paper-notes/tertess-2026-lymphopenia-bacterial]],
  [[paper-notes/xu-2026-burn-sepsis-trajectories]],
  [[paper-notes/kothari-2026-host-response-biomarkers]],
  [[paper-notes/cao-2026-HBP-PCT-CRP-SAA-pneumonia]]

## Daily log breadcrumbs

- [[daily/2026-05-12]] — initial council fan-out
- [[daily/2026-05-14]] — Biostatistician revision after re-reading Xu 2026
- [[daily/2026-05-19]] — manuscript draft pass + workshop demo build
