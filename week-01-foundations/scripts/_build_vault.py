#!/usr/bin/env python3
"""Workshop demo Obsidian vault builder. ~35 cross-linked notes designed
to demonstrate the Organon → Obsidian integration at a glance.

Run:
    python3 projects/briefs/agentic-ai-workshop/_build_vault.py
"""
from __future__ import annotations
from pathlib import Path

VAULT = Path(__file__).resolve().parent / "obsidian-vault"

def w(rel: str, body: str, frontmatter: dict | None = None) -> None:
    path = VAULT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    if frontmatter is not None:
        fm = ["---"]
        for k, v in frontmatter.items():
            if isinstance(v, list):
                fm.append(f"{k}:")
                for item in v:
                    fm.append(f"  - {item}")
            else:
                fm.append(f"{k}: {v}")
        fm.append("---\n")
        body = "\n".join(fm) + body
    path.write_text(body + ("\n" if not body.endswith("\n") else ""), encoding="utf-8")


# ---- Minimal .obsidian config (graph view tuned for the demo) ----
import json
(VAULT / ".obsidian").mkdir(parents=True, exist_ok=True)
(VAULT / ".obsidian" / "app.json").write_text(json.dumps({
    "promptDelete": False,
    "alwaysUpdateLinks": True,
    "newLinkFormat": "shortest",
    "showLineNumber": False,
    "useTab": False,
    "tabSize": 2,
    "showFrontmatter": True,
    "useMarkdownLinks": False,
    "attachmentFolderPath": "_attachments",
}, indent=2) + "\n", encoding="utf-8")

(VAULT / ".obsidian" / "graph.json").write_text(json.dumps({
    "collapse-filter": True,
    "search": "",
    "showTags": True,
    "showAttachments": False,
    "hideUnresolved": False,
    "showOrphans": True,
    "collapse-color-groups": False,
    "colorGroups": [
        {"query": "path:paper-notes", "color": {"a": 1, "rgb": 5479590}},      # cool blue
        {"query": "path:concepts", "color": {"a": 1, "rgb": 11250603}},        # warm gold
        {"query": "path:experiments", "color": {"a": 1, "rgb": 14635040}},     # red — hypotheses pop
        {"query": "path:data-notes", "color": {"a": 1, "rgb": 7847479}},       # teal
        {"query": "path:drafts", "color": {"a": 1, "rgb": 16770305}},          # bright yellow
        {"query": "path:daily", "color": {"a": 1, "rgb": 12369084}},           # purple
        {"query": "path:inbox", "color": {"a": 1, "rgb": 11189196}},           # neutral grey
        {"query": "path:identity", "color": {"a": 1, "rgb": 16753219}},        # orange
    ],
    "collapse-display": False,
    "showArrow": True,
    "textFadeMultiplier": 0,
    "nodeSizeMultiplier": 1.4,
    "lineSizeMultiplier": 1.2,
    "collapse-forces": False,
    "centerStrength": 0.6,
    "repelStrength": 12,
    "linkStrength": 1.1,
    "linkDistance": 280,
    "scale": 1,
    "close": False,
}, indent=2) + "\n", encoding="utf-8")

(VAULT / ".obsidian" / "workspace.json").write_text(json.dumps({
    "main": {
        "id": "main",
        "type": "split",
        "children": [
            {"id": "tab-graph", "type": "leaf", "state": {"type": "graph"}},
        ],
    },
    "active": "tab-graph",
    "lastOpenFiles": ["README.md", "identity/profile-kerem.md",
                      "experiments/hyp-cbc-vitals-antibiotic-response.md"],
}, indent=2) + "\n", encoding="utf-8")


# ---- README (gateway note) ----
w("README.md", """# Organon Workshop Vault

This is a **standalone sample vault** built for the *Agentic AI for Scientists* workshop
(Week 1 — Foundations of Gen AI, 15 May 2026). It is **separate** from the user's main
iCloud Obsidian vault on purpose: nothing here touches personal notes.

## What you're looking at

Every note in this vault is the kind of artifact Organon writes into Obsidian over the
course of a researcher's day. Open the **Graph View** (Cmd+G) and you'll see the
seven artifact families colour-coded:

- 🟧 **identity** — who the researcher is (profile, interests, lab context)
- 🟦 **paper-notes** — one note per paper picked up by `sci-literature-research`
- 🟨 **concepts** — biological / methodological notions that show up across papers
- 🟥 **experiments** — hypothesis notes from `sci-hypothesis` (with council critiques inlined)
- 🟦 **data-notes** — observations and decisions from `sci-data-analysis`
- 🟨 **drafts** — manuscript pointers + blog drafts from `sci-writing` / `sci-communication`
- 🟪 **daily** — session summaries from `meta-wrap-up`
- ⬜ **inbox** — quick-capture ideas, brainstorms, meeting notes

The point of the graph view is to show that *every* artifact a researcher creates
through Organon lands as a node in this connected vault. The connections are the
[[wikilinks]] between notes; they are how the graph becomes the unit of recall.

## Starting points

- [[identity/profile-kerem]] — the researcher's profile
- [[experiments/hyp-cbc-vitals-antibiotic-response]] — the active hypothesis at the
  centre of the workshop demo
- [[drafts/manuscript-cbc-antibiotic-response]] — the manuscript-in-progress that
  the dashboard's Draft workspace is building

## How this vault was generated

A single Python script (`_build_vault.py`, sibling to this vault) wrote every note
in one pass. In a real Organon session, these notes accumulate one at a time as the
researcher works — each skill that produces a knowledge artifact prompts to also
write it here via the [[concepts/obsidian-sync-gate|Obsidian Sync Gate]].

## Portability

This vault travels with the workshop folder. To use it on another laptop:

```bash
# After cloning / pulling the Organon repo on the second laptop:
rsync -av projects/briefs/agentic-ai-workshop/obsidian-vault/ \\
  <second-laptop>:/path/to/projects/briefs/agentic-ai-workshop/obsidian-vault/
# Then in Obsidian: File → Open folder as vault → select obsidian-vault/
```

See `../PORTABILITY.md` (one level up) for the full project-portability story.
""")


