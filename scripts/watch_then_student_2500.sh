#!/usr/bin/env bash
# Overnight watchdog: if the API chain dies after 2500 labels, still train.
# While the live chain PID is up, do not start a second trainer.
# If labels never reach 2500, exit without training.
set -euo pipefail
PAPER="/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper"
OUT="$PAPER/data/silver_plus_10k_prep_20260913/run2500_public_api_v1"
ROOT="$PAPER/output/silver_public_2500_student_20260913"
LOG="$OUT/watchdog.log"
CHAIN_PID="${1:-}"
MAX_HOURS="${MAX_HOURS:-8}"
mkdir -p "$OUT" "$ROOT"
echo "[watch] start $(date -Is) chain_pid=${CHAIN_PID:-none}" | tee -a "$LOG"
deadline=$((SECONDS + MAX_HOURS * 3600))
n=0
fail=0
while (( SECONDS < deadline )); do
  if [[ -f "$ROOT/COMPARE_v6a.json" ]]; then
    echo "[watch] student already finished $(date -Is)" | tee -a "$LOG"
    exit 0
  fi
  if [[ -f "$OUT/progress.json" ]]; then
    n=$(python3 -c "import json; print(json.load(open('$OUT/progress.json')).get('n_labeled',0))")
    fail=$(python3 -c "import json; print(json.load(open('$OUT/progress.json')).get('n_failed_batches',0))")
  fi
  chain_alive=0
  if [[ -n "$CHAIN_PID" ]] && kill -0 "$CHAIN_PID" 2>/dev/null; then
    chain_alive=1
  fi
  echo "[watch] $(date -Is) n_labeled=$n fail=$fail chain_alive=$chain_alive" | tee -a "$LOG"
  if [[ "$n" == "2500" && "$fail" == "0" ]]; then
    if [[ "$chain_alive" == "1" ]]; then
      echo "[watch] labels complete; live chain still owns the next step" | tee -a "$LOG"
      sleep 60
      continue
    fi
    echo "[watch] labels complete and chain is dead; ensure student $(date -Is)" | tee -a "$LOG"
    bash "$PAPER/scripts/ensure_student_2500.sh"
    exit $?
  fi
  if [[ -n "$CHAIN_PID" && "$chain_alive" == "0" && "$n" != "2500" ]]; then
    echo "[watch] chain pid $CHAIN_PID is dead with n_labeled=$n; not training" | tee -a "$LOG"
    exit 5
  fi
  sleep 60
done
echo "[watch] timeout $(date -Is) n_labeled=${n:-0}" | tee -a "$LOG"
exit 6
