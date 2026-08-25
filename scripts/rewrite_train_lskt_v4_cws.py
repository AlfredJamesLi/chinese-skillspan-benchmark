#!/usr/bin/env python3
"""Rewrite LSKT v4 silver spans onto jieba word boundaries. New files only.

Does not overwrite train_lskt_v4_silver, Gold v2, train.json, or SOP rule test gold.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
sys.path.insert(0, str(PAPER / "scripts"))
import cws_snap as cws  # noqa: E402

GOLD_V2 = PAPER / "data/gold_canonical_v2.jsonl"
PAIRS = [
    (PAPER / "data/train_lskt_v4_silver.jsonl", PAPER / "data/train_lskt_v4_cws.jsonl"),
    (PAPER / "data/dev_lskt_v4_silver.jsonl", PAPER / "data/dev_lskt_v4_cws.jsonl"),
    (PAPER / "data/test_lskt_v4_rule_g2ids.jsonl", PAPER / "data/test_lskt_v4_cws_g2ids.jsonl"),
]
META = PAPER / "reports/sandbox_lskt_v4_silver/cws_snap/silver_meta.json"
EXAMPLES = [
    "培训其",
    "当前服",
    "机器学",
    "维护和支持服",
    "存储和备",
    "量化分析领",
    "语言交",
    "运维自动",
]


def demo_examples(rows: list[dict], k: int = 12) -> list[dict]:
    out = []
    for rec in rows:
        toks = rec.get("tokens") or []
        before = cws.g.bio_spans(cws.tags_of(rec, "list_of_selection_bio4"))
        # original tags were overwritten; use cws vs stored? rewrite already replaced tags.
        # Callers pass pre-rewrite rows. After rewrite, compare v4_spans vs cws_spans.
        old = rec.get("v4_spans") or [[a, b, t] for a, b, t in before]
        new = rec.get("cws_spans") or []
        old_t = ["".join(toks[a:b]) for a, b, _ in (tuple(x) for x in old)]
        new_t = ["".join(toks[a:b]) for a, b, _ in (tuple(x) for x in new)]
        if old_t == new_t:
            continue
        out.append(
            {
                "id": rec.get("id"),
                "sentence": (rec.get("sentence") or "")[:80],
                "before": old_t,
                "after": new_t,
            }
        )
        if len(out) >= k:
            break
    return out


def main() -> int:
    META.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "gold_v2_untouched": True,
        "train_json_untouched": True,
        "v4_silver_untouched": True,
        "tool": "jieba + data/cws_userdict.txt",
        "hard_cap": cws.HARD_CAP,
        "splits": {},
        "named_fixes": [],
    }
    for src, dst in PAIRS:
        if not src.is_file():
            report["splits"][src.name] = {"missing": str(src)}
            continue
        raw = cws.load_jsonl(src)
        before_rows = []
        for r in raw:
            spans = cws.g.bio_spans(cws.tags_of(r, "list_of_selection_bio4"))
            before_rows.append(
                {
                    **r,
                    "cws_spans": [[a, b, t] for a, b, t in spans],
                    "cws_n_changed": 0,
                }
            )
        before_stats = cws.span_stats(before_rows)
        rows = [cws.rewrite_record(r, tag_field="list_of_selection_bio4") for r in raw]
        # keep original v4 spans for diff
        for rec, src_rec in zip(rows, raw):
            rec["v4_spans"] = src_rec.get("v4_spans") or [
                [a, b, t] for a, b, t in cws.g.bio_spans(cws.tags_of(src_rec, "list_of_selection_bio4"))
            ]
            rec["cws_source"] = "jieba_snap_v4"
        cws.write_jsonl(dst, rows)
        after = cws.span_stats(rows)
        report["splits"][src.name] = {
            "in": str(src),
            "out": str(dst),
            "before": before_stats,
            "after": after,
            "examples": demo_examples(rows),
        }
        print(src.name, "changed", after["n_sents_changed"], "incomplete", after["pct_incomplete_spans"])
    # named mid-word examples from SOP test if present
    sop = PAPER / "data/test_lskt_v4_cws_g2ids.jsonl"
    if sop.is_file():
        by_id = {str(r["id"]): r for r in cws.load_jsonl(sop)}
        for needle in EXAMPLES:
            hit = None
            for rec in by_id.values():
                toks = rec.get("tokens") or []
                before = ["".join(toks[a:b]) for a, b, _ in rec.get("v4_spans") or []]
                after = ["".join(toks[a:b]) for a, b, _ in rec.get("cws_spans") or []]
                if any(needle in x for x in before):
                    hit = {
                        "id": rec.get("id"),
                        "needle": needle,
                        "sentence": rec.get("sentence"),
                        "before": before,
                        "after": after,
                    }
                    break
            if hit:
                report["named_fixes"].append(hit)
    META.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("wrote", META)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
