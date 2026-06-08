#!/usr/bin/env bash
# Week 3 local setup — installs the LangGraph 1.x stack into the current environment.
# Colab users do NOT need this: each notebook's first cell installs what it needs.
# Usage: bash setup.sh   (ideally inside a fresh venv / conda env, Python 3.10+)
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "[week-03] installing the LangGraph 1.x stack..."
python3 -m pip install -q --upgrade pip

# Core graph + Gemini provider (LangChain / LangGraph 1.0 GA line).
python3 -m pip install -q \
  "langgraph>=1.2.4" \
  "langgraph-checkpoint-sqlite>=3.1.0" \
  "langchain>=1.3.2" \
  "langchain-core>=1.4.0" \
  "langchain-google-genai>=4.2.4" \
  "langchain-community>=0.4" \
  "langchain-text-splitters>=0.3" \
  "beautifulsoup4" \
  "tavily-python>=0.7" \
  "python-dotenv"

echo "[week-03] done."
echo "[week-03] next: cp .env.example .env  and add your GOOGLE_API_KEY (free: https://aistudio.google.com/apikey)"
