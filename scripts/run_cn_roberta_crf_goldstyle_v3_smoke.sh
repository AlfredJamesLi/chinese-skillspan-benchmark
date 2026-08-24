#!/usr/bin/env bash
# Vanilla RoBERTa-wwm + CRF on goldstyle v3. Comparison arm for the JobBERT demo.
set -euo pipefail
export TRANSFORMERS_OFFLINE=1 HF_HUB_OFFLINE=1 TOKENIZERS_PARALLELISM=false PYTHONUNBUFFERED=1
export PYTHONPATH="/home/guojingli3/SCESC-LLM-skill-extraction/Baseline_Models_Collection/pytorch-crf:${PYTHONPATH:-}"
ROOT="/home/guojingli3/SCESC-LLM-skill-extraction"
PAPER="$ROOT/Chinese_skill_benchmark_Paper"
OUT="${OUT_DIR:-$PAPER/output/cn_roberta_wwm_crf/smoke_goldstyle_v3_seed42}"
mkdir -p "$OUT"
echo $$ > "$OUT/smoke.pid"
echo "SMOKE goldstyle v3 GPU=${CUDA_VISIBLE_DEVICES:-?} start $(date -Is)" | tee -a "$OUT/smoke.log"
python3 "$PAPER/scripts/train_cn_roberta_crf.py" \
  --seed 42 \
  --train "$PAPER/data/train_goldstyle_v3.jsonl" \
  --dev "$PAPER/data/dev_goldstyle_v3.jsonl" \
  --test "$ROOT/data/annotated/processed/chinese_skillspan/test.json" \
  --gold "$PAPER/data/gold_canonical_v2.jsonl" \
  --out_dir "$OUT" \
  --epochs 6 --patience 2 --batch_size 16 --max_len 256 --lr 2e-5 \
  2>&1 | tee -a "$OUT/smoke.log"
echo "SMOKE goldstyle v3 done $(date -Is) exit=$?" | tee -a "$OUT/smoke.log"
