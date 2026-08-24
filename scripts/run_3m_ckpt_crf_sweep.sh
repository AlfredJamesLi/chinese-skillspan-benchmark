#!/usr/bin/env bash
# Export every hf_trainer/checkpoint-* and run goldstyle-v3 CRF + Gold v2 score.
# Usage: MLM_DIR=output/jobbert_zh_3m/mlm CUDA_VISIBLE_DEVICES=2 bash run_3m_ckpt_crf_sweep.sh
set -euo pipefail
export TRANSFORMERS_OFFLINE=1 HF_HUB_OFFLINE=1 TOKENIZERS_PARALLELISM=false PYTHONUNBUFFERED=1
PY="${PYTHON:-/opt/anaconda3/envs/adasparse/bin/python3}"
ROOT="/home/guojingli3/SCESC-LLM-skill-extraction"
PAPER="$ROOT/Chinese_skill_benchmark_Paper"
MLM_DIR="${MLM_DIR:-$PAPER/output/jobbert_zh_3m/mlm}"
SWEEP_ROOT="${SWEEP_ROOT:-$PAPER/output/jobbert_zh_3m_ckpt_sweep}"
HF="$MLM_DIR/hf_trainer"
mkdir -p "$SWEEP_ROOT"
echo "[sweep] mlm_dir=$MLM_DIR gpu=${CUDA_VISIBLE_DEVICES:-0} $(date -Is)" | tee "$SWEEP_ROOT/sweep.log"

mapfile -t CKPTS < <(find "$HF" -maxdepth 1 -type d -name 'checkpoint-*' 2>/dev/null | sort -V)
if ((${#CKPTS[@]} == 0)); then
  echo "[sweep] no checkpoint-* under $HF" | tee -a "$SWEEP_ROOT/sweep.log"
  exit 1
fi

for ck in "${CKPTS[@]}"; do
  step="${ck##*-}"
  enc="$MLM_DIR/encoder_ckpt${step}"
  out="$SWEEP_ROOT/crf_ckpt${step}"
  if [[ -f "$out/run_summary.json" ]]; then
    echo "[skip] ckpt${step} already scored" | tee -a "$SWEEP_ROOT/sweep.log"
    continue
  fi
  if [[ ! -f "$enc/config.json" ]]; then
    echo "[export] $ck -> $enc" | tee -a "$SWEEP_ROOT/sweep.log"
    "$PY" "$PAPER/scripts/export_jobbert_mlm_encoder.py" \
      --checkpoint "$ck" --out_dir "$enc" >>"$SWEEP_ROOT/sweep.log" 2>&1
  fi
  mkdir -p "$out"
  echo "[crf] ckpt${step} $(date -Is)" | tee -a "$SWEEP_ROOT/sweep.log"
  "$PY" "$PAPER/scripts/train_cn_roberta_crf.py" \
    --seed 42 \
    --model_dir "$enc" \
    --train "$PAPER/data/train_goldstyle_v3.jsonl" \
    --dev "$PAPER/data/dev_goldstyle_v3.jsonl" \
    --test "$ROOT/data/annotated/processed/chinese_skillspan/test.json" \
    --gold "$PAPER/data/gold_canonical_v2.jsonl" \
    --out_dir "$out" \
    --epochs 6 --patience 2 --batch_size 16 --max_len 256 --lr 2e-5 \
    >>"$out/run.log" 2>&1
  echo "[done] ckpt${step} $(date -Is)" | tee -a "$SWEEP_ROOT/sweep.log"
done

"$PY" "$PAPER/scripts/summarize_3m_ckpt_sweep.py" | tee -a "$SWEEP_ROOT/sweep.log"
