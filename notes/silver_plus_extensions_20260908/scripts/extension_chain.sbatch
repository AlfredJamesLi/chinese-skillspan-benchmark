#!/bin/bash
#SBATCH --job-name=ext_silver
#SBATCH --partition=LocalQ
#SBATCH --nodes=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=96G
#SBATCH --gres=gpu:2
#SBATCH --account=student
#SBATCH --time=12:00:00
#SBATCH --output=/home/guojingli3/Chinese-Skillspan-Benchmark/Chinese_skill_benchmark_Paper/output/silver_plus_extensions/logs/slurm_%j.out
#SBATCH --error=/home/guojingli3/Chinese-Skillspan-Benchmark/Chinese_skill_benchmark_Paper/output/silver_plus_extensions/logs/slurm_%j.err
# Two GPUs via Slurm GRES. Use CUDA_VISIBLE_DEVICES; do not hardcode physical 2/3.

set -euo pipefail
mkdir -p /home/guojingli3/Chinese-Skillspan-Benchmark/Chinese_skill_benchmark_Paper/output/silver_plus_extensions/logs
echo "[slurm] job=${SLURM_JOB_ID:-na} host=$(hostname) date=$(date -Is) CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-unset}"
nvidia-smi --query-gpu=index,name,memory.total,memory.used,utilization.gpu --format=csv
bash /home/guojingli3/Chinese-Skillspan-Benchmark/Chinese_skill_benchmark_Paper/scripts/run_extension_chain.sh
echo "[slurm_exit] $? $(date -Is)"
