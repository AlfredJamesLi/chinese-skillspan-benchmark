#!/usr/bin/env bash
# Wait for 1M CRF, score it, then launch 3.2M if decision.json says so.
# Corpus prep is started separately. Does not write paper numbers.
set -euo pipefail
PY="${PYTHON:-/opt/anaconda3/envs/adasparse/bin/python3}"
ROOT="/home/guojingli3/SCESC-LLM-skill-extraction"
PAPER="$ROOT/Chinese_skill_benchmark_Paper"
OUT1="$PAPER/output/jobbert_zh_1m"
OUT3="$PAPER/output/jobbert_zh_3m"
CORPUS="$PAPER/data/jobbert_3m_sents.jsonl"
META="$PAPER/data/jobbert_3m_sents.meta.json"
WAITLOG="$OUT1/wait_then_3m.log"
mkdir -p "$OUT1" "$OUT3"
echo "[wait] start $(date -Is)" | tee -a "$WAITLOG"

CRF="$OUT1/crf_v3_seed42/run_summary.json"
PIDFILE="$OUT1/run.pid"
while [[ ! -f "$CRF" ]]; do
  if [[ -f "$PIDFILE" ]]; then
    rp=$(cat "$PIDFILE" || true)
    if [[ -n "${rp:-}" ]] && ! kill -0 "$rp" 2>/dev/null; then
      if [[ ! -f "$CRF" ]]; then
        echo "[wait] 1M runner pid $rp dead and no CRF summary $(date -Is)" | tee -a "$WAITLOG"
        exit 2
      fi
    fi
  fi
  sleep 60
done
echo "[wait] 1M CRF ready $(date -Is)" | tee -a "$WAITLOG"

"$PY" "$PAPER/scripts/after_jobbert_1m.py" | tee -a "$WAITLOG"
DEC="$OUT1/decision.json"
if [[ ! -f "$DEC" ]]; then
  echo "[wait] no decision.json" | tee -a "$WAITLOG"
  exit 3
fi
LAUNCH=$("$PY" -c 'import json,sys; print(json.load(open(sys.argv[1])).get("launch_3m"))' "$DEC")
INIT=$("$PY" -c 'import json,sys; print(json.load(open(sys.argv[1])).get("init_model"))' "$DEC")
EPOCHS=$("$PY" -c 'import json,sys; print(json.load(open(sys.argv[1])).get("epochs"))' "$DEC")
echo "[wait] launch_3m=$LAUNCH init=$INIT epochs=$EPOCHS" | tee -a "$WAITLOG"

if [[ "$LAUNCH" != "True" ]]; then
  echo "[wait] not launching 3M. Corpus stays at $CORPUS" | tee -a "$WAITLOG"
  exit 0
fi

echo "[wait] waiting for 3.2M corpus $META" | tee -a "$WAITLOG"
for i in $(seq 1 180); do
  if [[ -f "$META" && -s "$CORPUS" ]]; then
    break
  fi
  sleep 30
done
if [[ ! -f "$META" ]]; then
  echo "[wait] 3.2M corpus not ready after 90min" | tee -a "$WAITLOG"
  exit 4
fi
echo "[wait] corpus ready $(date -Is) n=$(wc -l < "$CORPUS")" | tee -a "$WAITLOG"

# Pick two cards with >=20GiB free (same rule as 1M).
GPUS=$("$PY" - << 'PY'
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
    print("PAIR", ",".join(str(r[0]) for r in ok[:2]), flush=True)
elif ok:
    print("PAIR", ok[0][0], flush=True)
else:
    raise SystemExit("no GPU with >=20GiB free")
PY
)
PAIR=$(echo "$GPUS" | awk '/^PAIR /{print $2; exit}')
echo "$GPUS" | tee -a "$WAITLOG"
if [[ -z "${PAIR:-}" ]]; then
  echo "[wait] no GPU pair" | tee -a "$WAITLOG"
  exit 5
fi
export CUDA_VISIBLE_DEVICES="$PAIR"
export INIT_MODEL="$INIT"
export EPOCHS="$EPOCHS"
export CORPUS
export OUT_DIR="$OUT3"
echo "[wait] launching 3M on GPU=$PAIR $(date -Is)" | tee -a "$WAITLOG"
setsid bash "$PAPER/scripts/run_jobbert_zh_3m.sh" </dev/null >>"$OUT3/launch.out" 2>&1 &
echo $! > "$OUT3/launch.pid"
echo "[wait] 3M launch.pid=$(cat "$OUT3/launch.pid")" | tee -a "$WAITLOG"
sleep 8
tail -n 20 "$OUT3/run.log" 2>/dev/null | tee -a "$WAITLOG" || true
echo "[wait] handed off $(date -Is)" | tee -a "$WAITLOG"
