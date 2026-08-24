#!/usr/bin/env python3
"""Overlay human380 BIO labels onto full train_goldstyle_v3. New file only."""
from __future__ import annotations

import json
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
V3 = PAPER / "data/train_goldstyle_v3.jsonl"
H380 = PAPER / "data/train_goldstyle_human380.jsonl"
OUT = PAPER / "data/train_goldstyle_v3_human380.jsonl"
META = PAPER / "reports/gold_style_relabel/train_human_80_300/merge_v3_human380.json"


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def main() -> None:
    human = {r["id"]: r for r in load_jsonl(H380)}
    rows = []
    n_overlay = n_missing = n_tag_mismatch = 0
    for rec in load_jsonl(V3):
        iid = rec["id"]
        if iid not in human:
            rows.append(rec)
            continue
        h = human[iid]
        tags = h.get("list_of_selection_bio4")
        if not tags:
            rows.append(rec)
            n_missing += 1
            continue
        toks = rec.get("tokens") or h.get("tokens") or []
        if len(tags) != len(toks):
            n_tag_mismatch += 1
        out = dict(rec)
        out["list_of_selection_bio4"] = tags
        gs = h.get("_goldstyle") or {}
        out["goldstyle_source"] = gs.get("source", "human380")
        out["goldstyle_spans"] = gs.get("spans_text")
        out["_human380"] = {
            "overlay": True,
            "decision": gs.get("decision", "draft"),
            "from": str(H380),
        }
        rows.append(out)
        n_overlay += 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    meta = {
        "n_total": len(rows),
        "n_overlay": n_overlay,
        "n_human380_ids": len(human),
        "n_missing_in_v3": sorted(set(human) - {r["id"] for r in rows}),
        "n_missing_tags": n_missing,
        "n_tag_len_mismatch": n_tag_mismatch,
        "out": str(OUT),
        "overwrote_v3": False,
        "touched_gold_v2": False,
        "paper_numbers": False,
        "note": "380-row human overlay on v3 train. Smoke only until human review.",
    }
    META.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(meta, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
