#!/usr/bin/env python3
"""STL L/K/S/T + greedy combine on repartition_v1 test. Character gold, no jieba.

Does not overwrite tables/appendix_stl_v4.csv or old STL dirs.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
sys.path.insert(0, str(PAPER / "scripts"))
sys.path.insert(0, str(PAPER / "scorer"))
from eval_repartition_v1 import pack  # noqa: E402
from eval_stl_v4 import TYPES, merge_four  # noqa: E402
from score_lskt import rec_id, score  # noqa: E402

GOLD = PAPER / "data/repartition_v1/test.jsonl"
ROOT = PAPER / "output/repartition_v1/stl_1m/seed_42"
JOINT = PAPER / "output/repartition_v1/jobbert_1m/seed_42/test_pred.jsonl"
REP = PAPER / "reports/repartition_v1"


def load_jsonl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def main() -> int:
    missing = [t for t in TYPES if not (ROOT / t / "test_pred.jsonl").is_file()]
    if missing:
        print(json.dumps({"status": "pending", "missing_types": missing}, ensure_ascii=False))
        return 2
    gold_rows = load_jsonl(GOLD)
    gold_map = {rec_id(r): r for r in gold_rows}
    REP.mkdir(parents=True, exist_ok=True)
    pred_dir = ROOT / "combined"
    pred_dir.mkdir(parents=True, exist_ok=True)

    out: dict = {"gold": str(GOLD), "scorer": "cnss-lskt-1.2.0", "n_test": len(gold_rows)}
    if JOINT.is_file():
        jrep = score(str(GOLD), str(JOINT), align_mode="official", n_boot=0)
        out["joint_1m"] = pack(jrep)
    stl_paths = {t: ROOT / t / "test_pred.jsonl" for t in TYPES}
    stl = {}
    for t, p in stl_paths.items():
        stl[t] = pack(score(str(GOLD), str(p), align_mode="official", n_boot=0))
    out["stl"] = stl
    merged_path = pred_dir / "test_pred.jsonl"
    out["merge"] = merge_four(stl_paths, gold_map, merged_path)
    out["combined"] = pack(score(str(GOLD), str(merged_path), align_mode="official", n_boot=0))
    (REP / "stl_results.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"combined_exact": out["combined"]["typed_exact_f1"], "joint": (out.get("joint_1m") or {}).get("typed_exact_f1")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
