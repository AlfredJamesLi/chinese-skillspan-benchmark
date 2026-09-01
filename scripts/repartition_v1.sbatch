#!/bin/bash
#SBATCH --job-name=rep_v1_crf
#SBATCH --nodes=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --time=11:59:00
#SBATCH --output=/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/repartition_v1/slurm_%j.out
#SBATCH --error=/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/repartition_v1/slurm_%j.err
# No --gres=gpu. Account MaxJobs=1. Do not nohup.

set -euo pipefail
ROOT="/home/guojingli3/SCESC-LLM-skill-extraction"
PAPER="$ROOT/Chinese_skill_benchmark_Paper"
OUT="$PAPER/output/repartition_v1"
mkdir -p "$OUT" "$PAPER/runs/repartition_v1"
echo "[host] $(hostname) date=$(date -Is) slurm=${SLURM_JOB_ID:-na}" | tee -a "$OUT/run.log"

GPU=$(ALLOW_SINGLE=1 PAIR_WAIT_SEC=7200 USED_MAX_MIB=4096 bash "$PAPER/scripts/wait_idle_gpu_pair.sh" | tail -n1)
export CUDA_VISIBLE_DEVICES="$GPU"
echo "[gpu] CUDA_VISIBLE_DEVICES=$GPU" | tee -a "$OUT/run.log"
nvidia-smi --query-gpu=index,memory.used,memory.free,utilization.gpu --format=csv | tee -a "$OUT/run.log"

echo "$$ ${SLURM_JOB_ID:-na} $GPU $(date -Is)" > "$PAPER/runs/repartition_v1/job.txt"
SMOKE=0 bash "$PAPER/scripts/run_repartition_v1_crf.sh"
echo "[exit] $? $(date -Is)" | tee -a "$OUT/run.log"
