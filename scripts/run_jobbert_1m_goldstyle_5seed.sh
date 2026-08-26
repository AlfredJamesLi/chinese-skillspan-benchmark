#!/usr/bin/env bash
# Extra CRF seeds 7 and 13 on frozen JobBERT-zh 1M MLM + goldstyle v3.
# Does NOT re-run MLM. Gold v2 scoring via train_cn_roberta_crf.py.
# Seeds 42 / 123 / 2026 already exist.
set -euo pipefail
export TRANSFORMERS_OFFLINE=1 HF_HUB_OFFLINE=1 TOKENIZERS_PARALLELISM=false PYTHONUNBUFFERED=1
export PYTHONPATH="/home/guojingli3/SCESC-LLM-skill-extraction/Baseline_Models_Collection/pytorch-crf:${PYTHONPATH:-}"
PY="${PYTHON:-/opt/anaconda3/envs/adasparse/bin/python3}"
ROOT="/home/guojingli3/SCESC-LLM-skill-extraction"
PAPER="$ROOT/Chinese_skill_benchmark_Paper"
ENC="$PAPER/output/jobbert_zh_1m/mlm/encoder"
OUT_ROOT="${OUT_ROOT:-$PAPER/output/encoder_5seed/jobbert_zh_1m}"
mkdir -p "$OUT_ROOT"
echo "$$" > "$OUT_ROOT/run.pid"
echo "[5seed-1m] start GPU=${CUDA_VISIBLE_DEVICES:-?} py=$PY $(date -Is)" | tee -a "$OUT_ROOT/run.log"

if [[ ! -f "$ENC/config.json" ]]; then
  echo "[fail] missing frozen encoder $ENC" | tee -a "$OUT_ROOT/run.log"
  exit 1
fi

run_one() {
  local seed="$1"
  local out="$OUT_ROOT/seed_${seed}"
  if [[ -f "$out/run_summary.json" ]]; then
    echo "[skip] jobbert_zh_1m seed=$seed already scored" | tee -a "$OUT_ROOT/run.log"
    return 0
  fi
  mkdir -p "$out"
  echo "[crf] jobbert_zh_1m seed=$seed $(date -Is)" | tee -a "$OUT_ROOT/run.log"
  "$PY" "$PAPER/scripts/train_cn_roberta_crf.py" \
    --seed "$seed" \
    --model_dir "$ENC" \
    --train "$PAPER/data/train_goldstyle_v3.jsonl" \
    --dev "$PAPER/data/dev_goldstyle_v3.jsonl" \
    --test "$ROOT/data/annotated/processed/chinese_skillspan/test.json" \
    --gold "$PAPER/data/gold_canonical_v2.jsonl" \
    --out_dir "$out" \
    --epochs 6 --patience 2 --batch_size 16 --max_len 256 --lr 2e-5 \
    >>"$out/run.log" 2>&1
  echo "[done] jobbert_zh_1m seed=$seed $(date -Is)" | tee -a "$OUT_ROOT/run.log"
  cp -f "$out/run_summary.json" "$PAPER/results_snapshots/encoder_5seed__jobbert_zh_1m__seed_${seed}.json"
}

run_one 7
run_one 13

"$PY" - << 'PY'
import json, statistics
from pathlib import Path
PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
paths = {
    42: PAPER / "output/jobbert_zh_1m/crf_v3_seed42/run_summary.json",
    123: PAPER / "output/encoder_3seed/jobbert_zh_1m/seed_123/run_summary.json",
    2026: PAPER / "output/encoder_3seed/jobbert_zh_1m/seed_2026/run_summary.json",
    7: PAPER / "output/encoder_5seed/jobbert_zh_1m/seed_7/run_summary.json",
    13: PAPER / "output/encoder_5seed/jobbert_zh_1m/seed_13/run_summary.json",
}
rows, f1s = [], []
for seed in (42, 123, 2026, 7, 13):
    p = paths[seed]
    if not p.is_file():
        rows.append({"seed": seed, "status": "pending"})
        continue
    s = json.loads(p.read_text())
    f1 = (s.get("typed_exact") or {}).get("f1")
    f1s.append(f1)
    rows.append({"seed": seed, "status": "complete", "test_typed_f1": f1, "path": str(p)})
out = {"runs": rows, "n": len(f1s)}
if f1s:
    out["mean"] = sum(f1s) / len(f1s)
    out["std_sample"] = statistics.stdev(f1s) if len(f1s) > 1 else 0.0
root = PAPER / "output/encoder_5seed/jobbert_zh_1m"
root.mkdir(parents=True, exist_ok=True)
(root / "five_seed_summary.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
print(json.dumps(out, indent=2, ensure_ascii=False))
PY

echo "[5seed-1m] all done $(date -Is)" | tee -a "$OUT_ROOT/run.log"
