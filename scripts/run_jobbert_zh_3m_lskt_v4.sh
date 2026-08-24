#!/usr/bin/env bash
# JobBERT-zh 3M ckpt65000 encoder + CRF on LSKT v4 silver.
# New dir only. Does not touch 1M crf_lskt_v4_silver_seed42 or goldstyle-v3 3M CRF.
set -euo pipefail
export TRANSFORMERS_OFFLINE=1 HF_HUB_OFFLINE=1 TOKENIZERS_PARALLELISM=false PYTHONUNBUFFERED=1
export PYTHONPATH="/home/guojingli3/SCESC-LLM-skill-extraction/Baseline_Models_Collection/pytorch-crf:${PYTHONPATH:-}"
PY="${PYTHON:-/opt/anaconda3/envs/adasparse/bin/python3}"
ROOT="/home/guojingli3/SCESC-LLM-skill-extraction"
PAPER="$ROOT/Chinese_skill_benchmark_Paper"
ENC="${ENC:-$PAPER/output/jobbert_zh_3m/mlm/encoder_ckpt65000}"
OUT="${OUT_DIR:-$PAPER/output/jobbert_zh_3m/crf_lskt_v4_silver_seed42}"
KEEP_1M="$PAPER/output/jobbert_zh_1m/crf_lskt_v4_silver_seed42"

if [[ ! -f "$ENC/config.json" ]]; then
  echo "missing 3M encoder: $ENC" >&2
  exit 2
fi
if [[ "$OUT" == "$KEEP_1M" ]]; then
  echo "refusing to overwrite 1M v4 CRF dir" >&2
  exit 2
fi
mkdir -p "$OUT"
if [[ -f "$OUT/run_summary.json" ]]; then
  echo "[skip] already scored $OUT" | tee -a "$OUT/run.log"
  "$PY" "$PAPER/scripts/score_sop_v4_pred.py" --pred "$OUT/test_pred.jsonl" --out "$OUT/sop_eval.json"
  exit 0
fi

echo $$ > "$OUT/run.pid"
echo "3M+v4 CRF start GPU=${CUDA_VISIBLE_DEVICES:-?} enc=$ENC out=$OUT $(date -Is)" | tee -a "$OUT/run.log"

"$PY" "$PAPER/scripts/train_cn_roberta_crf.py" \
  --seed 42 \
  --model_dir "$ENC" \
  --train "$PAPER/data/train_lskt_v4_silver.jsonl" \
  --dev "$PAPER/data/dev_lskt_v4_silver.jsonl" \
  --test "$ROOT/data/annotated/processed/chinese_skillspan/test.json" \
  --gold "$PAPER/data/gold_canonical_v2.jsonl" \
  --out_dir "$OUT" \
  --epochs 6 --patience 2 --batch_size 16 --max_len 256 --lr 2e-5 \
  2>&1 | tee -a "$OUT/run.log"

"$PY" "$PAPER/scripts/score_sop_v4_pred.py" \
  --pred "$OUT/test_pred.jsonl" \
  --out "$OUT/sop_eval.json" \
  2>&1 | tee -a "$OUT/run.log"

echo "3M+v4 CRF done $(date -Is) exit=$?" | tee -a "$OUT/run.log"
echo "official Gold v2 summary: $OUT/run_summary.json" | tee -a "$OUT/run.log"
echo "SOP eval: $OUT/sop_eval.json" | tee -a "$OUT/run.log"
