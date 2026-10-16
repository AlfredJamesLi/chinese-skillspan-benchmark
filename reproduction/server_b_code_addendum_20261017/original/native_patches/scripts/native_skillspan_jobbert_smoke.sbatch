#!/bin/bash
#SBATCH --job-name=ss_smoke
#SBATCH --partition=LocalQ
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --time=04:00:00
# Native SkillSpan JobBERT skills smoke: 1 seed, patched MaChAmp path, 1-epoch config copy.
set -euo pipefail
ROOT=/home/guojingli3/cnss_external_benchmarks_20260921
SS=$ROOT/upstream_full/SkillSpan
export HF_HOME=$ROOT/hf_cache
export HF_HUB_CACHE=$ROOT/hf_cache/hub
export PYTHONNOUSERSITE=1
if [ -n "${GPU:-}" ]; then export CUDA_VISIBLE_DEVICES=$GPU; fi
PY=$ROOT/env/bin/python
OUT=$ROOT/runs/native_smoke/skillspan_jobbert_skills_3477689
mkdir -p "$OUT" $ROOT/logs $ROOT/patches/skillspan_smoke
# 1-epoch copy of jobbert.json for smoke only; full runs use original 20 epochs.
python3 - << 'PY'
from pathlib import Path
src=Path("/home/guojingli3/cnss_external_benchmarks_20260921/upstream_full/SkillSpan/configs/jobbert.json")
dst=Path("/home/guojingli3/cnss_external_benchmarks_20260921/patches/skillspan_smoke/jobbert.1epoch.json")
t=src.read_text().replace('"num_epochs": 20','"num_epochs": 1')
dst.write_text(t)
PY
LOG=$ROOT/logs/native_skillspan_jobbert_skills_smoke
cd "$SS"
exec > >(tee -a "$LOG.out") 2> >(tee -a "$LOG.err" >&2)
echo "[start] $(date -Is) gpu=$CUDA_VISIBLE_DEVICES"
"$PY" "$SS/machamp/train.py" \
  --dataset_configs "$SS/configs/skills.json" \
  --parameters_config "$ROOT/patches/skillspan_smoke/jobbert.1epoch.json" \
  --name skill.jobbert.skills.smoke.3477689 \
  --seed 3477689
echo "[done] $(date -Is)"
