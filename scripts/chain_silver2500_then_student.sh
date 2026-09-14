#!/usr/bin/env bash
# Label 2500 public-API Silver sentences, then train the JobBERT student.
# Does not rewrite Gold150 / V4 / v6a / confirmed-results.
set -euo pipefail
PAPER="/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper"
SCR="$PAPER/scripts"
OUT="$PAPER/data/silver_plus_10k_prep_20260913/run2500_public_api_v1"
LOG="$OUT/chain.log"
LOCK="$OUT/chain.lock"
mkdir -p "$OUT"
exec 9>"$LOCK"
if ! flock -n 9; then
  echo "another chain holds $LOCK; refusing to start a second writer" >&2
  exit 4
fi
cd "$SCR"
echo "[chain] start $(date -Is)" | tee -a "$LOG"
python3 run_silver_public_api.py \
  --n 2500 \
  --batch-size 10 \
  --out-dir "$OUT" \
  --retries 3 \
  --sleep 0.4 \
  --timeout 240 \
  2>&1 | tee -a "$OUT/api.log"
echo "[chain] api exit=${PIPESTATUS[0]} $(date -Is)" | tee -a "$LOG"
echo "[chain] train $(date -Is)" | tee -a "$LOG"
# Do not default to GPU 0 (often occupied). pick_free_cuda runs inside the student script.
bash "$SCR/ensure_student_2500.sh"
echo "[chain] done $(date -Is)" | tee -a "$LOG"
