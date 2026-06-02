#!/usr/bin/env bash
# Week 2 — local setup. Extends the Week 1 base env with patterns + RAG deps.
# Run from week-02-patterns/. Creates .venv, installs pinned wheels, prints status.

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PY="${PYTHON:-python3}"
VENV=".venv"

echo "==> Week 2 setup"

# 1. Python version check
if ! command -v "$PY" >/dev/null 2>&1; then
  echo "[ERROR] $PY not found. Install Python 3.10+ first." >&2
  exit 1
fi
PY_VER=$("$PY" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "    Python: $PY_VER"
case "$PY_VER" in
  3.10|3.11|3.12) ;;
  *) echo "[WARN] Tested on 3.10-3.12; got $PY_VER. Proceeding anyway." >&2 ;;
esac

# 2. Virtualenv
if [ ! -d "$VENV" ]; then
  echo "    Creating venv at $VENV"
  "$PY" -m venv "$VENV"
fi
# shellcheck disable=SC1091
. "$VENV/bin/activate"
python -m pip install --quiet --upgrade pip wheel

# 3. Install deps (pinned for stability across the workshop)
echo "    Installing dependencies (this takes ~2 min on first run)"
pip install --quiet \
  "anthropic>=0.39.0,<0.50.0" \
  "openai>=1.50.0,<2.0.0" \
  "langchain==0.3.7" \
  "langchain-anthropic==0.2.4" \
  "langchain-openai==0.2.8" \
  "langchain-community==0.3.5" \
  "langchain-text-splitters==0.3.2" \
  "langchain-huggingface==0.1.2" \
  "langchain-chroma==0.1.4" \
  "faiss-cpu==1.9.0" \
  "chromadb==0.5.23" \
  "rank-bm25==0.2.2" \
  "sentence-transformers==3.3.0" \
  "pypdf==5.1.0" \
  "duckduckgo-search==6.3.5" \
  "pandas==2.2.3" \
  "matplotlib==3.9.2" \
  "tabulate==0.9.0" \
  "python-dotenv==1.0.1" \
  "jupyterlab==4.3.1" \
  "ipykernel==6.29.5"

# 4. Optional: elasticsearch client for Notebook 04
if [ "${INSTALL_ELASTIC:-1}" = "1" ]; then
  pip install --quiet "elasticsearch==8.15.1"
  echo "    [optional] elasticsearch client installed (Notebook 04)"
fi

# 5. Register kernel so JupyterLab picks it up
python -m ipykernel install --user --name=agentic-w2 --display-name="Agentic W2" >/dev/null

# 6. .env scaffold
if [ ! -f .env ]; then
  cp .env.example .env
  echo "    Created .env from .env.example. Fill in ANTHROPIC_API_KEY at minimum."
fi

echo ""
echo "==> Done."
echo "    Activate:  source $VENV/bin/activate"
echo "    Launch:    jupyter lab notebooks/"
echo "    First run will download ~7 MB of papers into sample_articles/."
