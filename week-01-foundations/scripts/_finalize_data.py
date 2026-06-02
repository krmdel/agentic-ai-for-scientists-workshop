#!/usr/bin/env python3
"""Convert the cohort CSV into a DataframeArtifact preview JSON
so the dashboard's Data workspace picks it up.
"""
from __future__ import annotations
import csv
import json
import os
from pathlib import Path
from statistics import mean, stdev

SCRIPT_DIR = Path(__file__).resolve().parent
# Support two layouts: workshop repo (week-01-foundations/dashboard-project/data/)
# and Organon-side symlink (projects/briefs/agentic-ai-workshop/data/).
_candidates = [
    SCRIPT_DIR.parent / "dashboard-project",  # workshop repo
    SCRIPT_DIR.parent,                         # script lives at project root
]
PROJ = next((p for p in _candidates if (p / "data" / "cohort_cbc_vitals.csv").exists()), _candidates[0])
CSV = PROJ / "data" / "cohort_cbc_vitals.csv"
NOW_ISO = "2026-05-19T03:35:00.000Z"
SLUG = "agentic-ai-workshop"

# 1. Parse rows
rows = []
with CSV.open() as f:
    reader = csv.DictReader(f)
    cols = reader.fieldnames or []
    for r in reader:
        rows.append(r)

size_bytes = CSV.stat().st_size

# 2. Build columns with stats
NUMERIC_COLS = {c for c in cols if any(c.startswith(p) for p in
                ("NEUT_pct_", "EOS_pct_", "IG_pct_", "HR_", "Temp_", "RR_", "SpO2_", "age"))}
CATEGORICAL_COLS = {"patient_id", "sex", "infection_site", "antibiotic_regimen", "outcome"}

columns_out = []
for c in cols:
    if c in NUMERIC_COLS:
        vals = [float(r[c]) for r in rows if r[c] not in ("", None)]
        nulls = len(rows) - len(vals)
        stats = {
            "count": len(vals),
            "mean": round(mean(vals), 4),
            "std": round(stdev(vals) if len(vals) > 1 else 0.0, 4),
            "min": round(min(vals), 4),
            "max": round(max(vals), 4),
            "q1": round(sorted(vals)[len(vals)//4], 4),
            "median": round(sorted(vals)[len(vals)//2], 4),
            "q3": round(sorted(vals)[3*len(vals)//4], 4),
        }
        columns_out.append({
            "name": c, "type": "numeric",
            "type_inferred_by": "auto", "null_count": nulls, "stats": stats,
        })
    else:
        vals = [r[c] for r in rows if r[c] not in ("", None)]
        from collections import Counter
        counter = Counter(vals)
        top = counter.most_common(8)
        stats = {
            "count": len(vals),
            "unique_count": len(counter),
            "top": [[str(v), n] for v, n in top],
        }
        columns_out.append({
            "name": c, "type": "categorical",
            "type_inferred_by": "auto", "null_count": 0, "stats": stats,
        })

# 3. Preview rows — first 10
preview = rows[:10]

# 4. Find data id matching the existing dataset descriptor
data_id = None
for f in (PROJ / "data").glob("data-*.json"):
    if f.suffix == ".json" and ".preview" not in f.name:
        data_id = f.stem
        break
if not data_id:
    data_id = "data-20260519-ae5722"

obj = {
    "_artifact": "dataframe",
    "schema_version": 1,
    "id": data_id,
    "project_slug": SLUG,
    "filename": "cohort_cbc_vitals.csv",
    "format": "csv",
    "size_bytes": size_bytes,
    "rows_total": len(rows),
    "columns": columns_out,
    "preview_rows": preview,
    "data_path": f"projects/briefs/{SLUG}/data/cohort_cbc_vitals.csv",
    "preview_path": f"projects/briefs/{SLUG}/data/{data_id}.preview.json",
    "uploaded_at": NOW_ISO,
    "library_path": f"projects/briefs/{SLUG}/data/{data_id}.preview.json",
}

preview_path = PROJ / "data" / f"{data_id}.preview.json"
preview_path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")
print(f"wrote {preview_path.relative_to(PROJ.parent.parent.parent)}")
print(f"  rows={len(rows)} cols={len(columns_out)} size={size_bytes} bytes")
