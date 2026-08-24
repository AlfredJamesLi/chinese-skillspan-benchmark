#!/bin/bash
#SBATCH --job-name=jbzh_1m
#SBATCH --nodes=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=12:00:00
#SBATCH --output=/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/jobbert_zh_1m/slurm_%j.out
#SBATCH --error=/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/jobbert_zh_1m/slurm_%j.err
# Do not set --gres=gpu: LocalQ can pin cards already used by other users.

set -euo pipefail
ROOT="/home/guojingli3/SCESC-LLM-skill-extraction"
PAPER="$ROOT/Chinese_skill_benchmark_Paper"
OUT="$PAPER/output/jobbert_zh_1m"
mkdir -p "$OUT"
echo "[host] $(hostname) date=$(date -Is) slurm=$SLURM_JOB_ID" | tee -a "$OUT/run.log"

# Prefer two cards with >=20GiB free (RoBERTa-base MLM). Fallback: one empty card.
pick_gpu() {
  python3 - << 'PY'
import subprocess
rows = []
for i in range(4):
    q = subprocess.check_output(
        ["nvidia-smi", "-i", str(i),
         "--query-gpu=memory.free,utilization.gpu",
         "--format=csv,noheader,nounits"],
        text=True,
    ).strip().replace(" ", "")
    free, util = [int(x) for x in q.split(",")]
    rows.append((i, free, util))
    print(f"[gpu-pick] GPU{i} free={free}MiB util={util}%", flush=True)
ok = [r for r in rows if r[1] >= 20000]
ok.sort(key=lambda r: (-r[1], r[2]))
if len(ok) >= 2:
    pair = ",".join(str(r[0]) for r in ok[:2])
    print(f"[gpu-pick] two-card {pair}", flush=True)
    print(pair)
    raise SystemExit
if ok:
    print(f"[gpu-pick] one-card GPU{ok[0][0]}", flush=True)
    print(ok[0][0])
    raise SystemExit
raise SystemExit("no GPU with >=20GiB free")
PY
}

GPU=$(pick_gpu | tail -n1)
export CUDA_VISIBLE_DEVICES="$GPU"
echo "[gpu-pick] CUDA_VISIBLE_DEVICES=$GPU" | tee -a "$OUT/run.log"
nvidia-smi --query-gpu=index,memory.used,memory.free,utilization.gpu --format=csv | tee -a "$OUT/run.log"

bash "$PAPER/scripts/run_jobbert_zh_1m.sh"
echo "[exit] $? $(date -Is)" | tee -a "$OUT/run.log"
