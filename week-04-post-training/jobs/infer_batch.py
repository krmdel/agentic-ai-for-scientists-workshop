#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "fire>=0.7.1",
#   "unsloth",
#   "transformers",
#   "datasets",
#   "huggingface_hub",
# ]
# ///
"""
infer_batch.py, offline batch INFERENCE on Hugging Face Jobs.

Run your fine-tuned model over a whole dataset split on a GPU, headless, and push the
predictions back to the Hub as a dataset. Week 5's evaluation can then score those
predictions without anyone holding a Colab session open. This is the "inference" half of
'training/inference on HF Jobs', for *serving* a live API instead, use HF Inference
Endpoints (point-and-click from your pushed model; see jobs/README.md).

    hf jobs uv run --flavor t4-small --timeout 1h \\
        -s HF_TOKEN=hf_xxx \\
        infer_batch.py -- \\
        --model_id YOUR_USERNAME/qwen3-medquad-qlora \\
        --dataset_name YOUR_USERNAME/medquad-structured --split test \\
        --out_repo YOUR_USERNAME/medquad-predictions
"""
import sys
import logging as log

from unsloth import FastLanguageModel
import fire
from datasets import load_dataset, Dataset

log.basicConfig(level=log.INFO, stream=sys.stdout, format="%(asctime)s - %(levelname)s - %(message)s")

SYSTEM_PROMPT = (
    "You are a clinical assistant. Read the medical question and respond with a JSON object "
    "containing: disease, patient_info, symptoms (list), treatment (list), answer_summary."
)


def main(
    model_id: str = "Qwen/Qwen3-0.6B",
    dataset_name: str = "lavita/MedQuAD",
    split: str = "test",
    out_repo: str = None,                 # optional: push predictions here as a dataset
    max_new_tokens: int = 220,
    limit: int = None,                    # cap rows for a quick run
) -> None:
    log.info(f"=== BATCH INFERENCE, {model_id} on {dataset_name}[{split}] ===")
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=model_id, max_seq_length=1024, dtype=None, load_in_4bit=False)
    FastLanguageModel.for_inference(model)

    try:
        ds = load_dataset(dataset_name, split=split)
    except Exception:
        ds = load_dataset("lavita/MedQuAD", split="train").filter(lambda r: r.get("answer")).select(range(200))
    if limit:
        ds = ds.select(range(min(limit, len(ds))))

    def question_of(row):
        if "messages" in row:
            return next((m["content"] for m in row["messages"] if m["role"] == "user"), "")
        return row.get("question") or row.get("Question") or ""

    preds = []
    for i, row in enumerate(ds):
        q = question_of(row)
        ids = tokenizer.apply_chat_template(
            [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": q}],
            tokenize=True, add_generation_prompt=True, return_tensors="pt").to(model.device)
        out = model.generate(input_ids=ids, max_new_tokens=max_new_tokens, temperature=0.0, do_sample=False)
        text = tokenizer.decode(out[0][ids.shape[1]:], skip_special_tokens=True)
        preds.append({"question": q, "prediction": text})
        if (i + 1) % 25 == 0:
            log.info(f"  {i+1}/{len(ds)}")

    log.info(f"Generated {len(preds)} predictions.")
    if out_repo:
        Dataset.from_list(preds).push_to_hub(out_repo, split=split)
        log.info(f"Pushed predictions -> {out_repo} (split={split}). Score them in Week 5.")
    else:
        for p in preds[:3]:
            log.info(f"Q: {p['question'][:80]} -> {p['prediction'][:120]}")


if __name__ == "__main__":
    fire.Fire(main)
