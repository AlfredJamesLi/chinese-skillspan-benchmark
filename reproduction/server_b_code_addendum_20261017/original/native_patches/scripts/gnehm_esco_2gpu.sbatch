#!/bin/bash
#SBATCH --job-name=gnehm_esco
#SBATCH --partition=LocalQ
#SBATCH --nodes=1
#SBATCH --gres=gpu:2
#SBATCH --cpus-per-task=16
#SBATCH --mem=128G
#SBATCH --time=12:00:00
#SBATCH --output=/home/guojingli3/cnss_external_benchmarks_20260921/logs/gnehm_esco.out
#SBATCH --error=/home/guojingli3/cnss_external_benchmarks_20260921/logs/gnehm_esco.err
# Retry the 5 Gnehm ICT ESCOXLM-R native cells after adding batching.shuffle.
set -u
ROOT=/home/guojingli3/cnss_external_benchmarks_20260921
export HF_HOME=$ROOT/hf_cache
export HF_HUB_CACHE=$ROOT/hf_cache/hub
export TRANSFORMERS_CACHE=$ROOT/hf_cache/hub
export TOKENIZERS_PARALLELISM=false
export PYTHONNOUSERSITE=1
PY=$ROOT/env/bin/python
mkdir -p $ROOT/logs
echo "[gnehm_esco start] $(date -Is) CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-unset}"
"$PY" "$ROOT/scripts/run_remaining_today.py" --workers 2 --retries 3 --skip-chinese --skip-native
rc=$?
echo "[run_remaining_today rc=$rc] $(date -Is)"
"$PY" "$ROOT/scripts/emit_verified_results.py" || true
echo "[gnehm_esco done] $(date -Is)"
exit $rc
