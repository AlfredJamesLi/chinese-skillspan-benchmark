#!/usr/bin/env bash
# JobBERTa-zh Zhang-scale rung: 3.2M JD sents MLM, then goldstyle v3 CRF.
# INIT_MODEL / EPOCHS come from after_jobbert_1m.py. Does not overwrite train.json / Gold v2.
set -euo pipefail
export TRANSFORMERS_OFFLINE=1 HF_HUB_OFFLINE=1 TOKENIZERS_PARALLELISM=false PYTHONUNBUFFERED=1
export PYTHONPATH="/home/guojingli3/SCESC-LLM-skill-extraction/Baseline_Models_Collection/pytorch-crf:${PYTHONPATH:-}"
PY="${PYTHON:-/opt/anaconda3/envs/adasparse/bin/python3}"
ROOT="/home/guojingli3/SCESC-LLM-skill-extraction"
PAPER="$ROOT/Chinese_skill_benchmark_Paper"
OUT="${OUT_DIR:-$PAPER/output/jobbert_zh_3m}"
CORPUS="${CORPUS:-$PAPER/data/jobbert_3m_sents.jsonl}"
INIT="${INIT_MODEL:-$ROOT/Baseline_Models_Collection/chinese-roberta-wwm-ext}"
EPOCHS="${EPOCHS:-3}"
mkdir -p "$OUT"
echo $$ > "$OUT/run.pid"
NGPU=$(echo "${CUDA_VISIBLE_DEVICES:-0}" | awk -F, '{print NF}')
echo "3M start GPU=${CUDA_VISIBLE_DEVICES:-?} nproc=$NGPU epochs=$EPOCHS init=$INIT $(date -Is)" | tee -a "$OUT/run.log"

LAUNCH=("$PY")
if [[ "$NGPU" -gt 1 ]]; then
  LAUNCH=("$PY" -m torch.distributed.run --standalone --nproc_per_node="$NGPU")
fi
"${LAUNCH[@]}" "$PAPER/scripts/train_jobbert_zh_mlm.py" \
  --corpus "$CORPUS" \
  --model_dir "$INIT" \
  --out_dir "$OUT/mlm" \
  --epochs "$EPOCHS" --batch_size 32 --max_len 128 --lr 5e-5 \
  2>&1 | tee -a "$OUT/run.log"

"$PY" "$PAPER/scripts/train_cn_roberta_crf.py" \
  --seed 42 \
  --model_dir "$OUT/mlm/encoder" \
  --train "$PAPER/data/train_goldstyle_v3.jsonl" \
  --dev "$PAPER/data/dev_goldstyle_v3.jsonl" \
  --test "$ROOT/data/annotated/processed/chinese_skillspan/test.json" \
  --gold "$PAPER/data/gold_canonical_v2.jsonl" \
  --out_dir "$OUT/crf_v3_seed42" \
  --epochs 6 --patience 2 --batch_size 16 --max_len 256 --lr 2e-5 \
  2>&1 | tee -a "$OUT/run.log"

echo "3M done $(date -Is) exit=$?" | tee -a "$OUT/run.log"
"$PY" "$PAPER/scripts/after_jobbert_1m.py" >/dev/null 2>&1 || true
# 3M-specific compare is written by after script only for 1M; dump a one-line pointer
echo "3M CRF summary: $OUT/crf_v3_seed42/run_summary.json" | tee -a "$OUT/run.log"
