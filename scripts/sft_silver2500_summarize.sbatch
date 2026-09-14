#!/bin/bash
#SBATCH --job-name=qwen_s2500_sum
#SBATCH --partition=LocalQ
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=00:20:00
#SBATCH --output=/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/qwen_silver2500_sft_20260914/logs/summarize_%j.out
#SBATCH --error=/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/qwen_silver2500_sft_20260914/logs/summarize_%j.err

set -euo pipefail
PAPER=/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper
PY=/opt/anaconda3/envs/jpy-qwen25/bin/python
"$PY" -u "$PAPER/scripts/summarize_qwen_silver2500_sft.py"
