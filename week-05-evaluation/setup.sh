#!/usr/bin/env bash
# Week 5 local setup — installs the evaluation stack.
# Colab users do NOT need this: each notebook's first cell installs what it needs.
# Usage: bash setup.sh   (Python 3.10-3.12; a CUDA GPU for the inference notebooks)
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "[week-05] checking for an NVIDIA GPU (NB00/02/03 generate from a local model)..."
if ! command -v nvidia-smi >/dev/null 2>&1; then
  echo "[week-05] WARNING: nvidia-smi not found. The inference notebooks need a CUDA GPU."
  echo "[week-05]          No local GPU? Use Google Colab (free T4) — the intended path."
fi

echo "[week-05] installing the eval stack..."
python3 -m pip install -q --upgrade pip
python3 -m pip install -q unsloth datasets rouge-score
python3 -m pip install -q --no-deps transformers
# NB01 (LLM-as-judge) extras.
python3 -m pip install -q "langchain-google-genai>=2.0" pydantic python-dotenv

echo "[week-05] done."
echo "[week-05] next: cp .env.example .env  and add your GOOGLE_API_KEY (only NB01 needs it)"
echo "[week-05]       then: jupyter lab  and run notebooks/ in order 00 -> 03"
