#!/usr/bin/env bash
# Submit Silver-2500 Qwen LoRA via Slurm: 2-GPU job (seeds 42/43), then 1-GPU seed 44.
# Do not occupy 3 GPUs interactively. Account MaxJobs=1, MaxWall=12h.
set -euo pipefail
PAPER=/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper
ROOT=$PAPER/output/qwen_silver2500_sft_20260914
mkdir -p "$ROOT/logs"
cd "$PAPER"

if [[ ! -f "$ROOT/MODEL.md" || ! -f "$ROOT/MODEL_PROVENANCE.json" ]]; then
  echo "missing model docs under $ROOT" >&2
  exit 2
fi

running=$(squeue -u "$USER" -h -t R | wc -l)
if [[ "$running" -ge 1 ]]; then
  echo "MaxJobs=1: a job is already running. Queue only." >&2
fi

jid1=$(sbatch --parsable "$PAPER/scripts/sft_silver2500_two_gpu.sbatch")
jid2=$(sbatch --parsable --dependency=afterok:"$jid1" "$PAPER/scripts/sft_silver2500_seed44.sbatch")
jid3=$(sbatch --parsable --dependency=afterok:"$jid2" "$PAPER/scripts/sft_silver2500_summarize.sbatch")
echo "submitted two_gpu=$jid1 seed44=$jid2 summarize=$jid3"
echo "two_gpu=$jid1 seed44=$jid2 summarize=$jid3 $(date -Is)" | tee -a "$ROOT/logs/SLURM_SUBMIT.txt"
squeue -u "$USER"
