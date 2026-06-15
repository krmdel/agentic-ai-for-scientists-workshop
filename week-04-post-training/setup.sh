#!/usr/bin/env bash
# Week 4 local setup — installs the fine-tuning stack (Unsloth + TRL + PEFT).
# Colab users do NOT need this: each notebook's first cell installs what it needs,
# and Colab provides the GPU. This is for running locally on an NVIDIA GPU box.
# Usage: bash setup.sh   (Python 3.10-3.12, a CUDA GPU; ideally a fresh venv)
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "[week-04] checking for an NVIDIA GPU..."
if ! command -v nvidia-smi >/dev/null 2>&1; then
  echo "[week-04] WARNING: nvidia-smi not found. Training needs a CUDA GPU."
  echo "[week-04]          No local GPU? Use Google Colab (free T4) — the intended path."
fi

echo "[week-04] installing the fine-tuning stack..."
python3 -m pip install -q --upgrade pip

# Unsloth pulls a matched torch/triton/transformers/trl stack on first install.
python3 -m pip install -q unsloth
python3 -m pip install -q --no-deps "trl<0.24" peft accelerate bitsandbytes datasets

# NB00 (dataset prep) extras — Gemini labeler + structured output.
python3 -m pip install -q "langchain-google-genai>=2.0" pydantic python-dotenv

echo "[week-04] done."
echo "[week-04] next: cp .env.example .env  and add your GOOGLE_API_KEY (free: https://aistudio.google.com/apikey)"
echo "[week-04]       then: jupyter lab  and run notebooks/ in order 00 -> 04"
