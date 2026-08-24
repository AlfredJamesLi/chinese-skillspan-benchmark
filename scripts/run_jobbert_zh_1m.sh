#!/usr/bin/env bash
# JobBERTa-zh mid-rung: 1M JD sents x 3 MLM epochs, then goldstyle v3 CRF.
# Does not overwrite train.json / Gold v2. Not Zhang 3.2M.
set -euo pipefail
export TRANSFORMERS_OFFLINE=1 HF_HUB_OFFLINE=1 TOKENIZERS_PARALLELISM=false PYTHONUNBUFFERED=1
export PYTHONPATH="/home/guojingli3/SCESC-LLM-skill-extraction/Baseline_Models_Collection/pytorch-crf:${PYTHONPATH:-}"
# Pin to adasparse: ~/.local/torchrun would spawn /usr/bin/python3 (no transformers).
PY="${PYTHON:-/opt/anaconda3/envs/adasparse/bin/python3}"
ROOT="/home/guojingli3/SCESC-LLM-skill-extraction"
PAPER="$ROOT/Chinese_skill_benchmark_Paper"
OUT="${OUT_DIR:-$PAPER/output/jobbert_zh_1m}"
mkdir -p "$OUT"
echo $$ > "$OUT/run.pid"
NGPU=$(echo "${CUDA_VISIBLE_DEVICES:-0}" | awk -F, '{print NF}')
echo "1M start GPU=${CUDA_VISIBLE_DEVICES:-?} nproc=$NGPU py=$PY $(date -Is)" | tee -a "$OUT/run.log"

LAUNCH=("$PY")
if [[ "$NGPU" -gt 1 ]]; then
  LAUNCH=("$PY" -m torch.distributed.run --standalone --nproc_per_node="$NGPU")
fi
"${LAUNCH[@]}" "$PAPER/scripts/train_jobbert_zh_mlm.py" \
  --corpus "$PAPER/data/jobbert_1m_sents.jsonl" \
  --model_dir "$ROOT/Baseline_Models_Collection/chinese-roberta-wwm-ext" \
  --out_dir "$OUT/mlm" \
  --epochs 3 --batch_size 32 --max_len 128 --lr 5e-5 \
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

echo "1M done $(date -Is) exit=$?" | tee -a "$OUT/run.log"
