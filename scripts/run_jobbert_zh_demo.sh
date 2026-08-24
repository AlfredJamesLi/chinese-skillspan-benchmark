#!/usr/bin/env bash
# Small JobBERT-zh demo: 80k JD sents x 1 epoch MLM, then v3 CRF smoke.
# Does not overwrite train.json / Gold v2. Not Zhang-scale.
set -euo pipefail
export TRANSFORMERS_OFFLINE=1 HF_HUB_OFFLINE=1 TOKENIZERS_PARALLELISM=false PYTHONUNBUFFERED=1
export PYTHONPATH="/home/guojingli3/SCESC-LLM-skill-extraction/Baseline_Models_Collection/pytorch-crf:${PYTHONPATH:-}"
ROOT="/home/guojingli3/SCESC-LLM-skill-extraction"
PAPER="$ROOT/Chinese_skill_benchmark_Paper"
OUT="${OUT_DIR:-$PAPER/output/jobbert_zh_demo}"
mkdir -p "$OUT"
echo $$ > "$OUT/demo.pid"
echo "DEMO start GPU=${CUDA_VISIBLE_DEVICES:-?} $(date -Is)" | tee -a "$OUT/demo.log"

python3 "$PAPER/scripts/prepare_jobbert_demo_corpus.py" \
  --n 80000 \
  --out "$PAPER/data/jobbert_demo_sents.jsonl" \
  2>&1 | tee -a "$OUT/demo.log"

python3 "$PAPER/scripts/train_jobbert_zh_mlm.py" \
  --corpus "$PAPER/data/jobbert_demo_sents.jsonl" \
  --model_dir "$ROOT/Baseline_Models_Collection/chinese-roberta-wwm-ext" \
  --out_dir "$OUT/mlm" \
  --epochs 1 --batch_size 32 --max_len 128 --lr 5e-5 \
  2>&1 | tee -a "$OUT/demo.log"

python3 "$PAPER/scripts/train_cn_roberta_crf.py" \
  --seed 42 \
  --model_dir "$OUT/mlm/encoder" \
  --train "$PAPER/data/train_goldstyle_v3.jsonl" \
  --dev "$PAPER/data/dev_goldstyle_v3.jsonl" \
  --test "$ROOT/data/annotated/processed/chinese_skillspan/test.json" \
  --gold "$PAPER/data/gold_canonical_v2.jsonl" \
  --out_dir "$OUT/crf_v3_seed42" \
  --epochs 6 --patience 2 --batch_size 16 --max_len 256 --lr 2e-5 \
  2>&1 | tee -a "$OUT/demo.log"

echo "DEMO done $(date -Is) exit=$?" | tee -a "$OUT/demo.log"
