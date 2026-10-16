#!/bin/bash
#SBATCH --job-name=g150qwen
#SBATCH --partition=LocalQ
#SBATCH --nodes=1
#SBATCH --ntasks=2
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=12:00:00
#SBATCH --gres=gpu:2
#SBATCH --output=/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/gold150_shared_prompt_rev2_run_20260910/logs/qwen_%j.out
#SBATCH --error=/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/gold150_shared_prompt_rev2_run_20260910/logs/qwen_%j.err

set -euo pipefail
RUN="/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/gold150_shared_prompt_rev2_run_20260910"
PY="/opt/anaconda3/envs/jpy-qwen25/bin/python"
mkdir -p "$RUN/logs" "$RUN/runs/qwen25-14b-instruct"
echo "[host] $(hostname) date=$(date -Is) job=${SLURM_JOB_ID:-na}" | tee -a "$RUN/logs/qwen_job.log"
echo "[slurm] JOB_GPUS=${SLURM_JOB_GPUS:-} STEP_GPUS=${SLURM_STEP_GPUS:-} CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-}" | tee -a "$RUN/logs/qwen_job.log"
echo "[scontrol]" | tee -a "$RUN/logs/qwen_job.log"
scontrol show job "$SLURM_JOB_ID" | tee -a "$RUN/logs/qwen_job.log"
nvidia-smi --query-gpu=index,uuid,name,memory.used,memory.total,utilization.gpu --format=csv | tee -a "$RUN/logs/qwen_job.log"

# Prefer independent steps so each worker gets one allocated GPU.
set +e
srun --ntasks=1 --exact --gres=gpu:1 --cpu-bind=none \
  "$PY" -u "$RUN/scripts/run_qwen_worker.py" --worker 0 --phase smoke-then-formal \
  > "$RUN/logs/qwen_w0_${SLURM_JOB_ID}.log" 2>&1 &
pid0=$!
srun --ntasks=1 --exact --gres=gpu:1 --cpu-bind=none \
  "$PY" -u "$RUN/scripts/run_qwen_worker.py" --worker 1 --phase smoke-then-formal \
  > "$RUN/logs/qwen_w1_${SLURM_JOB_ID}.log" 2>&1 &
pid1=$!
wait $pid0
ec0=$?
wait $pid1
ec1=$?
set -e
echo "[workers] ec0=$ec0 ec1=$ec1" | tee -a "$RUN/logs/qwen_job.log"
"$PY" -u "$RUN/scripts/merge_qwen_shards.py" | tee -a "$RUN/logs/qwen_job.log"
nvidia-smi --query-gpu=index,uuid,memory.used,utilization.gpu --format=csv | tee -a "$RUN/logs/qwen_job.log"
exit $(( ec0 != 0 || ec1 != 0 ? 1 : 0 ))
