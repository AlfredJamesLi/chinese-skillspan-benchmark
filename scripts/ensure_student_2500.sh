#!/usr/bin/env bash
# Build train/dev from the finished 2500 public-API labels and train JobBERT.
# Safe to call twice: flock + skip-if-scored. Does not rewrite Gold150 / V4 / v6a.
set -euo pipefail
PAPER="/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper"
SCR="$PAPER/scripts"
LABELED="$PAPER/data/silver_plus_10k_prep_20260913/run2500_public_api_v1/labeled.jsonl"
PROG="$PAPER/data/silver_plus_10k_prep_20260913/run2500_public_api_v1/progress.json"
OUT_ROOT="$PAPER/output/silver_public_2500_student_20260913"
LOCK="$OUT_ROOT/student.lock"
LOG="$OUT_ROOT/ensure.log"
mkdir -p "$OUT_ROOT"
exec 8>"$LOCK"
if ! flock -n 8; then
  echo "[ensure] another student holder has $LOCK; waiting" | tee -a "$LOG"
  flock 8
fi
echo "[ensure] start $(date -Is)" | tee -a "$LOG"
python3 - <<'PY'
import json, sys
from pathlib import Path
p = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/data/silver_plus_10k_prep_20260913/run2500_public_api_v1/progress.json")
prog = json.loads(p.read_text())
print(json.dumps(prog, ensure_ascii=False))
if prog.get("n_labeled") != 2500 or prog.get("n_failed_batches"):
    sys.exit(3)
n = sum(1 for line in Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/data/silver_plus_10k_prep_20260913/run2500_public_api_v1/labeled.jsonl").open() if line.strip())
if n != 2500:
    print(f"labeled.jsonl n={n} != 2500", file=sys.stderr)
    sys.exit(3)
PY
if [[ -f "$OUT_ROOT/COMPARE_v6a.json" ]]; then
  echo "[ensure] COMPARE_v6a.json already present; skip train" | tee -a "$LOG"
else
  python3 "$SCR/build_student_from_public_silver.py" \
    --labeled "$LABELED" \
    --out-dir "$OUT_ROOT/data"
  echo "[ensure] train $(date -Is)" | tee -a "$LOG"
  bash "$SCR/run_student_jobbert_silver2500.sh"
  echo "[ensure] student done $(date -Is)" | tee -a "$LOG"
fi
if [[ "${WAVE3_AFTER_STUDENT:-1}" == "1" ]]; then
  echo "[ensure] wave3 $(date -Is)" | tee -a "$LOG"
  bash "$SCR/run_wave3.sh"
fi
echo "[ensure] done $(date -Is)" | tee -a "$LOG"
