#!/usr/bin/env bash
# Train JobBERT-zh 3M CRF student on public-API Silver-2500; score Gold150.
# Does not overwrite v6a weights or confirmed-results.
set -euo pipefail
export TRANSFORMERS_OFFLINE=1 HF_HUB_OFFLINE=1 TOKENIZERS_PARALLELISM=false PYTHONUNBUFFERED=1
export PYTHONPATH="/home/guojingli3/SCESC-LLM-skill-extraction/Baseline_Models_Collection/pytorch-crf:${PYTHONPATH:-}"
PY="${PYTHON:-/opt/anaconda3/envs/adasparse/bin/python3}"
ROOT="/home/guojingli3/SCESC-LLM-skill-extraction"
PAPER="$ROOT/Chinese_skill_benchmark_Paper"
ENC="$PAPER/output/jobbert_zh_3m/mlm/encoder_ckpt65000"
INIT="$PAPER/release/huggingface-model/staging/crf/best.pt"
DATA="${STUDENT_DATA:-$PAPER/output/silver_public_2500_student_20260913/data}"
OUT="${STUDENT_OUT:-$PAPER/output/silver_public_2500_student_20260913/jobbert3m}"
GOLD_BIO="$PAPER/data/gold150_test.bio.jsonl"
LOG="${STUDENT_LOG:-$PAPER/output/silver_public_2500_student_20260913/train.log}"
SEEDS="${STUDENT_SEEDS:-42 43 44}"
EPOCHS="${STUDENT_EPOCHS:-6}"
PATIENCE="${STUDENT_PATIENCE:-2}"
GPU_WAIT_SEC="${GPU_WAIT_SEC:-21600}"

mkdir -p "$OUT" "$(dirname "$LOG")"
gpu_used_mib() {
  nvidia-smi -i "$1" --query-gpu=memory.used --format=csv,noheader,nounits 2>/dev/null | head -1 | tr -d ' '
}
if [[ -n "${CUDA_VISIBLE_DEVICES:-}" && -z "${STUDENT_FORCE_GPU:-}" ]]; then
  first="${CUDA_VISIBLE_DEVICES%%,*}"
  used="$(gpu_used_mib "$first" || echo 999999)"
  if ! "$PY" -c "import sys; sys.exit(0 if float('${used:-999999}') < 800 else 1)"; then
    echo "[student] GPU $first is busy (${used} MiB); ignoring CUDA_VISIBLE_DEVICES" | tee -a "$LOG"
    unset CUDA_VISIBLE_DEVICES
  fi
fi
if [[ -z "${CUDA_VISIBLE_DEVICES:-}" ]]; then
  deadline=$((SECONDS + GPU_WAIT_SEC))
  gpu=""
  while (( SECONDS < deadline )); do
    gpu="$("$PY" "$PAPER/scripts/pick_free_cuda.py" --max-used-mib 800 || true)"
    if [[ -n "$gpu" ]]; then
      export CUDA_VISIBLE_DEVICES="$gpu"
      break
    fi
    echo "[student] no free GPU, sleep 60s $(date -Is)" | tee -a "$LOG"
    sleep 60
  done
  if [[ -z "${CUDA_VISIBLE_DEVICES:-}" ]]; then
    echo "[student] no free GPU after wait" | tee -a "$LOG"
    exit 7
  fi
fi
echo "[student] start $(date -Is) gpu=${CUDA_VISIBLE_DEVICES:-unset} epochs=$EPOCHS seeds=$SEEDS" | tee -a "$LOG"
export STUDENT_OUT_RESOLVED="$OUT"
export STUDENT_SEEDS_RESOLVED="$SEEDS"
export STUDENT_COMPARE="${STUDENT_COMPARE:-$(dirname "$OUT")/COMPARE_v6a.json}"
if [[ ! -f "$DATA/train.jsonl" || ! -f "$DATA/dev.jsonl" ]]; then
  echo "missing $DATA/train.jsonl" | tee -a "$LOG"
  exit 2
fi
if [[ ! -f "$INIT" ]]; then
  echo "missing V4 CRF $INIT" | tee -a "$LOG"
  exit 2
fi

run_seed() {
  local seed="$1"
  local dir="$OUT/seed${seed}"
  mkdir -p "$dir"
  if [[ -f "$dir/score_gold150.json" ]]; then
    echo "[skip] seed $seed already scored" | tee -a "$LOG"
    return 0
  fi
  if [[ ! -f "$dir/best.pt" ]]; then
    echo "[train] seed $seed $(date -Is)" | tee -a "$LOG"
    "$PY" "$PAPER/scripts/train_cn_roberta_crf.py" \
      --seed "$seed" \
      --model_dir "$ENC" \
      --train "$DATA/train.jsonl" \
      --dev "$DATA/dev.jsonl" \
      --test "$GOLD_BIO" \
      --gold "$PAPER/data/gold150_test.jsonl" \
      --out_dir "$dir" \
      --epochs "$EPOCHS" --patience "$PATIENCE" --batch_size 16 --max_len 256 --lr 2e-5 \
      --init_crf "$INIT" \
      --freeze_encoder \
      --resume \
      --local_files_only \
      --skip_score \
      >>"$dir/train.log" 2>&1
  fi
  "$PY" "$PAPER/scripts/eval_gold150_ext.py" \
    --protocol jobbert_v6a \
    --gold_eval "$GOLD_BIO" \
    --pred "$dir/test_pred.jsonl" \
    --out "$dir/score_gold150.json"
  echo "[scored] seed $seed $(date -Is)" | tee -a "$LOG"
}

for seed in $SEEDS; do
  run_seed "$seed"
done

"$PY" - <<PY
import json, os, statistics
from pathlib import Path
root = Path(os.environ["STUDENT_OUT_RESOLVED"])
seeds = [int(x) for x in os.environ["STUDENT_SEEDS_RESOLVED"].split()]
compare = Path(os.environ["STUDENT_COMPARE"])
rows = []
for seed in seeds:
    p = root / f"seed{seed}" / "score_gold150.json"
    if not p.is_file():
        rows.append({"seed": seed, "status": "missing"})
        continue
    s = json.loads(p.read_text())
    f1 = s.get("gold150", {}).get("typed_exact_f1")
    rows.append({"seed": seed, "typed_exact_f1": f1, "complete_150": (s.get("coverage") or {}).get("complete_150")})
f1s = [r["typed_exact_f1"] for r in rows if isinstance(r.get("typed_exact_f1"), (int, float))]
out = {
    "rows": rows,
    "mean": statistics.mean(f1s) if f1s else None,
    "sd": statistics.stdev(f1s) if len(f1s) > 1 else None,
    "reference_v6a_mean": 0.5536,
    "reference_v6a_sd": 0.0054,
    "not_paper_main": True,
    "note": "Public-API Silver student. Do not write into confirmed-results until author confirms.",
}
compare.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=2))
PY
echo "[student] done $(date -Is)" | tee -a "$LOG"
