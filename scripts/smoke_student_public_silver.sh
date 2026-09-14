#!/usr/bin/env bash
# Small-n pipeline check on currently labeled public-API Silver.
# Writes only under output/.../smoke_partial/. Does not touch the 2500 chain
# or Gold150 / V4 / v6a freeze files. F1 is not a paper number.
set -euo pipefail
export TRANSFORMERS_OFFLINE=1 HF_HUB_OFFLINE=1 TOKENIZERS_PARALLELISM=false PYTHONUNBUFFERED=1
PAPER="/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper"
PY="${PYTHON:-/opt/anaconda3/envs/adasparse/bin/python3}"
LABELED="$PAPER/data/silver_plus_10k_prep_20260913/run2500_public_api_v1/labeled.jsonl"
SMOKE="$PAPER/output/silver_public_2500_student_20260913/smoke_partial"
N="${SMOKE_N:-240}"
mkdir -p "$SMOKE"
echo "[smoke] start $(date -Is) n=$N" | tee "$SMOKE/smoke.log"

"$PY" - <<PY
import json, random
from collections import defaultdict
from pathlib import Path

src = Path("$LABELED")
out = Path("$SMOKE")
raw = src.read_text(encoding="utf-8")
if raw and not raw.endswith("\n"):
    raw = raw.rsplit("\n", 1)[0]
rows = [json.loads(l) for l in raw.splitlines() if l.strip()]
n = min(int("$N"), len(rows))
by = defaultdict(list)
for r in rows:
    by[r.get("source_domain") or "unk"].append(r)
rng = random.Random(20260914)
picked = []
# Hamilton-like per domain, then fill remainder
quota = {}
keys = sorted(by)
remain = n
for i, k in enumerate(keys):
    if i == len(keys) - 1:
        quota[k] = remain
    else:
        q = int(round(n * len(by[k]) / len(rows)))
        quota[k] = min(q, len(by[k]), remain)
        remain -= quota[k]
for k in keys:
    grp = list(by[k])
    rng.shuffle(grp)
    picked.extend(grp[: quota[k]])
# top up if rounding dropped rows
have = {r["id"] for r in picked}
if len(picked) < n:
    rest = [r for r in rows if r["id"] not in have]
    rng.shuffle(rest)
    picked.extend(rest[: n - len(picked)])
picked = picked[:n]
(out / "labeled_subset.jsonl").write_text(
    "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in picked), encoding="utf-8"
)
print(json.dumps({
    "n_available": len(rows),
    "n_smoke": len(picked),
    "domains": {k: sum(1 for r in picked if r.get("source_domain")==k) for k in keys},
    "status": {s: sum(1 for r in picked if r.get("status")==s) for s in sorted({r.get("status") for r in picked})},
}, ensure_ascii=False))
PY

python3 "$PAPER/scripts/build_student_from_public_silver.py" \
  --labeled "$SMOKE/labeled_subset.jsonl" \
  --out-dir "$SMOKE/data" \
  --min-n 50

export STUDENT_DATA="$SMOKE/data"
export STUDENT_OUT="$SMOKE/jobbert3m"
export STUDENT_LOG="$SMOKE/train.log"
export STUDENT_COMPARE="$SMOKE/COMPARE_v6a.json"
export STUDENT_SEEDS="42"
export STUDENT_EPOCHS="1"
export STUDENT_PATIENCE="1"
export GPU_WAIT_SEC="${GPU_WAIT_SEC:-600}"
if [[ -z "${CUDA_VISIBLE_DEVICES:-}" ]]; then
  gpu="$("$PY" "$PAPER/scripts/pick_free_cuda.py" --max-used-mib 800)"
  export CUDA_VISIBLE_DEVICES="$gpu"
fi
bash "$PAPER/scripts/run_student_jobbert_silver2500.sh"
"$PY" - <<'PY'
import json
from pathlib import Path
root = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/output/silver_public_2500_student_20260913/smoke_partial")
score = json.loads((root / "jobbert3m/seed42/score_gold150.json").read_text())
split = json.loads((root / "data/SPLIT.json").read_text())
out = {
    "ok": True,
    "not_paper_f1": True,
    "not_comparable_to_0.5536": True,
    "n_train": split["n_train"],
    "n_dev": split["n_dev"],
    "n_labeled": split["n_labeled"],
    "gold150_typed_exact_f1": score["gold150"]["typed_exact_f1"],
    "complete_150": score["coverage"]["complete_150"],
    "protocol": score["protocol"],
    "note": "1 epoch / 1 seed / ~240 current Silver rows. Pipeline check only.",
}
(root / "SMOKE_RESULT.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=2))
PY
echo "[smoke] done $(date -Is)" | tee -a "$SMOKE/smoke.log"
