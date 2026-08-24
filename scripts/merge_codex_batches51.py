#!/usr/bin/env python3
"""Merge Codex batches 01-51 into LSKT v4 test silver. Does not touch Gold v2 or train."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
sys.path.insert(0, str(PAPER / "scripts"))
from merge_codex_corrections import (  # noqa: E402
    align_record,
    load_json,
    patch_compact,
    patch_file,
)

PACK = PAPER / "reports/sandbox_lskt_v4_silver/codex_pack"
INP = PACK / "batches_51"
OUTS = PACK / "outputs_51"
SOURCE = "codex_batches51"


def main() -> int:
    test_full = {str(r["id"]): r for r in load_json(PAPER / "data/test_lskt_v4_silver.jsonl")}
    batch_reports = []
    aligned: dict[str, list[tuple[int, int, str]]] = {}
    all_corr_ids: list[str] = []
    types: Counter[str] = Counter()
    n_empty = n_changed = n_over = 0
    align_errors: list[dict] = []
    id_problems: list[dict] = []

    for b in range(1, 52):
        gold_path = INP / f"batch_{b:02d}.jsonl"
        corr_path = OUTS / f"batch_{b:02d}_corrected.json"
        gold_rows = load_json(gold_path)
        gold_ids = [str(r["id"]) for r in gold_rows]
        gold_map = {str(r["id"]): r for r in gold_rows}
        corr = load_json(corr_path)
        corr_ids = [str(r["id"]) for r in corr]
        missing = [i for i in gold_ids if i not in set(corr_ids)]
        extra = [i for i in corr_ids if i not in set(gold_ids)]
        order_ok = corr_ids == gold_ids
        if missing or extra or not order_ok:
            id_problems.append(
                {
                    "batch": b,
                    "n_gold": len(gold_ids),
                    "n_corr": len(corr_ids),
                    "order_ok": order_ok,
                    "n_missing": len(missing),
                    "n_extra": len(extra),
                    "missing_head": missing[:8],
                    "extra_head": extra[:8],
                }
            )
        for rec in corr:
            rid = str(rec["id"])
            if rid not in gold_map:
                continue
            if rid in aligned:
                id_problems.append({"batch": b, "dup_id": rid})
                continue
            base = test_full.get(rid) or gold_map[rid]
            toks = [str(t) for t in (base.get("tokens") or list(base.get("sentence") or ""))]
            sent = base.get("sentence") or gold_map[rid].get("sentence") or ""
            spans, errs = align_record(toks, sent, rec.get("spans") or [])
            if errs:
                align_errors.append({"id": rid, "batch": b, "errs": errs[:12], "n_errs": len(errs)})
            aligned[rid] = spans
            all_corr_ids.append(rid)
            old = gold_map[rid].get("spans") or []
            old_txt = [(s.get("start"), s.get("end"), s.get("type")) for s in old]
            if [(a, b_, t) for a, b_, t in spans] != old_txt:
                n_changed += 1
            if not spans:
                n_empty += 1
            for a, b_, t in spans:
                types[t] += 1
                if (b_ - a) > 8:
                    n_over += 1
        batch_reports.append(
            {
                "batch": b,
                "n_gold": len(gold_ids),
                "n_corr": len(corr_ids),
                "n_merged": sum(1 for i in gold_ids if i in aligned),
                "order_ok": order_ok,
            }
        )

    expected = []
    for b in range(1, 52):
        expected.extend(str(r["id"]) for r in load_json(INP / f"batch_{b:02d}.jsonl"))
    report = {
        "gold_v2_untouched": True,
        "train_untouched": True,
        "source": SOURCE,
        "n_files": 51,
        "n_expected": len(expected),
        "n_merged": len(aligned),
        "n_unique_expected": len(set(expected)),
        "missing_ids": sorted(set(expected) - set(aligned)),
        "extra_ids": sorted(set(aligned) - set(expected)),
        "n_changed_vs_rule": n_changed,
        "n_empty": n_empty,
        "n_over_cap8": n_over,
        "n_align_error_sents": len(align_errors),
        "type_counts": dict(types),
        "id_problems": id_problems,
        "align_errors_head": align_errors[:40],
        "batches": batch_reports,
        "patched": [],
    }

    report["patched"].append(patch_file(PAPER / "data/test_lskt_v4_silver.jsonl", aligned, SOURCE))
    report["patched"].append(patch_file(PAPER / "data/test_lskt_v4_silver_g2ids.jsonl", aligned, SOURCE))
    patched_rows = [r for r in load_json(PAPER / "data/test_lskt_v4_silver.jsonl") if str(r["id"]) in aligned]
    report["patched"].append(patch_compact(PACK / "test_compact.jsonl", patched_rows))
    report["patched"].append(patch_compact(PACK / "test_g2ids_compact.jsonl", patched_rows))

    out_json = PACK / "MERGE_batches51.json"
    out_md = PACK / "MERGE_batches51.md"
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# Codex batches 01–51 merge (sandbox)",
        "",
        "Gold v2 untouched. Train/dev silver untouched.",
        "",
        f"- merged {report['n_merged']} / {report['n_expected']} expected Gold-v2 IDs",
        f"- changed vs rule_v4: {n_changed}",
        f"- empty: {n_empty}",
        f"- align-error sentences (bad spans dropped, rest kept): {len(align_errors)}",
        f"- spans >8 tokens kept: {n_over}",
        f"- types: {dict(types)}",
        f"- id problems: {len(id_problems)}",
        "",
        "Together with sample_50, test_g2ids should be fully Codex-corrected.",
        "Do not copy into confirmed-results.md.",
    ]
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                k: report[k]
                for k in (
                    "n_merged",
                    "n_expected",
                    "missing_ids",
                    "n_changed_vs_rule",
                    "n_empty",
                    "n_align_error_sents",
                    "n_over_cap8",
                    "type_counts",
                    "id_problems",
                    "patched",
                )
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if not report["missing_ids"] and not id_problems else 1


if __name__ == "__main__":
    raise SystemExit(main())
