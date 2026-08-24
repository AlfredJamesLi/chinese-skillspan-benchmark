#!/bin/bash
#SBATCH --job-name=jbzh_3m
#SBATCH --nodes=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=12:00:00
#SBATCH --output=/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/jobbert_zh_3m/slurm_%j.out
#SBATCH --error=/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/jobbert_zh_3m/slurm_%j.err
# No --gres=gpu: wait on CPU until the 1M setsid job finishes, then pick free cards.

set -euo pipefail
PY="${PYTHON:-/opt/anaconda3/envs/adasparse/bin/python3}"
ROOT="/home/guojingli3/SCESC-LLM-skill-extraction"
PAPER="$ROOT/Chinese_skill_benchmark_Paper"
OUT1="$PAPER/output/jobbert_zh_1m"
OUT3="$PAPER/output/jobbert_zh_3m"
mkdir -p "$OUT3"
echo "[host] $(hostname) date=$(date -Is) slurm=$SLURM_JOB_ID" | tee -a "$OUT3/run.log"

# Do not touch GPUs while 1M runner (MLM + CRF) is alive.
WAIT_PID_FILE="$OUT1/run.pid"
echo "[wait] 1M pidfile=$WAIT_PID_FILE $(date -Is)" | tee -a "$OUT3/run.log"
for i in $(seq 1 360); do
  alive=0
  if [[ -f "$WAIT_PID_FILE" ]]; then
    rp=$(cat "$WAIT_PID_FILE" || true)
    if [[ -n "${rp:-}" ]] && kill -0 "$rp" 2>/dev/null; then
      alive=1
    fi
  fi
  if [[ "$alive" -eq 0 ]]; then
    echo "[wait] 1M runner gone $(date -Is)" | tee -a "$OUT3/run.log"
    break
  fi
  if (( i % 5 == 1 )); then
    echo "[wait] 1M still pid=$rp tick=$i $(date -Is)" | tee -a "$OUT3/run.log"
  fi
  sleep 60
done
if [[ -f "$WAIT_PID_FILE" ]]; then
  rp=$(cat "$WAIT_PID_FILE" || true)
  if [[ -n "${rp:-}" ]] && kill -0 "$rp" 2>/dev/null; then
    echo "[wait] timeout: 1M still running" | tee -a "$OUT3/run.log"
    exit 2
  fi
fi

# Score 1M if CRF finished; use recipe if present. Always continue to 3.2M (user queued it).
if [[ -f "$OUT1/crf_v3_seed42/run_summary.json" ]]; then
  "$PY" "$PAPER/scripts/after_jobbert_1m.py" | tee -a "$OUT3/run.log" || true
fi
DEC="$OUT1/decision.json"
INIT="$ROOT/Baseline_Models_Collection/chinese-roberta-wwm-ext"
EPOCHS=3
if [[ -f "$DEC" ]]; then
  INIT=$("$PY" -c 'import json,sys; print(json.load(open(sys.argv[1])).get("init_model"))' "$DEC")
  EPOCHS=$("$PY" -c 'import json,sys; print(json.load(open(sys.argv[1])).get("epochs"))' "$DEC")
elif [[ -f "$OUT1/mlm/encoder/config.json" ]]; then
  INIT="$OUT1/mlm/encoder"
  EPOCHS=2
fi
export INIT_MODEL="$INIT"
export EPOCHS
export OUT_DIR="$OUT3"
export CORPUS="$PAPER/data/jobbert_3m_sents.jsonl"
echo "[recipe] init=$INIT_MODEL epochs=$EPOCHS" | tee -a "$OUT3/run.log"

pick_gpu() {
  "$PY" - << 'PY'
import subprocess, time, sys
for attempt in range(60):
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
        print(f"[gpu-pick] try={attempt} GPU{i} free={free}MiB util={util}%", flush=True)
    ok = [r for r in rows if r[1] >= 20000]
    ok.sort(key=lambda r: (-r[1], r[2]))
    if len(ok) >= 2:
        pair = ",".join(str(r[0]) for r in ok[:2])
        print(f"[gpu-pick] two-card {pair}", flush=True)
        print(pair)
        raise SystemExit
    if ok and attempt >= 5:
        print(f"[gpu-pick] one-card GPU{ok[0][0]}", flush=True)
        print(ok[0][0])
        raise SystemExit
    time.sleep(30)
print("no GPU with >=20GiB free after wait", file=sys.stderr)
raise SystemExit(5)
PY
}

GPU=$(pick_gpu | tail -n1)
export CUDA_VISIBLE_DEVICES="$GPU"
echo "[gpu-pick] CUDA_VISIBLE_DEVICES=$GPU $(date -Is)" | tee -a "$OUT3/run.log"
nvidia-smi --query-gpu=index,memory.used,memory.free,utilization.gpu --format=csv | tee -a "$OUT3/run.log"

bash "$PAPER/scripts/run_jobbert_zh_3m.sh"
echo "[exit] $? $(date -Is)" | tee -a "$OUT3/run.log"
