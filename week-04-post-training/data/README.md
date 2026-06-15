# Week 4: `data/`

## `medquad_structured.jsonl` (committed: the seed)

A **small offline-labeled sample seed** (~12 rows) in the exact chat format the
training notebooks consume. Each line:

```json
{"messages": [{"role":"system",...},{"role":"user",...},{"role":"assistant","content":"<JSON>"}],
 "focus": "Hashimoto's Disease", "qtype": "symptoms"}
```

The assistant turn is a JSON string with `disease`, `patient_info`, `symptoms[]`,
`treatment[]`, `answer_summary`. The `focus`/`qtype` keys are MedQuAD's weak labels,
kept so **Week 5** can score the model's extracted `disease` against `focus`.

**This is a teaching seed, not a real training set.** It exists so NB01–04 run
end-to-end even before you run NB00's labeler. For a serious fine-tune, run
`00_dataset_prep.ipynb` with your `GOOGLE_API_KEY` to label thousands of MedQuAD
rows and overwrite this file.

## Generated at runtime (gitignored)

- `medquad_train.jsonl` / `medquad_validation.jsonl` / `medquad_test.jsonl`: splits NB00 writes
- `medquad_live_demo.jsonl`: the few rows NB00 labels live
- `run_full_sft.json` / `run_lora.json` / `run_qlora.json`: VRAM/loss each training notebook records, read back by NB03's comparison table
