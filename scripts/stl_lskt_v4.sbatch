#!/bin/bash
#SBATCH --job-name=stl_lskt_v4
#SBATCH --nodes=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --time=11:59:00
#SBATCH --output=/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/stl_v4/jobbert_zh_1m/seed42/slurm_%j.out
#SBATCH --error=/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/stl_v4/jobbert_zh_1m/seed42/slurm_%j.err
# Do not set --gres=gpu: LocalQ can pin cards already used by other users.
# Account MaxJobs=1. Do not nohup this trainer; the 2026-08-27 nohup run was Killed.

set -euo pipefail
ROOT="/home/guojingli3/SCESC-LLM-skill-extraction"
PAPER="$ROOT/Chinese_skill_benchmark_Paper"
OUT="$PAPER/output/stl_v4/jobbert_zh_1m/seed42"
mkdir -p "$OUT"
echo "[host] $(hostname) date=$(date -Is) slurm=${SLURM_JOB_ID:-na}" | tee -a "$OUT/run.log"

GPU=$(ALLOW_SINGLE=1 PAIR_WAIT_SEC=7200 USED_MAX_MIB=4096 bash "$PAPER/scripts/wait_idle_gpu_pair.sh" | tail -n1)
export CUDA_VISIBLE_DEVICES="$GPU"
echo "[gpu] CUDA_VISIBLE_DEVICES=$GPU" | tee -a "$OUT/run.log"
nvidia-smi --query-gpu=index,memory.used,memory.free,utilization.gpu --format=csv | tee -a "$OUT/run.log"

bash "$PAPER/scripts/run_jobbert_zh_1m_stl_lskt_v4.sh"
echo "[exit] $? $(date -Is)" | tee -a "$OUT/run.log"
