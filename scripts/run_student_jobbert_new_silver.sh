#!/usr/bin/env bash
# v6a-recipe JobBERT-zh 3M CRF on merged new public-API Silver.
# Freeze encoder, continue V4 CRF, seeds 42/43/44. Does not overwrite v6a.
set -euo pipefail
export TRANSFORMERS_OFFLINE=1 HF_HUB_OFFLINE=1 TOKENIZERS_PARALLELISM=false PYTHONUNBUFFERED=1
export PYTHONPATH="/home/guojingli3/SCESC-LLM-skill-extraction/Baseline_Models_Collection/pytorch-crf:${PYTHONPATH:-}"
PY="${PYTHON:-/opt/anaconda3/envs/adasparse/bin/python3}"
ROOT="/home/guojingli3/SCESC-LLM-skill-extraction"
PAPER="$ROOT/Chinese_skill_benchmark_Paper"
ENC="$PAPER/output/jobbert_zh_3m/mlm/encoder_ckpt65000"
INIT="$PAPER/release/huggingface-model/staging/crf/best.pt"
DATA="${STUDENT_DATA:-$PAPER/output/silver_new_merged_student_20260914/data}"
OUT="${STUDENT_OUT:-$PAPER/output/silver_new_merged_student_20260914/jobbert3m}"
GOLD_BIO="$PAPER/data/gold150_test.bio.jsonl"
LOG="${STUDENT_LOG:-$PAPER/output/silver_new_merged_student_20260914/train.log}"
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
export STUDENT_DATA_RESOLVED="$DATA"
export STUDENT_SEEDS_RESOLVED="$SEEDS"
export STUDENT_COMPARE="${STUDENT_COMPARE:-$(dirname "$OUT")/COMPARE.json}"
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
  if [[ ! -f "$dir/score_gold150.json" ]]; then
    "$PY" "$PAPER/scripts/eval_gold150_ext.py" \
      --protocol jobbert_v6a \
      --gold_eval "$GOLD_BIO" \
      --pred "$dir/test_pred.jsonl" \
      --out "$dir/score_gold150.json"
    echo "[scored gold150] seed $seed $(date -Is)" | tee -a "$LOG"
  fi
  local sdir="$(dirname "$OUT")/silver_as_test/seed${seed}"
  mkdir -p "$sdir"
  if [[ ! -f "$sdir/score_silver_dev.json" ]]; then
    echo "[predict silver-dev] seed $seed $(date -Is)" | tee -a "$LOG"
    "$PY" "$PAPER/scripts/train_cn_roberta_crf.py" \
      --seed "$seed" \
      --model_dir "$ENC" \
      --train "$DATA/train.jsonl" \
      --dev "$DATA/dev.jsonl" \
      --test "$DATA/dev.jsonl" \
      --gold "$DATA/dev.jsonl" \
      --out_dir "$sdir" \
      --epochs 1 --patience 1 --batch_size 16 --max_len 256 --lr 2e-5 \
      --init_crf "$dir/best.pt" \
      --freeze_encoder \
      --predict_only \
      --local_files_only \
      >>"$sdir/predict.log" 2>&1
    "$PY" - "$DATA/dev.jsonl" "$sdir/test_pred.jsonl" "$sdir/score_silver_dev.json" <<'PY'
import json, sys
from pathlib import Path
sys.path.insert(0, "/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/scorer")
from score_lskt import score
g, p, out = sys.argv[1], sys.argv[2], sys.argv[3]
sc = score(g, p, align_mode="official", n_boot=0)
te, tr = sc["typed_exact"], sc["typed_relaxed"]
Path(out).write_text(json.dumps({
    "not_gold150": True,
    "typed_exact_p": te["precision"],
    "typed_exact_r": te["recall"],
    "typed_exact_f1": te["f1"],
    "typed_relaxed_f1": tr["f1"],
    "alignment_ok": sc.get("alignment_ok"),
    "per_type_exact": sc.get("per_type_exact"),
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"silver_dev_exact": te["f1"]}, ensure_ascii=False))
PY
    echo "[scored silver-dev] seed $seed $(date -Is)" | tee -a "$LOG"
  fi
}

for seed in $SEEDS; do
  run_seed "$seed"
done

"$PY" - <<'PY'
import json, os, statistics
from pathlib import Path
root = Path(os.environ["STUDENT_OUT_RESOLVED"])
data = Path(os.environ["STUDENT_DATA_RESOLVED"])
seeds = [int(x) for x in os.environ["STUDENT_SEEDS_RESOLVED"].split()]
compare = Path(os.environ["STUDENT_COMPARE"])
parent = root.parent
rows_g, rows_s = [], []
for seed in seeds:
    g = json.loads((root / f"seed{seed}" / "score_gold150.json").read_text())
    s = json.loads((parent / "silver_as_test" / f"seed{seed}" / "score_silver_dev.json").read_text())
    gf = (g.get("gold150") or g).get("typed_exact_f1")
    sf = s.get("typed_exact_f1")
    rows_g.append({"seed": seed, "typed_exact_f1": gf})
    rows_s.append({"seed": seed, "typed_exact_f1": sf})
g1 = [r["typed_exact_f1"] for r in rows_g if isinstance(r.get("typed_exact_f1"), (int, float))]
s1 = [r["typed_exact_f1"] for r in rows_s if isinstance(r.get("typed_exact_f1"), (int, float))]
split = json.loads((data / "SPLIT.json").read_text())
out = {
    "not_paper_main": True,
    "not_comparable_to_0.5536": True,
    "n_train": split.get("n_train"),
    "n_dev": split.get("n_dev"),
    "gold150": {
        "rows": rows_g,
        "mean": statistics.mean(g1) if g1 else None,
        "sd": statistics.stdev(g1) if len(g1) > 1 else None,
        "reference_v6a_mean": 0.5536,
    },
    "silver_dev_teacher": {
        "rows": rows_s,
        "mean": statistics.mean(s1) if s1 else None,
        "sd": statistics.stdev(s1) if len(s1) > 1 else None,
        "note": "Held-out new Silver teacher labels, not human gold.",
    },
    "note": "Merged public-API Silver student (2500+wave1/2+wave3, drop adjudication). Do not write into confirmed-results.md.",
}
compare.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=2))
PY
echo "[student] done $(date -Is)" | tee -a "$LOG"
