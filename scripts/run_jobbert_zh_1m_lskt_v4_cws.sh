#!/usr/bin/env bash
# JobBERT-zh 1M encoder + CRF on jieba-snapped LSKT v4 silver.
# New dir only. Does not touch crf_lskt_v4_silver_seed42 or Gold v2.
set -euo pipefail
export TRANSFORMERS_OFFLINE=1 HF_HUB_OFFLINE=1 TOKENIZERS_PARALLELISM=false PYTHONUNBUFFERED=1
export PYTHONPATH="/home/guojingli3/SCESC-LLM-skill-extraction/Baseline_Models_Collection/pytorch-crf:${PYTHONPATH:-}"
PY="${PYTHON:-/opt/anaconda3/envs/adasparse/bin/python3}"
ROOT="/home/guojingli3/SCESC-LLM-skill-extraction"
PAPER="$ROOT/Chinese_skill_benchmark_Paper"
ENC="${ENC:-$PAPER/output/jobbert_zh_1m/mlm/encoder}"
OUT="${OUT_DIR:-$PAPER/output/jobbert_zh_1m/crf_lskt_v4_cws_seed42}"
KEEP="$PAPER/output/jobbert_zh_1m/crf_lskt_v4_silver_seed42"

if [[ ! -f "$ENC/config.json" ]]; then
  echo "missing 1M encoder: $ENC" >&2
  exit 2
fi
if [[ "$OUT" == "$KEEP" ]]; then
  echo "refusing to overwrite 1M v4 CRF dir" >&2
  exit 2
fi
if [[ ! -f "$PAPER/data/train_lskt_v4_cws.jsonl" ]]; then
  echo "missing CWS train silver" >&2
  exit 2
fi
mkdir -p "$OUT"
if [[ -f "$OUT/run_summary.json" ]]; then
  echo "[skip] already scored $OUT" | tee -a "$OUT/run.log"
  "$PY" "$PAPER/scripts/score_sop_v4_pred.py" --pred "$OUT/test_pred.jsonl" --out "$OUT/sop_eval.json"
  exit 0
fi

echo $$ > "$OUT/run.pid"
echo "1M+v4-cws CRF start GPU=${CUDA_VISIBLE_DEVICES:-?} enc=$ENC out=$OUT $(date -Is)" | tee -a "$OUT/run.log"

"$PY" "$PAPER/scripts/train_cn_roberta_crf.py" \
  --seed 42 \
  --model_dir "$ENC" \
  --train "$PAPER/data/train_lskt_v4_cws.jsonl" \
  --dev "$PAPER/data/dev_lskt_v4_cws.jsonl" \
  --test "$ROOT/data/annotated/processed/chinese_skillspan/test.json" \
  --gold "$PAPER/data/gold_canonical_v2.jsonl" \
  --out_dir "$OUT" \
  --epochs 6 --patience 2 --batch_size 16 --max_len 256 --lr 2e-5 \
  2>&1 | tee -a "$OUT/run.log"

"$PY" "$PAPER/scripts/score_sop_v4_pred.py" \
  --pred "$OUT/test_pred.jsonl" \
  --out "$OUT/sop_eval.json" \
  2>&1 | tee -a "$OUT/run.log"

"$PY" - << PY
import json, sys
from pathlib import Path
sys.path.insert(0, "$PAPER/scorer")
from score_lskt import score
pred = Path("$OUT/test_pred.jsonl")
golds = [
    ("sop_cws_2601", Path("$PAPER/data/test_lskt_v4_cws_g2ids.jsonl")),
    ("sop_rule_v4_2601", Path("$PAPER/data/test_lskt_v4_rule_g2ids.jsonl")),
    ("gold_v2_official", Path("$PAPER/data/gold_canonical_v2.jsonl")),
]
rows = []
for name, g in golds:
    if not g.is_file():
        continue
    r = score(str(g), str(pred), align_mode="official", n_boot=0)
    te, tr = r["typed_exact"], r["typed_relaxed"]
    rows.append({"name": name, "typed_exact_f1": te["f1"], "typed_relaxed_f1": tr["f1"]})
out = Path("$OUT/cws_eval.json")
out.write_text(json.dumps({"pred": str(pred), "not_for_confirmed_results": True, "scores": rows}, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(rows, ensure_ascii=False, indent=2))
PY

echo "1M+v4-cws CRF done $(date -Is)" | tee -a "$OUT/run.log"
