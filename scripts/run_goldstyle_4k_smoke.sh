#!/usr/bin/env bash
# One-seed smoke on Gold-style 4k train. Does not overwrite old encoder dumps.
set -euo pipefail
export CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:-1}"
export TRANSFORMERS_OFFLINE=1
export HF_HUB_OFFLINE=1
export TOKENIZERS_PARALLELISM=false
export PYTHONUNBUFFERED=1
export PYTHONPATH="/home/guojingli3/SCESC-LLM-skill-extraction/Baseline_Models_Collection/pytorch-crf:${PYTHONPATH:-}"
ROOT="/home/guojingli3/SCESC-LLM-skill-extraction"
DATA="$ROOT/Chinese_skill_benchmark_Paper/output/goldstyle_train_4k"
OUT="$ROOT/Chinese_skill_benchmark_Paper/output/cn_roberta_wwm_crf/goldstyle4k_smoke42"
mkdir -p "$OUT"
echo "SMOKE GPU=$CUDA_VISIBLE_DEVICES start $(date -Is)" | tee -a "$OUT/smoke.log"
python3 "$ROOT/Chinese_skill_benchmark_Paper/scripts/train_cn_roberta_crf.py" \
  --seed 42 \
  --train "$DATA/train_goldstyle_4k.json" \
  --dev "$DATA/dev_goldstyle_4k.json" \
  --test "$ROOT/data/annotated/processed/chinese_skillspan/test.json" \
  --gold "$ROOT/Chinese_skill_benchmark_Paper/data/gold_canonical_v2.jsonl" \
  --out_dir "$OUT" \
  --epochs 6 \
  --patience 2 \
  --batch_size 16 \
  --max_len 256 \
  --lr 2e-5 \
  2>&1 | tee -a "$OUT/smoke.log"
echo "SMOKE done $(date -Is) exit=$?" | tee -a "$OUT/smoke.log"