# ---- identity ----
w("identity/profile-kerem.md", """# Profile — Kerem Delikoyun

Senior researcher at **[[identity/lab-context|TUMCREATE]]** (Singapore), working at the
interface of **hematology diagnostics**, **acute care**, and **AI for science**.

## Core research focus

- [[concepts/label-free-imaging-flow-cytometry]] — direct cell-morphology readout
  without staining; the lab's flagship instrument capability.
- [[concepts/platelet-aggregation-activation]] — platelet function as a real-time
  marker of inflammation and coagulopathy.
- Acute diagnostics for [[concepts/sepsis-3-criteria|bacterial sepsis]],
  viral infection, and the bacterial–viral discrimination problem.

## Active questions (2026)

- Can [[experiments/hyp-cbc-vitals-antibiotic-response|sequential CBC and vital-sign
  trajectories]] serve as real-time indicators of antibiotic-response trajectory in
  bacterial infection?
- Does [[concepts/eosinopenia-of-stress|eosinophil recovery slope]] separate
  improvers from non-responders earlier than admission CBC?
- Can [[experiments/hyp-imaging-flow-cytometry-platelets|label-free imaging flow
  cytometry of platelets]] catch infection-driven activation before classical CBC
  parameters move?

## Communication style

- Terse, scientific, opinionated.
- Always check statistical assumptions before reporting results.
- Hedge appropriately — "suggests", "consistent with", not "proves".
- American spelling. No em dashes (period or comma instead).

## Tool ecosystem

- Compute: TUMCREATE GPU cluster + local M4 MacBook.
- Stats: R for survival, Python (statsmodels) for mixed-effects, no SPSS.
- Writing: Markdown → LaTeX via pandoc; references via BibTeX.
- Knowledge: this vault (Obsidian), Organon for daily workflow, GitHub for code.

See also: [[identity/research-interests]], [[identity/lab-context]].
""")

w("identity/research-interests.md", """# Research interests

A living index of what I'm reading, thinking about, and likely to pursue. Refreshed
across daily notes.

## Hot — actively building

- [[experiments/hyp-cbc-vitals-antibiotic-response]] — CBC + vitals as response markers
- [[concepts/label-free-imaging-flow-cytometry]] in [[concepts/platelet-aggregation-activation|platelet]] activation studies
- [[concepts/host-response-paradigm]] — moving from pathogen detection to host trajectory

## Warm — reading and noting

- [[concepts/procalcitonin]] and its limits in the elderly
- [[concepts/neutrophil-left-shift]] — biological prior for the IG% story
- [[concepts/sepsis-3-criteria]] — the SOFA-delta endpoint we'll use

## Cold — backlog, may surface later

- [[experiments/hyp-viral-vs-bacterial-classification]] — discrimination at admission
- [[concepts/antibiotic-stewardship]] as a deployment-side problem
- Mass-spec / proteomics integration ([[inbox/idea-mass-spec-CBC-fusion]])

## Anti-interests

- Pure pathogen genomics (orthogonal to my host-response focus).
- Clinical-trial design at scale — better suited to a clinical-epi group.
""")

w("identity/lab-context.md", """# TUMCREATE — lab context

[TUMCREATE](https://www.tum-create.edu.sg/) is the Singapore-based joint research
platform between Technical University of Munich and Nanyang Technological University.
The acute-diagnostics group focuses on point-of-care hematology with
[[concepts/label-free-imaging-flow-cytometry|label-free imaging flow cytometry]] as
the flagship instrument capability.

## Group composition

- Faculty PIs: 2 (engineering + clinical)
- Postdocs / senior researchers: 4 (including [[identity/profile-kerem|me]])
- Graduate students: 6
- Clinical collaborators: 3 (NUH, SGH, KK Women's & Children's)

## Active grants / collaborations

- Clinical pilot at NUH for [[experiments/hyp-imaging-flow-cytometry-platelets|imaging
  flow cytometry in critically ill patients]].
- Singapore Eye Research Institute joint project on retinal vascular imaging
  (separate track, not part of this workshop).

## Equipment

- Custom label-free imaging flow cytometer (in-house, prototype #4)
- Sysmex XN-9100 hematology analyzer (clinical reference)
- TUM-CREATE GPU cluster for training (4× A100, 8× L40)

See also: [[identity/profile-kerem]], [[identity/research-interests]].
""")


