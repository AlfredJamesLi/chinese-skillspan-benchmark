#!/usr/bin/env bash
# Two-GPU pair scheduler for repartition_v1 CRF.
# Pins one CRF per visible card. Skips finished run_summary.json.
# Does not overwrite old v4 CRF dirs. No F1-based skip logic.
set -euo pipefail
export TRANSFORMERS_OFFLINE=1 HF_HUB_OFFLINE=1 TOKENIZERS_PARALLELISM=false PYTHONUNBUFFERED=1
export PYTHONPATH="/home/guojingli3/SCESC-LLM-skill-extraction/Baseline_Models_Collection/pytorch-crf:${PYTHONPATH:-}"
PY="${PYTHON:-/opt/anaconda3/envs/adasparse/bin/python3}"
ROOT="/home/guojingli3/SCESC-LLM-skill-extraction"
PAPER="$ROOT/Chinese_skill_benchmark_Paper"
OUT_ROOT="${OUT_ROOT:-$PAPER/output/repartition_v1}"
STATUS="$PAPER/reports/repartition_v1/night_run_status.md"
TRAIN="$PAPER/data/repartition_v1/train.jsonl"
DEV="$PAPER/data/repartition_v1/dev.jsonl"
TEST="$PAPER/data/repartition_v1/test.jsonl"
KEEP_OLD="$PAPER/output/jobbert_zh_1m/crf_lskt_v4_silver_seed42"
ENC_1M="$PAPER/output/jobbert_zh_1m/mlm/encoder"
ENC_3M="$PAPER/output/jobbert_zh_3m/mlm/encoder_ckpt65000"
ENC_RB="$ROOT/Baseline_Models_Collection/chinese-roberta-wwm-ext"

if [[ -z "${CUDA_VISIBLE_DEVICES:-}" ]]; then
  echo "CUDA_VISIBLE_DEVICES unset" >&2
  exit 2
fi
IFS=',' read -r GPU0 GPU1 _rest <<< "$CUDA_VISIBLE_DEVICES"
if [[ -z "${GPU1:-}" ]]; then
  echo "need two visible GPUs, got ${CUDA_VISIBLE_DEVICES}" >&2
  exit 2
fi
mkdir -p "$OUT_ROOT"
echo "[pair] start vis=$CUDA_VISIBLE_DEVICES pin $GPU0+$GPU1 slurm=${SLURM_JOB_ID:-na} $(date -Is)" | tee -a "$OUT_ROOT/run.log"

run_one() {
  local name="$1" enc="$2" seed="$3" gpu="$4"
  local out="$OUT_ROOT/${name}/seed_${seed}"
  if [[ "$out" == "$KEEP_OLD" ]]; then
    echo "refusing overwrite $KEEP_OLD" >&2
    return 1
  fi
  if [[ -f "$out/run_summary.json" ]]; then
    echo "[skip] $name seed=$seed" | tee -a "$OUT_ROOT/run.log"
    return 0
  fi
  mkdir -p "$out"
  echo "[crf] $name seed=$seed gpu=$gpu $(date -Is)" | tee -a "$OUT_ROOT/run.log" "$STATUS"
  CUDA_VISIBLE_DEVICES="$gpu" "$PY" "$PAPER/scripts/train_cn_roberta_crf.py" \
    --seed "$seed" \
    --model_dir "$enc" \
    --train "$TRAIN" \
    --dev "$DEV" \
    --test "$TEST" \
    --gold "$TEST" \
    --out_dir "$out" \
    --epochs 6 --patience 2 --batch_size 16 --max_len 256 --lr 2e-5 \
    >>"$out/run.log" 2>&1
  CUDA_VISIBLE_DEVICES="$gpu" "$PY" "$PAPER/scripts/eval_repartition_v1.py" \
    "$out/test_pred.jsonl" "$name" "$seed" "$out" \
    | tee -a "$OUT_ROOT/run.log"
  echo "[done] $name seed=$seed gpu=$gpu $(date -Is)" | tee -a "$OUT_ROOT/run.log" "$STATUS"
}

run_pair() {
  local n1="$1" e1="$2" s1="$3"
  local n2="$4" e2="$5" s2="$6"
  local p1=0 p2=0
  run_one "$n1" "$e1" "$s1" "$GPU0" &
  p1=$!
  run_one "$n2" "$e2" "$s2" "$GPU1" &
  p2=$!
  wait "$p1"
  local r1=$?
  wait "$p2"
  local r2=$?
  if [[ "$r1" -ne 0 || "$r2" -ne 0 ]]; then
    echo "[fail] pair $n1/$s1 r=$r1 $n2/$s2 r=$r2" | tee -a "$OUT_ROOT/run.log"
    return 1
  fi
}

SMOKE_DIR="$OUT_ROOT/jobbert_1m/seed_42"
SMOKE_SUMMARY="$SMOKE_DIR/run_summary.json"
echo "[pair] wait smoke $SMOKE_SUMMARY $(date -Is)" | tee -a "$OUT_ROOT/run.log"
while [[ ! -f "$SMOKE_SUMMARY" ]]; do
  sleep 30
done
echo "[pair] smoke summary present $(date -Is)" | tee -a "$OUT_ROOT/run.log"
# Sequential wrapper is the Slurm batch step — keep it STOPPED, never SIGKILL.
# Score smoke here because the stopped wrapper cannot run eval_repartition_v1.py.
if [[ -f "$SMOKE_DIR/test_pred.jsonl" ]]; then
  CUDA_VISIBLE_DEVICES="$GPU0" "$PY" "$PAPER/scripts/eval_repartition_v1.py" \
    "$SMOKE_DIR/test_pred.jsonl" jobbert_1m 42 "$SMOKE_DIR" \
    | tee -a "$OUT_ROOT/run.log"
fi

# Remaining 8 runs, 4 waves. Smoke 1M/42 already done (or skipped).
run_pair jobbert_1m "$ENC_1M" 123  jobbert_3m "$ENC_3M" 42
run_pair jobbert_1m "$ENC_1M" 2026 jobbert_3m "$ENC_3M" 123
run_pair jobbert_3m "$ENC_3M" 2026 roberta_wwm "$ENC_RB" 42
run_pair roberta_wwm "$ENC_RB" 123 roberta_wwm "$ENC_RB" 2026

echo "[pair] all remaining CRF done $(date -Is)" | tee -a "$OUT_ROOT/run.log" "$STATUS"
# Same job, same pair: STL then Qwen. Do not CONT the batch step until these finish.
if [[ "${NIGHT_REST:-1}" == "1" ]]; then
  echo "[pair] night rest STL+Qwen $(date -Is)" | tee -a "$OUT_ROOT/run.log" "$STATUS"
  bash "$PAPER/scripts/run_repartition_v1_stl.sh"
  bash "$PAPER/scripts/run_repartition_v1_qwen.sh"
fi
# Resume sequential wrapper so the Slurm batch step skip-finishes and exits 0.
if [[ -n "${SEQ_BASH_PID:-}" ]] && kill -0 "$SEQ_BASH_PID" 2>/dev/null; then
  echo "[pair] CONT sequential wrapper pid=$SEQ_BASH_PID" | tee -a "$OUT_ROOT/run.log"
  kill -CONT "$SEQ_BASH_PID" || true
fi
