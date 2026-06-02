## Methods

**Cohort.** The workshop-demo cohort comprises 100 hypothetical adult inpatients with documented bacterial infection across six body sites (bloodstream, pneumonia, urinary tract, intra-abdominal, skin and soft tissue, other) on twelve empirical antibiotic regimens spanning monotherapies and common combinations. Patient ages are sampled from $\mathcal{N}(64, 16^2)$ truncated to [18, 95], reflecting the older skew of bacterial-sepsis cohorts in tertiary care \cite{LaVia2026}.

**Variables.** For each patient we record at admission (T0) and at 24, 48, 72 h:
- *CBC indices*: neutrophil percentage (NEUT%), eosinophil percentage (EOS%), immature granulocyte percentage (IG%)
- *Vital signs*: heart rate (HR), temperature (Temp, °C), respiratory rate (RR), oxygen saturation (SpO2, %)

Outcome is scored on a four-level ordinal scale: *improver*, *slow responder*, *non-responder*, *died*, with weights chosen to reflect the published distribution in mixed acute-care cohorts \cite{LaVia2026}.

**Trajectory features.** Each feature is summarised by its admission value and its 0–72 h slope (least-squares fit through the four timepoints). The combination $(\text{value}_0, \text{slope}_{0\to 72})$ defines a two-dimensional trajectory signature per feature per patient.

**Analyses.** Outcome groups are compared by ANOVA on continuous features and chi-squared on categorical features. Effect sizes are reported as $\eta^2$. Age-band stratification ($<65$ vs $\geq 65$ y) is pre-specified per Domain-expert critique of the underlying hypothesis. Multiple-comparison correction within the seven-feature family uses Benjamini–Hochberg FDR at $q = 0.05$.

**Reproducibility.** The cohort CSV (`cohort_cbc_vitals.csv`), the analysis script (`analyze_cohort.py`), and the dataset descriptor (`data-{ds_id}.json`) ship with the workshop project; running `python3 analyze_cohort.py` from `data/` regenerates all summary statistics.
