---
tags:
  - #data
  - #MIMIC-IV
  - #access-notes
type: data-note
---
# MIMIC-IV access notes

For the prospective second-stage validation pass of
[[experiments/hyp-cbc-vitals-antibiotic-response|the active hypothesis]], MIMIC-IV
is the obvious retrospective substrate.

## Credentialled-user setup

- PhysioNet account → CITI human-subjects training → Data Use Agreement.
- Lead time: ~3 weeks at TUMCREATE (mostly the training step).
- Storage: project-isolated bucket on TUMCREATE GPU cluster.

## Cohort definition (proposed)

- Adult inpatients (>= 18 y) with ICD-10 bacterial infection diagnosis.
- Excludes: oncology immunosuppressed (cortisol-driven eosinopenia confounding),
  burn unit (separate trajectory; see [[paper-notes/xu-2026-burn-sepsis-trajectories]]).
- Antibiotic regimen extractable from `inputevents_mv` table.
- CBC + vitals time-aligned to first antibiotic dose timestamp.

## Open question

- *How frequent are 5-part differentials in MIMIC-IV?* If IG% is not reliably
  recorded across the cohort, the IG% leg of the
  [[experiments/hyp-cbc-vitals-antibiotic-response|hypothesis]] cannot be tested
  on MIMIC-IV — needs to wait for the prospective TUMCREATE cohort.

## Connections

- [[paper-notes/khanghah-2025-vital-signs-mrsa]] — uses MIMIC-IV substrate.
- [[paper-notes/zhu-2026-RPR-sepsis-coagulopathy]] — uses MIMIC-IV substrate.