# ---- concepts ----
CONCEPTS = {
    "immature-granulocytes": ("""# Immature Granulocytes (IG%)

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
""", ["#cbc", "#hematology", "#bone-marrow"]),

    "eosinopenia-of-stress": ("""# Eosinopenia of stress

Acute drop in peripheral eosinophil percentage during the cortisol-and-cytokine
surge of severe infection, trauma, or surgery. Eosinophils don't disappear — they
*sequester* to lymphoid tissue.

## Why it matters for the demo

Two predictions follow:
1. *Admission EOS% will be near zero across all severities* — diagnostic value is low.
2. *EOS% recovery slope* (admission → 48 h) separates improvers from non-responders:
   improvers climb toward 1–2%, non-responders stay flat.

This is a textbook clinical observation that under-uses modern longitudinal modeling.
The [[experiments/hyp-cbc-vitals-antibiotic-response|active hypothesis]] tests it.

## Confounders

- **Steroid use** dominates the eosinophil signal — must exclude or stratify.
- **Asthma / atopic baseline** sets a higher floor — needs baseline EOS% if available.
- **Parasitic co-infection** (rare in Singapore acute care, but worth flagging).

## What the literature says

- [[paper-notes/grudzinska-2020-neutrophils-CAP]]: indirect — neutrophil response
  shifts in extremes of age, eosinopenia framework is the inverse.
- [[paper-notes/tertess-2026-lymphopenia-bacterial]]: longitudinal lymphocyte
  trajectories outperform single timepoints. Same logic applies to eosinophils.

Related: [[concepts/neutrophil-left-shift]], [[concepts/immature-granulocytes]],
[[concepts/host-response-paradigm]].
""", ["#cbc", "#hematology", "#stress-response"]),

    "neutrophil-left-shift": ("""# Neutrophil left shift

Increase in immature neutrophil forms (bands, metamyelocytes, myelocytes) in the
peripheral differential. Classically described as the bone-marrow's response to
acute bacterial infection.

## Why "left shift"

Historical: in the Schilling differential count (Hugo Schilling, 1923), immature
forms were tallied to the left of mature segmented neutrophils. A *left shift* is
literally more entries on the left column.

## Mechanism in one sentence

G-CSF and IL-6 surge → bone-marrow demargination → release of band cells and earlier
forms into peripheral circulation. See [[paper-notes/grudzinska-2020-neutrophils-CAP]].

## Modern operationalisation

[[concepts/immature-granulocytes|IG%]] on an automated 5-part differential is the
modern, automated proxy for the left shift. The Schilling count is still done
manually in low-resource settings.

## Why it matters for the demo

The left shift is the *biologically prior* signal — it appears before peripheral
NEUT% saturates and before vital-sign trajectories diverge enough to be clinically
obvious. Tail end: in non-responders, it does not resolve.

Related: [[concepts/immature-granulocytes]], [[concepts/host-response-paradigm]],
[[experiments/hyp-cbc-vitals-antibiotic-response]].
""", ["#cbc", "#hematology", "#bacterial-infection"]),

    "procalcitonin": ("""# Procalcitonin (PCT)

Precursor of calcitonin; in healthy adults, peripheral PCT is near-undetectable.
Bacterial endotoxin drives extra-thyroidal PCT release within 2–4 h, peaking
12–24 h after stimulus.

## Why it matters

PCT is the textbook biomarker for *bacterial-vs-other* differential. It's better
than CRP for early bacterial signal but has well-documented limits:

- Low specificity in burns, trauma, and post-surgical states.
- Suppressed in immunocompromised patients.
- Less informative in localised infections without bacteraemia.

## What the literature says

- [[paper-notes/kothari-2026-host-response-biomarkers]]: PCT lacks the specificity
  required for precision antimicrobial stewardship; the field is moving to
  multi-parametric mRNA signatures and host-response panels.
- [[paper-notes/cao-2026-HBP-PCT-CRP-SAA-pneumonia]]: HBP + PCT + CRP + SAA panel
  outperforms PCT alone for early bacterial pneumonia.
- [[paper-notes/devaguru-2026-neonatal-sepsis-diagnostics]]: PCT in neonatal sepsis
  diagnostics review.

## Where this fits in the demo hypothesis

PCT is an *adjunct*, not a replacement, for the
[[experiments/hyp-cbc-vitals-antibiotic-response|CBC + vitals trajectory]] story.
Both are host-response signals. PCT is more pathogen-class specific; CBC + vitals
are higher-frequency and capture *resolution* dynamics.

Related: [[concepts/host-response-paradigm]], [[concepts/antibiotic-stewardship]].
""", ["#biomarker", "#bacterial-infection", "#diagnostics"]),

    "host-response-paradigm": ("""# Host-response paradigm

The shift from *direct pathogen detection* (culture, PCR) to *measuring the
patient's immune response* (transcriptomic signatures, biomarker panels, cellular
phenotypes) as the primary axis of infectious-disease diagnostics.

## Why it's reframing the field

Direct pathogen detection has two failure modes: (1) the pathogen may be sterile-site
inaccessible, (2) it can take hours to days. Host response is universally measurable
at the bedside, immediately, with routine specimens.

## The Kothari 2026 thesis

[[paper-notes/kothari-2026-host-response-biomarkers]] argues that the integration
of circulating host-response biomarkers (presepsin, mRNA signatures, panels) with
AI decision support is the path to precision antimicrobial stewardship — and that
this will *replace* empiric treatment for bacterial vs viral infection within the
clinical "golden hour".

## How it connects to this lab

[[concepts/label-free-imaging-flow-cytometry]] is a host-response readout: it
measures peripheral cell morphology directly, without staining or pathogen capture.
The TUMCREATE imaging flow cytometer is a host-response instrument by design.

## Related ideas

- [[concepts/immature-granulocytes]] is a host-response feature (bone-marrow stress).
- [[concepts/eosinopenia-of-stress]] is a host-response feature (cortisol drive).
- [[concepts/procalcitonin]] is a host-response biomarker (bacterial-specific).

Related: [[experiments/hyp-cbc-vitals-antibiotic-response]],
[[experiments/hyp-imaging-flow-cytometry-platelets]],
[[experiments/hyp-viral-vs-bacterial-classification]].
""", ["#paradigm", "#diagnostics", "#host-response"]),

    "antibiotic-stewardship": ("""# Antibiotic stewardship

The clinical-systems practice of using the right antibiotic, at the right dose,
for the right duration — minimising both individual harm and population-scale
resistance.

## Why it matters here

The downstream consumer of every signal in the
[[experiments/hyp-cbc-vitals-antibiotic-response|CBC + vitals]] hypothesis is a
stewardship decision: keep the empirical regimen, escalate, de-escalate, or stop.

## What the literature says

- [[paper-notes/van-veen-2026-EOS-stewardship]]: stewardship implementation in
  neonatal early-onset sepsis is well-evidenced but poorly adopted.
- [[paper-notes/devaguru-2026-neonatal-sepsis-diagnostics]]: rapid diagnostics are
  the gating step for stewardship traction.
- [[paper-notes/kothari-2026-host-response-biomarkers]]: precision stewardship is
  the named goal of the host-response paradigm.

## Open question

Is the *48-h re-evaluation point* the right operating threshold for a CBC + vitals
trajectory model — or do clinicians need a continuously updating "trajectory score"
visible at the bedside?

Related: [[concepts/host-response-paradigm]], [[concepts/procalcitonin]],
[[concepts/sepsis-3-criteria]].
""", ["#stewardship", "#antibiotics", "#clinical-systems"]),

    "sepsis-3-criteria": ("""# Sepsis-3 criteria

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
""", ["#sepsis", "#endpoint", "#scoring"]),

    "label-free-imaging-flow-cytometry": ("""# Label-free imaging flow cytometry

Single-cell imaging at flow-cytometry rates *without fluorescent staining*.
Brightfield + quantitative phase + deep-learning morphology classification.
The TUMCREATE flagship capability.

## Why it matters

The standard CBC differential is reductive: 5 classes (NEUT, LYMPH, MONO, EOS, BASO)
plus IG%. Imaging flow cytometry can resolve:
- [[concepts/neutrophil-left-shift|Band cells vs segmented neutrophils]] directly,
  without serial 5-part differentials.
- [[concepts/platelet-aggregation-activation|Platelet activation states]] in real time.
- Reticulocyte maturation stages (clinically relevant in
  [[experiments/hyp-bone-marrow-recovery-after-sepsis|post-sepsis recovery]]).

## How it ties to this work

[[experiments/hyp-imaging-flow-cytometry-platelets]] is the adjacent imaging
hypothesis — measuring platelet activation before classical CBC parameters move.
The same instrument can also direct-measure the band-cell fraction that
[[concepts/immature-granulocytes|IG%]] *infers*.

## Instrument logistics

- Throughput: ~3000 cells/s in current prototype #4
- Sample volume: 50 µL whole blood (heparinised)
- Turnaround: 5–10 min including sample prep
- Cost per run: $4–7 (consumables + GPU time)

Related: [[experiments/hyp-imaging-flow-cytometry-platelets]],
[[concepts/platelet-aggregation-activation]],
[[data-notes/TUMCREATE-imaging-flow-pilot]].
""", ["#instrument", "#imaging-flow-cytometry", "#TUMCREATE"]),

    "platelet-aggregation-activation": ("""# Platelet aggregation and activation

Two related but distinct platelet behaviours, both of which shift in acute
inflammation and infection.

## Activation

Conformational change exposing GPIIb/IIIa, surface P-selectin (CD62P), shape change
from discoid to spherical with pseudopodia. Visible as morphology change in
[[concepts/label-free-imaging-flow-cytometry|label-free imaging flow]] *without
staining*.

## Aggregation

Activated platelets binding to each other via fibrinogen bridges. Visible as
clusters in flow.

## Why this matters for infection

Sepsis-induced coagulopathy is a recognised mortality predictor
([[paper-notes/tejada-2026-INR-platelets-sepsis|Tejada 2026]],
[[paper-notes/zhu-2026-RPR-sepsis-coagulopathy|Zhu 2026]]). Both groups use
admission platelet *count*; we hypothesise that platelet *activation morphology*
moves earlier and is detectable at the bedside via imaging flow.

## Active work

[[experiments/hyp-imaging-flow-cytometry-platelets]] is the lab's primary
imaging-flow hypothesis for 2026.

Related: [[concepts/label-free-imaging-flow-cytometry]],
[[concepts/host-response-paradigm]],
[[paper-notes/tejada-2026-INR-platelets-sepsis]].
""", ["#platelets", "#imaging-flow-cytometry"]),

    "obsidian-sync-gate": ("""# Obsidian Sync Gate

The Organon pattern: *every knowledge artifact a skill produces is offered to
the user for sync into this vault*. Not silent — explicit, one prompt per
artifact.

## What gets offered

- Paper summaries from [[concepts/host-response-paradigm|literature-research]] → `paper-notes/`
- Hypothesis designs → `experiments/`
- Data observations from `sci-data-analysis` → `data-notes/`
- Manuscript drafts from `sci-writing` → `drafts/`
- Daily session summaries from `meta-wrap-up` → `daily/`

## What doesn't get offered

- Binary files (PDFs, CSVs, PNGs) — those go via the Drive Push Gate, not here.
- Organon framework files (memory/, .planning/, cron status) — those stay in
  Organon, not Obsidian.

## Why the gate matters

The graph view is only useful if the cluster is *connected*. The gate exists to
prompt the researcher to write a one-paragraph summary at write-time, with
explicit `[[wikilinks]]` to related notes — so the next time they search the
graph, the structure they expect is there.

Related: [[README]], [[identity/research-interests]].
""", ["#organon", "#workflow"]),
}

