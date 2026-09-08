#!/usr/bin/env python3
"""Score Gold150 / Audit-50 / Challenge-100. Keep all 150 rows. No history subtraction."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path("/home/guojingli3/Chinese-Skillspan-Benchmark")
PAPER = ROOT / "Chinese_skill_benchmark_Paper"
sys.path.insert(0, str(PAPER / "scorer"))
from score_lskt import score  # noqa: E402

GOLD_TEST = ROOT / "Gold150_locked_complete_20260908/gold150_test.jsonl"


def load(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def dump(p: Path, rows: list[dict]) -> None:
    p.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


def slim(sc: dict) -> dict:
    te, tr = sc["typed_exact"], sc["typed_relaxed"]
    return {
        "typed_exact_p": te["precision"],
        "typed_exact_r": te["recall"],
        "typed_exact_f1": te["f1"],
        "typed_relaxed_p": tr["precision"],
        "typed_relaxed_r": tr["recall"],
        "typed_relaxed_f1": tr["f1"],
        "per_type_exact": sc.get("per_type_exact"),
        "alignment_ok": sc.get("alignment_ok"),
        "scorer_version": sc.get("scorer_version"),
        "n_matched": sc.get("n_matched"),
        "n_missing": sc.get("n_missing"),
    }


def empty_fp(gold_rows, pred_rows) -> dict:
    g = {r.get("id") or r.get("source_id"): r for r in gold_rows}
    n_empty_gold = 0
    n_fp = 0
    for p in pred_rows:
        rid = p.get("id")
        gr = g.get(rid)
        if gr is None:
            continue
        g_empty = not (gr.get("spans") or [])
        p_empty = not (p.get("pred_spans") or [])
        if g_empty:
            n_empty_gold += 1
            if not p_empty:
                n_fp += 1
    return {"n_empty_gold": n_empty_gold, "empty_label_fp": n_fp}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gold_eval", required=True)
    ap.add_argument("--pred", required=True)
    ap.add_argument("--gold_test", default=str(GOLD_TEST))
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    gold_eval = load(Path(args.gold_eval))
    gold_test = load(Path(args.gold_test))
    preds = load(Path(args.pred))
    split_of = {r["source_id"]: r.get("split") for r in gold_test}
    chal = {i for i, s in split_of.items() if s == "gold100_page1"}
    aud = {i for i, s in split_of.items() if s == "iaa50"}
    pred_ids = {p["id"] for p in preds}
    gold_ids = {r["id"] for r in gold_eval}
    missing = sorted(gold_ids - pred_ids)
    extra = sorted(pred_ids - gold_ids)
    if len(preds) != 150 or missing:
        # do not drop; still score intersection but flag
        coverage = {"n_pred": len(preds), "missing_ids": missing, "extra_ids": extra, "complete_150": False}
    else:
        coverage = {"n_pred": 150, "missing_ids": [], "extra_ids": extra, "complete_150": True}

    tmp = Path(args.out).parent / "_score_tmp"
    tmp.mkdir(parents=True, exist_ok=True)

    def subset(rows, ids):
        return [r for r in rows if (r.get("id") or r.get("source_id")) in ids]

    g_all, p_all = Path(args.gold_eval), Path(args.pred)
    dump(tmp / "g_c.jsonl", subset(gold_eval, chal))
    dump(tmp / "p_c.jsonl", subset(preds, chal))
    dump(tmp / "g_a.jsonl", subset(gold_eval, aud))
    dump(tmp / "p_a.jsonl", subset(preds, aud))
    out = {
        "coverage": coverage,
        "gold150": slim(score(str(g_all), str(p_all), align_mode="official", n_boot=0)),
        "challenge100": slim(score(str(tmp / "g_c.jsonl"), str(tmp / "p_c.jsonl"), align_mode="official", n_boot=0)),
        "audit50": slim(score(str(tmp / "g_a.jsonl"), str(tmp / "p_a.jsonl"), align_mode="official", n_boot=0)),
        "empty_label": empty_fp(gold_eval, preds),
        "parse": {
            "n_ok": sum(1 for p in preds if p.get("parse_status") == "ok"),
            "n_partial": sum(1 for p in preds if p.get("parse_status") == "partial"),
            "n_fail": sum(1 for p in preds if p.get("parse_status") not in {"ok", "partial"}),
            "statuses": {p.get("parse_status", ""): 0 for p in preds},
        },
        "not_comparable_to_0.4331": True,
        "not_comparable_to_0.1724": True,
        "not_independent_b2_vs_b1_claim": True,
        "sample_sd_is_not_test_ci": True,
    }
    for p in preds:
        st = p.get("parse_status") or ""
        out["parse"]["statuses"][st] = out["parse"]["statuses"].get(st, 0) + 1
    if preds:
        out["cost"] = {
            "mean_seconds": sum(p.get("seconds") or 0 for p in preds) / len(preds),
            "sum_seconds": sum(p.get("seconds") or 0 for p in preds),
            "mean_input_tokens": sum(p.get("n_input_tokens") or 0 for p in preds) / len(preds),
            "mean_output_tokens": sum(p.get("n_output_tokens") or 0 for p in preds) / len(preds),
        }
    Path(args.out).write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"out": args.out, "exact_f1": out["gold150"]["typed_exact_f1"], "complete": coverage["complete_150"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
