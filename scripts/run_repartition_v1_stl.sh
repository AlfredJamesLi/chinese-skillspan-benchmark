#!/usr/bin/env bash
# STL L/K/S/T on frozen repartition_v1. Two heads at a time on the job's GPU pair.
# Does not overwrite old output/stl_v4 or joint v4 CRF.
set -euo pipefail
export TRANSFORMERS_OFFLINE=1 HF_HUB_OFFLINE=1 TOKENIZERS_PARALLELISM=false PYTHONUNBUFFERED=1
export PYTHONPATH="/home/guojingli3/SCESC-LLM-skill-extraction/Baseline_Models_Collection/pytorch-crf:${PYTHONPATH:-}"
PY="${PYTHON:-/opt/anaconda3/envs/adasparse/bin/python3}"
ROOT="/home/guojingli3/SCESC-LLM-skill-extraction"
PAPER="$ROOT/Chinese_skill_benchmark_Paper"
OUT_ROOT="${OUT_ROOT:-$PAPER/output/repartition_v1/stl_1m/seed_42}"
ENC="$PAPER/output/jobbert_zh_1m/mlm/encoder"
TRAIN="$PAPER/data/repartition_v1/train.jsonl"
DEV="$PAPER/data/repartition_v1/dev.jsonl"
TEST="$PAPER/data/repartition_v1/test.jsonl"
STATUS="$PAPER/reports/repartition_v1/night_run_status.md"
LOG="$PAPER/output/repartition_v1/run.log"

if [[ -z "${CUDA_VISIBLE_DEVICES:-}" ]]; then
  echo "CUDA_VISIBLE_DEVICES unset" >&2
  exit 2
fi
IFS=',' read -r GPU0 GPU1 _rest <<< "$CUDA_VISIBLE_DEVICES"
if [[ -z "${GPU1:-}" ]]; then
  echo "need two visible GPUs" >&2
  exit 2
fi
mkdir -p "$OUT_ROOT"
echo "[stl] start pin $GPU0+$GPU1 slurm=${SLURM_JOB_ID:-na} $(date -Is)" | tee -a "$LOG" "$STATUS"

run_head() {
  local typ="$1" gpu="$2"
  local out="$OUT_ROOT/$typ"
  if [[ -f "$out/run_summary.json" ]]; then
    echo "[skip] STL-$typ" | tee -a "$LOG"
    return 0
  fi
  mkdir -p "$out"
  echo "[stl] $typ gpu=$gpu $(date -Is)" | tee -a "$LOG" "$STATUS"
  CUDA_VISIBLE_DEVICES="$gpu" "$PY" "$PAPER/scripts/train_cn_roberta_crf.py" \
    --seed 42 --keep_type "$typ" \
    --model_dir "$ENC" \
    --train "$TRAIN" --dev "$DEV" --test "$TEST" --gold "$TEST" \
    --out_dir "$out" \
    --epochs 6 --patience 2 --batch_size 16 --max_len 256 --lr 2e-5 \
    --resume \
    >>"$out/run.log" 2>&1
  echo "[done] STL-$typ gpu=$gpu $(date -Is)" | tee -a "$LOG" "$STATUS"
}

run_pair() {
  local t1="$1" t2="$2"
  run_head "$t1" "$GPU0" &
  local p1=$!
  run_head "$t2" "$GPU1" &
  local p2=$!
  wait "$p1"; local r1=$?
  wait "$p2"; local r2=$?
  if [[ "$r1" -ne 0 || "$r2" -ne 0 ]]; then
    echo "[fail] STL $t1/$t2 r=$r1/$r2" | tee -a "$LOG"
    return 1
  fi
}

run_pair S K
run_pair T L
"$PY" "$PAPER/scripts/eval_stl_repartition_v1.py" | tee -a "$LOG"
echo "[stl] all heads done $(date -Is)" | tee -a "$LOG" "$STATUS"