for name, (body, tags) in CONCEPTS.items():
    w(f"concepts/{name}.md", body, frontmatter={"tags": tags, "type": "concept"})


# ---- paper-notes (10 picks from the 20 papers in the dashboard) ----
PAPER_NOTES = {
    "grudzinska-2020-neutrophils-CAP": (
        "Grudzinska 2020 — Neutrophils in community-acquired pneumonia",
        "Thorax",
        2020,
        "10.1136/thoraxjnl-2018-212826",
        """Two-population review: neutrophil dysfunction at the extremes of age (older adults
+ preterm infants) parallels each other in community-acquired pneumonia.

## Key claims
- G-CSF response governs immature-neutrophil release from bone marrow; this
  response is *attenuated in older adults* — they run lower
  [[concepts/immature-granulocytes|IG%]] for the same severity.
- Older adults present afebrile and non-tachycardic in 20–30% of bacterial-pneumonia
  cases — must stratify by age band ([[experiments/hyp-cbc-vitals-antibiotic-response]]
  Domain-expert critique).
- Storage-pool depletion in preterm infants mirrors elderly response failure.

## Why it's in my library
- Strongest single citation for the *age-attenuation* leg of the
  [[experiments/hyp-cbc-vitals-antibiotic-response|active hypothesis]].
- Anchors the [[concepts/neutrophil-left-shift]] mechanism in CAP.

## Open thread
- Does the same attenuation apply to oncology immunosuppressed adults? Not covered
  here. Possibly an extension lit-search.
""", ["#paper", "#neutrophil", "#CAP", "#extremes-of-age"],
    ),

    "khanghah-2025-vital-signs-mrsa": (
        "Khanghah 2025 — Deep learning vital signs predicts MRSA screening",
        "IEEE EMBC Proceedings",
        2025,
        "10.1109/EMBC58623.2025.11253426",
        """BiLSTM model on six MIMIC-IV vital signs (temperature, HR, systolic + diastolic BP,
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
""", ["#paper", "#vital-signs", "#MRSA", "#deep-learning"],
    ),

    "liporaci-2024-picu-bsi-ML": (
        "Liporaci 2024 — ML for early BSI detection in PICU",
        "PLoS ONE",
        2024,
        "10.1371/journal.pone.0299884",
        """Retrospective PICU cohort, 76 patients, 8816 records. Combines CBC differentials, CRP,
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
""", ["#paper", "#PICU", "#BSI", "#machine-learning"],
    ),

    "buell-2024-early-untreated-infection": (
        "Buell 2024 — ML for early detection of untreated infection",
        "Critical Care Explorations",
        2024,
        "10.1097/CCE.0000000000001165",
        """Develops and validates a machine-learning model for early detection of
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
""", ["#paper", "#ML", "#antibiotic-timing"],
    ),

    "hernandez-2025-sepsis-ML-living-review": (
        "Hernandez 2025 — Sepsis ML living literature review",
        "Artificial Intelligence in Medicine",
        2025,
        "10.1016/j.artmed.2024.103008",
        """Living review of ML for bacteraemia, bloodstream infection, and sepsis. Surveys
model efficacy, limitations, and clinical-integration challenges.

## Most-cited takeaway in this vault
- Prospective external validation is the gating step. Without it, ML for sepsis
  stays at the "promising" stage no matter how high the in-sample AUROC.

## Why it's load-bearing for the demo
- Cited from the [[experiments/hyp-cbc-vitals-antibiotic-response|active hypothesis]]
  Methodologist critique as the rationale for two-stage design (retrospective
  hypothesis → prospective registration).
- Reading recommendation for anyone proposing single-centre AUROC headlines.

## Connections
- [[paper-notes/khanghah-2025-vital-signs-mrsa]]
- [[paper-notes/liporaci-2024-picu-bsi-ML]]
- [[paper-notes/buell-2024-early-untreated-infection]]
- [[concepts/host-response-paradigm]]
""", ["#paper", "#review", "#sepsis-ML"],
    ),

    "kothari-2026-host-response-biomarkers": (
        "Kothari 2026 — Circulatory biomarkers for microbial infections",
        "Journal of Circulating Biomarkers",
        2026,
        "10.33393/jcb.2026.3777",
        """Manifesto for the [[concepts/host-response-paradigm|host-response paradigm]] in
infectious-disease diagnostics. Argues CRP and PCT lack the specificity for
precision stewardship; presepsin and multi-parametric mRNA signatures are the
near-future replacements.

## Two strong claims
- The clinical "golden hour" can be triangulated via host-response biomarkers
  before pathogen culture returns.
- AI-driven decision support + host-response panels is what replaces empiric
  treatment with precision [[concepts/antibiotic-stewardship|antibiotic stewardship]].

## Why it framing-anchors this work
- The [[experiments/hyp-cbc-vitals-antibiotic-response|active hypothesis]] is a
  CBC-and-vitals incarnation of the same paradigm shift.
- [[concepts/label-free-imaging-flow-cytometry]] is a *direct-cell-morphology*
  incarnation of the same shift.

## Connections
- [[concepts/host-response-paradigm]] — the manifesto note.
- [[concepts/procalcitonin]] — the biomarker this paper critiques.
- [[paper-notes/cao-2026-HBP-PCT-CRP-SAA-pneumonia]] — concrete-panel implementation.
""", ["#paper", "#host-response", "#paradigm"],
    ),

    "tertess-2026-lymphopenia-bacterial": (
        "Tertess 2026 — Lymphopenia in bacterial sepsis vs SARS-CoV-2",
        "Biomedicines",
        2026,
        "10.3390/biomedicines14020438",
        """Prospective cohort (n = 95). Serial absolute lymphocyte counts (ALC) and NLR on
days 1, 3, 5, 7. Viral sepsis (COVID-19) showed sustained lymphopenia and
progressive NLR rise; non-survivors had lower ALC from day 3 onward and higher NLR
on day 7. Longitudinal trends outperformed single-timepoint values.

## Why it's load-bearing
- *Trajectories beat snapshots* — the empirical core of the
  [[experiments/hyp-cbc-vitals-antibiotic-response|active hypothesis]].
- Direct precedent for serial-CBC-features approach.

## Caveat
- Etiology-specific (bacterial vs viral comparison). The CBC + vitals hypothesis is
  bacterial-only — Tertess's *bacterial arm* is the only relevant subgroup.

## Connections
- [[concepts/eosinopenia-of-stress]] — analogous trajectory framing for eosinophils.
- [[paper-notes/xu-2026-burn-sepsis-trajectories]] — same trajectory principle, burn
  sepsis subpopulation.
""", ["#paper", "#lymphopenia", "#trajectories"],
    ),

    "xu-2026-burn-sepsis-trajectories": (
        "Xu 2026 — Burn sepsis biomarker trajectories",
        "Frontiers in Cellular and Infection Microbiology",
        2026,
        "10.3389/fcimb.2026.1710916",
        """Growth-mixture modeling of longitudinal biomarker trajectories in burn sepsis
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
""", ["#paper", "#trajectories", "#growth-mixture-modeling"],
    ),

    "tejada-2026-INR-platelets-sepsis": (
        "Tejada 2026 — INR vs platelet count for sepsis mortality",
        "Biomedicines",
        2026,
        "10.3390/biomedicines14040839",
        """6433 sepsis patients (2006–2022). INR at diagnosis independently predicted in-hospital
mortality (OR 2.18). Platelet count alone did not improve the model. Combined
INR > 3.0 + platelets < 50 × 10⁹/L identified a 50%-mortality subgroup.

## Why it sits in this vault
- Sets the bar for the [[experiments/hyp-imaging-flow-cytometry-platelets|imaging
  flow cytometry of platelets]] hypothesis: classical platelet *count* alone
  doesn't add value over INR. We have to show that platelet *morphology /
  activation state* does.
- Reporting style is exemplary — AUROC + OR + CI + threshold-based subgroup.

## Connections
- [[concepts/platelet-aggregation-activation]] — the cellular axis we're claiming
  the count misses.
- [[paper-notes/zhu-2026-RPR-sepsis-coagulopathy]] — adjacent CBC-ratio-based work.
""", ["#paper", "#platelets", "#sepsis-mortality", "#INR"],
    ),

    "cao-2026-HBP-PCT-CRP-SAA-pneumonia": (
        "Cao 2026 — HBP + PCT + CRP + SAA in early pneumonia",
        "Virology Journal",
        2026,
        "10.1186/s12985-026-03078-5",
        """Evaluates heparin-binding protein (HBP) as standalone and in combination panels
(with PCT, CRP, SAA) for distinguishing early bacterial vs viral pneumonia, and for
predicting progression to severe disease.

## Why it's in the bibliography
- *Panels beat single biomarkers* — direct evidence supporting the
  [[experiments/hyp-cbc-vitals-antibiotic-response|active hypothesis]]'s
  multi-feature framing.
- Critique from the Domain-expert: panels of *protein* biomarkers may outperform
  panels of *cellular* features. The CBC-only framing is locally optimal,
  globally vulnerable.

## Connections
- [[concepts/procalcitonin]] — one of the panel members.
- [[concepts/host-response-paradigm]] — panel approach embodies the paradigm.
- [[paper-notes/kothari-2026-host-response-biomarkers]] — the paradigm manifesto.
""", ["#paper", "#biomarker-panel", "#pneumonia"],
    ),

    "van-veen-2026-EOS-stewardship": (
        "van Veen 2026 — Antibiotic stewardship implementation in EOS",
        "JBI Evidence Implementation",
        2026,
        "10.1097/XEB.0000000000000556",
        """Identifies facilitators and barriers when implementing antibiotic-stewardship
interventions for early-onset sepsis in neonates. Notes that despite evidence
supporting various stewardship interventions, real-world implementation remains
limited.

## Why it's in the bibliography
- The bottleneck isn't the *signal* — it's the *systems integration* into clinical
  workflow. A perfect [[experiments/hyp-cbc-vitals-antibiotic-response|CBC + vitals
  trajectory model]] without an EHR-integrated decision-support tool is a poster,
  not a deployable thing.

## Connections
- [[concepts/antibiotic-stewardship]]
- [[paper-notes/devaguru-2026-neonatal-sepsis-diagnostics]]
""", ["#paper", "#stewardship", "#implementation"],
    ),

    "devaguru-2026-neonatal-sepsis-diagnostics": (
        "Devaguru 2026 — Rapid diagnostics in neonatal sepsis",
        "Journal of Pharmacy and Bioallied Sciences",
        2026,
        "10.4103/jpbs.jpbs_34_25",
        """Reviews rapid diagnostic platforms in neonatal sepsis (PCR, microfluidics, PCT).
Identifies slow pathogen detection as the limiting factor and benchmarks emerging
platforms on accuracy, turnaround, and impact on stewardship.

## Why it's in the bibliography
- Anchors the *time-to-decision* framing that the
  [[experiments/hyp-cbc-vitals-antibiotic-response|active hypothesis]] addresses
  by moving the decision-support inputs upstream (vitals + CBC, available at
  admission) rather than downstream (cultures, available 24–48 h later).

## Connections
- [[concepts/procalcitonin]] — one of the platforms surveyed.
- [[concepts/antibiotic-stewardship]] — the downstream goal.
""", ["#paper", "#neonatal-sepsis", "#diagnostics-review"],
    ),

    "zhu-2026-RPR-sepsis-coagulopathy": (
        "Zhu 2026 — RDW-to-platelet ratio in sepsis coagulopathy",
        "BMC Infectious Diseases",
        2026,
        "10.1186/s12879-026-13374-8",
        """Red cell distribution width-to-platelet ratio (RPR) is associated with adverse
outcomes in critically ill patients with sepsis-induced coagulopathy in MIMIC-IV.

## Why it's noted
- *CBC-derived ratios* are a parallel research thread to the
  [[experiments/hyp-cbc-vitals-antibiotic-response|active hypothesis]]. Worth
  having NLR, PLR, RPR computed for the cohort as control features.

## Connections
- [[paper-notes/tejada-2026-INR-platelets-sepsis]]
- [[concepts/platelet-aggregation-activation]]
""", ["#paper", "#CBC-ratios", "#MIMIC-IV"],
    ),
}

