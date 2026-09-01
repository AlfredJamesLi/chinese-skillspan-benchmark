#!/usr/bin/env bash
# CRF on frozen repartition_v1 splits. New output dirs only.
# Does not overwrite Gold v2, old silver, hybrid eval, or existing CRF dirs.
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

if [[ "$OUT_ROOT" == "$KEEP_OLD" ]]; then
  echo "refusing to overwrite old 1M v4 CRF dir" >&2
  exit 2
fi
if [[ -z "${CUDA_VISIBLE_DEVICES:-}" ]]; then
  echo "CUDA_VISIBLE_DEVICES unset; use sbatch scripts/repartition_v1.sbatch" >&2
  exit 2
fi
mkdir -p "$OUT_ROOT" "$PAPER/runs/repartition_v1"
echo "repartition_v1 CRF start GPU=${CUDA_VISIBLE_DEVICES} slurm=${SLURM_JOB_ID:-na} $(date -Is)" | tee -a "$OUT_ROOT/run.log"

run_one() {
  local name="$1" enc="$2" seed="$3"
  local out="$OUT_ROOT/${name}/seed_${seed}"
  if [[ "$out" == "$KEEP_OLD" ]]; then
    echo "refusing overwrite $KEEP_OLD" >&2
    return 1
  fi
  if [[ -f "$out/run_summary.json" ]]; then
    echo "[skip] $name seed=$seed" | tee -a "$OUT_ROOT/run.log"
    return 0
  fi
  if [[ ! -f "$enc/config.json" ]]; then
    echo "[fail] missing encoder $enc" | tee -a "$OUT_ROOT/run.log"
    return 1
  fi
  mkdir -p "$out"
  echo "[crf] $name seed=$seed $(date -Is)" | tee -a "$OUT_ROOT/run.log" "$STATUS"
  "$PY" "$PAPER/scripts/train_cn_roberta_crf.py" \
    --seed "$seed" \
    --model_dir "$enc" \
    --train "$TRAIN" \
    --dev "$DEV" \
    --test "$TEST" \
    --gold "$TEST" \
    --out_dir "$out" \
    --epochs 6 --patience 2 --batch_size 16 --max_len 256 --lr 2e-5 \
    >>"$out/run.log" 2>&1
  "$PY" "$PAPER/scripts/eval_repartition_v1.py" \
    "$out/test_pred.jsonl" "$name" "$seed" "$out" \
    | tee -a "$OUT_ROOT/run.log"
  echo "[done] $name seed=$seed $(date -Is)" | tee -a "$OUT_ROOT/run.log" "$STATUS"
}

SMOKE="${SMOKE:-0}"
ENC_1M="$PAPER/output/jobbert_zh_1m/mlm/encoder"
ENC_3M="$PAPER/output/jobbert_zh_3m/mlm/encoder_ckpt65000"
ENC_RB="$ROOT/Baseline_Models_Collection/chinese-roberta-wwm-ext"

# Smoke: official seed 42, JobBERT 1M only.
run_one "jobbert_1m" "$ENC_1M" 42
if [[ ! -f "$OUT_ROOT/jobbert_1m/seed_42/test_pred.jsonl" ]]; then
  echo "SMOKE FAIL jobbert_1m seed 42" | tee -a "$OUT_ROOT/run.log" "$STATUS"
  exit 3
fi
echo "SMOKE PASS jobbert_1m seed 42 $(date -Is)" | tee -a "$OUT_ROOT/run.log" "$STATUS"
if [[ "$SMOKE" == "1" ]]; then
  exit 0
fi

for seed in 123 2026; do
  run_one "jobbert_1m" "$ENC_1M" "$seed"
done
for seed in 42 123 2026; do
  run_one "jobbert_3m" "$ENC_3M" "$seed"
done
for seed in 42 123 2026; do
  run_one "roberta_wwm" "$ENC_RB" "$seed"
done

echo "repartition_v1 all CRF done $(date -Is)" | tee -a "$OUT_ROOT/run.log" "$STATUS"
