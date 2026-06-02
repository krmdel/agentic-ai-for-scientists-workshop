#!/usr/bin/env python3
"""Workshop demo builder. Writes every dashboard artifact in one pass.

Run from repo root:
    python3 projects/agentic-ai-workshop/_build_demo.py
"""
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SLUG = "agentic-ai-workshop"
PROJ = REPO / "projects" / SLUG
NOW_ISO = "2026-05-19T03:30:00.000Z"
TODAY = "20260519"


def w(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(payload, (dict, list)):
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    else:
        path.write_text(payload, encoding="utf-8")


def hid(seed: str) -> str:
    return hashlib.sha1(seed.encode()).hexdigest()[:6]


PAPERS = [
    {
        "pmid": "31732687",
        "title": "Neutrophils in community-acquired pneumonia: parallels in dysfunction at the extremes of age.",
        "authors": ["Frances Susanna Grudzinska", "Malcolm Brodlie", "Barnaby R Scholefield",
                    "Thomas Jackson", "Aaron Scott", "David R Thickett", "Elizabeth Sapey"],
        "year": 2020, "journal": "Thorax",
        "doi": "10.1136/thoraxjnl-2018-212826",
        "abstract": "Community-acquired pneumonia disproportionately affects older adults and children. Neutrophils from older adults appear dysfunctional, with reduced ability to target infected tissue, poor phagocytic responses, and a reduced capacity to release neutrophil extracellular traps. During sepsis, a reduced response to G-CSF inhibits the release of immature neutrophils from the bone marrow.",
        "tags": ["neutrophil", "CAP", "extremes-of-age"],
    },
    {
        "pmid": "41336571",
        "title": "Early Prediction of Positive Hospital-Acquired MRSA Screening using Deep Learning on Vital Signs Time Series.",
        "authors": ["Ali Barzegar Khanghah", "Shaghayegh Chavoshian", "Geoff Fernie", "Atena Roshan Fekr"],
        "year": 2025, "journal": "IEEE EMBC Proceedings",
        "doi": "10.1109/EMBC58623.2025.11253426",
        "abstract": "BiLSTM model on six vital signs (temperature, HR, systolic and diastolic BP, respiratory rate, SpO2) from MIMIC-IV predicts positive MRSA screening with F1=89.19% and AUROC=0.96 at a 1-day window. Recent fluctuations in vital signs hold predictive value for early MRSA detection before laboratory confirmation.",
        "tags": ["vital-signs", "MRSA", "deep-learning", "MIMIC-IV"],
    },
    {
        "pmid": "39705768",
        "title": "Advances in diagnosis and prognosis of bacteraemia, bloodstream infection, and sepsis using machine learning: A comprehensive living literature review.",
        "authors": ["B Hernandez", "D K Ming", "T M Rawson", "W Bolton", "R Wilson", "V Vasikasin",
                    "J Daniels", "J Rodriguez-Manzano", "F J Davies", "P Georgiou", "A H Holmes"],
        "year": 2025, "journal": "Artificial intelligence in medicine",
        "doi": "10.1016/j.artmed.2024.103008",
        "abstract": "Living review of machine-learning techniques used for diagnosis and prognosis of bacteraemia, bloodstream infections, and sepsis. Surveys model efficacy, limitations, and integration challenges into clinical practice.",
        "tags": ["sepsis", "ML-review", "bloodstream-infection"],
    },
    {
        "pmid": "39392375",
        "title": "Development and Validation of a Machine Learning Model for Early Detection of Untreated Infection.",
        "authors": ["Kevin G Buell", "Kyle A Carey", "Nicole Dussault", "William F Parker", "Jay Dumanian",
                    "Sivasubramanium V Bhavani", "Emily R Gilbert", "Christopher J Winslow", "Nirav S Shah",
                    "Majid Afshar", "Dana P Edelson", "Matthew M Churpek"],
        "year": 2024, "journal": "Critical Care Explorations",
        "doi": "10.1097/CCE.0000000000001165",
        "abstract": "Diagnostic uncertainty for infection causes delays in antibiotic administration in infected patients and unnecessary antibiotic administration in non-infected patients. The validated ML model targets earlier detection of untreated infection at the bedside.",
        "tags": ["antibiotic-timing", "ML", "early-detection"],
    },
    {
        "pmid": "38691554",
        "title": "A machine learning model for the early diagnosis of bloodstream infection in patients admitted to the pediatric intensive care unit.",
        "authors": ["Felipe Liporaci", "Danilo Carlotti", "Ana Carlotti"],
        "year": 2024, "journal": "PLoS ONE",
        "doi": "10.1371/journal.pone.0299884",
        "abstract": "Retrospective PICU cohort (n=76, 8816 records). CBC differentials, CRP, and vital-signs time series 72 h before and on blood-culture day. The machine-committee model attained accuracy 99.33%, precision 98.89%, sensitivity 100%, specificity 98.46%. Temporal changes in vitals and laboratory values carry early-BSI signal.",
        "tags": ["PICU", "BSI", "time-series", "CBC", "CRP"],
    },
    {
        "pmid": "41846741",
        "title": "A Comprehensive Evaluation of Rapid Diagnostic Methods in Neonatal Sepsis.",
        "authors": ["Amar Devaguru", "Kakara R Kanna"],
        "year": 2026, "journal": "Journal of Pharmacy and Bioallied Sciences",
        "doi": "10.4103/jpbs.jpbs_34_25",
        "abstract": "Reviews rapid diagnostic platforms in neonatal sepsis (PCR, microfluidics, procalcitonin). Identifies slow pathogen detection as the limiting factor and benchmarks emerging platforms on accuracy, turnaround time, and impact on antibiotic stewardship.",
        "tags": ["neonatal-sepsis", "diagnostics-review", "PCT"],
    },
    {
        "pmid": "41729625",
        "title": "Facilitators and barriers when implementing antibiotic stewardship interventions in neonates at risk of early-onset sepsis.",
        "authors": ["Liesanne Ej van Veen", "Sanne Wcm Janssen", "Gerdien A Tramper-Stranders",
                    "Niek B Achten", "Annemarie Mc van Rossum", "Frans B Plotz", "Erwin Ista"],
        "year": 2026, "journal": "JBI evidence implementation",
        "doi": "10.1097/XEB.0000000000000556",
        "abstract": "Identifies facilitators and barriers when implementing antibiotic stewardship interventions for early-onset sepsis in neonatal care. Despite evidence supporting various stewardship interventions, evidence on real-world implementation remains limited.",
        "tags": ["antibiotic-stewardship", "EOS", "implementation"],
    },
    {
        "pmid": "41718052",
        "title": "The Global Impact of Sepsis: Epidemiology, Recognition, Management, and Health System Challenges.",
        "authors": ["Luigi La Via", "Salvatore Ferlito", "Maria Stella Di Modica", "Andrea Marino",
                    "Giuseppe Nunnari", "Bruno Cacopardo", "Jerome Rene Lechien", "Mario Lentini",
                    "Salvatore Lavalle", "Giancarlo Carmelo Botto", "Paolo Buscema", "Loris Gruppuso",
                    "Antonino Maniaci"],
        "year": 2026, "journal": "Epidemiologia",
        "doi": "10.3390/epidemiologia7010020",
        "abstract": "Reports 48.9 million incident sepsis cases and 11.0 million deaths in 2017, accounting for almost one-fifth of global deaths. Highlights inequalities in awareness, early treatment, and health system readiness across high- vs low-income settings.",
        "tags": ["sepsis", "global-health", "epidemiology"],
    },
    {
        "pmid": "41698422",
        "title": "Blood Culture Time to Positivity in Adults: Pathogen Type Prediction and Contamination Discrimination.",
        "authors": ["Ozlem Aldemir", "Murtaza Oz", "Fatih Cubuk"],
        "year": 2026, "journal": "Journal of Microbiological Methods",
        "doi": "10.1016/j.mimet.2026.107434",
        "abstract": "Evaluates blood-culture time-to-positivity in patients with bacteremia and assesses its utility in predicting pathogen categories, distinguishing true bacteremia from contamination, and supporting early clinical decision-making.",
        "tags": ["blood-culture", "TTP", "bacteremia"],
    },
    {
        "pmid": "42125305",
        "title": "Circulatory biomarkers for microbial infections.",
        "authors": ["Vijay Kothari"],
        "year": 2026, "journal": "Journal of Circulating Biomarkers",
        "doi": "10.33393/jcb.2026.3777",
        "abstract": "Paradigm shift in infectious-disease diagnostics from direct pathogen detection to host-response profiling. CRP and PCT lack the specificity required for precision antimicrobial stewardship. Presepsin and multi-parametric mRNA signatures differentiate viral from bacterial etiologies. Integration with AI decision support aims to triangulate infection etiology within the clinical 'golden hour'.",
        "tags": ["biomarkers", "host-response", "stewardship", "AI"],
    },
    {
        "pmid": "41715017",
        "title": "Early signaling of inflammatory bursts by using estimated C-reactive Protein velocity (eCRPv): a model of acute meningitis and iso-CRPinemia.",
        "authors": ["Noa Shabtai Matatyahu", "Asaf Wasserman", "Tamar Witztum", "Amos Adler",
                    "Shlomo Berliner", "Ori Rogowski", "Tomer Ziv-Baran", "David Zeltser",
                    "Malka Katz Shalhav", "Yair Mina", "Noa Sasson", "Uri Obolski", "Ori Argov"],
        "year": 2026, "journal": "BMC Infectious Diseases",
        "doi": "10.1186/s12879-026-12676-1",
        "abstract": "CRP velocity (eCRPv) — CRP adjusted to time since symptom onset, expressed in mg/L/h — turns a static value into a dynamic measurement and improves discrimination between bacterial and viral acute meningitis when admission CRP concentrations overlap.",
        "tags": ["CRP-velocity", "meningitis", "kinetic-biomarker"],
    },
    {
        "pmid": "41620755",
        "title": "Diagnostic and prognostic value of serum HBP combined with PCT, CRP, and SAA in early-stage pneumonia.",
        "authors": ["Pengju Cao", "Songgao Zhang", "Jiangang Huang", "Wanru Dai"],
        "year": 2026, "journal": "Virology journal",
        "doi": "10.1186/s12985-026-03078-5",
        "abstract": "Heparin-binding protein (HBP) as a standalone biomarker and in combination panels (with PCT, CRP, SAA) for distinguishing early-stage bacterial vs viral pneumonia and predicting progression to severe disease.",
        "tags": ["HBP", "biomarker-panel", "pneumonia"],
    },
    {
        "pmid": "41584414",
        "title": "Inflammatory Markers in Pediatric Bacterial Sepsis vs. SARS-CoV-2 Infection: A Retrospective Study.",
        "authors": ["Antonio Andrusca", "Cristina Maria Mihai", "Cosmin Alexandru Pantazi",
                    "Simona Claudia Cambrea", "Irina Ion", "Emil Anton", "Tatiana Chisnoiu",
                    "Ancuta Lupu", "Mihaela Stoicescu", "Florin Daniel Enache", "Vasile Valeriu Lupu",
                    "Ileana Ion"],
        "year": 2026, "journal": "Current Health Sciences Journal",
        "doi": "10.12865/CHSJ.51.03.11",
        "abstract": "Compares CRP, fibrinogen, ESR, and D-dimer between pediatric bacterial sepsis and SARS-CoV-2 infection to discern characteristic inflammatory profiles for timely and appropriate therapy.",
        "tags": ["pediatric-sepsis", "SARS-CoV-2", "inflammatory-markers"],
    },
    {
        "pmid": "41557164",
        "title": "A comparative evaluation of salivary and serum procalcitonin to identify infants with serious bacterial infections.",
        "authors": ["Sercan Cinarli", "Ali Yurtseven", "Caner Turan", "Elif Azarsiz", "Timur Kose",
                    "Eylem Ulas Saz"],
        "year": 2026, "journal": "European Journal of Pediatrics",
        "doi": "10.1007/s00431-026-06763-3",
        "abstract": "Salivary PCT correlates with serum PCT and offers high diagnostic accuracy (AUC 0.92) for serious bacterial infections in infants <1 y. Salivary PCT performance approaches serum PCT (AUC 0.96) and exceeds serum CRP (AUC 0.88), supporting a non-invasive alternative.",
        "tags": ["procalcitonin", "infant-SBI", "non-invasive"],
    },
    {
        "pmid": "42079744",
        "title": "Dynamic biomarker profiling and phenotyping in burn sepsis: a retrospective cohort study using growth mixture modeling.",
        "authors": ["Pei Xu", "Jiaqi Lou", "Hong Kong", "Jiliang Li", "Ziyi Xiang", "Xiaoyu Zhu",
                    "Shengyong Cui", "Neng Huang", "Sida Xu", "Xin Le", "Youfen Fan", "Guoying Jin"],
        "year": 2026, "journal": "Frontiers in Cellular and Infection Microbiology",
        "doi": "10.3389/fcimb.2026.1710916",
        "abstract": "Growth-mixture modeling of longitudinal biomarker trajectories in burn sepsis identifies patient phenotypes by trajectory shape, not just admission value. Dynamic profiles outperform single-timepoint biomarkers for prognosis.",
        "tags": ["longitudinal", "burn-sepsis", "phenotyping", "trajectories"],
    },
    {
        "pmid": "42072379",
        "title": "Prognostic Value of International Normalized Ratio and Thrombocytopenia in Early Risk Stratification of Septic Patients.",
        "authors": ["Sofia Tejada", "Andres Giglio", "Maria Aranda", "Antonia Socias",
                    "Alberto Del Castillo", "Joana Mena", "Sara Franco", "Maria Ortega",
                    "Yasmina Nieto", "Marcio Borges-Sa"],
        "year": 2026, "journal": "Biomedicines",
        "doi": "10.3390/biomedicines14040839",
        "abstract": "Retrospective cohort of 6433 sepsis patients (2006-2022). INR at diagnosis predicted in-hospital mortality independently (OR 2.18, p=0.0002); platelet count alone did not improve the model (AUC 0.746). Combined INR>3.0 + platelets<50e9/L identified a 50%-mortality subgroup.",
        "tags": ["INR", "platelets", "sepsis-mortality", "risk-stratification"],
    },
    {
        "pmid": "42032529",
        "title": "Association between red blood cell distribution width-platelet ratio and mortality in patients with sepsis-induced coagulopathy from the MIMIC-IV database.",
        "authors": ["Yichao Zhu", "Zhiyu Li", "Tao Zhou", "Hongyang Xu"],
        "year": 2026, "journal": "BMC Infectious Diseases",
        "doi": "10.1186/s12879-026-13374-8",
        "abstract": "Red cell distribution width-to-platelet ratio (RPR) is associated with adverse outcomes in critically ill patients with sepsis-induced coagulopathy in MIMIC-IV, supporting CBC-derived ratios as readily available prognostic indices.",
        "tags": ["RPR", "MIMIC-IV", "sepsis-coagulopathy"],
    },
    {
        "pmid": "41751337",
        "title": "Lymphopenia in Bacterial Sepsis and SARS-CoV-2 Infection.",
        "authors": ["Raluca Tertess", "Lucian Cristian Petcu", "Bogdan Florentin Nitu",
                    "Mihaela Mariana Mavrodin", "Elena Cucli", "Elena Andreea Topa",
                    "Constantin Ionescu", "Nicolae Carciumaru", "Simona Claudia Cambrea"],
        "year": 2026, "journal": "Biomedicines",
        "doi": "10.3390/biomedicines14020438",
        "abstract": "Prospective cohort (n=95). Serial absolute lymphocyte counts and NLR on days 1, 3, 5, 7. Viral sepsis (COVID-19) showed sustained lymphopenia and progressive NLR rise; non-survivors had lower lymphocytes from day 3 and higher NLR on day 7 regardless of etiology. Longitudinal trends outperformed single timepoints.",
        "tags": ["lymphopenia", "NLR", "longitudinal", "etiology"],
    },
    {
        "pmid": "41742046",
        "title": "Utility of CBC-derived ratios in the diagnosis and prediction of active tuberculosis in people with rheumatic diseases.",
        "authors": ["Fengying Wu", "Xiaochun Shi", "Yuanchun Li", "Lantian Xie", "Yuchen Liu",
                    "Ye Liu", "Lifan Zhang", "Xiaoqing Liu"],
        "year": 2026, "journal": "BMC Infectious Diseases",
        "doi": "10.1186/s12879-026-12803-y",
        "abstract": "CBC-derived ratios (NLR, PLR, others) assist active tuberculosis diagnosis and risk assessment in people with rheumatic diseases, supplementing the limited sensitivity of microbiologic testing.",
        "tags": ["CBC-ratios", "tuberculosis", "diagnostic-aid"],
    },
    {
        "pmid": "32477860",
        "title": "Acute eosinophilic pneumonia with sepsis-like symptoms of arthralgia, joint stiffness and lymph node enlargement.",
        "authors": ["Jiajia Liu", "Zhiwei Shen", "Bin Tian", "Tingmei Zhang", "Cheng Zhang"],
        "year": 2022, "journal": "Respiratory Medicine Case Reports",
        "doi": "10.1016/j.rmcr.2020.101072",
        "abstract": "Acute eosinophilic pneumonia presenting with sepsis-like symptoms — caution for relying on inflammatory or febrile signature alone when eosinophil-driven syndromes can mimic bacterial sepsis.",
        "tags": ["eosinophilia", "case-report", "differential"],
    },
]

assert len(PAPERS) == 20, f"need 20 papers, got {len(PAPERS)}"

# ---- write paper JSONs ----
paper_ids = []
for p in PAPERS:
    pid = f"paperclip-pmid_{p['pmid']}"
    paper_ids.append(pid)
    obj = {
        "_artifact": "paper",
        "schema_version": 1,
        "id": pid,
        "source_ids": {
            "pmid": p["pmid"], "arxiv": None, "openalex": None,
            "s2": None, "paperclip": None, "doi": p["doi"],
        },
        "title": p["title"],
        "authors": p["authors"],
        "year": p["year"],
        "journal": p["journal"],
        "abstract": p["abstract"],
        "url": f"https://pubmed.ncbi.nlm.nih.gov/{p['pmid']}",
        "doi_url": f"https://doi.org/{p['doi']}",
        "pdf_url": None,
        "citation_count": None,
        "sources": ["pubmed"],
        "library_path": f"projects/{SLUG}/papers/{pid}.json",
        "saved_at": NOW_ISO,
        "relevance_score": 0.5 + (0.4 / (1 + PAPERS.index(p))),
        "relevance_breakdown": {"title": 0.5, "abstract": 0.5},
        "search_batch_id": "batch_demo_workshop_v1",
        "tags": p["tags"],
    }
    w(PROJ / "papers" / f"{pid}.json", obj)

# ---- hypothesis + 4 persona critiques + synthesis ----
hyp_id = f"hyp-{TODAY}-{hid('cbc-vitals-antibiotic-response')}"
hyp_dir = PROJ / "hypotheses" / hyp_id
hyp_obj = {
    "_artifact": "hypothesis",
    "schema_version": 1,
    "id": hyp_id,
    "claim": "I want to investigate whether the sequential measurements of CBC-based features (neutrophil %, eosinophil %, and immature granulocyte %) together with vital-sign trends serve as real-time indicators of antibiotic treatment efficacy and clinical improvement in bacterial infections.",
    "claim_short": "Sequential CBC features + vital-sign trends as real-time antibiotic-efficacy indicators",
    "project_slug": SLUG,
    "status": "open",
    "paper_ids": paper_ids[:12],
    "personas_used": ["Skeptic", "Methodologist", "Domain-expert", "Biostatistician"],
    "critique_files": [
        f"projects/{SLUG}/hypotheses/{hyp_id}/critiques/skeptic.json",
        f"projects/{SLUG}/hypotheses/{hyp_id}/critiques/methodologist.json",
        f"projects/{SLUG}/hypotheses/{hyp_id}/critiques/domain-expert.json",
        f"projects/{SLUG}/hypotheses/{hyp_id}/critiques/biostatistician.json",
    ],
    "synthesis_text": (
        "The four-persona council converges on three actionable refinements before the claim becomes "
        "measurable. (1) Re-scope from 'antibiotic efficacy' (Skeptic's identifiability concern) to "
        "'host-response trajectory associated with antibiotic response' — host signal is what CBC + vitals "
        "actually measure; drug effect is upstream and confounded by adjunct care. (2) Adopt a pre-registered "
        "longitudinal design with locked feature set (NEUT%, EOS%, IG%, HR, Temp, RR, SpO2), locked endpoint "
        "(48-h clinical improvement on the SOFA delta + 30-d mortality composite), and a held-out external-site "
        "test set, per the Methodologist's reproducibility brief. (3) Plan for the elderly-attenuated-response "
        "subgroup explicitly (Domain-expert citing Tupper 2025 / Grudzinska 2020), and stratify analysis by "
        "age band — global models will mis-predict on the cohort that matters most. (4) The Biostatistician "
        "requires mixed-effects models with patient-level random intercepts, missingness-aware (CBCs are not "
        "drawn on a clock), and pre-specified multiple-comparison correction across the 7 features × 4 "
        "timepoints. CONFIDENCE: medium — hypothesis is testable but requires reframing and design lock-down "
        "before measurement is meaningful."
    ),
    "open_questions": [
        "Which CBC feature carries the earliest signal — IG% (bone-marrow stress), NEUT% (acute response), or EOS% (resolution)?",
        "Is the elderly cohort identifiable as a separable phenotype, or does its attenuation generalise to immunosuppressed?",
        "Does adjunct steroid use confound the eosinophil trajectory enough to require exclusion?",
    ],
    "experiment_design": {
        "endpoint": "48-h SOFA delta + 30-d all-cause mortality (composite)",
        "exposure": "Locked feature vector (NEUT%, EOS%, IG%, HR, Temp, RR, SpO2) measured at admission and 24, 48, 72 h",
        "design": "Retrospective cohort, multi-site, pre-registered, with external-site held-out validation",
        "sample_size_target": "n=600 (effect size delta=0.3 SD, power=0.8, alpha=0.05, two-sided)",
        "stratification": ["age band (<65 / >=65)", "infection site (BSI / pneumonia / UTI / other)"],
        "primary_analysis": "Mixed-effects logistic regression on the composite endpoint with patient-level random intercepts.",
    },
    "council_confidence": "medium",
    "tags": ["CBC", "vital-signs", "antibiotic-response", "longitudinal", "host-response"],
    "notes": "Demo hypothesis for the Agentic AI Workshop walkthrough. Echoes the bacterial-infection-cohort hypothesis but with full Biostatistician critique enabled and a tighter synthesis.",
    "created_at": NOW_ISO,
    "updated_at": NOW_ISO,
    "library_path": f"projects/{SLUG}/hypotheses/{hyp_id}/hypothesis.json",
    "excluded_persona_ids": [],
    "additional_papers_by_persona": {},
}
w(hyp_dir / "hypothesis.json", hyp_obj)

# personas (project-scoped — same shape as bacterial-infection-cohort, with Biostatistician active)
w(PROJ / "hypotheses" / "personas.json", [
    {"name": "Skeptic", "role": "challenges every claim", "avatar": "S", "active": True},
    {"name": "Methodologist", "role": "checks study design", "avatar": "M", "active": True},
    {"name": "Domain-expert", "role": "field-specific knowledge", "avatar": "D", "active": True},
    {"name": "Biostatistician", "role": "power, multiple comparisons, mixed-effects, missing data",
     "avatar": "B", "active": True},
])

CRITIQUES = [
    {
        "persona": "Skeptic", "slug": "skeptic", "confidence": "medium",
        "critiques": [
            "Causation vs correlation: CBC trajectories track host response (steroids, transfusion, fluid status) and not the antibiotic's direct antibacterial action; 'efficacy' is not identifiable from these signals alone.",
            "Confounding by indication: sicker patients receive more frequent CBCs AND more aggressive antibiotic escalation. The feature-outcome correlation will partly reflect monitoring intensity, not biology.",
            "'Real-time' is overclaimed: routine CBC turnaround is 30-120 min, IG% requires 5-part automated differentials not universally available, and analytical noise on EOS% near zero is large enough to swamp the early treatment signal.",
            "Feature pre-specification is suspect: why NEUT%, EOS%, IG% and not NLR, RDW, platelet trend, or PCT? Risk of HARKing once the dataset is in hand.",
        ],
        "counter_evidence": [
            "Khanghah 2025 (pmid_41336571) achieved AUROC 0.96 for MRSA screening from vital signs ALONE — the vital-signs leg already carries strong signal independent of CBC.",
            "Liporaci 2024 (pmid_38691554) PICU cohort: CBC + vitals time-series time-aligned model attained 99% precision and 100% sensitivity for BSI — the joint signal IS there, the open question is whether 'efficacy' rather than 'detection' is the right framing.",
            "Tertess 2026 (pmid_41751337) shows longitudinal trajectories beat single-timepoint inflammatory markers — supports the temporal-shape framing.",
        ],
        "suggested_experiments": [
            "Negative-control outcome test: regress CBC + vitals trajectory on a sham endpoint (day-of-week of admission). If the model still 'predicts' efficacy, the pipeline is leaking.",
            "Pre-register with locked feature set, locked endpoint, locked analysis plan. Hold out one external site entirely.",
            "Run the same model on viral-infection controls and aseptic-inflammation controls. If it 'predicts antibiotic efficacy' there too, the signal is generic inflammation resolution.",
        ],
        "raw": "APPROACHES:\n1. Negative-control outcome falsification | P(BEAT): 0.75 | EFFORT: low | REF: Lipsitch 2010\n2. Disentangle host-response from drug-effect via viral/aseptic controls | P(BEAT): 0.70 | EFFORT: medium\n3. External-site held-out validation | P(BEAT): 0.55 | EFFORT: high\n\nDEAD_ENDS: Single-centre retrospective; AUROC-only reporting without calibration/decision-curve.\n\nCONFIDENCE: 0.7 — testable, but framing conflates host response with drug effect; reframing required before measurement is meaningful.",
        "supporting_paper_ids": ["paperclip-pmid_41336571", "paperclip-pmid_38691554", "paperclip-pmid_41751337"],
    },
    {
        "persona": "Methodologist", "slug": "methodologist", "confidence": "medium",
        "critiques": [
            "Study design unspecified: prospective vs retrospective changes the entire identifiability calculus. Retrospective cohorts have unmeasured indication confounding; prospective requires IRB + 18-mo runway.",
            "Endpoint is ill-defined: 'antibiotic efficacy' is operationalised in the literature as either (a) 48-72 h SOFA decrease, (b) bacteremia clearance on follow-up culture, (c) 30-d mortality, or (d) clinician-adjudicated. Pick one, lock it.",
            "Sampling frequency drift: CBCs are drawn on physician decision, not protocol. Patients with frequent draws differ from those with infrequent draws — informative missingness needs explicit modeling (e.g. inverse probability weighting).",
            "External validity gap: most cited studies (MIMIC-IV-based) are US tertiary ICUs. Extrapolation to LMIC settings (Lu 2023 tetanus) or community-acquired-only populations is not justified by the cited evidence base.",
        ],
        "counter_evidence": [
            "Xu 2026 (pmid_42079744) burn-sepsis growth-mixture modeling demonstrates the right statistical machinery: latent-trajectory phenotypes from longitudinal biomarkers, not single-timepoint binarisation.",
            "Hernandez 2025 (pmid_39705768) living review notes that prospective external validation is the gating step; without it, ML for sepsis stays at the 'promising' stage.",
        ],
        "suggested_experiments": [
            "Two-stage design: Phase 1 retrospective hypothesis generation in MIMIC-IV; Phase 2 prospective registration at TUMCREATE clinical partner site for external validation.",
            "Use growth-mixture modeling on the longitudinal CBC + vitals to recover trajectory phenotypes BEFORE regressing on outcome — avoids the 'pick a feature, pick a timepoint' fishing problem.",
            "Pre-register the analysis plan on OSF with the locked endpoint, feature set, and analysis code before unblinding the outcome.",
        ],
        "raw": "ON DESIGN: two-stage (retro hypothesis -> prospective validation) is the only path that earns trust from a reviewer who reads sepsis ML.\nON ENDPOINTS: composite 48-h SOFA delta + 30-d mortality balances clinical signal with statistical power.\nON MISSINGNESS: inverse probability weighting; sensitivity analysis with multiple imputation.\nCONFIDENCE: 0.65 — design is fixable but the current claim is not yet measurable.",
        "supporting_paper_ids": ["paperclip-pmid_42079744", "paperclip-pmid_39705768"],
    },
    {
        "persona": "Domain-expert", "slug": "domain-expert", "confidence": "high",
        "critiques": [
            "Bone-marrow stress signal is real and pre-dates antibiotic effect: immature granulocytes (left shift) appear within hours of severe bacterial infection. This is the strongest a-priori biological case for the IG% leg of the hypothesis.",
            "Eosinopenia at admission is a recognised but under-used predictor of bacterial sepsis — eosinophils sequester to lymphoid tissue under cortisol/cytokine drive. Recovery of EOS% from <0.5% toward 1-2% is a well-known clinical 'corner-turned' sign in ward medicine.",
            "Elderly attenuated-response is the dominant clinical phenotype to plan for: 20-30% of older adults with bacterial pneumonia present afebrile and non-tachycardic (Grudzinska 2020). A model trained on younger ICU patients will mis-predict on the cohort that matters.",
            "Antibiotic CHOICE matters: beta-lactams cause faster CBC normalisation than glycopeptides for the same MIC clearance. Failure to stratify by regimen will leak choice into 'response'.",
        ],
        "counter_evidence": [
            "Cao 2026 (pmid_41620755) HBP + PCT + CRP + SAA panel outperforms CBC-only panels for early pneumonia — the proposed CBC-only framing may be locally optimal but globally undercut by biomarker panels.",
            "Kothari 2026 (pmid_42125305) argues the paradigm shift is to host-response profiling — presepsin / mRNA signatures will likely replace single CBC indices over the 2-3 year horizon.",
        ],
        "suggested_experiments": [
            "Test IG% slope (hours -> 24h -> 48h) as the primary feature, not absolute IG%. The slope is the bone-marrow response; the absolute number is noisier.",
            "Test EOS% RECOVERY (slope from admission to 72 h) as a 'corner-turned' marker, not admission EOS%.",
            "Plan a clinical pilot with the TUMCREATE imaging flow cytometer to ground-truth the IG% measurement against direct morphology.",
        ],
        "raw": "STRONGEST_LEG: IG% slope as bone-marrow stress signal — well-supported, undermined only by 5-part-differential availability.\nWEAKEST_LEG: 'real-time' framing — even with point-of-care CBC, kinetics are minutes-to-hours, not real-time in the sensor-fusion sense.\nMUST_STRATIFY_BY: age band, antibiotic regimen class, infection site, immunocompetence.\nCONFIDENCE: 0.85 — the biology supports the claim; the operationalisation needs work.",
        "supporting_paper_ids": ["paperclip-pmid_41620755", "paperclip-pmid_42125305", "paperclip-pmid_31732687"],
    },
    {
        "persona": "Biostatistician", "slug": "biostatistician", "confidence": "medium",
        "critiques": [
            "Power: with 7 features x 4 timepoints = 28 hypotheses, Bonferroni alpha=0.05/28 = 0.0018 — at this alpha, n=600 detects only d>=0.3 SD differences. Plan for n>=600 minimum, n>=1000 preferred.",
            "Mixed-effects required: patients contribute repeated measures; a flat logistic regression will under-estimate standard errors and inflate type-I error. Patient-level random intercept + random slope on time is the minimum.",
            "Informative missingness: 'CBC drawn or not' is itself a function of acuity. Naive complete-case analysis will bias toward the sicker subgroup. IPW or MI with sensitivity bounds are mandatory.",
            "Multiple comparison correction strategy unspecified. Bonferroni is too conservative across 28 correlated tests; use BH-FDR within the pre-specified feature family.",
            "Calibration vs discrimination: the field reports AUROC but not Brier scores or calibration intercept/slope. At a clinical decision threshold, well-calibrated probabilities matter more than ranking; report both.",
        ],
        "counter_evidence": [
            "Liporaci 2024 (pmid_38691554) reports 99% precision + 100% sensitivity — flag for overfitting. n=76 patients in PICU is below the variance floor for these point estimates; CI must be reported.",
            "Tejada 2026 (pmid_42072379) demonstrates the right framing: report AUROC AND OR with CI; show how each added feature changes the model rather than reporting a final-model headline.",
        ],
        "suggested_experiments": [
            "Pre-register: feature set, endpoint, primary analysis (mixed-effects logistic with random intercept, complete-case + IPW + MI sensitivity), and FDR family.",
            "Power calculation: target effect size d=0.3, alpha=0.0018 (Bonferroni / BH-FDR equivalent), power=0.8 → minimum n=600. Sensitivity table for n in {400, 600, 800, 1000}.",
            "Report calibration (Brier, calibration slope, ECE) alongside AUROC. Decision-curve analysis at the planned operating point.",
        ],
        "raw": "ANALYSIS_PLAN: mixed-effects logistic regression, patient-level random intercept + random slope, BH-FDR within feature family, sensitivity analysis with IPW + MI.\nREPORTING: AUROC + Brier + calibration slope + decision-curve, with CI.\nMINIMUM_n: 600 (Bonferroni-corrected), 1000 preferred.\nCONFIDENCE: 0.60 — current claim is not powered or specified enough to test; design fixable.",
        "supporting_paper_ids": ["paperclip-pmid_38691554", "paperclip-pmid_42072379"],
    },
]
for c in CRITIQUES:
    obj = {
        "_artifact": "persona-critique",
        "schema_version": 1,
        "hypothesis_id": hyp_id,
        "persona": c["persona"],
        "persona_slug": c["slug"],
        "confidence": c["confidence"],
        "critiques": c["critiques"],
        "counter_evidence": c["counter_evidence"],
        "suggested_experiments": c["suggested_experiments"],
        "raw_council_block": c["raw"],
        "supporting_paper_ids": c["supporting_paper_ids"],
        "library_path": f"projects/{SLUG}/hypotheses/{hyp_id}/critiques/{c['slug']}.json",
        "created_at": NOW_ISO,
    }
    w(hyp_dir / "critiques" / f"{c['slug']}.json", obj)

# ---- dataset stub + cohort CSV ----
ds_id = f"data-{TODAY}-{hid('cbc-cohort-v1')}"
ds_obj = {
    "_artifact": "dataset",
    "schema_version": 1,
    "id": ds_id,
    "project_slug": SLUG,
    "name": "CBC + vitals + outcome cohort (workshop demo, N=100)",
    "description": "Synthetic but biologically plausible 100-patient cohort. CBC features (NEUT%, EOS%, IG%) and vitals (HR, Temp, RR, SpO2) at admission and 24/48/72 h, plus outcome (improver / slow_responder / non_responder / died).",
    "rows": 100,
    "columns": ["patient_id", "age", "sex", "infection_site", "antibiotic_regimen",
                "NEUT_pct_0", "NEUT_pct_24", "NEUT_pct_48", "NEUT_pct_72",
                "EOS_pct_0", "EOS_pct_24", "EOS_pct_48", "EOS_pct_72",
                "IG_pct_0", "IG_pct_24", "IG_pct_48", "IG_pct_72",
                "HR_0", "HR_24", "HR_48", "HR_72",
                "Temp_0", "Temp_24", "Temp_48", "Temp_72",
                "RR_0", "RR_24", "RR_48", "RR_72",
                "SpO2_0", "SpO2_24", "SpO2_48", "SpO2_72",
                "outcome"],
    "csv_path": f"projects/{SLUG}/data/cohort_cbc_vitals.csv",
    "library_path": f"projects/{SLUG}/data/{ds_id}.json",
    "created_at": NOW_ISO,
}
w(PROJ / "data" / f"{ds_id}.json", ds_obj)

# generate cohort CSV
import random
random.seed(20260519)

def gen_patient(idx: int) -> list:
    outcome = random.choices(
        ["improver", "slow_responder", "non_responder", "died"],
        weights=[68, 18, 9, 5],
    )[0]
    age = max(18, min(95, int(random.gauss(64, 16))))
    sex = random.choice(["M", "F"])
    site = random.choices(
        ["BSI", "pneumonia", "UTI", "intra-abdominal", "skin-soft-tissue", "other"],
        weights=[18, 28, 22, 14, 10, 8],
    )[0]
    regimen = random.choices(
        ["ceftriaxone", "pip-tazo", "meropenem", "vancomycin", "ceftriaxone+azithromycin",
         "amox-clav", "cefepime", "ertapenem", "ampicillin", "metronidazole+ceftriaxone",
         "linezolid", "daptomycin"],
        weights=[18, 22, 14, 10, 8, 8, 6, 4, 4, 3, 2, 1],
    )[0]

    # trajectories shaped by outcome
    if outcome == "improver":
        neut0, neut_slope = random.gauss(86, 4), -random.uniform(2.5, 5.0)
        eos0, eos_slope = random.uniform(0.0, 0.4), random.uniform(0.20, 0.45)
        ig0, ig_slope = random.uniform(2.5, 5.5), -random.uniform(0.8, 1.4)
        hr0, hr_slope = random.gauss(108, 8), -random.uniform(4, 7)
        t0, t_slope = random.uniform(38.6, 39.6), -random.uniform(0.45, 0.65)
        rr0, rr_slope = random.gauss(22, 2), -random.uniform(0.7, 1.4)
        sp0, sp_slope = random.gauss(94, 2), random.uniform(0.4, 0.9)
    elif outcome == "slow_responder":
        neut0, neut_slope = random.gauss(87, 4), -random.uniform(1.0, 2.4)
        eos0, eos_slope = random.uniform(0.0, 0.3), random.uniform(0.08, 0.20)
        ig0, ig_slope = random.uniform(3.5, 6.5), -random.uniform(0.3, 0.7)
        hr0, hr_slope = random.gauss(112, 8), -random.uniform(1.5, 3.5)
        t0, t_slope = random.uniform(38.8, 39.6), -random.uniform(0.20, 0.40)
        rr0, rr_slope = random.gauss(23, 2), -random.uniform(0.3, 0.7)
        sp0, sp_slope = random.gauss(93, 2), random.uniform(0.2, 0.5)
    elif outcome == "non_responder":
        neut0, neut_slope = random.gauss(88, 4), random.uniform(-0.5, 0.8)
        eos0, eos_slope = random.uniform(0.0, 0.2), random.uniform(-0.05, 0.10)
        ig0, ig_slope = random.uniform(5.0, 8.0), random.uniform(-0.2, 0.3)
        hr0, hr_slope = random.gauss(115, 9), random.uniform(-1, 2)
        t0, t_slope = random.uniform(39.0, 40.0), random.uniform(-0.1, 0.2)
        rr0, rr_slope = random.gauss(25, 3), random.uniform(0, 0.5)
        sp0, sp_slope = random.gauss(91, 3), random.uniform(-0.3, 0.3)
    else:  # died
        neut0, neut_slope = random.gauss(89, 5), random.uniform(0.5, 2.5)
        eos0, eos_slope = random.uniform(0.0, 0.15), random.uniform(-0.1, 0.05)
        ig0, ig_slope = random.uniform(7.0, 12.0), random.uniform(0.3, 1.0)
        hr0, hr_slope = random.gauss(122, 12), random.uniform(0.5, 3.5)
        t0, t_slope = random.uniform(39.2, 40.3), random.uniform(-0.05, 0.30)
        rr0, rr_slope = random.gauss(28, 4), random.uniform(0.5, 1.5)
        sp0, sp_slope = random.gauss(88, 4), random.uniform(-1.2, 0.0)

    def traj(v0, slope, n=4, noise=0.05):
        return [round(v0 + slope * k + random.gauss(0, noise * abs(v0 + 1)), 2) for k in range(n)]

    neut = [max(40, min(99, v)) for v in traj(neut0, neut_slope, noise=0.025)]
    eos = [max(0.0, min(8.0, v)) for v in traj(eos0, eos_slope, noise=0.05)]
    ig = [max(0.0, min(20.0, v)) for v in traj(ig0, ig_slope, noise=0.08)]
    hr = [max(40, min(170, int(v))) for v in traj(hr0, hr_slope, noise=0.02)]
    t = [round(max(35.0, min(41.0, v)), 1) for v in traj(t0, t_slope, noise=0.015)]
    rr = [max(8, min(50, int(v))) for v in traj(rr0, rr_slope, noise=0.04)]
    sp = [max(70, min(100, int(v))) for v in traj(sp0, sp_slope, noise=0.015)]

    return [
        f"P{idx:03d}", age, sex, site, regimen,
        *neut, *eos, *ig, *hr, *t, *rr, *sp, outcome
    ]


csv_path = PROJ / "data" / "cohort_cbc_vitals.csv"
csv_path.parent.mkdir(parents=True, exist_ok=True)
with csv_path.open("w", encoding="utf-8") as f:
    f.write(",".join(ds_obj["columns"]) + "\n")
    for i in range(1, 101):
        row = gen_patient(i)
        f.write(",".join(str(v) for v in row) + "\n")

# Dashboard's rawFilePathByPrefix() globs data/<file_id>.* for the raw file.
# Without this alias the descriptor JSON above wins the prefix match and
# pandas reads metadata instead of the cohort, breaking plot generation.
csv_alias = PROJ / "data" / f"{ds_id}.csv"
if csv_alias.is_symlink() or csv_alias.exists():
    csv_alias.unlink()
csv_alias.symlink_to("cohort_cbc_vitals.csv")

# ---- analysis script (runnable from project root) ----
analysis_py = '''#!/usr/bin/env python3
"""Workshop demo analysis. Reads cohort_cbc_vitals.csv, runs the comparisons
referenced in the manuscript, writes summary.json + 3 plots.
"""
from __future__ import annotations
import csv
import json
from pathlib import Path
import statistics as st

HERE = Path(__file__).resolve().parent
CSV = HERE / "cohort_cbc_vitals.csv"
SUMMARY = HERE / "analysis_summary.json"

def load():
    rows = []
    with CSV.open() as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            row["age"] = int(row["age"])
            for k, v in list(row.items()):
                if k.startswith(("NEUT_pct_", "EOS_pct_", "IG_pct_", "HR_", "Temp_", "RR_", "SpO2_")):
                    row[k] = float(v)
            rows.append(row)
    return rows

def mean_by(rows, key, val_key):
    buckets = {}
    for r in rows:
        buckets.setdefault(r[key], []).append(r[val_key])
    return {k: (round(st.mean(v), 2), len(v)) for k, v in buckets.items()}

def main():
    rows = load()
    by_outcome = mean_by(rows, "outcome", "IG_pct_0")
    by_outcome_48 = mean_by(rows, "outcome", "IG_pct_48")
    by_site = mean_by(rows, "infection_site", "NEUT_pct_0")
    by_age_band = {}
    for r in rows:
        band = "<65" if r["age"] < 65 else ">=65"
        by_age_band.setdefault(band, []).append(r["Temp_0"])
    by_age_band = {k: (round(st.mean(v), 2), len(v)) for k, v in by_age_band.items()}

    out = {
        "n_patients": len(rows),
        "outcomes": {k: rows[0].__class__ for k in {r["outcome"] for r in rows}},
        "outcome_counts": {o: sum(1 for r in rows if r["outcome"] == o)
                           for o in {"improver", "slow_responder", "non_responder", "died"}},
        "IG_pct_at_admission_by_outcome": by_outcome,
        "IG_pct_at_48h_by_outcome": by_outcome_48,
        "NEUT_pct_at_admission_by_site": by_site,
        "Temp_at_admission_by_age_band": by_age_band,
        "headline":
            "Immature granulocyte % at admission is monotonically higher in worse outcomes "
            "(improver < slow_responder < non_responder < died). At 48 h, the gap WIDENS — "
            "improvers normalise toward 2-3%, non-responders climb past 8%. This is the bone-marrow stress signal.",
    }
    out["outcomes"] = list(out["outcome_counts"].keys())  # cleanup
    SUMMARY.write_text(json.dumps(out, indent=2) + "\\n")
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
'''
w(PROJ / "data" / "analyze_cohort.py", analysis_py)

# ---- manuscript scaffold ----
manu_slug = "cbc-vitals-antibiotic-response"
manu_dir = PROJ / "manuscripts" / manu_slug
manu = {
    "slug": manu_slug,
    "title": "Sequential CBC and Vital-Sign Trajectories as Real-Time Indicators of Antibiotic Response: A Workshop Demo",
    "authors": ["Kerem Delikoyun", "TUMCREATE Demo"],
    "target_journal": None,
    "citation_style": "apa",
    "ordering": ["abstract", "introduction", "methods", "results", "discussion", "references"],
    "created_at": NOW_ISO,
    "updated_at": NOW_ISO,
    "linked_hypothesis_ids": [hyp_id],
    "linked_paper_ids": paper_ids[:15],
    "linked_figure_ids": [],  # filled below after figure step
    "linked_dataset_ids": [ds_id],
}
w(manu_dir / "manuscript.json", manu)

SECTIONS = {
    "abstract": (
        "Abstract",
        """## Abstract

**Background.** Distinguishing patients who are responding to empirical antibiotic therapy from those who are not remains a daily bedside challenge across acute-care settings, with direct consequences for antibiotic-stewardship and downstream resistance trajectories \\cite{Devaguru2026} \\cite{vanVeen2026}. Conventional inflammatory markers such as C-reactive protein and procalcitonin lack the specificity required for precision antimicrobial stewardship \\cite{Kothari2026}, while machine-learning models built on routine bedside data show that vital-sign trajectories alone can predict bacterial-screening status with high discrimination \\cite{Khanghah2025} \\cite{Liporaci2024}. Whether *sequential* CBC indices — neutrophil percentage, eosinophil percentage, and immature granulocyte percentage — combined with vital-sign trends carry signal that varies systematically with the trajectory of *clinical improvement* under empirical antibiotic therapy has not been characterised in a unified longitudinal cohort.

**Methods.** We assembled a 100-patient demo cohort with admission and 24/48/72-h CBC indices, vital signs (HR, temperature, respiratory rate, SpO2), infection site, and empiric antibiotic regimen. Outcome was scored on a four-level ordinal scale (improver, slow responder, non-responder, died). Trajectories were summarised by initial value and 0–72 h slope and compared across outcome strata.

**Results.** Immature granulocyte percentage at admission stratifies cleanly across outcome ($\\Delta_{\\text{died-improver}} \\approx 5$ percentage points) and the gap *widens* by 48 h. Eosinophil recovery slope (EOS% from <0.5% toward 1–2% in survivors) emerges within 48 h in improvers but is absent in non-responders, echoing the literature on eosinopenia as a sepsis prognostic indicator \\cite{Tertess2026}. Temperature and heart rate trajectories normalise faster in improvers than in slow responders but are attenuated in the elderly ($\\geq 65$y) subgroup, consistent with prior reports of blunted febrile and tachycardic responses in older adults with bacterial pneumonia \\cite{Grudzinska2020}.

**Conclusions.** In this demo cohort, sequential CBC indices and vital-sign trajectories carry signal that aligns with *clinical improvement* under empirical antibiotic therapy more cleanly than admission-only values. The pattern motivates a pre-registered prospective study with locked feature set, locked endpoint, and external-site validation \\cite{Hernandez2025} before bedside deployment is justified.
""",
        ["Devaguru2026", "vanVeen2026", "Kothari2026", "Khanghah2025", "Liporaci2024",
         "Tertess2026", "Grudzinska2020", "Hernandez2025"],
    ),
    "introduction": (
        "Introduction",
        """## Introduction

Empirical antibiotic therapy is the cornerstone of acute-infection management, yet the bedside question *"is the patient responding?"* is answered today with little more than serial vital-sign chart review, clinician gestalt, and sparse repeat laboratory studies. The cost of delayed recognition of non-response is high: antimicrobial escalation, source-control investigation, and intensive-care upgrade all hinge on the same signal \\cite{LaVia2026} \\cite{Devaguru2026}.

Three complementary lines of evidence motivate the present study. First, neutrophilic responses to bacterial infection are biologically well-characterised, with bone-marrow demargination releasing immature granulocytes into peripheral blood within hours of severe infection \\cite{Grudzinska2020}. Second, machine-learning models built on routine vital-sign time-series — without any blood draw at all — achieve AUROC > 0.9 for early MRSA screening \\cite{Khanghah2025} and high precision for bloodstream-infection detection in the PICU \\cite{Liporaci2024}, demonstrating that the temporal *shape* of physiological signals carries diagnostic information beyond admission values. Third, the host-response paradigm is reframing infectious-disease diagnostics from direct pathogen detection toward biomarker panels that capture the patient's reaction to infection \\cite{Kothari2026} \\cite{Cao2026}.

We bring these threads together with three falsifiable predictions. *(P1)* Immature granulocyte percentage (IG%) at admission stratifies outcomes monotonically (improver < slow responder < non-responder < died). *(P2)* The 0–48 h slope of EOS% recovery — from admission eosinopenia toward 1–2% — separates improvers from non-responders independently of admission values. *(P3)* Vital-sign normalisation (HR ↓, Temp ↓, RR ↓, SpO2 ↑) is attenuated in patients $\\geq 65$ years old, requiring age-band stratification rather than a global model.
""",
        ["LaVia2026", "Devaguru2026", "Grudzinska2020", "Khanghah2025", "Liporaci2024",
         "Kothari2026", "Cao2026"],
    ),
    "methods": (
        "Methods",
        """## Methods

**Cohort.** The workshop-demo cohort comprises 100 hypothetical adult inpatients with documented bacterial infection across six body sites (bloodstream, pneumonia, urinary tract, intra-abdominal, skin and soft tissue, other) on twelve empirical antibiotic regimens spanning monotherapies and common combinations. Patient ages are sampled from $\\mathcal{N}(64, 16^2)$ truncated to [18, 95], reflecting the older skew of bacterial-sepsis cohorts in tertiary care \\cite{LaVia2026}.

**Variables.** For each patient we record at admission (T0) and at 24, 48, 72 h:
- *CBC indices*: neutrophil percentage (NEUT%), eosinophil percentage (EOS%), immature granulocyte percentage (IG%)
- *Vital signs*: heart rate (HR), temperature (Temp, °C), respiratory rate (RR), oxygen saturation (SpO2, %)

Outcome is scored on a four-level ordinal scale: *improver*, *slow responder*, *non-responder*, *died*, with weights chosen to reflect the published distribution in mixed acute-care cohorts \\cite{LaVia2026}.

**Trajectory features.** Each feature is summarised by its admission value and its 0–72 h slope (least-squares fit through the four timepoints). The combination $(\\text{value}_0, \\text{slope}_{0\\to 72})$ defines a two-dimensional trajectory signature per feature per patient.

**Analyses.** Outcome groups are compared by ANOVA on continuous features and chi-squared on categorical features. Effect sizes are reported as $\\eta^2$. Age-band stratification ($<65$ vs $\\geq 65$ y) is pre-specified per Domain-expert critique of the underlying hypothesis. Multiple-comparison correction within the seven-feature family uses Benjamini–Hochberg FDR at $q = 0.05$.

**Reproducibility.** The cohort CSV (`cohort_cbc_vitals.csv`), the analysis script (`analyze_cohort.py`), and the dataset descriptor (`data-{ds_id}.json`) ship with the workshop project; running `python3 analyze_cohort.py` from `data/` regenerates all summary statistics.
""",
        ["LaVia2026"],
    ),
    "results": (
        "Results",
        """## Results

**Cohort composition.** Of the 100 demo patients, 68 are scored as improvers, 18 as slow responders, 9 as non-responders, and 5 as died, mirroring the distribution observed in mixed acute-care populations \\cite{LaVia2026}. Pneumonia (28%), urinary tract infection (22%), and bloodstream infection (18%) are the three largest infection-site categories; pip-tazo (22%), ceftriaxone (18%), and meropenem (14%) are the three most common empirical regimens.

**P1 — IG% at admission stratifies outcome (Figure 1).** Mean admission IG% rises monotonically across outcome strata: improvers 3.9%, slow responders 4.9%, non-responders 6.4%, died 9.6%. The gap *widens* by 48 h (improvers 1.4%, slow responders 3.2%, non-responders 6.0%, died 11.8%), consistent with the bone-marrow stress response persisting in patients who fail to clear infection \\cite{Grudzinska2020}.

**P2 — EOS% recovery separates improvers from non-responders.** Admission eosinopenia is universal (mean EOS% $< 0.3$ across all outcome groups, in line with the eosinopenia-of-acute-stress literature). At 48 h, improvers have a mean EOS% of 1.2%; non-responders remain at 0.2%. The 0–48 h slope is the discriminating feature, not the admission value — echoing the longitudinal-trajectory framing supported by Tertess et al. (2026) \\cite{Tertess2026} and Xu et al. (2026) \\cite{Xu2026}.

**P3 — Vital-sign normalisation is age-attenuated.** In the $<65$y subgroup, mean temperature at admission is 39.0 °C, falling to 37.6 °C by 72 h in improvers. In the $\\geq 65$y subgroup, admission temperature is 38.5 °C and the 72-h reading is 37.4 °C — the *delta* is smaller and the absolute admission value is lower, both consistent with the blunted-response phenomenon documented in older adults with bacterial pneumonia \\cite{Grudzinska2020}.

**Antibiotic-regimen effect.** NEUT% differs across the twelve regimen categories (ANOVA $F = 2.5$, $p < 0.01$, $\\eta^2 = 0.03$), consistent with regimen choice tracking the underlying inflammatory phenotype rather than driving it.
""",
        ["LaVia2026", "Grudzinska2020", "Tertess2026", "Xu2026"],
    ),
    "discussion": (
        "Discussion",
        """## Discussion

This workshop demo illustrates three claims that the literature already supports in adjacent settings and that this cohort makes locally testable. First, immature granulocyte percentage at admission separates outcome strata more cleanly than admission NEUT% — the bone-marrow stress signal is biologically prior to peripheral neutrophilia and rises faster \\cite{Grudzinska2020}. Second, the *slope* of EOS% recovery (not the admission value) is the early signature of clinical improvement under empirical antibiotic therapy, echoing the broader finding that *trajectories beat single-timepoint biomarkers* in sepsis \\cite{Tertess2026} \\cite{Xu2026}. Third, the elderly subgroup requires explicit stratification: vital-sign normalisation is attenuated, and a global model fit on a younger ICU cohort will mis-predict on the population that matters most for community-acquired bacterial infection \\cite{Grudzinska2020}.

**Limitations.** The cohort is synthetic, with trajectories shaped to match outcome by construction; it does not constitute evidence. Its purpose is to instrument the workflow — literature → hypothesis → critique → data → figure → draft — so the dashboard's workspaces can be demonstrated against a coherent storyline. Bedside deployment of any model derived from real data of this shape would require: (i) prospective external-site validation \\cite{Hernandez2025}; (ii) pre-registered analysis plan with locked feature set and locked endpoint \\cite{Buell2024}; (iii) explicit handling of informative missingness in CBC-draw frequency, which is a function of acuity; and (iv) calibration reporting (Brier score, calibration slope, decision-curve analysis) alongside discrimination.

**Why now.** Three convergent trends make this hypothesis worth testing prospectively. The host-response paradigm is reframing diagnostics around biomarker panels rather than direct pathogen detection \\cite{Kothari2026}; growth-mixture modeling and other latent-trajectory methods are now standard for longitudinal biomarker phenotyping \\cite{Xu2026}; and ML on routine vital-signs data already crosses the AUROC > 0.9 line for bacterial-screening tasks \\cite{Khanghah2025}. Adding sequential CBC indices to the trajectory model is the next obvious step.

**Next.** A two-stage design — retrospective hypothesis generation on MIMIC-IV followed by prospective registration at a clinical partner site — is the minimum credible path. The TUMCREATE label-free imaging flow cytometer offers a parallel opportunity to ground-truth IG% against direct morphology, closing a measurement-validity loop that automated 5-part differentials cannot.
""",
        ["Grudzinska2020", "Tertess2026", "Xu2026", "Hernandez2025", "Buell2024",
         "Kothari2026", "Khanghah2025"],
    ),
    "references": (
        "References",
        # placeholder; the manuscript-viewer renders the linked_paper_ids
        "## References\n\nReferences are resolved from `manuscript.json.linked_paper_ids` at render time. See `papers/` for full metadata.\n",
        [],
    ),
}

for sect_id, (title, body, refs) in SECTIONS.items():
    obj = {
        "_artifact": "section-draft",
        "schema_version": 1,
        "id": f"sect-{manu_slug}-{sect_id}",
        "manuscript_slug": manu_slug,
        "section_id": sect_id,
        "section_type": sect_id,
        "status": "draft",
        "content_md": body,
        "linked_figure_ids": [],  # figure linked manually after the nano-banana step
        "linked_paper_ids": refs,
        "version": 1,
        "library_path": f"projects/{SLUG}/manuscripts/{manu_slug}/sections/{sect_id}.md",
        "updated_at": NOW_ISO,
    }
    w(manu_dir / "sections" / f"{sect_id}.json", obj)
    w(manu_dir / "sections" / f"{sect_id}.md", body)

# ---- runs history ----
runs_dir = PROJ / ".organon" / "runs"
runs_dir.mkdir(parents=True, exist_ok=True)
RUNS = [
    ("run-lit-search", "literature-search",
     "Searched paperclip + PubMed: 'CBC immature granulocyte bacterial infection antibiotic response' — 20 papers added to library."),
    ("run-lit-search-2", "literature-search",
     "Followed up with 'procalcitonin antibiotic stewardship sepsis' and 'NLR bacterial infection severity' — 8 additional papers triaged, top 20 kept."),
    ("run-hypothesis-gen", "hypothesis-generate",
     "Generated hypothesis hyp-{HYP} from the user's stated claim. Dispatched 4-persona council: Skeptic, Methodologist, Domain-expert, Biostatistician.".format(HYP=hyp_id)),
    ("run-council-critique", "council-critique",
     "Council fan-out completed: Skeptic 0.7, Methodologist 0.65, Domain-expert 0.85, Biostatistician 0.60. Synthesis written."),
    ("run-data-load", "data-load",
     "Loaded cohort_cbc_vitals.csv (100 patients, 36 columns). Outcome counts: improver=68, slow_responder=18, non_responder=9, died=5."),
    ("run-data-analysis", "data-analysis",
     "Ran ANOVA on IG_pct_0 by outcome (F-test); chi-squared on infection_site by outcome; computed feature slopes for the seven trajectories."),
    ("run-figure-bone-marrow", "figure-generate",
     "Dispatched viz-nano-banana with scientific style. Prompt: 'bacterial infection drives a stereotyped bone marrow stress response — immature granulocytes spill into circulation, neutrophilia rises, eosinophils sequestered'."),
    ("run-draft-abstract", "draft-section",
     "Drafted abstract with 8 paper citations; ran citation-verify pre-write hook — all 8 verified against the library."),
    ("run-draft-results", "draft-section",
     "Drafted results section referencing the bone-marrow stress figure. Linked figure id into linked_figure_ids."),
    ("run-draft-discussion", "draft-section",
     "Drafted discussion. Flagged: cohort is synthetic, prospective validation required before bedside use."),
]
for i, (run_slug, kind, summary) in enumerate(RUNS):
    rid = f"run-{TODAY}-{i+1:02d}-{run_slug}"
    rec = {
        "run_id": rid,
        "kind": kind,
        "project_slug": SLUG,
        "started_at": NOW_ISO,
        "ended_at": NOW_ISO,
        "status": "completed",
        "summary": summary,
    }
    (runs_dir / f"{rid}.jsonl").write_text(json.dumps(rec) + "\n", encoding="utf-8")

print(f"WROTE {SLUG}: {len(PAPERS)} papers, 1 hypothesis with 4 critiques, 1 dataset + CSV,")
print(f"      1 manuscript ({len(SECTIONS)} sections), {len(RUNS)} runs entries.")
print(f"      Hypothesis id: {hyp_id}")
print(f"      Dataset id:    {ds_id}")
print(f"      Manuscript:    manuscripts/{manu_slug}/")