for slug, (title, journal, year, doi, body, tags) in PAPER_NOTES.items():
    w(f"paper-notes/{slug}.md",
      body,
      frontmatter={"title": title, "journal": journal, "year": year,
                   "doi": doi, "tags": tags, "type": "paper-note"})


# ---- experiments / hypotheses ----
w("experiments/hyp-cbc-vitals-antibiotic-response.md", """# Hypothesis — CBC + vital-sign trajectories as antibiotic-response indicators

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
  IG% for same severity. Stratify by age band ($<65$ / $\\geq 65$y).
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
""", frontmatter={"tags": ["#hypothesis", "#active", "#CBC", "#sepsis", "#antibiotic-response"],
                  "type": "experiment", "status": "active"})

w("experiments/hyp-imaging-flow-cytometry-platelets.md", """# Hypothesis — Label-free imaging flow cytometry catches platelet activation before CBC

**Status**: Adjacent track, instrument-side. Pilot underway.

**Claim**. Label-free imaging flow cytometry of platelet *morphology and
activation state* detects sepsis-induced platelet activation hours before
classical CBC platelet *count* drops below a clinically actionable threshold.

## Why this matters

- Tejada 2026 ([[paper-notes/tejada-2026-INR-platelets-sepsis]]) shows that
  classical platelet *count* alone does not improve the INR-based mortality model.
- We hypothesise that platelet *morphology* (activation state via shape +
  pseudopod presence) moves earlier and harder.
- See [[concepts/platelet-aggregation-activation]] for the biology.

## Instrument context

- [[concepts/label-free-imaging-flow-cytometry|TUMCREATE imaging flow cytometer
  prototype #4]] — 3000 cells/s, 5–10 min turnaround.
- See [[data-notes/TUMCREATE-imaging-flow-pilot]] for the pilot logistics.

## Status

- Pilot recruitment underway at NUH (n = 12 of target 60).
- Adjacent to but distinct from
  [[experiments/hyp-cbc-vitals-antibiotic-response|the active CBC + vitals
  hypothesis]] — both share the [[concepts/host-response-paradigm|host-response
  paradigm]] framing.
""", frontmatter={"tags": ["#hypothesis", "#adjacent", "#imaging-flow", "#platelets"],
                  "type": "experiment", "status": "pilot"})

