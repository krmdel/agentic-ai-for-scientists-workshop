---
tags:
  - #cbc
  - #hematology
  - #bone-marrow
type: concept
---
# Immature Granulocytes (IG%)

Promyelocytes, myelocytes, and metamyelocytes — band cells and earlier — released
from the bone marrow under acute infection stress.

## Why it matters

The IG% reading on an automated 5-part differential is the *peripheral signature of
the bone-marrow stress response*. Within hours of severe bacterial infection, the
[[concepts/neutrophil-left-shift|left shift]] populates IG% well before peripheral
NEUT% saturates.

## What the literature says

- [[paper-notes/grudzinska-2020-neutrophils-CAP]]: G-CSF response governs the
  release of immature neutrophils from bone marrow; this response is *attenuated*
  in older adults — the elderly cohort runs lower IG% for the same severity.
- [[paper-notes/liporaci-2024-picu-bsi-ML]]: CBC differentials including IG-class
  features show predictive value in the PICU.
- [[paper-notes/xu-2026-burn-sepsis-trajectories]]: trajectory shape carries more
  signal than admission value.

## Open question

Is the IG% *slope* over 0–48 h a cleaner separator of improvers vs non-responders
than admission IG%? Working assumption: yes — see
[[experiments/hyp-cbc-vitals-antibiotic-response]].

## Caveats

- Requires automated 5-part differential. Manual differentials are too slow + too
  noisy for the real-time framing.
- Analytical noise on IG% is non-trivial in low-acuity samples; signal floor ~1%.

Related: [[concepts/neutrophil-left-shift]], [[concepts/eosinopenia-of-stress]],
[[concepts/host-response-paradigm]].
