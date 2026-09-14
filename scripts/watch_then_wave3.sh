#!/usr/bin/env bash
# After the 2500 student COMPARE exists, label Codex wave3 on gpt-6-astra.
# Does not start while the 2500 API is still running. Does not touch wave1/wave2.
set -euo pipefail
PAPER="/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper"
COMPARE="$PAPER/output/silver_public_2500_student_20260913/COMPARE_v6a.json"
WAVE="$PAPER/data/silver_plus_10k_prep_20260913/codex_remaining_5436/waves/wave3"
LOG="$WAVE/watch_then_wave3.log"
MAX_HOURS="${MAX_HOURS:-14}"
mkdir -p "$WAVE"
echo "[watch-w3] start $(date -Is)" | tee -a "$LOG"
deadline=$((SECONDS + MAX_HOURS * 3600))
while (( SECONDS < deadline )); do
  n_out=$(find "$WAVE/batches_out" -name 'batch_*.json' ! -name '*.failed.json' 2>/dev/null | wc -l | tr -d ' ')
  if [[ -f "$WAVE/progress.json" ]]; then
    n_lab=$(python3 -c "import json; print(json.load(open('$WAVE/progress.json')).get('n_labeled',0))")
  else
    n_lab=0
  fi
  echo "[watch-w3] $(date -Is) compare=$([[ -f $COMPARE ]] && echo yes || echo no) n_out=$n_out n_labeled=$n_lab" | tee -a "$LOG"
  if [[ "$n_lab" == "1816" ]]; then
    echo "[watch-w3] wave3 already complete $(date -Is)" | tee -a "$LOG"
    exit 0
  fi
  if [[ -f "$COMPARE" ]]; then
    echo "[watch-w3] student COMPARE present; start wave3 $(date -Is)" | tee -a "$LOG"
    bash "$PAPER/scripts/run_wave3.sh"
    exit $?
  fi
  sleep 60
done
echo "[watch-w3] timeout waiting for COMPARE $(date -Is)" | tee -a "$LOG"
exit 6
