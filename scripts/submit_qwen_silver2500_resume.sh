#!/usr/bin/env bash
# Queue remaining Silver-2500 Qwen LoRA after job 51056 timeout.
# seed43 already completed; resume seed42 from epoch_5; then seed44; then summarize.
# Account MaxJobs=1 / MaxWall=12h. Do not occupy GPUs interactively.
set -euo pipefail
PAPER=/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper
ROOT=$PAPER/output/qwen_silver2500_sft_20260914
mkdir -p "$ROOT/logs"
cd "$PAPER"

# Drop the afterok chain that can never start, plus a failed wait-less resume.
for j in 51057 51058 51064 51065 51066; do
  if squeue -j "$j" -h >/dev/null 2>&1; then
    scancel "$j" || true
    echo "cancelled $j"
  fi
done

jid1=$(sbatch --parsable "$PAPER/scripts/sft_silver2500_seed42_resume.sbatch")
jid2=$(sbatch --parsable --dependency=afterok:"$jid1" "$PAPER/scripts/sft_silver2500_seed44.sbatch")
jid3=$(sbatch --parsable --dependency=afterok:"$jid2" "$PAPER/scripts/sft_silver2500_summarize.sbatch")
echo "submitted seed42_resume=$jid1 seed44=$jid2 summarize=$jid3"
echo "seed42_resume=$jid1 seed44=$jid2 summarize=$jid3 $(date -Is)" | tee -a "$ROOT/logs/SLURM_SUBMIT.txt"
squeue -u "$USER"
