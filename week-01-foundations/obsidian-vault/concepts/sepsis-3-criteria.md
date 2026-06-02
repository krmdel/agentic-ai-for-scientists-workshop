---
tags:
  - #sepsis
  - #endpoint
  - #scoring
type: concept
---
# Sepsis-3 criteria

International consensus definition of sepsis (Singer et al. 2016 JAMA): sepsis is
*life-threatening organ dysfunction caused by a dysregulated host response to
infection*, operationalised as a SOFA score increase ≥ 2 in a patient with
suspected infection.

## SOFA delta as endpoint

For the [[experiments/hyp-cbc-vitals-antibiotic-response|active hypothesis]], the
composite primary endpoint is **48-h SOFA delta + 30-d all-cause mortality**.

SOFA delta captures:
- Respiratory (PaO₂/FiO₂ + ventilation status)
- Coagulation (platelets)
- Liver (bilirubin)
- Cardiovascular (MAP + vasopressors)
- Neurological (GCS)
- Renal (creatinine + urine output)

A *decrease* of ≥ 2 over 48 h aligns with clinical improvement; *increase* of ≥ 2
flags clinical deterioration.

## Caveats

- SOFA assumes ICU-level data availability. Ward-level data may not have continuous
  MAP or vasopressor input.
- qSOFA (heart rate, RR, GCS) is the screening proxy at admission — but it's a
  *binary* classifier, not a trajectory.

Related: [[concepts/host-response-paradigm]], [[concepts/antibiotic-stewardship]],
[[experiments/hyp-cbc-vitals-antibiotic-response]].
