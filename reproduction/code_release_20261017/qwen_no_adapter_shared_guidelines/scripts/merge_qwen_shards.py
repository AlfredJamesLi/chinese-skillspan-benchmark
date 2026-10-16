#!/usr/bin/env python3
"""Merge Qwen worker0/worker1 records in frozen Gold150 order. No overlap."""
from __future__ import annotations

import json
from pathlib import Path

RUN = Path(__file__).resolve().parents[1]
GOLD = RUN / "inputs" / "gold150_id_text.jsonl"
ROOT = RUN / "runs" / "qwen25-14b-instruct"


def load_states(worker: int) -> dict[str, dict]:
    out = {}
    d = ROOT / f"worker{worker}" / "states"
    if not d.is_dir():
        return out
    for p in d.glob("*.json"):
        rec = json.loads(p.read_text(encoding="utf-8"))
        if rec.get("phase") != "formal":
            continue
        out[rec["id"]] = rec
    return out


def main() -> int:
    gold = [json.loads(l) for l in GOLD.read_text(encoding="utf-8").splitlines() if l.strip()]
    ids = [r["id"] for r in gold]
    assert len(ids) == 150 and len(set(ids)) == 150
    w0 = load_states(0)
    w1 = load_states(1)
    inter = set(w0) & set(w1)
    union = set(w0) | set(w1)
    report = {
        "n_gold": 150,
        "n_w0": len(w0),
        "n_w1": len(w1),
        "intersection": sorted(inter),
        "intersection_n": len(inter),
        "union_n": len(union),
        "missing": [i for i in ids if i not in union],
        "complete": len(inter) == 0 and set(ids) == union,
    }
    if inter:
        report["error"] = "worker_id_overlap"
    ordered = []
    missing = []
    for i in ids:
        rec = w0.get(i) or w1.get(i)
        if rec is None:
            missing.append(i)
            continue
        ordered.append(rec)
    (ROOT / "MERGE_REPORT.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if report["complete"]:
        (ROOT / "records_merged.jsonl").write_text(
            "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in ordered),
            encoding="utf-8",
        )
    print(json.dumps(report, ensure_ascii=False), flush=True)
    return 0 if report["complete"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
