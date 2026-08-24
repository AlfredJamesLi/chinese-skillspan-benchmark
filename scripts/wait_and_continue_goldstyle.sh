#!/usr/bin/env bash
# Overnight: wait for goldstyle v1 smoke, write report, optionally start tighter v2 smoke.
# Does not start 3-seed. Does not overwrite train.json or Gold v2.
set -euo pipefail
ROOT="/home/guojingli3/SCESC-LLM-skill-extraction"
PAPER="$ROOT/Chinese_skill_benchmark_Paper"
V1="$PAPER/output/cn_roberta_wwm_crf/smoke_goldstyle_seed42"
V2="$PAPER/output/cn_roberta_wwm_crf/smoke_goldstyle_v2_seed42"
LOG="$V1/overnight.log"
mkdir -p "$V1"
echo "WAIT start $(date -Is)" | tee -a "$LOG"

for i in $(seq 1 240); do
  if [[ -f "$V1/run_summary.json" ]] && grep -q "SMOKE goldstyle done" "$V1/smoke.log" 2>/dev/null; then
    echo "V1 complete $(date -Is) iter=$i" | tee -a "$LOG"
    break
  fi
  if [[ "$i" -eq 240 ]]; then
    echo "TIMEOUT waiting for v1 $(date -Is)" | tee -a "$LOG"
    exit 3
  fi
  sleep 60
done

python3 "$PAPER/scripts/after_goldstyle_smoke.py" | tee -a "$LOG"

ACTION=$(python3 - << 'PY'
import json
from pathlib import Path
p = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/cn_roberta_wwm_crf/smoke_goldstyle_seed42/run_summary.json")
r = json.loads(p.read_text())
f1 = float((r.get("typed_exact") or {}).get("f1") or 0)
print("consider_3seed" if f1 >= 0.05 else "tighten")
print(f1)
PY
)
F1=$(echo "$ACTION" | tail -n1)
DEC=$(echo "$ACTION" | head -n1)
echo "decision=$DEC f1=$F1" | tee -a "$LOG"

if [[ "$DEC" == "consider_3seed" ]]; then
  echo "F1>=0.05: leave 3-seed for human. Not launching." | tee -a "$LOG"
  exit 0
fi

echo "F1 low: write tighter v2 labels and smoke seed 42" | tee -a "$LOG"
python3 "$PAPER/scripts/rewrite_train_goldstyle.py" --tight \
  --out_train "$PAPER/data/train_goldstyle_v2.jsonl" \
  --out_dev "$PAPER/data/dev_goldstyle_v2.jsonl" \
  --out_meta "$PAPER/reports/gold_style_relabel/goldstyle_v2_meta.json" \
  | tee -a "$LOG"

GPU=$(nvidia-smi --query-gpu=index,memory.free --format=csv,noheader,nounits | sort -t, -k2 -nr | head -1 | cut -d, -f1 | tr -d ' ')
mkdir -p "$V2"
echo "V2 smoke GPU=$GPU $(date -Is)" | tee -a "$LOG" "$V2/smoke.log"
export CUDA_VISIBLE_DEVICES="$GPU"
export TRANSFORMERS_OFFLINE=1 HF_HUB_OFFLINE=1 TOKENIZERS_PARALLELISM=false PYTHONUNBUFFERED=1
export PYTHONPATH="$ROOT/Baseline_Models_Collection/pytorch-crf:${PYTHONPATH:-}"
python3 "$PAPER/scripts/train_cn_roberta_crf.py" \
  --seed 42 \
  --train "$PAPER/data/train_goldstyle_v2.jsonl" \
  --dev "$PAPER/data/dev_goldstyle_v2.jsonl" \
  --test "$ROOT/data/annotated/processed/chinese_skillspan/test.json" \
  --gold "$PAPER/data/gold_canonical_v2.jsonl" \
  --out_dir "$V2" \
  --epochs 6 --patience 2 --batch_size 16 --max_len 256 --lr 2e-5 \
  2>&1 | tee -a "$V2/smoke.log" | tee -a "$LOG"
echo "V2 done $(date -Is) exit=$?" | tee -a "$LOG" "$V2/smoke.log"

python3 - << 'PY'
import json
from pathlib import Path
p = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/cn_roberta_wwm_crf/smoke_goldstyle_v2_seed42/run_summary.json")
rep = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/reports/gold_style_relabel/goldstyle_smoke_result.md")
if p.is_file() and rep.is_file():
    r = json.loads(p.read_text())
    te = r.get("typed_exact") or {}
    extra = (
        "\n\n## Gold-style v2 smoke\n\n"
        f"- typed F1: {te.get('f1')}\n"
        f"- collapsed: {(r.get('collapsed_exact') or {}).get('f1')}\n"
        f"- align: {r.get('alignment_ok')}\n"
        f"- best_dev: {r.get('best_dev_typed_f1')}\n"
    )
    rep.write_text(rep.read_text(encoding="utf-8") + extra, encoding="utf-8")
    print(json.dumps({"v2_typed_f1": te.get("f1"), "align": r.get("alignment_ok")}, ensure_ascii=False))
elif not p.is_file():
    print("v2 run_summary missing")
PY
echo "OVERNIGHT done $(date -Is)" | tee -a "$LOG"
