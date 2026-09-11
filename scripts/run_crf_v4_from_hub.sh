#!/usr/bin/env bash
# V4 silver CRF from Hub JobBERT-zh. No laboratory PYTHONPATH / absolute roots.
# Does not overwrite data/frozen_preds/ or the hybrid gold.
set -euo pipefail
PAPER="$(cd "$(dirname "$0")/.." && pwd)"
export TOKENIZERS_PARALLELISM=false PYTHONUNBUFFERED=1
PY="${PYTHON:-python3}"
OUT="${OUT_DIR:-$PAPER/output/crf_v4_from_hub_seed42}"
MODEL="${MODEL_DIR:-AlfredJames/jobbert-zh}"
mkdir -p "$OUT"
exec "$PY" "$PAPER/scripts/train_cn_roberta_crf.py" \
  --seed 42 \
  --model_dir "$MODEL" \
  --train "$PAPER/data/train_lskt_v4_silver.jsonl" \
  --dev "$PAPER/data/dev_lskt_v4_silver.jsonl" \
  --test "$PAPER/data/corpus_splits/test.json" \
  --gold "$PAPER/data/gold_canonical_v2.jsonl" \
  --out_dir "$OUT" \
  --epochs 6 --patience 2 --batch_size 16 --max_len 256 --lr 2e-5 \
  "$@"
