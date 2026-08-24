#!/bin/bash
#SBATCH --job-name=jbzh_domain1m
#SBATCH --nodes=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=11:59:00
#SBATCH --output=/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/jobbert_zh_domain_1m/slurm_%j.out
#SBATCH --error=/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/jobbert_zh_domain_1m/slurm_%j.err
# Do not set --gres=gpu: LocalQ can pin cards already used by other users.
# Two-GPU DDP only on an idle legal pair (0+1 or 2+3). Never stack.
# Account MaxJobs=1: this job waits behind hyb_panelB / aseries_rest if queued.

set -euo pipefail
PY="${PYTHON:-/opt/anaconda3/envs/adasparse/bin/python3}"
ROOT="/home/guojingli3/SCESC-LLM-skill-extraction"
PAPER="$ROOT/Chinese_skill_benchmark_Paper"
OUT="$PAPER/output/jobbert_zh_domain_1m"
mkdir -p "$OUT"
echo "[host] $(hostname) date=$(date -Is) slurm=${SLURM_JOB_ID:-na}" | tee -a "$OUT/run.log"

# Local waiter already owns this experiment when MaxJobs blocked sbatch.
if [[ -f "$OUT/wait_then_run.pid" ]]; then
  wpid=$(cat "$OUT/wait_then_run.pid" || true)
  if [[ -n "${wpid:-}" ]] && kill -0 "$wpid" 2>/dev/null; then
    echo "[skip] local waiter pid=$wpid already running; not stacking" | tee -a "$OUT/run.log"
    exit 0
  fi
fi

if [[ -f "$OUT/corpus_prep.pid" ]]; then
  ppid=$(cat "$OUT/corpus_prep.pid" || true)
  while [[ -n "${ppid:-}" ]] && kill -0 "$ppid" 2>/dev/null; do
    echo "[wait] corpus_prep pid=$ppid still running $(date -Is)" | tee -a "$OUT/run.log"
    sleep 30
  done
fi

# Prefer idle 0+1 or 2+3. After 5 min, one idle card. Do not stack.
GPU=$(USED_MAX_MIB=4096 PAIR_WAIT_SEC=300 ALLOW_SINGLE=1 \
  bash "$PAPER/scripts/wait_idle_gpu_pair.sh" | tail -n1)
export CUDA_VISIBLE_DEVICES="$GPU"
export OUT_DIR="$OUT"
export CORPUS="$PAPER/data/jobbert_domain_mix_1m_sents.jsonl"
export CORPUS_N=1000000
export INIT_MODEL="$ROOT/Baseline_Models_Collection/chinese-roberta-wwm-ext"
export EPOCHS=3
echo "[gpu-pick] CUDA_VISIBLE_DEVICES=$GPU" | tee -a "$OUT/run.log"
nvidia-smi --query-gpu=index,memory.used,memory.free,utilization.gpu --format=csv | tee -a "$OUT/run.log"

bash "$PAPER/scripts/run_jobbert_zh_domain_1m.sh"
echo "[exit] $? $(date -Is)" | tee -a "$OUT/run.log"
