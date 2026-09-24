#!/bin/bash
#SBATCH --job-name=zh_full
#SBATCH --partition=LocalQ
#SBATCH --nodes=1
#SBATCH --gres=gpu:2
#SBATCH --cpus-per-task=16
#SBATCH --mem=128G
#SBATCH --time=12:00:00
set -euo pipefail
ROOT=/home/guojingli3/cnss_external_benchmarks_20260921
export HF_HOME=$ROOT/hf_cache
export HF_HUB_CACHE=$ROOT/hf_cache/hub
export PYTHONNOUSERSITE=1
PY=$ROOT/env/bin/python
LOG=$ROOT/logs/chinese_full
mkdir -p $ROOT/logs
exec > >(tee -a "$LOG.out") 2> >(tee -a "$LOG.err" >&2)
echo "[start] $(date -Is) CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"
i=0
for MODEL_SHORT in xlm-roberta-large esco-xlm-roberta-large; do
  for SEED in 42 43 44; do
    case $MODEL_SHORT in
      xlm-roberta-large) MODEL=FacebookAI/xlm-roberta-large ;;
      *) MODEL=jjzha/esco-xlm-roberta-large ;;
    esac
    REV=$($PY -c "import json; d={r['model']:r['revision'] for r in json.load(open('$ROOT/models.json'))}; print(d['$MODEL'])")
    OUT=$ROOT/runs/chinese/full/$MODEL_SHORT/$SEED
    if [ -f "$OUT/result.json" ]; then
      echo "[skip] $OUT"
      continue
    fi
    rm -rf "$OUT"
    GPU=$((i % 2))
    echo "[start] gpu=$GPU $MODEL_SHORT $SEED"
    CUDA_VISIBLE_DEVICES=$GPU $PY $ROOT/run_chinese_encoder.py --model "$MODEL" --revision "$REV" --seed "$SEED" --output "$OUT" \
      > $ROOT/logs/chinese_full_${MODEL_SHORT}_${SEED}.out 2>&1 &
    i=$((i+1))
    if [ $((i % 2)) -eq 0 ]; then wait; fi
  done
done
wait
echo "[done] $(date -Is)"
