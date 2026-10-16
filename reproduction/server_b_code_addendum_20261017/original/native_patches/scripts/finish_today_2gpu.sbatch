#!/bin/bash
#SBATCH --job-name=finish_td
#SBATCH --partition=LocalQ
#SBATCH --nodes=1
#SBATCH --gres=gpu:2
#SBATCH --cpus-per-task=16
#SBATCH --mem=128G
#SBATCH --time=12:00:00
#SBATCH --output=/home/guojingli3/cnss_external_benchmarks_20260921/logs/finish_today.out
#SBATCH --error=/home/guojingli3/cnss_external_benchmarks_20260921/logs/finish_today.err
# Remaining Chinese 4 cells, then native SkillSpan, then Gnehm ICT.
# Do NOT use `exec > >(tee)` plus bare `wait`: that hung job 8540 on the tee PIDs.
set -u
ROOT=/home/guojingli3/cnss_external_benchmarks_20260921
export HF_HOME=$ROOT/hf_cache
export HF_HUB_CACHE=$ROOT/hf_cache/hub
export TRANSFORMERS_CACHE=$ROOT/hf_cache/hub
export TOKENIZERS_PARALLELISM=false
export PYTHONNOUSERSITE=1
PY=$ROOT/env/bin/python
mkdir -p $ROOT/logs
echo "[finish_today start] $(date -Is) CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-unset} host=$(hostname)"
"$PY" "$ROOT/scripts/run_remaining_today.py" --workers 2 --retries 3
rc=$?
echo "[run_remaining_today rc=$rc] $(date -Is)"
"$PY" "$ROOT/scripts/emit_verified_results.py" || true
echo "[finish_today done] $(date -Is)"
exit $rc
