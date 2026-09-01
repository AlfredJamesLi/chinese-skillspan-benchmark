#!/usr/bin/env bash
# JobBERT-zh 1M encoder + 3-tag CRF, one type at a time (L / K / S / T).
# Appendix backup vs the joint 9-tag CRF. Does not overwrite
# crf_lskt_v4_silver_seed42, Gold v2, or v4 silver jsonl.
set -euo pipefail
export TRANSFORMERS_OFFLINE=1 HF_HUB_OFFLINE=1 TOKENIZERS_PARALLELISM=false PYTHONUNBUFFERED=1
export PYTHONPATH="/home/guojingli3/SCESC-LLM-skill-extraction/Baseline_Models_Collection/pytorch-crf:${PYTHONPATH:-}"
# Slurm sbatch sets CUDA_VISIBLE_DEVICES after picking an idle card.
# Do not hard-pin a GPU here; unschedled nohup jobs get Killed.
PY="${PYTHON:-/opt/anaconda3/envs/adasparse/bin/python3}"
ROOT="/home/guojingli3/SCESC-LLM-skill-extraction"
PAPER="$ROOT/Chinese_skill_benchmark_Paper"
ENC="${ENC:-$PAPER/output/jobbert_zh_1m/mlm/encoder}"
OUT_ROOT="${OUT_DIR:-$PAPER/output/stl_v4/jobbert_zh_1m/seed42}"
KEEP_JOINT="$PAPER/output/jobbert_zh_1m/crf_lskt_v4_silver_seed42"

if [[ ! -f "$ENC/config.json" ]]; then
  echo "missing 1M encoder: $ENC" >&2
  exit 2
fi
if [[ "$OUT_ROOT" == "$KEEP_JOINT" ]]; then
  echo "refusing to overwrite joint v4 CRF dir" >&2
  exit 2
fi
mkdir -p "$OUT_ROOT"
echo $$ > "$OUT_ROOT/run.pid"
if [[ -z "${CUDA_VISIBLE_DEVICES:-}" ]]; then
  echo "CUDA_VISIBLE_DEVICES unset; refuse unschedled run. Use sbatch scripts/stl_lskt_v4.sbatch" | tee -a "$OUT_ROOT/run.log"
  exit 2
fi
echo "STL v4 start GPU=${CUDA_VISIBLE_DEVICES:-?} slurm=${SLURM_JOB_ID:-na} enc=$ENC out=$OUT_ROOT $(date -Is)" | tee -a "$OUT_ROOT/run.log"

# S then K then T then L: most support first if the job is preempted.
for typ in S K T L; do
  out="$OUT_ROOT/$typ"
  if [[ -f "$out/test_pred.jsonl" ]]; then
    echo "[skip] STL-$typ already has test_pred.jsonl" | tee -a "$OUT_ROOT/run.log"
    continue
  fi
  mkdir -p "$out"
  echo "[crf] STL-$typ $(date -Is)" | tee -a "$OUT_ROOT/run.log"
  "$PY" "$PAPER/scripts/train_cn_roberta_crf.py" \
    --seed 42 \
    --keep_type "$typ" \
    --model_dir "$ENC" \
    --train "$PAPER/data/train_lskt_v4_silver.jsonl" \
    --dev "$PAPER/data/dev_lskt_v4_silver.jsonl" \
    --test "$ROOT/data/annotated/processed/chinese_skillspan/test.json" \
    --gold "$PAPER/data/gold_canonical_v2.jsonl" \
    --out_dir "$out" \
    --epochs 6 --patience 2 --batch_size 16 --max_len 256 --lr 2e-5 \
    --resume \
    >>"$out/run.log" 2>&1
  echo "[done] STL-$typ $(date -Is)" | tee -a "$OUT_ROOT/run.log"
done

echo "[eval] V4 hybrid jieba $(date -Is)" | tee -a "$OUT_ROOT/run.log"
"$PY" "$PAPER/scripts/eval_stl_v4.py" | tee -a "$OUT_ROOT/run.log"
echo "STL v4 all done $(date -Is)" | tee -a "$OUT_ROOT/run.log"
