#!/usr/bin/env python3
"""Compare CWS engines for boundary snap only. jieba is the baseline.

Does not overwrite Gold v2, v4 silver, jieba train_lskt_v4_cws, or CRF dirs.
Does not let CWS choose types or empty vs non-empty.
Sandbox; not for confirmed-results.md.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")
os.environ.setdefault(
    "PKUSEG_HOME",
    "/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/.cache/pkuseg",
)

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
sys.path.insert(0, str(PAPER / "scripts"))
sys.path.insert(0, str(PAPER / "scorer"))
import cws_snap as cws  # noqa: E402
from score_lskt import score  # noqa: E402

OUT = PAPER / "reports/sandbox_lskt_v4_silver/cws_snap"
PRED_DIR = OUT / "engine_preds"
SRC = PAPER / "output/jobbert_zh_1m/crf_lskt_v4_silver_seed42/test_pred.jsonl"
KEEP_JIEBA = PAPER / "output/jobbert_zh_1m/crf_lskt_v4_silver_seed42/test_pred_cws.jsonl"
G2 = PAPER / "data/gold_canonical_v2.jsonl"
SOP = PAPER / "data/test_lskt_v4_rule_g2ids.jsonl"

ENGINES = [
    "jieba",
    "pkuseg_mixed",
    "pkuseg_news",
    "pkuseg_web",
    "pkuseg_news_nodict",
]
EXAMPLES = [
    ("1802-s0005", "培训其"),
    ("1802-s0000", "当前服"),
    ("1804-s0000", "机器学"),
    ("1802-s0004", "维护和支持服"),
    ("1802-s0000", "存储和备"),
    ("1804-s0000", "量化分析领"),
]


def score_one(gold: Path, pred: Path) -> dict:
    r = score(str(gold), str(pred), align_mode="official", n_boot=0)
    te, tr = r["typed_exact"], r["typed_relaxed"]
    return {
        "typed_exact_f1": te["f1"],
        "typed_relaxed_f1": tr["f1"],
        "typed_exact_p": te["precision"],
        "typed_exact_r": te["recall"],
        "alignment_ok": r.get("alignment_ok"),
    }


def example_row(raw_by_id: dict, snapped: list[dict], needle: str, sid: str) -> dict | None:
    rec = next((r for r in snapped if str(r.get("id")) == sid), None)
    src = raw_by_id.get(sid)
    if rec is None or src is None:
        return None
    toks = rec.get("tokens") or []
    before = ["".join(toks[a:b]) for a, b, _ in cws.g.bio_spans(cws.tags_of(src, "pred_tags"))]
    after = ["".join(toks[a:b]) for a, b, _ in rec.get("cws_spans") or []]
    return {"id": sid, "needle": needle, "before": before, "after": after}


def main() -> int:
    if not SRC.is_file():
        print("missing pred", SRC)
        return 2
    PRED_DIR.mkdir(parents=True, exist_ok=True)
    raw = cws.load_jsonl(SRC)
    raw_by_id = {str(r["id"]): r for r in raw}
    report = {
        "not_for_confirmed_results": True,
        "gold_v2_untouched": True,
        "jieba_baseline_untouched": str(KEEP_JIEBA),
        "hanlp": "HanLP 2.1.3 tok downloaded but unusable: transformers removed encode_plus",
        "note": "Boundary snap only. Types copied from CRF. Empty stays empty.",
        "engines": [],
    }
    lines = [
        "# CWS engine compare (sandbox)",
        "",
        "Same JobBERT-zh 1M+v4 CRF pred. Only word-boundary snap changes. **Not** Table 3.",
        "",
        "HanLP 2.x Electra tok: installed, model fetched, **failed** (`BertTokenizer.encode_plus` gone in this env's transformers). Do not downgrade transformers (CRF training uses the same env).",
        "",
        "| Engine | Gold v2 exact | Gold v2 IoU≥0.5 | SOP rule exact | mid-word spans | sents changed |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    jieba_spans = None
    for eng in ENGINES:
        dst = PRED_DIR / f"test_pred_{eng}.jsonl"
        rows = [cws.rewrite_record(r, tag_field="pred_tags", backend=eng) for r in raw]
        cws.write_jsonl(dst, rows)
        st = cws.span_stats(rows, backend=eng)
        g2 = score_one(G2, dst)
        sop = score_one(SOP, dst) if SOP.is_file() else {}
        span_set = {
            (str(r.get("id")), tuple((a, b, t) for a, b, t in r.get("cws_spans") or []))
            for r in rows
        }
        agree_jieba = None
        if eng == "jieba":
            jieba_spans = span_set
        elif jieba_spans is not None:
            agree_jieba = sum(1 for x in span_set if x in jieba_spans) / max(1, len(span_set))
        examples = []
        for sid, needle in EXAMPLES:
            hit = example_row(raw_by_id, rows, needle, sid)
            if hit:
                examples.append(hit)
        row = {
            "engine": eng,
            "pred": str(dst),
            "stats": st,
            "gold_v2": g2,
            "sop_rule_v4": sop,
            "sentence_agree_with_jieba": agree_jieba,
            "examples": examples,
        }
        report["engines"].append(row)
        mid = st.get("pct_midword_spans") or 0.0
        chg = st.get("pct_sents_changed") or 0.0
        lines.append(
            f"| {eng} | {g2['typed_exact_f1']:.4f} | {g2['typed_relaxed_f1']:.4f} | "
            f"{sop.get('typed_exact_f1', float('nan')):.4f} | {mid:.4f} | {chg:.3f} |"
        )
        print("done", eng, "gold_v2", round(g2["typed_exact_f1"], 4), flush=True)
    lines += [
        "",
        "jieba is the engineering baseline (userdict). pkuseg via `spacy_pkuseg` (original `pkuseg` does not build on Python 3.11).",
        "Do not copy into `confirmed-results.md`.",
        "",
    ]
    (OUT / "engine_compare.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "ENGINE_COMPARE.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
