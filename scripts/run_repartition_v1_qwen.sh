#!/usr/bin/env bash
# Qwen2.5-14B SOP extract on new test: two shards, one per visible GPU.
set -euo pipefail
export TRANSFORMERS_OFFLINE=1 HF_HUB_OFFLINE=1 TOKENIZERS_PARALLELISM=false PYTHONUNBUFFERED=1
PY="${PYTHON:-/opt/anaconda3/envs/adasparse/bin/python3}"
PAPER="/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper"
OUT="$PAPER/output/repartition_v1/qwen25_sop"
LOG="$PAPER/output/repartition_v1/run.log"
STATUS="$PAPER/reports/repartition_v1/night_run_status.md"

if [[ -z "${CUDA_VISIBLE_DEVICES:-}" ]]; then
  echo "CUDA_VISIBLE_DEVICES unset" >&2
  exit 2
fi
IFS=',' read -r GPU0 GPU1 _rest <<< "$CUDA_VISIBLE_DEVICES"
if [[ -z "${GPU1:-}" ]]; then
  echo "need two visible GPUs" >&2
  exit 2
fi
mkdir -p "$OUT"
echo "[qwen] start pin $GPU0+$GPU1 shards=2 $(date -Is)" | tee -a "$LOG" "$STATUS"

run_shard() {
  local shard="$1" gpu="$2"
  echo "[qwen] shard=$shard gpu=$gpu $(date -Is)" | tee -a "$LOG" "$STATUS"
  CUDA_VISIBLE_DEVICES="$gpu" "$PY" -u "$PAPER/scripts/run_repartition_v1_qwen_shard.py" \
    --shard "$shard" --n-shards 2 --out-dir "$OUT" \
    >>"$OUT/shard_${shard}.log" 2>&1
}

if [[ -f "$OUT/test_pred.jsonl" ]]; then
  echo "[skip] qwen test_pred exists" | tee -a "$LOG"
else
  run_shard 0 "$GPU0" &
  p0=$!
  run_shard 1 "$GPU1" &
  p1=$!
  wait "$p0"; r0=$?
  wait "$p1"; r1=$?
  if [[ "$r0" -ne 0 || "$r1" -ne 0 ]]; then
    echo "[fail] qwen shards r=$r0/$r1" | tee -a "$LOG"
    exit 1
  fi
  "$PY" "$PAPER/scripts/run_repartition_v1_qwen_shard.py" --shard 0 --n-shards 2 --out-dir "$OUT" --merge-only \
    | tee -a "$LOG"
  "$PY" "$PAPER/scripts/eval_repartition_v1.py" "$OUT/test_pred.jsonl" qwen25_sop 0 "$OUT" \
    | tee -a "$LOG"
fi
echo "[qwen] done $(date -Is)" | tee -a "$LOG" "$STATUS"
