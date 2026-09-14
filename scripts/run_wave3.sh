#!/usr/bin/env bash
# Run wave3 gpt-6-astra labeling. Does not touch wave1/wave2, the 2500 run, Gold150, V4, v6a.
set -euo pipefail
PAPER="/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper"
WAVE="$PAPER/data/silver_plus_10k_prep_20260913/codex_remaining_5436/waves/wave3"
LOCK="$WAVE/wave3.lock"
LOG="$WAVE/wave3_api.log"
mkdir -p "$WAVE/batches_out"
exec 9>"$LOCK"
if ! flock -n 9; then
  echo "[wave3] waiting for $LOCK $(date -Is)" | tee -a "$LOG"
  flock 9
fi
if [[ -f "$WAVE/progress.json" ]] && python3 -c "import json,sys; p=json.load(open('$WAVE/progress.json')); sys.exit(0 if p.get('n_labeled')==1816 and p.get('n_failed_batches',1)==0 else 1)"; then
  echo "[wave3] already complete $(date -Is)" | tee -a "$LOG"
  exit 0
fi
cd "$PAPER/scripts"
echo "[wave3] start $(date -Is)" | tee -a "$LOG"
python3 run_codex_wave_api.py --wave-dir "$WAVE" --retries 3 --sleep 0.4 --timeout 240 \
  2>&1 | tee -a "$LOG"
echo "[wave3] exit=${PIPESTATUS[0]} $(date -Is)" | tee -a "$LOG"
