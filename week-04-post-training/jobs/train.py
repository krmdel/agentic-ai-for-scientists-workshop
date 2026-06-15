#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "fire>=0.7.1",
#   "unsloth",
#   "transformers",
#   "datasets",
#   "trl<0.24",
#   "peft",
#   "bitsandbytes",
#   "huggingface_hub",
# ]
# ///
"""
train.py, the REAL training run, on Hugging Face Jobs.

Same model + dataset + hyperparameters as the Week 4 Colab notebooks (01/02/03), but
runs headless on HF's managed GPUs and pushes a finished model to the Hub. This is the
"do it for real" path: no tiny max_steps, no Colab session limit. The Hub model it
produces is the shared artifact Week 5 (evaluation) and Week 6 (deployment) consume.

One script, three methods, pick with --method:
    full   : full supervised fine-tuning (100% of weights)
    lora   : LoRA adapters on a full-precision base
    qlora  : LoRA adapters on a 4-bit NF4 base (lowest VRAM)

Run on HF Jobs (needs a Pro / Team / Enterprise account):

    hf jobs uv run --flavor a10g-small --timeout 2h \\
        -s HF_TOKEN=hf_xxx \\
        train.py -- \\
        --method qlora \\
        --dataset_name YOUR_USERNAME/medquad-structured \\
        --hub_model_id YOUR_USERNAME/qwen3-medquad-qlora

The dataset is the one you push from Notebook 00 (`dd.push_to_hub(...)`). Each row has a
`messages` field (system/user/assistant). If the dataset has no `messages` column, the
script falls back to formatting raw `lavita/MedQuAD` question/answer pairs so it still runs.
"""
import os
import sys
import logging as log

# Unsloth must be imported before transformers so its kernels patch correctly.
from unsloth import FastLanguageModel
import torch
import fire
from datasets import load_dataset, Dataset
from trl import SFTTrainer, SFTConfig

log.basicConfig(level=log.INFO, stream=sys.stdout,
                format="%(asctime)s - %(levelname)s - %(message)s")

SYSTEM_PROMPT = (
    "You are a clinical assistant. Read the medical question and respond with a JSON object "
    "containing: disease, patient_info, symptoms (list), treatment (list), answer_summary."
)
LORA_TARGETS = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]


def _load_split(dataset_name, split, tokenizer):
    """Return a Dataset with a 'text' column ready for SFT, from either our structured
    dataset (has 'messages') or raw lavita/MedQuAD (question/answer)."""
    try:
        ds = load_dataset(dataset_name, split=split)
    except Exception:
        # raw MedQuAD has only a 'train' split; carve validation off the tail.
        full = load_dataset("lavita/MedQuAD", split="train").filter(lambda r: r.get("answer"))
        full = full.shuffle(seed=3407)
        cut = int(0.9 * len(full))
        ds = full.select(range(cut)) if split == "train" else full.select(range(cut, min(cut + 500, len(full))))

    cols = ds.column_names
    if "messages" in cols:
        def to_text(r):
            return {"text": tokenizer.apply_chat_template(
                r["messages"], tokenize=False, add_generation_prompt=False)}
    else:  # raw question/answer fallback
        def to_text(r):
            q = r.get("question") or r.get("Question") or ""
            a = (r.get("answer") or r.get("Answer") or "")[:800]
            msgs = [{"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": q},
                    {"role": "assistant", "content": a}]
            return {"text": tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=False)}
    return ds.map(to_text)


def main(
    method: str = "qlora",                      # full | lora | qlora
    model_name: str = "Qwen/Qwen3-0.6B",
    dataset_name: str = "lavita/MedQuAD",       # override with YOUR_USERNAME/medquad-structured
    hub_model_id: str = "qwen3-medquad",        # where the finished model is pushed
    max_seq_length: int = 1024,
    batch_size: int = 4,
    gradient_accumulation_steps: int = 4,
    num_train_epochs: int = 1,
    max_steps: int = -1,                         # -1 = full epoch(s); set e.g. 500 for a shorter run
    lora_r: int = 32,
    lora_alpha: int = 16,
    learning_rate: float = None,                 # default: 2e-5 full, 2e-4 lora/qlora
) -> None:
    method = method.lower()
    assert method in {"full", "lora", "qlora"}, "method must be full | lora | qlora"
    if learning_rate is None:
        learning_rate = 2e-5 if method == "full" else 2e-4

    log.info(f"=== TRAINING ({method.upper()}), {model_name} on {dataset_name} ===")

    # --- model -----------------------------------------------------------------
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=model_name,
        max_seq_length=max_seq_length,
        dtype=None,                              # bf16 on Ampere+ (A10G/A100), fp16 on T4
        load_in_4bit=(method == "qlora"),        # 4-bit NF4 base only for QLoRA
        full_finetuning=(method == "full"),
    )
    if method in {"lora", "qlora"}:
        model = FastLanguageModel.get_peft_model(
            model, r=lora_r, lora_alpha=lora_alpha, lora_dropout=0.0,
            target_modules=LORA_TARGETS, bias="none",
            use_gradient_checkpointing="unsloth", random_state=3407,
        )
    n_total = sum(p.numel() for p in model.parameters())
    n_train = sum(p.numel() for p in model.parameters() if p.requires_grad)
    log.info(f"Trainable: {n_train/1e6:.2f}M / {n_total/1e6:.1f}M ({100*n_train/n_total:.2f}%)")

    # --- data ------------------------------------------------------------------
    train_ds = _load_split(dataset_name, "train", tokenizer)
    try:
        eval_ds = _load_split(dataset_name, "validation", tokenizer)
    except Exception:
        eval_ds = None
    log.info(f"train={len(train_ds)}" + (f" eval={len(eval_ds)}" if eval_ds else " (no eval split)"))

    # --- train -----------------------------------------------------------------
    cfg = SFTConfig(
        output_dir="outputs",
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=gradient_accumulation_steps,
        warmup_steps=20,
        num_train_epochs=num_train_epochs,
        max_steps=max_steps,
        learning_rate=learning_rate,
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        optim="adamw_8bit",
        weight_decay=0.01,
        logging_steps=10,
        eval_strategy="steps" if eval_ds else "no",
        eval_steps=100,
        save_strategy="no",
        seed=3407,
        report_to="none",
        max_seq_length=max_seq_length,
        dataset_text_field="text",
    )
    trainer = SFTTrainer(model=model, tokenizer=tokenizer,
                         train_dataset=train_ds, eval_dataset=eval_ds, args=cfg)

    torch.cuda.reset_peak_memory_stats()
    stats = trainer.train()
    peak = torch.cuda.max_memory_allocated() / 1024**3
    log.info(f"Done. loss={stats.training_loss:.4f}  peak_vram={peak:.2f}GB  steps={stats.global_step}")

    # --- push ------------------------------------------------------------------
    log.info(f"Pushing to the Hub: {hub_model_id}")
    if method == "qlora":
        # merge 4-bit base + adapters into a standalone fp16 model for easy deployment
        model.push_to_hub_merged(hub_model_id, tokenizer, save_method="merged_16bit")
    else:
        tokenizer.push_to_hub(hub_model_id)
        model.push_to_hub(hub_model_id)          # full = whole model; lora = adapters only
    log.info("Push complete. Load it anywhere with FastLanguageModel / AutoModelForCausalLM.")


if __name__ == "__main__":
    fire.Fire(main)