w("experiments/hyp-viral-vs-bacterial-classification.md", """# Hypothesis — CBC + vital-sign signature discriminates viral from bacterial at admission

**Status**: Backlog. Likely re-emerges after the
[[experiments/hyp-cbc-vitals-antibiotic-response|active hypothesis]] settles.

**Claim**. A pre-specified combination of admission CBC indices (NEUT%, LYMPH%,
EOS%, NLR) and vital-sign trajectories discriminates *bacterial* vs *viral*
infection at admission with AUROC > 0.85, before any biomarker panel result returns.

## Why backlog

The [[experiments/hyp-cbc-vitals-antibiotic-response|active hypothesis]] already
absorbs the bandwidth for prospective registration. This one waits.

## Anchor citations

- [[paper-notes/cao-2026-HBP-PCT-CRP-SAA-pneumonia]] — biomarker panels do this
  job; the question is whether CBC-only is sufficient.
- [[paper-notes/tertess-2026-lymphopenia-bacterial]] — lymphocyte trajectory
  differs between bacterial and viral.

## Connections

- [[concepts/host-response-paradigm]]
- [[concepts/procalcitonin]]
""", frontmatter={"tags": ["#hypothesis", "#backlog", "#discrimination"],
                  "type": "experiment", "status": "backlog"})


# ---- data-notes ----
w("data-notes/cohort-100-CBC-vitals.md", """# Demo cohort — 100 patients, CBC + vitals, 0–72 h

**File**: `projects/agentic-ai-workshop/data/cohort_cbc_vitals.csv`
**Analysis**: `projects/agentic-ai-workshop/data/analyze_cohort.py`
**Linked hypothesis**: [[experiments/hyp-cbc-vitals-antibiotic-response]]

## Shape

- 100 patients
- 36 columns (5 demographics + 7 features × 4 timepoints + outcome)
- Outcome distribution: improver 68, slow_responder 18, non_responder 9, died 5

## What the analysis showed

- IG% at admission rises *monotonically* across outcome strata (3.9 / 4.9 / 6.4 / 9.6).
- IG% gap *widens* by 48 h (1.4 / 3.2 / 6.0 / 11.8) — the bone-marrow stress
  response persists in non-responders.
- EOS% recovery slope is the discriminating feature for improvers vs
  non-responders, *not* admission EOS% (which is universally low).
- Temperature normalisation is attenuated in the $\\geq 65$y subgroup, echoing
  [[paper-notes/grudzinska-2020-neutrophils-CAP|Grudzinska 2020]].

## Caveats — read before citing

- *Synthetic cohort.* Trajectories were generated with outcome-conditioned slopes,
  so the analysis recovers exactly what was put in. This is for the workshop demo
  — not evidence.
- See the manuscript [[drafts/manuscript-cbc-antibiotic-response|discussion
  section]] for the full limitations passage.

## Connections

- [[concepts/immature-granulocytes]]
- [[concepts/eosinopenia-of-stress]]
- [[concepts/neutrophil-left-shift]]
- [[concepts/sepsis-3-criteria]] — endpoint framing.
""", frontmatter={"tags": ["#data", "#cohort", "#cbc", "#vitals"], "type": "data-note"})

