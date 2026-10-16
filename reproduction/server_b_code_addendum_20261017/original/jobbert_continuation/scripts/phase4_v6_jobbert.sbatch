#!/bin/bash
#SBATCH --job-name=v6_jobbert
#SBATCH --nodes=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --time=02:00:00
#SBATCH --output=/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/silver_plus_phase4_v6_runs/slurm_%j.out
#SBATCH --error=/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/silver_plus_phase4_v6_runs/slurm_%j.err
# No --gres=gpu. Use idle pair 0+1 or 2+3 only. Two cards at a time.

set -euo pipefail
ROOT="/home/guojingli3/SCESC-LLM-skill-extraction"
PAPER="$ROOT/Chinese_skill_benchmark_Paper"
OUT="$PAPER/output/silver_plus_phase4_v6_runs"
mkdir -p "$OUT"
echo "[host] $(hostname) date=$(date -Is) slurm=${SLURM_JOB_ID:-na}" | tee -a "$OUT/run.log"

GPU=$(ALLOW_SINGLE=0 PAIR_WAIT_SEC=7200 USED_MAX_MIB=4096 bash "$PAPER/scripts/wait_idle_gpu_pair.sh" | tail -n1)
export CUDA_VISIBLE_DEVICES="$GPU"
echo "[gpu] CUDA_VISIBLE_DEVICES=$GPU" | tee -a "$OUT/run.log"
nvidia-smi --query-gpu=index,memory.used,memory.free,utilization.gpu --format=csv | tee -a "$OUT/run.log"
echo "$$ ${SLURM_JOB_ID:-na} $GPU $(date -Is)" > "$OUT/job.txt"
bash "$PAPER/scripts/run_phase4_v6_jobbert12.sh"
echo "[exit] $? $(date -Is)" | tee -a "$OUT/run.log"
