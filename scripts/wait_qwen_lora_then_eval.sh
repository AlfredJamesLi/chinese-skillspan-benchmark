#!/usr/bin/env bash
# After Qwen LoRA SFT reaches 4365 steps, eval adapter on P2 2601.
# Does not overwrite Instruct preds. Does not write confirmed-results.md.
set -euo pipefail
PAPER="/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper"
OUT="/home/guojingli3/SCESC-LLM-skill-extraction/LLaMA-Factory/saves/qwen2_5_14b/lora/sft_lskt_v4_sop_extract"
LOG="$PAPER/reports/sft_lskt_v4_sop_extract.wait_eval.log"
EVAL_LOG="$PAPER/reports/qwen25_14b_lskt_v4_lora_sopv4_p2_2601.run.log"
PY="/opt/anaconda3/envs/LGJ_LLM_SE_Baseline_new/bin/python"
mkdir -p "$PAPER/reports"
echo "WAIT_EVAL start $(date -Is) pid=$$" | tee -a "$LOG"
sleep 180

last_step() {
  "$PY" - <<'PY'
import json
from pathlib import Path
p = Path("/home/guojingli3/SCESC-LLM-skill-extraction/LLaMA-Factory/saves/qwen2_5_14b/lora/sft_lskt_v4_sop_extract/trainer_log.jsonl")
step = 0
if p.is_file():
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        step = int(row.get("current_steps") or 0)
print(step)
PY
}

sft_running() {
  pgrep -f 'qwen25_14b_lskt_v4_sop_extract.yaml' >/dev/null
}

pick_adapter() {
  if [[ -f "$OUT/adapter_model.safetensors" ]]; then
    echo "$OUT"
    return
  fi
  latest=""
  local d n best=0
  for d in "$OUT"/checkpoint-*; do
    [[ -d "$d" && -f "$d/adapter_model.safetensors" ]] || continue
    n="${d##*-}"
    if [[ "$n" =~ ^[0-9]+$ ]] && (( n > best )); then
      best=$n
      latest=$d
    fi
  done
  echo "$latest"
}

while true; do
  step="$(last_step)"
  if sft_running; then
    echo "$(date -Is) still_training step=$step" >> "$LOG"
    sleep 60
    continue
  fi
  echo "$(date -Is) sft_process_gone step=$step" | tee -a "$LOG"
  if [[ "$step" != "4365" ]]; then
    echo "ABORT eval: expected 4365 steps, got $step" | tee -a "$LOG"
    exit 1
  fi
  adapter="$(pick_adapter)"
  if [[ -z "$adapter" || ! -f "$adapter/adapter_model.safetensors" ]]; then
    echo "ABORT eval: no adapter_model.safetensors" | tee -a "$LOG"
    exit 1
  fi
  echo "EVAL adapter=$adapter GPU=2 $(date -Is)" | tee -a "$LOG"
  cd "$PAPER"
  setsid env CUDA_VISIBLE_DEVICES=2 PYTHONNOUSERSITE=1 PYTHONUNBUFFERED=1 \
    "$PY" -u scripts/run_qwen25_sopv4_p2_2601.py \
      --skip-smoke-continue \
      --adapter "$adapter" \
      --run-name qwen25_14b_lskt_v4_lora_sopv4_p2_2601 \
    >> "$EVAL_LOG" 2>&1 < /dev/null &
  echo "eval_pid=$!" | tee -a "$LOG"
  exit 0
done
