#!/usr/bin/env python3
"""Aggregate Silver-dev official scores for Qwen Silver-2500 LoRA. Not a paper cell."""
from __future__ import annotations

import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
sys.path.insert(0, str(PAPER / "scripts"))
sys.path.insert(0, str(PAPER / "scorer"))
from qwen_silver2500_sft_lib import OUT_ROOT, gold_row, load_jsonl  # noqa: E402
from score_lskt import score  # noqa: E402
from train_qwen_silver2500_sft import score_pred  # noqa: E402

DEV = PAPER / "output/silver_public_2500_student_20260913/data/dev.jsonl"


def slim(sc: dict) -> dict:
    return {
        "n": sc.get("n_matched"),
        "typed_exact_p": sc.get("typed_exact_p"),
        "typed_exact_r": sc.get("typed_exact_r"),
        "typed_exact_f1": sc.get("typed_exact_f1"),
        "typed_relaxed_f1": sc.get("typed_relaxed_f1"),
        "alignment_ok": sc.get("alignment_ok"),
    }


def domain_f1(gold_rows: list[dict], pred_path: Path, tmp: Path) -> dict:
    gold_by = {r["id"]: r for r in gold_rows}
    preds = load_jsonl(pred_path)
    by = defaultdict(list)
    for p in preds:
        d = (gold_by[p["id"]].get("source_domain") or "unk")
        by[d].append((gold_by[p["id"]], p))
    out = {}
    tmp.mkdir(parents=True, exist_ok=True)
    for domain, pairs in by.items():
        g = [a for a, _ in pairs]
        p = [b for _, b in pairs]
        sc = score_pred(g, p, tmp / domain)
        out[domain] = {"n": len(pairs), "typed_exact_f1": sc["typed_exact_f1"], "typed_relaxed_f1": sc["typed_relaxed_f1"]}
    return out


def main() -> int:
    gold = [gold_row(r) for r in load_jsonl(DEV)]
    seeds = []
    for s in (42, 43, 44):
        sel_p = OUT_ROOT / "runs" / f"seed{s}" / "selected_checkpoint.json"
        pred_p = OUT_ROOT / "runs" / f"seed{s}" / "adapter" / "dev_pred.jsonl"
        if not sel_p.is_file() or not pred_p.is_file():
            print(json.dumps({"missing": str(sel_p)}), flush=True)
            return 2
        sel = json.loads(sel_p.read_text(encoding="utf-8"))
        sc = score_pred(gold, load_jsonl(pred_p), OUT_ROOT / "runs" / f"seed{s}" / "silver_test")
        rec = {
            "seed": s,
            "selected_epoch": sel.get("selected_epoch"),
            **slim(sc),
            "outcomes": {},
            "by_domain": domain_f1(gold, pred_p, OUT_ROOT / "runs" / f"seed{s}" / "domain_tmp"),
        }
        for p in load_jsonl(pred_p):
            rec["outcomes"][p.get("outcome") or "unknown"] = rec["outcomes"].get(p.get("outcome") or "unknown", 0) + 1
        seeds.append(rec)
    f1s = [r["typed_exact_f1"] for r in seeds]
    out = {
        "test_set": "public_api_silver2500_dev",
        "n_test": 182,
        "protocol": "silver_public_api_v1.0_qwen_lora_sft",
        "base_model": "Qwen2.5-14B-Instruct",
        "not_gold150": True,
        "not_paper_main": True,
        "not_comparable_to_0.4331": True,
        "not_shared_prompt_0.5403": True,
        "jobbert_same_split_typed_exact": 0.1874,
        "note": "Student vs Silver teacher labels on the 182-sentence held-out split. Checkpoint selected on the same 182. Not human gold.",
        "seeds": seeds,
        "mean_typed_exact": statistics.mean(f1s),
        "sd_typed_exact": statistics.stdev(f1s) if len(f1s) > 1 else None,
    }
    (OUT_ROOT / "COMPARE_silver_dev.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
