#!/bin/bash
#SBATCH --job-name=van_wwm_v4
#SBATCH --nodes=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --time=11:59:00
#SBATCH --output=/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/vanilla_wwm_v4/slurm_%j.out
#SBATCH --error=/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/vanilla_wwm_v4/slurm_%j.err
# No --gres=gpu. Account MaxJobs=1. Do not nohup. Do not overwrite Gold v2.

set -euo pipefail
ROOT="/home/guojingli3/SCESC-LLM-skill-extraction"
PAPER="$ROOT/Chinese_skill_benchmark_Paper"
OUT="$PAPER/output/vanilla_wwm_v4"
mkdir -p "$OUT" "$PAPER/runs/vanilla_wwm_v4"
echo "[host] $(hostname) date=$(date -Is) slurm=${SLURM_JOB_ID:-na}" | tee -a "$OUT/run.log"

LARGE="$ROOT/Baseline_Models_Collection/chinese-roberta-wwm-ext-large"
if [[ ! -f "$LARGE/config.json" || ( ! -f "$LARGE/pytorch_model.bin" && ! -f "$LARGE/model.safetensors" ) ]]; then
  echo "[download] missing large encoder; fetching on CPU first" | tee -a "$OUT/run.log"
  unset TRANSFORMERS_OFFLINE HF_HUB_OFFLINE
  /opt/anaconda3/envs/adasparse/bin/python3 "$PAPER/scripts/download_cn_roberta_wwm_ext_large.py" 2>&1 | tee -a "$OUT/run.log"
fi

GPU=$(ALLOW_SINGLE=1 PAIR_WAIT_SEC=7200 USED_MAX_MIB=4096 bash "$PAPER/scripts/wait_idle_gpu_pair.sh" | tail -n1)
export CUDA_VISIBLE_DEVICES="$GPU"
echo "[gpu] CUDA_VISIBLE_DEVICES=$GPU" | tee -a "$OUT/run.log"
nvidia-smi --query-gpu=index,memory.used,memory.free,utilization.gpu --format=csv | tee -a "$OUT/run.log"
echo "$$ ${SLURM_JOB_ID:-na} $GPU $(date -Is)" > "$PAPER/runs/vanilla_wwm_v4/job.txt"
bash "$PAPER/scripts/run_vanilla_wwm_v4_crf.sh"
echo "[exit] $? $(date -Is)" | tee -a "$OUT/run.log"
