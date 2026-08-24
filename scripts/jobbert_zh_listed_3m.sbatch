#!/bin/bash
#SBATCH --job-name=jbzh_listed3m
#SBATCH --nodes=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=96G
#SBATCH --time=18:00:00
#SBATCH --output=/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/jobbert_zh_listed_3m/slurm_%j.out
#SBATCH --error=/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/jobbert_zh_listed_3m/slurm_%j.err
# Do not set --gres=gpu. Two-GPU DDP only on idle 0+1 or 2+3.

set -euo pipefail
PY="${PYTHON:-/opt/anaconda3/envs/adasparse/bin/python3}"
ROOT="/home/guojingli3/SCESC-LLM-skill-extraction"
PAPER="$ROOT/Chinese_skill_benchmark_Paper"
OUT1="$PAPER/output/jobbert_zh_listed_1m"
OUT3="$PAPER/output/jobbert_zh_listed_3m"
mkdir -p "$OUT3"
echo "[host] $(hostname) date=$(date -Is) slurm=$SLURM_JOB_ID" | tee -a "$OUT3/run.log"

YEARLY="$PAPER/chineseskillspan-jobert-pretrain/上市公司招聘大数据2014-2026.3/分年份保存数据"
if [[ ! -f "$YEARLY/上市公司招聘数据2026.csv" ]]; then
  bash "$PAPER/scripts/extract_listed_yearly_csvs.sh" 2>&1 | tee -a "$OUT3/run.log"
fi

# Optional: warm-start MLM from listed 1M encoder if that run finished.
INIT="$ROOT/Baseline_Models_Collection/chinese-roberta-wwm-ext"
EPOCHS=3
if [[ -f "$OUT1/mlm/encoder/config.json" ]]; then
  INIT="$OUT1/mlm/encoder"
  EPOCHS=2
  echo "[recipe] warm-start from listed 1M encoder" | tee -a "$OUT3/run.log"
fi

# Prefer idle 0+1 or 2+3 for DDP. After 5 min, one idle card. Do not stack.
GPU=$(USED_MAX_MIB=4096 PAIR_WAIT_SEC=300 ALLOW_SINGLE=1 \
  bash "$PAPER/scripts/wait_idle_gpu_pair.sh" | tail -n1)
export CUDA_VISIBLE_DEVICES="$GPU"
export OUT_DIR="$OUT3"
export CORPUS="$PAPER/data/jobbert_listed_mix_3m_sents.jsonl"
export CORPUS_N=3000000
export INIT_MODEL="$INIT"
export EPOCHS="$EPOCHS"
echo "[gpu-pick] CUDA_VISIBLE_DEVICES=$GPU init=$INIT epochs=$EPOCHS" | tee -a "$OUT3/run.log"

bash "$PAPER/scripts/run_jobbert_zh_listed_3m.sh"
echo "[exit] $? $(date -Is)" | tee -a "$OUT3/run.log"
