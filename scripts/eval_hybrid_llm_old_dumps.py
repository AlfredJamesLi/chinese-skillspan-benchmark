#!/usr/bin/env python3
"""Score frozen LLM dumps on the matched-protocol hybrid gold. No API calls.

Missing Gold IDs are empty-filled so every model is scored on all 2601 IDs.
Writes a fill queue for Claude / Kimi so those IDs can be completed later.
Does not overwrite Gold v2 or original dumps.

Repro: python scripts/eval_hybrid_llm_old_dumps.py
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
sys.path.insert(0, str(PAPER / "scripts"))
sys.path.insert(0, str(PAPER / "scorer"))
import cws_snap as cws  # noqa: E402
from eval_hybrid_cws_simhuman import empty_pred, slim  # noqa: E402
from score_lskt import rec_id  # noqa: E402

OUT = PAPER / "reports/sandbox_lskt_v4_silver/hybrid_cws_eval"
PRED_DIR = OUT / "preds_cws_old_dumps"
GOLD_HYBRID = PAPER / "data/test_lskt_v4_cws_simhuman980_hybrid.jsonl"
GOLD_980 = PAPER / "data/test_lskt_v4_simhuman980_cws.jsonl"
CSV_OUT = PAPER / "tables/hybrid_cws_llm_old_dumps.csv"
QUEUE_DIR = OUT / "fill_later"

LLMS = [
    ("ChatGPT", PAPER / "reports/views/ChatGPT_unique_first_v2.jsonl"),
    ("Claude", PAPER / "reports/views/Claude_unique_first_v2.jsonl"),
    ("Kimi", PAPER / "reports/views/Kimi_unique_first_v2.jsonl"),
    ("DeepSeek", PAPER / "reports/views/DeepSeek_unique_first_v2.jsonl"),
    ("Qwen", PAPER / "reports/views/Qwen_unique_first_v2.jsonl"),
]


def pred_ids(src: Path) -> dict[str, dict]:
    by_id = {}
    for r in cws.load_jsonl(src):
        try:
            by_id[rec_id(r)] = r
        except Exception:
            continue
    return by_id


def slim_queue_row(gold: dict, in_980: bool) -> dict:
    return {
        "id": rec_id(gold),
        "sentence": gold.get("sentence") or "",
        "source_domain": gold.get("source_domain") or "",
        "title": gold.get("title") or gold.get("job_title") or "",
        "hybrid_source": gold.get("hybrid_source") or "",
        "in_simhuman980": in_980,
    }


def main() -> int:
    if not GOLD_HYBRID.is_file() or not GOLD_980.is_file():
        raise SystemExit(f"missing gold: {GOLD_HYBRID} or {GOLD_980}")
    PRED_DIR.mkdir(parents=True, exist_ok=True)
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)

    hybrid = cws.load_jsonl(GOLD_HYBRID)
    gold_map = {rec_id(r): r for r in hybrid}
    ids_980 = {rec_id(r) for r in cws.load_jsonl(GOLD_980)}
    if len(gold_map) != 2601:
        raise SystemExit(f"expected 2601 hybrid IDs, got {len(gold_map)}")

    rows = []
    coverage = []
    for name, src in LLMS:
        if not src.is_file():
            raise SystemExit(f"missing dump: {src}")
        by_id = pred_ids(src)
        missing = [gid for gid in gold_map if gid not in by_id]
        missing.sort()
        n_980_miss = sum(1 for gid in missing if gid in ids_980)
        coverage.append(
            {
                "model": name,
                "dump": str(src),
                "n_dump_ids": len(by_id),
                "n_missing_vs_hybrid2601": len(missing),
                "n_missing_in_simhuman980": n_980_miss,
                "complete": len(missing) == 0,
            }
        )

        snapped = [cws.rewrite_record(r, tag_field=None) for r in by_id.values()]
        snap_by = {rec_id(r): r for r in snapped}
        filled = []
        for gid, g in gold_map.items():
            filled.append(snap_by[gid] if gid in snap_by else empty_pred(g))
        pred_path = PRED_DIR / f"{name}.jsonl"
        cws.write_jsonl(pred_path, filled)
        s2601 = slim(GOLD_HYBRID, pred_path)
        s980 = slim(GOLD_980, pred_path)
        rec = {
            "model": name,
            "n_dump_ids": len(by_id),
            "n_missing": len(missing),
            "n_missing_in_simhuman980": n_980_miss,
            "status": "complete" if not missing else f"incomplete_empty_fill_{len(missing)}",
            "full2601": s2601,
            "simhuman980": s980,
        }
        rows.append(rec)
        print(
            f"{name:10s} dump={len(by_id):4d} miss={len(missing):3d} "
            f"(980 miss {n_980_miss:3d})  "
            f"2601 exact={s2601['typed_exact_f1']:.4f} rel={s2601['typed_relaxed_f1']:.4f}  "
            f"980 exact={s980['typed_exact_f1']:.4f} rel={s980['typed_relaxed_f1']:.4f}"
        )

        if missing:
            queue = [slim_queue_row(gold_map[gid], gid in ids_980) for gid in missing]
            qpath = QUEUE_DIR / f"missing_queue_{name}.jsonl"
            ipath = QUEUE_DIR / f"missing_ids_{name}.txt"
            cws.write_jsonl(qpath, queue)
            ipath.write_text("\n".join(missing) + "\n", encoding="utf-8")
            print(f"  wrote {qpath.name} n={len(queue)}")

    report = {
        "protocol": "jieba_bilateral_old_llm_dumps",
        "api_calls": 0,
        "test_gold_full": str(GOLD_HYBRID),
        "test_gold_980": str(GOLD_980),
        "note": "Frozen @@span## dumps, jieba-snapped. Missing IDs empty-filled. Not Gold v2. Not a new API run.",
        "scorer": "cnss-lskt-1.2.0",
        "coverage": coverage,
        "rows": rows,
    }
    (OUT / "llm_old_dumps.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    with CSV_OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "model",
                "status",
                "n_dump_ids",
                "n_missing",
                "n_missing_in_simhuman980",
                "full2601_typed_exact_f1",
                "full2601_typed_relaxed_f1",
                "simhuman980_typed_exact_f1",
                "simhuman980_typed_relaxed_f1",
                "alignment_ok_2601",
            ]
        )
        for r in rows:
            a, b = r["full2601"], r["simhuman980"]
            w.writerow(
                [
                    r["model"],
                    r["status"],
                    r["n_dump_ids"],
                    r["n_missing"],
                    r["n_missing_in_simhuman980"],
                    f"{a['typed_exact_f1']:.6f}",
                    f"{a['typed_relaxed_f1']:.6f}",
                    f"{b['typed_exact_f1']:.6f}",
                    f"{b['typed_relaxed_f1']:.6f}",
                    int(a["alignment_ok"]),
                ]
            )
    print("wrote", CSV_OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
