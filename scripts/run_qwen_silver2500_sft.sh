#!/usr/bin/env bash
# Interactive 3-GPU launch is disabled. Use Slurm (2 GPUs).
set -euo pipefail
echo "Do not occupy 3 GPUs interactively." >&2
echo "Submitting via Slurm: 2-GPU seeds 42/43, then 1-GPU seed 44." >&2
exec bash /home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/scripts/submit_qwen_silver2500_slurm.sh
