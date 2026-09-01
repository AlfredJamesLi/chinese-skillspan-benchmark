#!/usr/bin/env bash
# Vanilla (no DAPT) Chinese-RoBERTa-wwm-ext base vs large + CRF on LSKT v4 silver.
# Seed 42 only. New dirs only. Does not overwrite Gold v2 or JobBERT CRF dirs.
set -euo pipefail
export TRANSFORMERS_OFFLINE=1 HF_HUB_OFFLINE=1 TOKENIZERS_PARALLELISM=false PYTHONUNBUFFERED=1
export PYTHONPATH="/home/guojingli3/SCESC-LLM-skill-extraction/Baseline_Models_Collection/pytorch-crf:${PYTHONPATH:-}"
PY="${PYTHON:-/opt/anaconda3/envs/adasparse/bin/python3}"
ROOT="/home/guojingli3/SCESC-LLM-skill-extraction"
PAPER="$ROOT/Chinese_skill_benchmark_Paper"
BASE_ENC="${BASE_ENC:-$ROOT/Baseline_Models_Collection/chinese-roberta-wwm-ext}"
LARGE_ENC="${LARGE_ENC:-$ROOT/Baseline_Models_Collection/chinese-roberta-wwm-ext-large}"
BASE_OUT="${BASE_OUT:-$PAPER/output/vanilla_wwm_base_v4_silver_seed42}"
LARGE_OUT="${LARGE_OUT:-$PAPER/output/vanilla_wwm_large_v4_silver_seed42}"
CMP="$PAPER/output/vanilla_wwm_v4"
TRAIN="$PAPER/data/train_lskt_v4_silver.jsonl"
DEV="$PAPER/data/dev_lskt_v4_silver.jsonl"
TEST="$ROOT/data/annotated/processed/chinese_skillspan/test.json"
GOLD_V2="$PAPER/data/gold_canonical_v2.jsonl"
KEEP_1M="$PAPER/output/jobbert_zh_1m/crf_lskt_v4_silver_seed42"
KEEP_3M="$PAPER/output/jobbert_zh_3m/crf_lskt_v4_silver_seed42"
KEEP_GS="$PAPER/output/cn_roberta_wwm_crf/smoke_goldstyle_v3_seed42"

refuse_overwrite() {
  local out="$1"
  if [[ "$out" == "$KEEP_1M" || "$out" == "$KEEP_3M" || "$out" == "$KEEP_GS" ]]; then
    echo "refusing to overwrite frozen CRF dir: $out" >&2
    exit 2
  fi
}

need_file() {
  if [[ ! -f "$1" ]]; then
    echo "missing $1" >&2
    exit 2
  fi
}

need_encoder() {
  if [[ ! -f "$1/config.json" ]]; then
    echo "missing encoder config: $1" >&2
    exit 2
  fi
  if [[ ! -f "$1/pytorch_model.bin" && ! -f "$1/model.safetensors" ]]; then
    echo "missing encoder weights: $1" >&2
    exit 2
  fi
}

train_arm() {
  local name="$1" enc="$2" out="$3"
  refuse_overwrite "$out"
  need_encoder "$enc"
  mkdir -p "$out"
  if [[ -f "$out/hybrid_eval.json" && -f "$out/test_pred.jsonl" ]]; then
    echo "[skip] already scored $name $out" | tee -a "$out/run.log"
    return 0
  fi
  echo "$$ ${SLURM_JOB_ID:-na} $name GPU=${CUDA_VISIBLE_DEVICES:-?} $(date -Is)" > "$out/run.pid"
  echo "[$name] CRF start enc=$enc out=$out $(date -Is)" | tee -a "$out/run.log"
  "$PY" "$PAPER/scripts/train_cn_roberta_crf.py" \
    --seed 42 \
    --model_dir "$enc" \
    --train "$TRAIN" \
    --dev "$DEV" \
    --test "$TEST" \
    --gold "$GOLD_V2" \
    --out_dir "$out" \
    --epochs 6 --patience 2 --batch_size 16 --max_len 256 --lr 2e-5 \
    2>&1 | tee -a "$out/run.log"
  "$PY" "$PAPER/scripts/eval_one_hybrid_cws.py" \
    --pred "$out/test_pred.jsonl" \
    --out_dir "$out" \
    --name "$name" \
    2>&1 | tee -a "$out/run.log"
  echo "[$name] CRF+eval done $(date -Is)" | tee -a "$out/run.log"
}

need_file "$TRAIN"
need_file "$DEV"
need_file "$TEST"
need_file "$GOLD_V2"
mkdir -p "$CMP"
echo "[host] $(hostname) slurm=${SLURM_JOB_ID:-na} gpu=${CUDA_VISIBLE_DEVICES:-?} $(date -Is)" | tee -a "$CMP/run.log"

train_arm "vanilla_wwm_base" "$BASE_ENC" "$BASE_OUT"
train_arm "vanilla_wwm_large" "$LARGE_ENC" "$LARGE_OUT"

"$PY" - << PY
import json
from pathlib import Path
base = Path("$BASE_OUT") / "hybrid_eval.json"
large = Path("$LARGE_OUT") / "hybrid_eval.json"
cmp_path = Path("$CMP") / "compare_seed42.json"
jobbert_1m = 0.4272
a = json.loads(base.read_text(encoding="utf-8"))["v4_hybrid"]["typed_exact_f1"]
b = json.loads(large.read_text(encoding="utf-8"))["v4_hybrid"]["typed_exact_f1"]
delta = b - a
if delta < 0.015 or b < 0.35:
    decision = "STOP: no 3-seed, no large DAPT"
elif delta >= 0.02:
    decision = "CONTINUE 3-seed"
else:
    decision = "BORDERLINE: hold 3-seed; review logs"
if b >= jobbert_1m:
    decision += "; discuss 1M DAPT on large (B >= JobBERT 1M v4 0.4272)"
out = {
    "status": "待验证",
    "not_for_confirmed_results": True,
    "gold_v2_untouched": True,
    "protocol": "V4 hybrid 2601 + jieba snap + cnss-lskt-1.2.0",
    "seed": 42,
    "vanilla_wwm_base_exact": a,
    "vanilla_wwm_large_exact": b,
    "delta_large_minus_base": delta,
    "jobbert_1m_v4_exact_ref": jobbert_1m,
    "decision": decision,
}
cmp_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=2))
PY

echo "[done] compare $CMP/compare_seed42.json $(date -Is)" | tee -a "$CMP/run.log"
