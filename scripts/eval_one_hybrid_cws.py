#!/usr/bin/env python3
"""Jieba-snap one CRF pred and score V4 hybrid (cnss-lskt-1.2.0).

Writes only under --out_dir. Does not overwrite Gold v2, V4 silver, or shared
hybrid pred dumps. Numbers are 待验证 until copied into confirmed-results.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
sys.path.insert(0, str(PAPER / "scripts"))
sys.path.insert(0, str(PAPER / "scorer"))
import cws_snap as cws  # noqa: E402
from diag_span_charlen import score_bands  # noqa: E402
from score_lskt import GOLD_FIELDS, index_by_id, load_records, rec_id, score  # noqa: E402

HYBRID = PAPER / "data/test_lskt_v4_cws_simhuman980_hybrid.jsonl"
GOLD_V2 = PAPER / "data/gold_canonical_v2.jsonl"
FORBIDDEN = {
    PAPER / "data/gold_canonical_v2.jsonl",
    PAPER / "data/train_lskt_v4_silver.jsonl",
    PAPER / "data/dev_lskt_v4_silver.jsonl",
    PAPER / "data/test_lskt_v4_cws_simhuman980_hybrid.jsonl",
}


def empty_pred(gold: dict) -> dict:
    toks = [str(t) for t in (gold.get("tokens") or list(gold.get("sentence") or ""))]
    tags = ["O"] * len(toks)
    return {
        "id": rec_id(gold),
        "sentence": gold.get("sentence") or "",
        "tokens": toks,
        "pred_tags": tags,
        "list_of_selection_bio4": tags,
    }


def slim(gold_path: Path, pred_path: Path) -> dict:
    r = score(str(gold_path), str(pred_path), align_mode="official", n_boot=0)
    te, tr = r["typed_exact"], r["typed_relaxed"]
    return {
        "gold": str(gold_path),
        "pred": str(pred_path),
        "scorer_version": r.get("scorer_version"),
        "alignment_ok": bool(r.get("alignment_ok")),
        "n_gold": r.get("gold_n_unique_ids"),
        "n_matched": r.get("n_matched"),
        "n_missing": r.get("n_missing"),
        "typed_exact_p": te["precision"],
        "typed_exact_r": te["recall"],
        "typed_exact_f1": te["f1"],
        "typed_relaxed_f1": tr["f1"],
        "collapsed_exact_f1": r["collapsed_exact"]["f1"],
        "collapsed_relaxed_f1": r["collapsed_relaxed"]["f1"],
    }


def snap_fill(src: Path, dst: Path, gold_rows: list[dict]) -> dict:
    if dst.resolve() in {p.resolve() for p in FORBIDDEN}:
        raise SystemExit(f"refusing to overwrite {dst}")
    raw = cws.load_jsonl(src)
    rows = [cws.rewrite_record(r, tag_field=None) for r in raw]
    by_id = {}
    for r in rows:
        try:
            by_id[rec_id(r)] = r
        except Exception:
            continue
    gold_map = {rec_id(g): g for g in gold_rows}
    filled, n_fill = [], 0
    for gid, g in gold_map.items():
        if gid in by_id:
            filled.append(by_id[gid])
        else:
            filled.append(empty_pred(g))
            n_fill += 1
    extra = [r for i, r in by_id.items() if i not in gold_map]
    cws.write_jsonl(dst, filled + extra)
    return {"n_src": len(raw), "n_snapped": len(rows), "n_filled_empty": n_fill, "n_extra": len(extra)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pred", required=True)
    ap.add_argument("--out_dir", required=True)
    ap.add_argument("--name", default="pred")
    args = ap.parse_args()
    pred = Path(args.pred)
    out_dir = Path(args.out_dir)
    if not pred.is_file():
        print("missing pred", pred, file=sys.stderr)
        return 2
    out_dir.mkdir(parents=True, exist_ok=True)
    gold_rows = load_records(str(HYBRID))
    snapped = out_dir / "test_pred_cws.jsonl"
    snap_meta = snap_fill(pred, snapped, gold_rows)
    hybrid = slim(HYBRID, snapped)
    gold_v2 = slim(GOLD_V2, snapped) if GOLD_V2.is_file() else None
    pred_by, _ = index_by_id(load_records(str(snapped)), "first")
    bands = score_bands(gold_rows, pred_by, typed=True)
    report = {
        "name": args.name,
        "not_for_confirmed_results": True,
        "status": "待验证",
        "gold_v2_untouched": True,
        "raw_pred": str(pred),
        "snapped_pred": str(snapped),
        "snap": snap_meta,
        "v4_hybrid": hybrid,
        "gold_v2_side": gold_v2,
        "span_char5_typed": bands,
    }
    out = out_dir / "hybrid_eval.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
