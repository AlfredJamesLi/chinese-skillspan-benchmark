#!/usr/bin/env bash
# Relabel ~4k train sentences on local Qwen. Does not overwrite corpus train.json or Gold v2.
set -euo pipefail
export PYTHONUNBUFFERED=1
export TRANSFORMERS_OFFLINE=1
export HF_HUB_OFFLINE=1
export TOKENIZERS_PARALLELISM=false
ROOT="/home/guojingli3/SCESC-LLM-skill-extraction"
export CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:-3}"
export GOLDSTYLE_BACKEND="${GOLDSTYLE_BACKEND:-local}"
export GOLDSTYLE_LOCAL_MODEL="${GOLDSTYLE_LOCAL_MODEL:-$ROOT/LLaMA-Factory/Qwen2.5-14B-Instruct}"
OUT="${OUT_DIR:-$ROOT/Chinese_skill_benchmark_Paper/output/goldstyle_train_4k}"
mkdir -p "$OUT"
echo "relabel start $(date -Is) backend=$GOLDSTYLE_BACKEND gpu=$CUDA_VISIBLE_DEVICES" | tee -a "$OUT/relabel.log"
python3 "$ROOT/Chinese_skill_benchmark_Paper/scripts/expand_goldstyle_train.py" \
  --backend "$GOLDSTYLE_BACKEND" \
  --local_model "$GOLDSTYLE_LOCAL_MODEL" \
  --n "${N:-4000}" \
  --batch "${BATCH:-4}" \
  --limit "${LIMIT:-0}" \
  --sleep 0 \
  --out_dir "$OUT" \
  2>&1 | tee -a "$OUT/relabel.log"
echo "relabel done $(date -Is) exit=$?" | tee -a "$OUT/relabel.log"
