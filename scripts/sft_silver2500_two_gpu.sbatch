#!/bin/bash
#SBATCH --job-name=qwen_s2500_42_43
#SBATCH --partition=LocalQ
#SBATCH --nodes=1
#SBATCH --ntasks=2
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH --time=12:00:00
#SBATCH --gres=gpu:2
#SBATCH --output=/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/qwen_silver2500_sft_20260914/logs/sft_42_43_%j.out
#SBATCH --error=/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/qwen_silver2500_sft_20260914/logs/sft_42_43_%j.err

# Two seeds on two GPUs. Do not start a third worker. Account MaxJobs=1 / MaxWall=12h.
# GRES on this node does not track occupancy; bind to the two cards with most free memory.
set -euo pipefail
PAPER=/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper
ROOT=$PAPER/output/qwen_silver2500_sft_20260914
PY=/opt/anaconda3/envs/jpy-qwen25/bin/python
SEED_A="${SEED_A:-42}"
SEED_B="${SEED_B:-43}"
MIN_FREE_MIB="${MIN_FREE_MIB:-60000}"
mkdir -p "$ROOT/logs"
export TRANSFORMERS_OFFLINE=1 HF_HUB_OFFLINE=1 TOKENIZERS_PARALLELISM=false PYTHONUNBUFFERED=1
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

echo "[host] $(hostname) date=$(date -Is) job=${SLURM_JOB_ID:-na}"
echo "[slurm] JOB_GPUS=${SLURM_JOB_GPUS:-} CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-}"
scontrol show job "$SLURM_JOB_ID" | head -20
nvidia-smi --query-gpu=index,uuid,memory.used,memory.free,utilization.gpu --format=csv

mapfile -t IDLE < <(nvidia-smi --query-gpu=index,memory.free --format=csv,noheader,nounits \
  | awk -F',' '{gsub(/ /,"",$1); gsub(/ /,"",$2); print $2, $1}' \
  | sort -nr | awk -v m="$MIN_FREE_MIB" '$1>=m {print $2}')

echo "[idle_ok] ${IDLE[*]:-}"
if [ "${#IDLE[@]}" -lt 2 ]; then
  echo "[fatal] need 2 GPUs with >= ${MIN_FREE_MIB} MiB free, got ${#IDLE[@]}"
  exit 2
fi
G0=${IDLE[0]}
G1=${IDLE[1]}
echo "[bind] seed ${SEED_A} -> GPU ${G0}; seed ${SEED_B} -> GPU ${G1}"
echo "seed${SEED_A}=${G0} seed${SEED_B}=${G1} $(date -Is)" >> "$ROOT/logs/idle_bind_${SLURM_JOB_ID}.txt"

# Do not srun --gres=gpu:1 (it can rewrite CUDA_VISIBLE_DEVICES onto a busy GRES card).
set +e
CUDA_VISIBLE_DEVICES="$G0" "$PY" -u "$PAPER/scripts/train_qwen_silver2500_sft.py" --seed "$SEED_A" \
  > "$ROOT/logs/seed${SEED_A}_${SLURM_JOB_ID}.log" 2>&1 &
pid_a=$!
CUDA_VISIBLE_DEVICES="$G1" "$PY" -u "$PAPER/scripts/train_qwen_silver2500_sft.py" --seed "$SEED_B" \
  > "$ROOT/logs/seed${SEED_B}_${SLURM_JOB_ID}.log" 2>&1 &
pid_b=$!
wait $pid_a
ec_a=$?
wait $pid_b
ec_b=$?
set -e
nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv
echo "[done] seed${SEED_A}=$ec_a seed${SEED_B}=$ec_b"
exit $(( ec_a != 0 || ec_b != 0 ? 1 : 0 ))
