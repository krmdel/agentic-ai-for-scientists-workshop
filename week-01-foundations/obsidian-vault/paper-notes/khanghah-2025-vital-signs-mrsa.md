---
title: Khanghah 2025 — Deep learning vital signs predicts MRSA screening
journal: IEEE EMBC Proceedings
year: 2025
doi: 10.1109/EMBC58623.2025.11253426
tags:
  - #paper
  - #vital-signs
  - #MRSA
  - #deep-learning
type: paper-note
---
BiLSTM model on six MIMIC-IV vital signs (temperature, HR, systolic + diastolic BP,
respiratory rate, SpO2) predicts positive MRSA screening with F1 = 89.19%, AUROC = 0.96
at a 1-day window.

## Why it's load-bearing
- Vital signs *alone* — no blood draw — achieve AUROC > 0.9 for a bacterial-screening
  task. This means the [[experiments/hyp-cbc-vitals-antibiotic-response|CBC + vitals
  hypothesis]] does not rest entirely on CBC: vitals already pull weight.
- BiLSTM is the right architecture for the longitudinal-trajectory framing.
- MIMIC-IV training environment is the standard external substrate.

## Caveats
- *Screening positivity* is a colonisation proxy, not active infection.
- Single-centre validation (MIMIC-IV alone) — external-site validation pending.

## Connections
- [[concepts/host-response-paradigm]] — vital-signs models are pure host-response readouts.
- [[paper-notes/hernandez-2025-sepsis-ML-living-review]] places this in the broader
  ML-for-sepsis landscape.
