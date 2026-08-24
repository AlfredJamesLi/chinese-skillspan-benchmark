#!/usr/bin/env bash
set -euo pipefail
export CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:-0}"
export TRANSFORMERS_OFFLINE=1
export HF_HUB_OFFLINE=1
export PYTHONUNBUFFERED=1
ROOT="/home/guojingli3/SCESC-LLM-skill-extraction"
SCRIPT="$ROOT/Chinese_skill_benchmark_Paper/scripts/train_cn_roberta_crf.py"
OUT="$ROOT/Chinese_skill_benchmark_Paper/output/cn_roberta_wwm_crf"
mkdir -p "$OUT"
echo "GPU=$CUDA_VISIBLE_DEVICES start $(date -Is)" | tee -a "$OUT/run.log"
for seed in 42 123 2026; do
  echo "===== seed $seed $(date -Is) =====" | tee -a "$OUT/run.log"
  python3 "$SCRIPT" \
    --seed "$seed" \
    --out_dir "$OUT/seed_$seed" \
    --epochs 6 \
    --patience 2 \
    --batch_size 16 \
    --max_len 256 \
    --lr 2e-5 \
    2>&1 | tee -a "$OUT/seed_${seed}.log"
done
echo "done $(date -Is)" | tee -a "$OUT/run.log"
python3 - << 'PY'
import json
from pathlib import Path
out = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/cn_roberta_wwm_crf")
rows=[]
for s in (42,123,2026):
    p=out/f"seed_{s}/run_summary.json"
    if p.is_file():
        rows.append(json.loads(p.read_text()))
print(json.dumps([{k:r.get(k) for k in ("seed","best_dev_typed_f1","alignment_ok","typed_exact","collapsed_exact")} for r in rows], indent=2, ensure_ascii=False))
(out/"three_seed_summary.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
PY
