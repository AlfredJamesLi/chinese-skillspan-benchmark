#!/usr/bin/env bash
# One-seed smoke: Chinese RoBERTa-wwm-ext + CRF. Do not start 3 seeds here.
set -euo pipefail
export CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:-0}"
export TRANSFORMERS_OFFLINE=1
export HF_HUB_OFFLINE=1
export TOKENIZERS_PARALLELISM=false
export PYTHONUNBUFFERED=1
export PYTHONPATH="/home/guojingli3/SCESC-LLM-skill-extraction/Baseline_Models_Collection/pytorch-crf:${PYTHONPATH:-}"
ROOT="/home/guojingli3/SCESC-LLM-skill-extraction"
SCRIPT="$ROOT/Chinese_skill_benchmark_Paper/scripts/train_cn_roberta_crf.py"
OUT="${OUT_DIR:-$ROOT/Chinese_skill_benchmark_Paper/output/cn_roberta_wwm_crf/smoke_seed42}"
mkdir -p "$OUT"
echo $$ > "$OUT/smoke.pid"
echo "SMOKE GPU=$CUDA_VISIBLE_DEVICES pid=$$ start $(date -Is)" | tee -a "$OUT/smoke.log"
python3 "$SCRIPT" \
  --seed 42 \
  --out_dir "$OUT" \
  --epochs 6 \
  --patience 2 \
  --batch_size 16 \
  --max_len 256 \
  --lr 2e-5 \
  2>&1 | tee -a "$OUT/smoke.log"
echo "SMOKE done $(date -Is) exit=$?" | tee -a "$OUT/smoke.log"
