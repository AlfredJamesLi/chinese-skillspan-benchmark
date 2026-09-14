#!/bin/bash
#SBATCH --job-name=qwen_s2500_42r
#SBATCH --partition=LocalQ
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=12:00:00
#SBATCH --gres=gpu:1
#SBATCH --output=/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/qwen_silver2500_sft_20260914/logs/sft_42r_%j.out
#SBATCH --error=/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/qwen_silver2500_sft_20260914/logs/sft_42r_%j.err

# Resume seed 42 from epoch_5 adapter (job 51056 timed out). One GPU.
# Remaining 1 epoch; lr matches the late-schedule value logged at step 720.
set -euo pipefail
PAPER=/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper
ROOT=$PAPER/output/qwen_silver2500_sft_20260914
PY=/opt/anaconda3/envs/jpy-qwen25/bin/python
MIN_FREE_MIB="${MIN_FREE_MIB:-60000}"
mkdir -p "$ROOT/logs"
export TRANSFORMERS_OFFLINE=1 HF_HUB_OFFLINE=1 TOKENIZERS_PARALLELISM=false PYTHONUNBUFFERED=1
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

echo "[host] $(hostname) date=$(date -Is) job=${SLURM_JOB_ID:-na}"
echo "[slurm] JOB_GPUS=${SLURM_JOB_GPUS:-} CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-}"
scontrol show job "$SLURM_JOB_ID" | head -20
nvidia-smi --query-gpu=index,memory.used,memory.free,utilization.gpu --format=csv

mapfile -t IDLE < <(nvidia-smi --query-gpu=index,memory.free --format=csv,noheader,nounits \
  | awk -F',' '{gsub(/ /,"",$1); gsub(/ /,"",$2); print $2, $1}' \
  | sort -nr | awk -v m="$MIN_FREE_MIB" '$1>=m {print $2}')
WAIT_SEC=60
while [ "${#IDLE[@]}" -lt 1 ]; do
  echo "[wait] no GPU with >= ${MIN_FREE_MIB} MiB free; sleep ${WAIT_SEC}s $(date -Is)"
  nvidia-smi --query-gpu=index,memory.used,memory.free,utilization.gpu --format=csv
  sleep "$WAIT_SEC"
  mapfile -t IDLE < <(nvidia-smi --query-gpu=index,memory.free --format=csv,noheader,nounits \
    | awk -F',' '{gsub(/ /,"",$1); gsub(/ /,"",$2); print $2, $1}' \
    | sort -nr | awk -v m="$MIN_FREE_MIB" '$1>=m {print $2}')
done
G0=${IDLE[0]}
echo "[bind] seed 42 resume -> GPU ${G0}"
CUDA_VISIBLE_DEVICES="$G0" "$PY" -u "$PAPER/scripts/train_qwen_silver2500_sft.py" \
  --seed 42 --resume --lr 1.67e-5
