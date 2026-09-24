#!/bin/bash
#SBATCH --job-name=cnss_zh
#SBATCH --partition=LocalQ
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=24:00:00
# Usage: sbatch --export=ALL,MODEL_SHORT=xlm-roberta-large,SEED=42,PHASE=smoke,GPU=1 scripts/one_chinese.sbatch
set -euo pipefail
ROOT=/home/guojingli3/cnss_external_benchmarks_20260921
MODEL_SHORT=${MODEL_SHORT:?}
SEED=${SEED:?}
PHASE=${PHASE:-full}
export HF_HOME="$ROOT/hf_cache"
export HF_HUB_CACHE="$ROOT/hf_cache/hub"
export TOKENIZERS_PARALLELISM=false
export PYTHONNOUSERSITE=1
PY="$ROOT/env/bin/python"
if [ -n "${GPU:-}" ]; then
  export CUDA_VISIBLE_DEVICES="$GPU"
else
  PICK=$(nvidia-smi --query-gpu=index,memory.free --format=csv,noheader,nounits \
    | awk -F',' '{gsub(/ /,"",$1); gsub(/ /,"",$2); if ($2+0>=60000) print $1}' \
    | head -n 1)
  export CUDA_VISIBLE_DEVICES="${PICK:?no idle GPU with 60GiB free}"
fi
case "$MODEL_SHORT" in
  xlm-roberta-large) MODEL=FacebookAI/xlm-roberta-large ;;
  esco-xlm-roberta-large) MODEL=jjzha/esco-xlm-roberta-large ;;
  *) echo "[abort] $MODEL_SHORT" >&2; exit 2 ;;
esac
REV=$("$PY" -c "import json; d={r['model']:r['revision'] for r in json.load(open('$ROOT/models.json'))}; print(d['$MODEL'])")
OUT="$ROOT/runs/chinese/$PHASE/$MODEL_SHORT/$SEED"
mkdir -p "$(dirname "$OUT")" "$ROOT/logs"
if [ -f "$OUT/config.json" ]; then
  echo "[abort] refuse overwrite $OUT"
  exit 4
fi
LOG="$ROOT/logs/chinese_${PHASE}_${MODEL_SHORT}_${SEED}"
CMD=("$PY" "$ROOT/run_chinese_encoder.py" --model "$MODEL" --revision "$REV" --seed "$SEED" --output "$OUT")
if [ "$PHASE" = smoke ]; then
  CMD+=(--smoke)
fi
exec > >(tee -a "${LOG}.out") 2> >(tee -a "${LOG}.err" >&2)
"${CMD[@]}"
echo "[done] chinese $MODEL_SHORT $SEED $(date -Is)"
