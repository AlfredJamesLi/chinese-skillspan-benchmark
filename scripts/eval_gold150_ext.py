#!/usr/bin/env python3
"""Score the human reference set (artifact Gold150). Keep all 150 rows. No history subtraction.

Clone-relative. Defaults to `data/gold150_test.jsonl` (freeze) plus a derived BIO
file; never overwrites the freeze.

Paper names: human reference set, challenge cohort, calibration cohort.
JSON keeps laboratory keys (`gold150`, `challenge100`, `audit50`) and adds
aliases (`human_reference`, `challenge_cohort`, `calibration_cohort`).

Two Qwen human-reference protocols are not interchangeable and must not share a default
checkpoint path:

- json_offset — this repo's `qwen_ext_protocol.py` / `train_qwen_ext_sft.py`
  (Table C typed exact **0.1215±0.0092**).
- shared_prompt — server-A common-handbook SFT (job 50981, **0.5403±0.0354**).

JobBERT-zh v6a B2 is **0.5536±0.0054**. None of these cells is V4 hybrid
JobBERT 3M **0.4331**.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from cnss_paths import paper_root

PAPER = paper_root()
sys.path.insert(0, str(PAPER / "scorer"))
sys.path.insert(0, str(PAPER / "scripts"))
from convert_gold150_to_bio import convert_record  # noqa: E402
from score_lskt import score  # noqa: E402

GOLD_TEST = PAPER / "data/gold150_test.jsonl"
GOLD_EVAL_DEFAULT = PAPER / "data/gold150_test.bio.jsonl"

PROTOCOLS = {
    "json_offset": "Human-reference Qwen JSON-offset LoRA (0.1215±0.0092). Not shared-prompt 0.5403.",
    "shared_prompt": "Human-reference shared-handbook SFT (job 50981, 0.5403±0.0354). Not JSON-offset 0.1215.",
    "jobbert_v6a": "Human-reference JobBERT-zh v6a B2 CRF (0.5536±0.0054).",
    "unspecified": "Protocol not declared; do not treat this F1 as a paper cell.",
}


def rec_key(r: dict) -> str:
    v = r.get("id") if r.get("id") is not None else r.get("source_id")
    if v is None:
        raise ValueError("record missing id and source_id")
    return str(v).strip()


def load(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def dump(p: Path, rows: list[dict]) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


def looks_like_doccano(rows: list[dict]) -> bool:
    if not rows:
        return False
    r = rows[0]
    return "list_of_selection_bio4" not in r and ("label" in r or "source_id" in r)


def as_bio(rows: list[dict]) -> list[dict]:
    if looks_like_doccano(rows):
        return [convert_record(r) for r in rows]
    out = []
    for r in rows:
        rec = dict(r)
        if rec.get("id") is None and rec.get("source_id") is not None:
            rec["id"] = str(rec["source_id"]).strip()
        out.append(rec)
    return out


def gold_is_empty(gr: dict) -> bool:
    if gr.get("spans") is not None:
        return not (gr.get("spans") or [])
    tags = gr.get("list_of_selection_bio4") or []
    if tags:
        return not any(t != "O" for t in tags)
    return not (gr.get("label") or [])


def pred_is_empty(pr: dict) -> bool:
    if pr.get("pred_spans") is not None:
        return not (pr.get("pred_spans") or [])
    tags = pr.get("pred_tags") or pr.get("list_of_selection_bio4") or []
    return not any(t != "O" for t in tags)


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
    g = {rec_key(r): r for r in gold_rows}
    n_empty_gold = 0
    n_fp = 0
    for p in pred_rows:
        gr = g.get(rec_key(p))
        if gr is None:
            continue
        if gold_is_empty(gr):
            n_empty_gold += 1
            if not pred_is_empty(p):
                n_fp += 1
    return {"n_empty_gold": n_empty_gold, "empty_label_fp": n_fp}


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Score the human reference set (artifact Gold150) from freeze or derived BIO. Does not rewrite the freeze."
    )
    ap.add_argument("--gold_eval", default="", help="BIO gold, or Doccano freeze (converted in memory). Default: derived BIO or freeze.")
    ap.add_argument("--pred", required=True)
    ap.add_argument("--gold_test", default=str(GOLD_TEST), help="Freeze with source_id + split (challenge/audit).")
    ap.add_argument("--out", required=True)
    ap.add_argument(
        "--protocol",
        default="unspecified",
        choices=sorted(PROTOCOLS),
        help="Label the prediction protocol. json_offset ≠ shared_prompt.",
    )
    args = ap.parse_args()

    gold_test_path = Path(args.gold_test)
    if not gold_test_path.is_file():
        raise SystemExit(f"missing human-reference freeze (gold150_test.jsonl): {gold_test_path}")
    gold_test = load(gold_test_path)

    if args.gold_eval:
        gold_src = Path(args.gold_eval)
        if gold_src.resolve() == GOLD_TEST.resolve():
            gold_eval = as_bio(load(gold_src))
        else:
            gold_eval = as_bio(load(gold_src))
    elif GOLD_EVAL_DEFAULT.is_file():
        gold_eval = as_bio(load(GOLD_EVAL_DEFAULT))
    else:
        gold_eval = as_bio(gold_test)

    preds = load(Path(args.pred))
    split_of = {}
    for r in gold_test:
        sid = r.get("source_id") or r.get("id")
        if sid is not None:
            split_of[str(sid).strip()] = r.get("split")
    chal = {i for i, s in split_of.items() if s == "gold100_page1"}
    aud = {i for i, s in split_of.items() if s == "iaa50"}
    pred_ids = {rec_key(p) for p in preds}
    gold_ids = {rec_key(r) for r in gold_eval}
    missing = sorted(gold_ids - pred_ids)
    extra = sorted(pred_ids - gold_ids)
    if len(preds) != 150 or missing:
        coverage = {"n_pred": len(preds), "missing_ids": missing, "extra_ids": extra, "complete_150": False}
    else:
        coverage = {"n_pred": 150, "missing_ids": [], "extra_ids": extra, "complete_150": True}

    tmp = Path(args.out).parent / "_score_tmp"
    tmp.mkdir(parents=True, exist_ok=True)

    def subset(rows, ids):
        return [r for r in rows if rec_key(r) in ids]

    g_all = tmp / "g_all.jsonl"
    p_all = tmp / "p_all.jsonl"
    dump(g_all, gold_eval)
    dump(p_all, preds)
    dump(tmp / "g_c.jsonl", subset(gold_eval, chal))
    dump(tmp / "p_c.jsonl", subset(preds, chal))
    dump(tmp / "g_a.jsonl", subset(gold_eval, aud))
    dump(tmp / "p_a.jsonl", subset(preds, aud))
    out = {
        "coverage": coverage,
        "protocol": args.protocol,
        "protocol_note": PROTOCOLS[args.protocol],
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
        "json_offset_is_not_shared_prompt": True,
        "not_independent_b2_vs_b1_claim": True,
        "sample_sd_is_not_test_ci": True,
        "freeze_not_rewritten": True,
    }
    out["human_reference"] = out["gold150"]
    out["challenge_cohort"] = out["challenge100"]
    out["calibration_cohort"] = out["audit50"]
    out["terminology"] = {
        "paper": {
            "human_reference": "gold150",
            "challenge_cohort": "challenge100",
            "calibration_cohort": "audit50",
        },
        "note": "0911 PDF names; laboratory keys gold150/challenge100/audit50 are unchanged.",
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
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "out": args.out,
                "exact_f1": out["gold150"]["typed_exact_f1"],
                "complete": coverage["complete_150"],
                "protocol": args.protocol,
                "not_comparable_to_0.4331": True,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
