#!/usr/bin/env bash
# Re-run 3.2M MLM with all checkpoints kept, then CRF sweep on each.
set -euo pipefail
PY="${PYTHON:-/opt/anaconda3/envs/adasparse/bin/python3}"
ROOT="/home/guojingli3/SCESC-LLM-skill-extraction"
PAPER="$ROOT/Chinese_skill_benchmark_Paper"
ARCH="$PAPER/output/jobbert_zh_3m_ckpt_archive"
LOG="$ARCH/pipeline.log"
mkdir -p "$ARCH"
echo "[mlm-archive] start $(date -Is) gpu=${CUDA_VISIBLE_DEVICES:-?}" | tee "$LOG"

export TRANSFORMERS_OFFLINE=1 HF_HUB_OFFLINE=1 TOKENIZERS_PARALLELISM=false PYTHONUNBUFFERED=1
export SAVE_TOTAL_LIMIT="${SAVE_TOTAL_LIMIT:-20}"
export SAVE_STEPS="${SAVE_STEPS:-5000}"

NGPU=$(echo "${CUDA_VISIBLE_DEVICES:-0}" | awk -F, '{print NF}')
LAUNCH=("$PY")
if [[ "$NGPU" -gt 1 ]]; then
  LAUNCH=("$PY" -m torch.distributed.run --standalone --nproc_per_node="$NGPU")
fi
"${LAUNCH[@]}" "$PAPER/scripts/train_jobbert_zh_mlm.py" \
  --corpus "$PAPER/data/jobbert_3m_sents.jsonl" \
  --model_dir "$PAPER/output/jobbert_zh_1m/mlm/encoder" \
  --out_dir "$ARCH/mlm" \
  --epochs 2 --batch_size 32 --max_len 128 --lr 5e-5 \
  2>&1 | tee -a "$LOG"

echo "[mlm-archive] done $(date -Is)" | tee -a "$LOG"
echo "[sweep] start $(date -Is)" | tee -a "$LOG"
MLM_DIR="$ARCH/mlm" SWEEP_ROOT="$PAPER/output/jobbert_zh_3m_ckpt_sweep" \
  bash "$PAPER/scripts/run_3m_ckpt_crf_sweep.sh" 2>&1 | tee -a "$LOG"
echo "[pipeline] all done $(date -Is)" | tee -a "$LOG"
