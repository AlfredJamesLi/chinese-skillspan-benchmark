#!/usr/bin/env bash
# 3-seed CRF on frozen encoders + goldstyle v3. No MLM. Gold v2 scoring.
# Priority: JobBERT-3M ckpt65000 (best), JobBERT-1M, vanilla RoBERTa-wwm.
# Seed 42 already exists for all three; this fills 123 and 2026.
set -euo pipefail
export TRANSFORMERS_OFFLINE=1 HF_HUB_OFFLINE=1 TOKENIZERS_PARALLELISM=false PYTHONUNBUFFERED=1
export PYTHONPATH="/home/guojingli3/SCESC-LLM-skill-extraction/Baseline_Models_Collection/pytorch-crf:${PYTHONPATH:-}"
PY="${PYTHON:-/opt/anaconda3/envs/adasparse/bin/python3}"
ROOT="/home/guojingli3/SCESC-LLM-skill-extraction"
PAPER="$ROOT/Chinese_skill_benchmark_Paper"
OUT_ROOT="${OUT_ROOT:-$PAPER/output/encoder_3seed}"
mkdir -p "$OUT_ROOT"
echo "$$" > "$OUT_ROOT/run.pid"
echo "[3seed] start GPU=${CUDA_VISIBLE_DEVICES:-?} py=$PY $(date -Is)" | tee -a "$OUT_ROOT/run.log"

run_one() {
  local name="$1" enc="$2" seed="$3"
  local out="$OUT_ROOT/${name}/seed_${seed}"
  if [[ -f "$out/run_summary.json" ]]; then
    echo "[skip] $name seed=$seed already scored" | tee -a "$OUT_ROOT/run.log"
    return 0
  fi
  if [[ ! -f "$enc/config.json" ]]; then
    echo "[fail] missing encoder $enc" | tee -a "$OUT_ROOT/run.log"
    return 1
  fi
  mkdir -p "$out"
  echo "[crf] $name seed=$seed $(date -Is)" | tee -a "$OUT_ROOT/run.log"
  "$PY" "$PAPER/scripts/train_cn_roberta_crf.py" \
    --seed "$seed" \
    --model_dir "$enc" \
    --train "$PAPER/data/train_goldstyle_v3.jsonl" \
    --dev "$PAPER/data/dev_goldstyle_v3.jsonl" \
    --test "$ROOT/data/annotated/processed/chinese_skillspan/test.json" \
    --gold "$PAPER/data/gold_canonical_v2.jsonl" \
    --out_dir "$out" \
    --epochs 6 --patience 2 --batch_size 16 --max_len 256 --lr 2e-5 \
    >>"$out/run.log" 2>&1
  echo "[done] $name seed=$seed $(date -Is)" | tee -a "$OUT_ROOT/run.log"
  cp -f "$out/run_summary.json" "$PAPER/results_snapshots/${name}__seed${seed}.json"
  if [[ -x "$PAPER/scripts/backup_push_github.sh" ]]; then
    bash "$PAPER/scripts/backup_push_github.sh" "3-seed CRF snapshot: ${name} seed ${seed}" || true
  fi
}

# Best encoder first (most important if wall-clock cuts us off).
run_one "jobbert_zh_3m_ckpt65000" "$PAPER/output/jobbert_zh_3m/mlm/encoder_ckpt65000" 123
run_one "jobbert_zh_3m_ckpt65000" "$PAPER/output/jobbert_zh_3m/mlm/encoder_ckpt65000" 2026
run_one "jobbert_zh_1m" "$PAPER/output/jobbert_zh_1m/mlm/encoder" 123
run_one "jobbert_zh_1m" "$PAPER/output/jobbert_zh_1m/mlm/encoder" 2026
run_one "cn_roberta_wwm_v3" "$ROOT/Baseline_Models_Collection/chinese-roberta-wwm-ext" 123
run_one "cn_roberta_wwm_v3" "$ROOT/Baseline_Models_Collection/chinese-roberta-wwm-ext" 2026

"$PY" - << 'PY'
import json, statistics
from pathlib import Path
PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
root = PAPER / "output/encoder_3seed"
# include seed 42 from older runs
alias = {
    "jobbert_zh_3m_ckpt65000": {
        42: PAPER / "output/jobbert_zh_3m/crf_ckpt65000_ep1/run_summary.json",
    },
    "jobbert_zh_1m": {
        42: PAPER / "output/jobbert_zh_1m/crf_v3_seed42/run_summary.json",
    },
    "cn_roberta_wwm_v3": {
        42: PAPER / "output/cn_roberta_wwm_crf/smoke_goldstyle_v3_seed42/run_summary.json",
    },
}
out = {}
for name, extra in alias.items():
    f1s = []
    rows = []
    for seed in (42, 123, 2026):
        p = extra.get(seed) or (root / name / f"seed_{seed}" / "run_summary.json")
        if not p.is_file():
            rows.append({"seed": seed, "status": "pending", "test_typed_f1": None})
            continue
        s = json.loads(p.read_text())
        f1 = (s.get("typed_exact") or {}).get("f1")
        f1s.append(f1)
        rows.append({"seed": seed, "status": "complete", "test_typed_f1": f1, "dev": s.get("best_dev_typed_f1"), "path": str(p)})
    summary = {"runs": rows}
    if f1s:
        summary["mean"] = sum(f1s) / len(f1s)
        summary["std"] = statistics.pstdev(f1s) if len(f1s) > 1 else 0.0
        summary["n"] = len(f1s)
    out[name] = summary
(root / "three_seed_summary.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
print(json.dumps(out, indent=2, ensure_ascii=False))
PY

echo "[3seed] all done $(date -Is)" | tee -a "$OUT_ROOT/run.log"
# refresh tables + git backup if helper exists
if [[ -x "$PAPER/scripts/backup_push_github.sh" ]]; then
  bash "$PAPER/scripts/backup_push_github.sh" "encoder 3-seed CRF snapshots" || true
fi