w("data-notes/MIMIC-IV-access-notes.md", """# MIMIC-IV access notes

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
""", frontmatter={"tags": ["#data", "#MIMIC-IV", "#access-notes"], "type": "data-note"})

w("data-notes/TUMCREATE-imaging-flow-pilot.md", """# TUMCREATE imaging flow cytometry pilot — logistics

For [[experiments/hyp-imaging-flow-cytometry-platelets|the platelet imaging
hypothesis]]. Pilot underway at NUH.

## Recruitment

- Target n = 60; current n = 12.
- Inclusion: adult inpatients with confirmed bacterial infection, within 24 h of
  empiric antibiotic start.
- Exclusion: known platelet disorder, recent antiplatelet therapy.

## Sample logistics

- 50 µL heparinised whole blood per timepoint.
- Timepoints: T0 (enrolment), T24 h, T48 h.
- Sample → instrument turnaround: < 1 h.

## Open issues

- Instrument runs 3 days/week — sample stability matters. Currently 4 °C, < 6 h
  to processing.
- Bridge to classical CBC for *count* comparison — Sysmex XN-9100 reference run
  in parallel.

## Connections

- [[concepts/label-free-imaging-flow-cytometry]]
- [[concepts/platelet-aggregation-activation]]
- [[experiments/hyp-imaging-flow-cytometry-platelets]]
- [[identity/lab-context]]
""", frontmatter={"tags": ["#data", "#imaging-flow", "#pilot", "#NUH"], "type": "data-note"})


# ---- drafts ----
w("drafts/manuscript-cbc-antibiotic-response.md", """# Manuscript — CBC + vital-sign trajectories as antibiotic-response indicators

**Status**: Draft in progress.

**Linked hypothesis**: [[experiments/hyp-cbc-vitals-antibiotic-response]]
**Linked dataset**: [[data-notes/cohort-100-CBC-vitals]]
**Dashboard path**: `projects/agentic-ai-workshop/manuscripts/cbc-vitals-antibiotic-response/`

## Section status

| Section | Status | Word count (approx) |
|---|---|---|
| Abstract | Draft v1 | 280 |
| Introduction | Draft v1 | 330 |
| Methods | Draft v1 | 290 |
| Results | Draft v1 | 380 |
| Discussion | Draft v1 | 410 |
| References | Auto-resolved from `linked_paper_ids` | — |

## Open threads for the next pass

- *Figure*: the [[concepts/neutrophil-left-shift|bone-marrow stress response]]
  schematic should live in Results, between P1 (IG% at admission) and P2 (EOS%
  recovery). Generated via viz-nano-banana — see
  `projects/agentic-ai-workshop/figures/`.
- *Methods*: add a paragraph on informative missingness (CBC-draw frequency is a
  function of acuity) — Biostatistician's flag from
  [[experiments/hyp-cbc-vitals-antibiotic-response|the council critique]].
- *Discussion*: tighten the prospective-design recommendation —
  [[paper-notes/hernandez-2025-sepsis-ML-living-review]] is the right citation
  for two-stage design.

## Acceptance criteria for v2

- [ ] All references resolve in the dashboard's citation gate.
- [ ] All figure links resolve via `linked_figure_ids`.
- [ ] Limitations section calls out synthetic cohort explicitly.
- [ ] Word count: 1500–2200 main text.
""", frontmatter={"tags": ["#draft", "#manuscript", "#in-progress"], "type": "draft"})

w("drafts/blog-acute-diagnostics-paradigm.md", """# Blog draft — "The acute diagnostics paradigm is shifting"

**Status**: Outline only. Not yet drafted.

**Target outlet**: Substack (keremdelikoyun.substack.com)

## Premise

For a non-clinician audience: the diagnostic question has shifted from *what
bug is this?* to *how is the patient responding?* — the
[[concepts/host-response-paradigm|host-response paradigm]]. Make the case using
two concrete examples:

1. CBC + vital-sign trajectories
   ([[experiments/hyp-cbc-vitals-antibiotic-response|active hypothesis]]) — the
   "every-hospital-already-has-this" version.
2. Label-free imaging flow cytometry
   ([[experiments/hyp-imaging-flow-cytometry-platelets|TUMCREATE pilot]]) — the
   "instrument-side" version.

## Outline

- Hook: the 2 a.m. ICU question
- Setup: why pathogen detection alone isn't enough
- Two stories: CBC + vitals → real-time response; imaging flow → platelet
  activation before count drops
- The paradigm name: [[concepts/host-response-paradigm|host response]]
- What this means for AI for diagnostics: the model is reading the *patient*,
  not the *culture*

## Tone

Same voice as the [[identity/profile-kerem|profile]]: terse, opinionated,
American spelling, no em dashes.
""", frontmatter={"tags": ["#draft", "#blog", "#outline"], "type": "draft"})


# ---- daily notes ----
w("daily/2026-05-12.md", """# Daily — 2026-05-12

## Session summary
Council fan-out on the [[experiments/hyp-cbc-vitals-antibiotic-response|CBC + vitals
hypothesis]]. Four personas active for the first time (Biostatistician switched
on). Skeptic and Methodologist agree the framing needs reworking from
"antibiotic efficacy" to "host-response trajectory" — see the synthesis in the
hypothesis note.

## Read
- [[paper-notes/grudzinska-2020-neutrophils-CAP]] — for the age-attenuation leg.
- [[paper-notes/khanghah-2025-vital-signs-mrsa]] — confirms vital-signs-alone signal.

## Open threads
- Domain-expert wants IG% *slope*, not absolute value, as primary feature.
- Biostatistician wants pre-registered analysis plan before unblinding outcome.

## Tomorrow
- Re-read Xu 2026 for growth-mixture modeling specifics.
""", frontmatter={"tags": ["#daily"], "type": "daily"})

