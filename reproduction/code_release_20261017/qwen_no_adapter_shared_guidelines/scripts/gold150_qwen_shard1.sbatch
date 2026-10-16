#!/bin/bash
#SBATCH --job-name=g150qw1
#SBATCH --partition=LocalQ
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --time=12:00:00
#SBATCH --gres=gpu:1
#SBATCH --output=/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/gold150_shared_prompt_rev2_run_20260910/logs/qwen_shard1_%j.out
#SBATCH --error=/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/gold150_shared_prompt_rev2_run_20260910/logs/qwen_shard1_%j.err

# Resume shard 1 only. Job 50966 worker1 OOM on allocated GPU 1 (other process ~59GiB).
# Do not pick unallocated GPUs. Wait for a free allocated card.
set -euo pipefail
RUN="/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/gold150_shared_prompt_rev2_run_20260910"
PY="/opt/anaconda3/envs/jpy-qwen25/bin/python"
mkdir -p "$RUN/logs"
echo "[host] $(hostname) date=$(date -Is) job=${SLURM_JOB_ID:-na} shard=1" | tee -a "$RUN/logs/qwen_job.log"
echo "[slurm] JOB_GPUS=${SLURM_JOB_GPUS:-} CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-}" | tee -a "$RUN/logs/qwen_job.log"
scontrol show job "$SLURM_JOB_ID" | tee -a "$RUN/logs/qwen_job.log"
nvidia-smi --query-gpu=index,uuid,memory.used,memory.total --format=csv | tee -a "$RUN/logs/qwen_job.log"
"$PY" -u "$RUN/scripts/run_qwen_worker.py" --worker 1 --phase smoke-then-formal
"$PY" -u "$RUN/scripts/merge_qwen_shards.py"
