#!/usr/bin/env bash
# Execute every notebook end-to-end against the local venv, leaving the
# committed .ipynb files output-free. Validation copies land in /tmp.
set -uo pipefail
W2="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$W2"
PY="$W2/.venv/bin/python3.11"
# load the key: prefer the gitignored local file, fall back to the Organon root .env
set -a
source "$W2/.env.local" 2>/dev/null
[ -z "${ANTHROPIC_API_KEY:-}" ] && source /Users/keremdelikoyun/Projects/scientific-os/.env 2>/dev/null
set +a
if [ -z "${ANTHROPIC_API_KEY:-}" ]; then echo "NO KEY: set ANTHROPIC_API_KEY in $W2/.env.local or the root .env"; exit 2; fi
export ANONYMIZED_TELEMETRY=False TOKENIZERS_PARALLELISM=false
mkdir -p /tmp/w2_executed
rc=0
for nb in notebooks/00_langchain_intro notebooks/01_tool_use notebooks/02_react_agent notebooks/03_rag_pipeline; do
  name="$(basename "$nb")"
  echo "===== executing $name ====="
  "$PY" -m jupyter nbconvert --to notebook --execute \
    --ExecutePreprocessor.timeout=600 \
    --output "/tmp/w2_executed/${name}" "$nb.ipynb" 2>"/tmp/w2_executed/${name}.log"
  if [ $? -eq 0 ]; then echo "  OK $name"; else echo "  FAIL $name (see /tmp/w2_executed/${name}.log)"; rc=1; fi
done
echo "DONE rc=$rc"
exit $rc
