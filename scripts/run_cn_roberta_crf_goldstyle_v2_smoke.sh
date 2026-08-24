#!/usr/bin/env bash
# One-seed smoke on Gold-style v2 (tight) train. Does not overwrite v1 or silver dumps.
set -euo pipefail
export CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:-0}"
export TRANSFORMERS_OFFLINE=1
export HF_HUB_OFFLINE=1
export TOKENIZERS_PARALLELISM=false
export PYTHONUNBUFFERED=1
export PYTHONPATH="/home/guojingli3/SCESC-LLM-skill-extraction/Baseline_Models_Collection/pytorch-crf:${PYTHONPATH:-}"
ROOT="/home/guojingli3/SCESC-LLM-skill-extraction"
PAPER="$ROOT/Chinese_skill_benchmark_Paper"
OUT="${OUT_DIR:-$PAPER/output/cn_roberta_wwm_crf/smoke_goldstyle_v2_seed42}"
mkdir -p "$OUT"
echo $$ > "$OUT/smoke.pid"
echo "SMOKE goldstyle v2 GPU=$CUDA_VISIBLE_DEVICES pid=$$ start $(date -Is)" | tee -a "$OUT/smoke.log"
python3 "$PAPER/scripts/train_cn_roberta_crf.py" \
  --seed 42 \
  --train "$PAPER/data/train_goldstyle_v2.jsonl" \
  --dev "$PAPER/data/dev_goldstyle_v2.jsonl" \
  --test "$ROOT/data/annotated/processed/chinese_skillspan/test.json" \
  --gold "$PAPER/data/gold_canonical_v2.jsonl" \
  --out_dir "$OUT" \
  --epochs 6 \
  --patience 2 \
  --batch_size 16 \
  --max_len 256 \
  --lr 2e-5 \
  2>&1 | tee -a "$OUT/smoke.log"
echo "SMOKE goldstyle v2 done $(date -Is) exit=$?" | tee -a "$OUT/smoke.log"
