#!/usr/bin/env python3
"""Overlay page-1 200 human labels onto the 980-queue IDs inside V4 hybrid.

Does not overwrite gold_canonical_v2.jsonl or
data/test_lskt_v4_cws_simhuman980_hybrid.jsonl.
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
sys.path.insert(0, str(PAPER / "scripts"))
sys.path.insert(0, str(PAPER / "scorer"))
import cws_snap as cws  # noqa: E402
from score_lskt import rec_id, score  # noqa: E402

HYBRID = PAPER / "data/test_lskt_v4_cws_simhuman980_hybrid.jsonl"
GOLD980 = PAPER / "data/test_lskt_v4_simhuman980_cws.jsonl"
HUMAN = PAPER / "data/human_gold_page1_200.jsonl"
OUT_H = PAPER / "data/test_lskt_v4_hybrid_human200_raw.jsonl"
OUT_H_CWS = PAPER / "data/test_lskt_v4_hybrid_human200_cws.jsonl"
OUT_980 = PAPER / "data/test_lskt_v4_simhuman980_human200_raw.jsonl"
OUT_980_CWS = PAPER / "data/test_lskt_v4_simhuman980_human200_cws.jsonl"
CSV = PAPER / "tables/hybrid_human200_overlay_scores.csv"
JSON = PAPER / "reports/human980_doccano/hybrid_human200_overlay_scores.json"
PRED_DIR = PAPER / "reports/sandbox_lskt_v4_silver/hybrid_human200_eval/preds_cws"

FROZEN = PAPER / "data/frozen_preds"
MODELS = [
    ("JobBERT_3M_v4", FROZEN / "jobbert_3m_v4.jsonl", False),
    ("JobBERT_1M_v4", FROZEN / "jobbert_1m_v4.jsonl", False),
    ("JobBERT_1M_cws_retrain", FROZEN / "jobbert_1m_v4_cws_retrain.jsonl", False),
    ("ChatGPT", PAPER / "reports/views/ChatGPT_unique_first_v2.jsonl", False),
    ("DeepSeek", PAPER / "reports/views/DeepSeek_unique_first_v2.jsonl", False),
    ("Qwen", PAPER / "reports/views/Qwen_unique_first_v2.jsonl", False),
    ("Claude", PAPER / "reports/views/Claude_unique_first_v2.jsonl", False),
    ("Kimi", PAPER / "reports/views/Kimi_unique_first_v2.jsonl", False),
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


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


def overlay(base_rows: list[dict], human_map: dict[str, dict], *, snap: bool) -> list[dict]:
    out = []
    n = 0
    for rec in base_rows:
        gid = rec_id(rec)
        if gid not in human_map:
            out.append(dict(rec))
            continue
        h = human_map[gid]
        row = dict(rec)
        row["tokens"] = list(h["tokens"])
        row["list_of_selection_bio4"] = list(h["list_of_selection_bio4"])
        row["hybrid_source"] = "human980_page1_200_cws" if snap else "human980_page1_200"
        row["human_page"] = h.get("page")
        if snap:
            row = cws.rewrite_record(row, tag_field="list_of_selection_bio4")
            row["hybrid_source"] = "human980_page1_200_cws"
        n += 1
        out.append(row)
    if n != len(human_map):
        missing = sorted(set(human_map) - {rec_id(r) for r in base_rows})
        raise SystemExit(f"overlay hit {n}/{len(human_map)}; missing in base: {missing[:10]}")
    return out


def slim(gold: Path, pred: Path) -> dict:
    r = score(str(gold), str(pred), align_mode="official", n_boot=0)
    te, tr = r["typed_exact"], r["typed_relaxed"]
    return {
        "alignment_ok": bool(r.get("alignment_ok")),
        "n_gold": r.get("gold_n_unique_ids"),
        "n_matched": r.get("n_matched"),
        "n_missing": r.get("n_missing"),
        "n_filled_empty_in_pred_file": None,
        "typed_exact_p": round(te["precision"], 4),
        "typed_exact_r": round(te["recall"], 4),
        "typed_exact_f1": round(te["f1"], 4),
        "typed_relaxed_f1": round(tr["f1"], 4),
        "collapsed_exact_f1": round(r["collapsed_exact"]["f1"], 4),
    }


def fill_pred(src: Path, gold_map: dict[str, dict], dst: Path) -> tuple[Path, int]:
    raw = cws.load_jsonl(src)
    snapped = [cws.rewrite_record(r, tag_field=None) for r in raw]
    by_id = {}
    for r in snapped:
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
    cws.write_jsonl(dst, filled + extra)
    return dst, n_fill


def main() -> int:
    hybrid = cws.load_jsonl(HYBRID)
    g980 = cws.load_jsonl(GOLD980)
    human = {rec_id(r): r for r in cws.load_jsonl(HUMAN)}
    if len(human) != 200:
        raise SystemExit(f"expected 200 human ids, got {len(human)}")

    src_counts = {}
    for rec in hybrid:
        gid = rec_id(rec)
        if gid in human:
            src_counts[rec.get("hybrid_source")] = src_counts.get(rec.get("hybrid_source"), 0) + 1
    print("200 IDs in hybrid were:", src_counts)

    raw_h = overlay(hybrid, human, snap=False)
    cws_h = overlay(hybrid, human, snap=True)
    raw_980 = overlay(g980, human, snap=False)
    cws_980 = overlay(g980, human, snap=True)
    cws.write_jsonl(OUT_H, raw_h)
    cws.write_jsonl(OUT_H_CWS, cws_h)
    cws.write_jsonl(OUT_980, raw_980)
    cws.write_jsonl(OUT_980_CWS, cws_980)
    print("wrote", OUT_H.name, OUT_H_CWS.name)

    golds = {
        "orig_hybrid": HYBRID,
        "overlay_raw": OUT_H,
        "overlay_cws": OUT_H_CWS,
        "orig_980": GOLD980,
        "overlay_980_raw": OUT_980,
        "overlay_980_cws": OUT_980_CWS,
    }
    PRED_DIR.mkdir(parents=True, exist_ok=True)
    gold_map = {rec_id(r): r for r in cws_h}
    rows = []
    for name, path, _ in MODELS:
        if not path.is_file():
            rows.append({"model": name, "missing": str(path)})
            print("MISSING", name, path)
            continue
        pred, n_fill = fill_pred(path, gold_map, PRED_DIR / f"{name}.jsonl")
        rec = {"model": name, "n_filled_empty": n_fill, "pred": str(pred)}
        for k, gp in golds.items():
            rec[k] = slim(gp, pred)
        rows.append(rec)
        print(
            f"{name:28s} orig={rec['orig_hybrid']['typed_exact_f1']:.4f} "
            f"raw200={rec['overlay_raw']['typed_exact_f1']:.4f} "
            f"cws200={rec['overlay_cws']['typed_exact_f1']:.4f} "
            f"| 980 orig={rec['orig_980']['typed_exact_f1']:.4f} "
            f"cws200={rec['overlay_980_cws']['typed_exact_f1']:.4f} "
            f"fill={n_fill} ok={rec['overlay_cws']['alignment_ok']}"
        )

    JSON.parent.mkdir(parents=True, exist_ok=True)
    meta = {
        "note": "Replace 200 of 980 SimHuman IDs with human page-1 labels inside V4 hybrid. Not a new main gold.",
        "n_overlay": 200,
        "n_hybrid": 2601,
        "n_980": 980,
        "human_sha256": sha256_file(HUMAN),
        "orig_hybrid_sha256": sha256_file(HYBRID),
        "overlay_raw_sha256": sha256_file(OUT_H),
        "overlay_cws_sha256": sha256_file(OUT_H_CWS),
        "gold_v2_untouched": True,
        "orig_hybrid_untouched": True,
        "scorer": "cnss-lskt-1.2.0",
        "human_ids_were": src_counts,
        "rows": rows,
    }
    JSON.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    cols = [
        "model",
        "n_filled_empty",
        "orig2601_exact",
        "orig2601_relaxed",
        "overlay_raw2601_exact",
        "overlay_raw2601_relaxed",
        "overlay_cws2601_exact",
        "overlay_cws2601_relaxed",
        "orig980_exact",
        "overlay_cws980_exact",
        "overlay_cws980_relaxed",
        "alignment_ok_cws2601",
    ]
    with CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for r in rows:
            if "orig_hybrid" not in r:
                w.writerow([r.get("model"), "", "", "", "", "", "", "", "", "", "", ""])
                continue
            w.writerow(
                [
                    r["model"],
                    r["n_filled_empty"],
                    f"{r['orig_hybrid']['typed_exact_f1']:.4f}",
                    f"{r['orig_hybrid']['typed_relaxed_f1']:.4f}",
                    f"{r['overlay_raw']['typed_exact_f1']:.4f}",
                    f"{r['overlay_raw']['typed_relaxed_f1']:.4f}",
                    f"{r['overlay_cws']['typed_exact_f1']:.4f}",
                    f"{r['overlay_cws']['typed_relaxed_f1']:.4f}",
                    f"{r['orig_980']['typed_exact_f1']:.4f}",
                    f"{r['overlay_980_cws']['typed_exact_f1']:.4f}",
                    f"{r['overlay_980_cws']['typed_relaxed_f1']:.4f}",
                    int(r["overlay_cws"]["alignment_ok"]),
                ]
            )
    print("wrote", CSV)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