w("daily/2026-05-14.md", """# Daily — 2026-05-14

## Session summary
Biostatistician revision after reading [[paper-notes/xu-2026-burn-sepsis-trajectories|Xu
2026]] end-to-end. Updated synthesis on the
[[experiments/hyp-cbc-vitals-antibiotic-response|active hypothesis]] to use
growth-mixture modeling as the primary statistical machinery, not flat logistic.

## Decisions
- Two-stage design (MIMIC-IV retrospective → TUMCREATE prospective) is the path.
- Endpoint locked: 48-h [[concepts/sepsis-3-criteria|SOFA delta]] + 30-d mortality
  composite.

## Open threads
- MIMIC-IV access lead time — see [[data-notes/MIMIC-IV-access-notes]].
- IG% availability in MIMIC-IV unknown — verify before designing on it.
""", frontmatter={"tags": ["#daily"], "type": "daily"})

w("daily/2026-05-16.md", """# Daily — 2026-05-16

## Session summary
Workshop-prep day. Rebuilt the [[identity/profile-kerem|researcher profile]] note
and started staging the demo notes for the workshop vault.

## Read
- [[paper-notes/kothari-2026-host-response-biomarkers]] — the paradigm manifesto
  — opens the workshop framing.

## Open threads
- Demo vault structure: ~30 notes across identity, paper-notes, concepts,
  experiments, data-notes, drafts, daily, inbox. Decided on 8 colour groups in
  the graph view.
""", frontmatter={"tags": ["#daily"], "type": "daily"})

w("daily/2026-05-19.md", """# Daily — 2026-05-19

## Session summary
Built the *Agentic AI Workshop* demo end-to-end: 20-paper library, full
[[experiments/hyp-cbc-vitals-antibiotic-response|hypothesis with 4-persona
council critique]], 100-patient cohort, manuscript draft with 6 sections, runs
history, this Obsidian vault.

## Decisions
- Vault lives at `projects/briefs/agentic-ai-workshop/obsidian-vault/` (portable
  with the workshop folder).
- Dashboard project lives at `projects/agentic-ai-workshop/` (auto-discovered
  by the dashboard's `listProjects()`).
- See `PORTABILITY.md` for the second-laptop rsync recipe.

## Open threads
- Nano-banana figure for the bone-marrow stress response — generating now.
- Verify graph view colour grouping in Obsidian once vault opens.
""", frontmatter={"tags": ["#daily", "#workshop-prep"], "type": "daily"})


# ---- inbox ----
w("inbox/idea-mass-spec-CBC-fusion.md", """# Idea — mass-spec / CBC fusion for early sepsis

What if we fuse CBC differential trajectories with point-of-care mass-spec markers
(e.g. presepsin) at the same timepoints? The
[[experiments/hyp-cbc-vitals-antibiotic-response|active hypothesis]] uses CBC
alone; the [[paper-notes/kothari-2026-host-response-biomarkers|Kothari manifesto]]
argues panels win.

**Next step**: literature search "presepsin trajectories sepsis 48h" — does
anyone serially measure?
""", frontmatter={"tags": ["#inbox", "#idea"], "type": "inbox"})

w("inbox/idea-pediatric-sub-cohort.md", """# Idea — pediatric sub-cohort

The TUMCREATE imaging flow pilot can recruit at KK Women's & Children's. Pediatric
sepsis has its own CBC dynamics (different reference ranges, different EOS%
baselines).

**Open question**: should the
[[experiments/hyp-cbc-vitals-antibiotic-response|main hypothesis]] include a
pediatric arm, or is that a separate study? Lean toward separate — different
endpoint thresholds, different IRB pathway.
""", frontmatter={"tags": ["#inbox", "#idea"], "type": "inbox"})

w("inbox/question-eos-recovery-mechanism.md", """# Question — what controls EOS recovery rate?

For [[concepts/eosinopenia-of-stress|eosinopenia of stress]], the
*sequestration* mechanism is documented. But the *recovery* (EOS% climbing back
toward 1–2% in improvers) — what governs the rate?

Candidates:
- Cortisol normalisation timing
- IL-5 reactivation
- Direct lymph-node release

**Lit-search task**: "eosinophil recovery kinetics sepsis" — adjacent to but
distinct from the eosinopenia-mechanism literature.
""", frontmatter={"tags": ["#inbox", "#question"], "type": "inbox"})

w("inbox/meeting-2026-05-13-collaborator-call.md", """# Meeting — 2026-05-13 — Collaborator call (NUH)

Clinical PI raised two concerns about the
[[experiments/hyp-cbc-vitals-antibiotic-response|active hypothesis]]:
1. *Steroid-treated patients* dominate the eosinophil signal. Either exclude or
   stratify — agreed: stratify, with a sensitivity analysis excluding them.
2. *Antibiotic-de-escalation timing* — wants the model to predict the 48-h
   re-evaluation, not just the final outcome. Agreed; this becomes the secondary
   endpoint.

**Action items**:
- Add steroid-use as covariate in the analysis plan (Methodologist concur).
- Add 48-h SOFA delta as primary endpoint (already in
  [[experiments/hyp-cbc-vitals-antibiotic-response|the council synthesis]]).

**Next call**: 2026-05-27.
""", frontmatter={"tags": ["#inbox", "#meeting", "#NUH"], "type": "inbox"})

w("inbox/brainstorm-workshop-followups.md", """# Brainstorm — workshop follow-ups

After the [[daily/2026-05-19|workshop demo build]], a few non-research threads
to pick up:

- *Week 2 of the workshop*: build-your-first-skill. Use this vault as the example
  for the [[concepts/obsidian-sync-gate|Obsidian sync gate]] integration.
- *Researcher outreach*: NTU / A*STAR / NUS targets in
  [[identity/research-interests|adjacent interests]]; coordinated through the
  positioning plan (separate project).
- *Open-source*: the workshop demo vault is a reasonable show-and-tell for the
  Organon README. Confirm with the user before linking out.
""", frontmatter={"tags": ["#inbox", "#brainstorm"], "type": "inbox"})


print(f"Vault built at {VAULT}")
print("Counts:")
print("  identity:    ", len(list((VAULT / "identity").glob("*.md"))))
print("  concepts:    ", len(list((VAULT / "concepts").glob("*.md"))))
print("  paper-notes: ", len(list((VAULT / "paper-notes").glob("*.md"))))
print("  experiments: ", len(list((VAULT / "experiments").glob("*.md"))))
print("  data-notes:  ", len(list((VAULT / "data-notes").glob("*.md"))))
print("  drafts:      ", len(list((VAULT / "drafts").glob("*.md"))))
print("  daily:       ", len(list((VAULT / "daily").glob("*.md"))))
print("  inbox:       ", len(list((VAULT / "inbox").glob("*.md"))))
