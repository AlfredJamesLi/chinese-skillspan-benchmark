#!/usr/bin/env python3
"""Jieba-bilateral eval on SOP-CWS 2601 with 980 SimHuman overlay.

Default path is **read-only**: it loads the frozen hybrid gold and does not
rewrite `data/test_lskt_v4_cws_simhuman980_hybrid.jsonl`. Lab-only rebuild:
`--rebuild-gold`.

Repro (paper-main encoder only, frozen JobBERT dump):
  python scripts/eval_hybrid_cws_simhuman.py --paper-main-only --use-frozen
# Guarantees JobBERT_3M_v4 typed exact 0.433118. Not the 0911 SOP LLM table.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

from cnss_paths import paper_root  # noqa: E402

PAPER = paper_root()
sys.path.insert(0, str(PAPER / "scripts"))
sys.path.insert(0, str(PAPER / "scorer"))
import cws_snap as cws  # noqa: E402
from score_lskt import rec_id, score  # noqa: E402

HYBRID_SHA256 = "2ad6342d8b762cf1abb289295315e2521bec0c540f4320113409fceab0818d99"
OUT = PAPER / "reports/sandbox_lskt_v4_silver/hybrid_cws_eval"
PRED_CWS_DIR = OUT / "preds_cws"
GOLD_HYBRID = PAPER / "data/test_lskt_v4_cws_simhuman980_hybrid.jsonl"
GOLD_980 = PAPER / "data/test_lskt_v4_simhuman980_cws.jsonl"
SOP_CWS = PAPER / "data/test_lskt_v4_cws_g2ids.jsonl"
SIM = PAPER / "data/test_lskt_v4_simhuman980.jsonl"
CSV_COMMITTED = PAPER / "tables/hybrid_cws_simhuman980_all_models.csv"

PAPER_MAIN_MODELS = ("JobBERT_3M_v4",)

MODELS = [
    ("ChatGPT", PAPER / "reports/views/ChatGPT_unique_first_v2.jsonl", "llm"),
    ("Claude", PAPER / "reports/views/Claude_unique_first_v2.jsonl", "llm_incomplete"),
    ("Kimi", PAPER / "reports/views/Kimi_unique_first_v2.jsonl", "llm_incomplete"),
    ("Kimi_filled", PAPER / "reports/views/Kimi_filled_v2.jsonl", "llm"),
    ("DeepSeek", PAPER / "reports/views/DeepSeek_unique_first_v2.jsonl", "llm"),
    ("Qwen", PAPER / "reports/views/Qwen_unique_first_v2.jsonl", "llm"),
    ("JobBERT-skill", PAPER / "reports/views/JobBERT-skill_unique_first_v2.jsonl", "en_head"),
    ("JobBERT-knowledge", PAPER / "reports/views/JobBERT-knowledge_unique_first_v2.jsonl", "en_head"),
    ("JobBERT_1M_v4", PAPER / "output/jobbert_zh_1m/crf_lskt_v4_silver_seed42/test_pred_cws.jsonl", "encoder_v4_cws_ready"),
    ("JobBERT_3M_v4", PAPER / "output/jobbert_zh_3m/crf_lskt_v4_silver_seed42/test_pred_cws.jsonl", "encoder_v4_cws_ready"),
    ("JobBERT_1M_v4_raw", PAPER / "output/jobbert_zh_1m/crf_lskt_v4_silver_seed42/test_pred.jsonl", "encoder_v4_needs_cws"),
    ("JobBERT_3M_v4_raw", PAPER / "output/jobbert_zh_3m/crf_lskt_v4_silver_seed42/test_pred.jsonl", "encoder_v4_needs_cws"),
    ("JobBERT_1M_v3_s42", PAPER / "output/jobbert_zh_1m/crf_v3_seed42/test_pred.jsonl", "encoder"),
    ("JobBERT_1M_v3_s123", PAPER / "output/encoder_3seed/jobbert_zh_1m/seed_123/test_pred.jsonl", "encoder"),
    ("JobBERT_1M_v3_s2026", PAPER / "output/encoder_3seed/jobbert_zh_1m/seed_2026/test_pred.jsonl", "encoder"),
    ("JobBERT_3M_ckpt65k_s42", PAPER / "output/jobbert_zh_3m/crf_ckpt65000_ep1/test_pred.jsonl", "encoder"),
    ("JobBERT_3M_ckpt65k_s123", PAPER / "output/encoder_3seed/jobbert_zh_3m_ckpt65000/seed_123/test_pred.jsonl", "encoder"),
    ("JobBERT_3M_ckpt65k_s2026", PAPER / "output/encoder_3seed/jobbert_zh_3m_ckpt65000/seed_2026/test_pred.jsonl", "encoder"),
    ("JobBERT_3M_final", PAPER / "output/jobbert_zh_3m/crf_v3_seed42/test_pred.jsonl", "encoder"),
    ("JobBERT_3M_ckpt100k", PAPER / "output/jobbert_zh_3m_ckpt_sweep/crf_ckpt100000/test_pred.jsonl", "encoder"),
    ("JobBERT_demo80k", PAPER / "output/jobbert_zh_demo/crf_v3_seed42/test_pred.jsonl", "encoder"),
    ("domain_mix_1M_s42", PAPER / "output/jobbert_zh_domain_1m/crf_v3_seed42/test_pred.jsonl", "encoder"),
    ("domain_mix_1M_s123", PAPER / "output/jobbert_zh_domain_1m/crf_v3_seed123/test_pred.jsonl", "encoder"),
    ("domain_mix_1M_s2026", PAPER / "output/jobbert_zh_domain_1m/crf_v3_seed2026/test_pred.jsonl", "encoder"),
    ("listed_mix_1M", PAPER / "output/jobbert_zh_listed_1m/crf_v3_seed42/test_pred.jsonl", "encoder"),
    ("human380_v3merge", PAPER / "output/jobbert_1m_human380_v3merge_seed42/test_pred.jsonl", "encoder"),
    ("RoBERTa_wwm_v3_s42", PAPER / "output/cn_roberta_wwm_crf/smoke_goldstyle_v3_seed42/test_pred.jsonl", "encoder"),
    ("RoBERTa_wwm_v3_s123", PAPER / "output/encoder_3seed/cn_roberta_wwm_v3/seed_123/test_pred.jsonl", "encoder"),
    ("RoBERTa_wwm_v3_s2026", PAPER / "output/encoder_3seed/cn_roberta_wwm_v3/seed_2026/test_pred.jsonl", "encoder"),
    ("JobBERT_1M_cws_retrain", PAPER / "output/jobbert_zh_1m/crf_lskt_v4_cws_seed42/test_pred.jsonl", "encoder"),
]

# Used when `output/` is not cloned. Raw jsonl is jieba-snapped at eval time.
FROZEN = PAPER / "data/frozen_preds"
FROZEN_FALLBACK = {
    "JobBERT_1M_v4": (FROZEN / "jobbert_1m_v4.jsonl", "encoder_v4_needs_cws"),
    "JobBERT_3M_v4": (FROZEN / "jobbert_3m_v4.jsonl", "encoder_v4_needs_cws"),
    "JobBERT_1M_v4_raw": (FROZEN / "jobbert_1m_v4.jsonl", "encoder_v4_needs_cws"),
    "JobBERT_3M_v4_raw": (FROZEN / "jobbert_3m_v4.jsonl", "encoder_v4_needs_cws"),
    "JobBERT_1M_cws_retrain": (FROZEN / "jobbert_1m_v4_cws_retrain.jsonl", "encoder"),
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


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_frozen_golds() -> tuple[list[dict], list[dict] | None, dict]:
    if not GOLD_HYBRID.is_file():
        raise SystemExit(f"missing frozen hybrid gold: {GOLD_HYBRID}")
    digest = sha256_file(GOLD_HYBRID)
    if digest != HYBRID_SHA256:
        raise SystemExit(
            f"hybrid gold SHA-256 is {digest}, expected {HYBRID_SHA256}. "
            "Refusing to score against a rewritten file."
        )
    hybrid = cws.load_jsonl(GOLD_HYBRID)
    sim_cws = cws.load_jsonl(GOLD_980) if GOLD_980.is_file() else None
    n_overlay = sum(1 for r in hybrid if r.get("hybrid_source") == "simhuman980_cws")
    meta = {
        "n_hybrid": len(hybrid),
        "n_simhuman_overlay": n_overlay,
        "n_sop_rest": len(hybrid) - n_overlay,
        "loaded_existing": True,
        "gold_980_present": sim_cws is not None,
        "hybrid_sha256": digest,
    }
    return hybrid, sim_cws, meta


def build_golds_lab_only() -> tuple[list[dict], list[dict], dict]:
    """Rebuild hybrid from SOP-CWS + SimHuman. Lab-only; changes SHA-256."""
    sop = {rec_id(r): r for r in cws.load_jsonl(SOP_CWS)}
    sim_raw = cws.load_jsonl(SIM)
    sim_cws = [cws.rewrite_record(r, tag_field="list_of_selection_bio4") for r in sim_raw]
    sim_map = {rec_id(r): r for r in sim_cws}
    missing = [i for i in sim_map if i not in sop]
    hybrid = []
    n_overlay = 0
    for gid, rec in sop.items():
        if gid in sim_map:
            row = dict(sim_map[gid])
            row["hybrid_source"] = "simhuman980_cws"
            n_overlay += 1
        else:
            row = dict(rec)
            row["hybrid_source"] = "sop_cws"
        row["id"] = gid
        hybrid.append(row)
    meta = {
        "n_hybrid": len(hybrid),
        "n_simhuman_overlay": n_overlay,
        "n_sop_rest": len(hybrid) - n_overlay,
        "simhuman_ids_not_in_sop_cws": missing,
        "loaded_existing": False,
        "wrote_gold": True,
    }
    cws.write_jsonl(GOLD_980, sim_cws)
    cws.write_jsonl(GOLD_HYBRID, hybrid)
    return hybrid, sim_cws, meta


def snap_and_fill(name: str, src: Path, already_cws: bool, gold_map: dict[str, dict]) -> Path:
    dst = PRED_CWS_DIR / f"{name}.jsonl"
    if already_cws and src.is_file():
        rows = cws.load_jsonl(src)
    else:
        raw = cws.load_jsonl(src)
        rows = [cws.rewrite_record(r, tag_field=None) for r in raw]
    by_id = {}
    for r in rows:
        try:
            by_id[rec_id(r)] = r
        except Exception:
            continue
    filled = []
    n_fill = 0
    for gid, g in gold_map.items():
        if gid in by_id:
            filled.append(by_id[gid])
        else:
            filled.append(empty_pred(g))
            n_fill += 1
    extra = [r for i, r in by_id.items() if i not in gold_map]
    out_rows = filled + extra
    cws.write_jsonl(dst, out_rows)
    return dst, n_fill, len(by_id)


def slim(gold_path: Path, pred_path: Path) -> dict:
    r = score(str(gold_path), str(pred_path), align_mode="official", n_boot=0)
    te, tr = r["typed_exact"], r["typed_relaxed"]
    return {
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


def mean_std(xs: list[float]) -> tuple[float, float]:
    if not xs:
        return 0.0, 0.0
    m = sum(xs) / len(xs)
    if len(xs) == 1:
        return m, 0.0
    var = sum((x - m) ** 2 for x in xs) / (len(xs) - 1)
    return m, var ** 0.5


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "model",
                "kind",
                "n_filled_empty",
                "full2601_typed_exact_p",
                "full2601_typed_exact_r",
                "full2601_typed_exact_f1",
                "full2601_typed_relaxed_f1",
                "full2601_collapsed_exact_f1",
                "simhuman980_typed_exact_f1",
                "simhuman980_typed_relaxed_f1",
                "alignment_ok_2601",
            ]
        )
        for r in rows:
            if "full2601" not in r:
                w.writerow([r.get("model"), r.get("kind"), "", "", "", "", "", "", "", "", ""])
                continue
            a, b = r["full2601"], r.get("simhuman980") or {}
            w.writerow(
                [
                    r["model"],
                    r["kind"],
                    r["n_filled_empty"],
                    f"{a['typed_exact_p']:.6f}",
                    f"{a['typed_exact_r']:.6f}",
                    f"{a['typed_exact_f1']:.6f}",
                    f"{a['typed_relaxed_f1']:.6f}",
                    f"{a['collapsed_exact_f1']:.6f}",
                    f"{b.get('typed_exact_f1', 0):.6f}" if b else "",
                    f"{b.get('typed_relaxed_f1', 0):.6f}" if b else "",
                    int(a["alignment_ok"]),
                ]
            )


def main() -> int:
    ap = argparse.ArgumentParser(description="Score models against frozen V4 hybrid gold (read-only by default).")
    ap.add_argument(
        "--rebuild-gold",
        action="store_true",
        help="Lab only: rebuild hybrid gold from SOP-CWS + SimHuman (changes SHA-256).",
    )
    ap.add_argument(
        "--paper-main-only",
        action="store_true",
        help="Score only JobBERT_3M_v4 (paper-main encoder 0.4331). Not the SOP LLM table.",
    )
    ap.add_argument(
        "--use-frozen",
        action="store_true",
        help="Prefer data/frozen_preds/ even when output/ CRF dumps exist.",
    )
    ap.add_argument(
        "--write-committed-csv",
        action="store_true",
        help="Overwrite tables/hybrid_cws_simhuman980_all_models.csv (lab).",
    )
    ap.add_argument("--out-dir", default=str(OUT), help="Snapped preds and eval.json (not gold).")
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    pred_dir = out_dir / "preds_cws"
    out_dir.mkdir(parents=True, exist_ok=True)
    pred_dir.mkdir(parents=True, exist_ok=True)
    global PRED_CWS_DIR
    PRED_CWS_DIR = pred_dir

    if args.rebuild_gold:
        hybrid, sim_cws, gmeta = build_golds_lab_only()
        print("WARNING: rebuilt hybrid gold; SHA-256 no longer matches the paper freeze", flush=True)
    else:
        hybrid, sim_cws, gmeta = load_frozen_golds()
    gold_map = {rec_id(r): r for r in hybrid}
    print(json.dumps(gmeta, ensure_ascii=False))

    models = MODELS
    if args.paper_main_only:
        models = [m for m in MODELS if m[0] in PAPER_MAIN_MODELS]

    rows = []
    for name, path, kind in models:
        if args.use_frozen and name in FROZEN_FALLBACK:
            path, kind = FROZEN_FALLBACK[name]
        elif not path.is_file() and name in FROZEN_FALLBACK:
            path, kind = FROZEN_FALLBACK[name]
        if not path.is_file():
            rows.append({"model": name, "kind": kind, "missing_file": str(path)})
            print(f"MISSING {name} {path}")
            continue
        already = kind == "encoder_v4_cws_ready"
        pred_cws, n_fill, n_raw = snap_and_fill(name, path, already, gold_map)
        s2601 = slim(GOLD_HYBRID, pred_cws)
        s980 = slim(GOLD_980, pred_cws) if sim_cws is not None and GOLD_980.is_file() else None
        rec = {
            "model": name,
            "kind": kind,
            "pred_src": str(path),
            "pred_cws": str(pred_cws),
            "n_raw_ids": n_raw,
            "n_filled_empty": n_fill,
            "full2601": s2601,
            "simhuman980": s980,
        }
        rows.append(rec)
        rel980 = f" | 980 exact={s980['typed_exact_f1']:.4f} rel={s980['typed_relaxed_f1']:.4f}" if s980 else ""
        print(
            f"{name:28s} 2601 exact={s2601['typed_exact_f1']:.6f} rel={s2601['typed_relaxed_f1']:.6f}"
            f"{rel980} fill={n_fill} ok={s2601['alignment_ok']}"
        )

    def group_mean(prefix: str, keys: list[str], metric: str = "typed_exact_f1") -> dict:
        xs = []
        ys = []
        for r in rows:
            if r.get("model") in keys and "full2601" in r:
                xs.append(r["full2601"][metric])
                ys.append(r["full2601"]["typed_relaxed_f1"])
        m, s = mean_std(xs)
        rm, rs = mean_std(ys)
        return {"models": keys, "n": len(xs), "exact_mean": m, "exact_std": s, "relaxed_mean": rm, "relaxed_std": rs}

    summaries = {
        "JobBERT_1M_v3_3seed": group_mean(
            "1m", ["JobBERT_1M_v3_s42", "JobBERT_1M_v3_s123", "JobBERT_1M_v3_s2026"]
        ),
        "JobBERT_3M_ckpt65k_3seed": group_mean(
            "3m",
            ["JobBERT_3M_ckpt65k_s42", "JobBERT_3M_ckpt65k_s123", "JobBERT_3M_ckpt65k_s2026"],
        ),
        "domain_mix_1M_3seed": group_mean(
            "dom", ["domain_mix_1M_s42", "domain_mix_1M_s123", "domain_mix_1M_s2026"]
        ),
        "RoBERTa_wwm_v3_3seed": group_mean(
            "rob", ["RoBERTa_wwm_v3_s42", "RoBERTa_wwm_v3_s123", "RoBERTa_wwm_v3_s2026"]
        ),
    }

    report = {
        "protocol": "jieba_bilateral",
        "test_gold_full": str(GOLD_HYBRID),
        "test_gold_980": str(GOLD_980) if sim_cws is not None else None,
        "gold_note": "2601 IDs = 980 SimHuman rule_v4 jieba-snapped + remaining SOP-CWS. Not Gold v2. Not human-final.",
        "gold_v2_untouched": True,
        "hybrid_read_only": not args.rebuild_gold,
        "hybrid_sha256": sha256_file(GOLD_HYBRID),
        "scorer": "cnss-lskt-1.2.0",
        "n_boot": 0,
        "gold_meta": gmeta,
        "summaries": summaries,
        "rows": rows,
    }
    (out_dir / "eval.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    csv_out = out_dir / "paper_main.csv"
    write_csv(csv_out, rows)
    print("wrote", csv_out)
    if args.write_committed_csv:
        write_csv(CSV_COMMITTED, rows)
        print("wrote committed", CSV_COMMITTED)
    print("summaries", json.dumps(summaries, indent=2))
    after = sha256_file(GOLD_HYBRID)
    if after != HYBRID_SHA256 and not args.rebuild_gold:
        raise SystemExit(f"hybrid gold SHA-256 changed during eval: {after}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
