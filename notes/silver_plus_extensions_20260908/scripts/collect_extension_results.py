#!/usr/bin/env python3
"""Assemble EXTENSION_RESULTS after official runs. Does not drop bad scores."""
from __future__ import annotations

import csv
import json
import os
import statistics
from pathlib import Path

PAPER = Path("/home/guojingli3/Chinese-Skillspan-Benchmark/Chinese_skill_benchmark_Paper")
EXT = PAPER / "output/silver_plus_extensions"


def loadj(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def mean_sd(xs):
    xs = [float(x) for x in xs]
    if not xs:
        return None, None
    if len(xs) == 1:
        return xs[0], 0.0
    return statistics.mean(xs), statistics.stdev(xs)


def qwen_official_score(gold_dir: Path) -> Path | None:
    for name in ("score.json", "score_SFT.json", "score_A.json"):
        p = gold_dir / name
        if p.is_file():
            return p
    return None


def harvest_resource(seed_dir: Path, gold_dir: Path) -> dict:
    out = {}
    cfg = seed_dir / "run_config.json"
    if cfg.is_file():
        rc = loadj(cfg)
        out["train_seconds"] = rc.get("seconds")
        out["train_device"] = rc.get("device")
    sel = seed_dir / "selected_checkpoint.json"
    if sel.is_file():
        out["selected_epoch"] = loadj(sel).get("selected_epoch")
        out["dev_typed_exact_f1"] = loadj(sel).get("value")
    res = gold_dir / "RESOURCE.json"
    if res.is_file():
        out["infer_resource"] = loadj(res)
    return out


def main() -> int:
    rows = []
    qwen_root = EXT / "qwen14b_b2"
    for seed in (42, 43, 44):
        seed_dir = qwen_root / f"seed{seed}"
        sel = seed_dir / "selected_checkpoint.json"
        gout = seed_dir / "gold150"
        scp = qwen_official_score(gout)
        if scp is None:
            continue
        sc = loadj(scp)
        rec = {
            "family": "qwen14b",
            "condition": "SFT",
            "seed": seed,
            "selected_epoch": loadj(sel)["selected_epoch"] if sel.is_file() else None,
            "gold150_exact_f1": sc["gold150"]["typed_exact_f1"],
            "gold150_relaxed_f1": sc["gold150"]["typed_relaxed_f1"],
            "challenge100_exact_f1": sc["challenge100"]["typed_exact_f1"],
            "audit50_exact_f1": sc["audit50"]["typed_exact_f1"],
            "per_type_exact": sc["gold150"].get("per_type_exact"),
            "empty_label_fp": sc.get("empty_label", {}).get("empty_label_fp"),
            "parse_fail": sc.get("parse", {}).get("n_fail"),
            "complete_150": sc.get("coverage", {}).get("complete_150"),
            "mean_input_tokens": (sc.get("cost") or {}).get("mean_input_tokens"),
            "mean_output_tokens": (sc.get("cost") or {}).get("mean_output_tokens"),
            "mean_seconds": (sc.get("cost") or {}).get("mean_seconds"),
            "resource": harvest_resource(seed_dir, gout),
            "score_file": str(scp.name),
        }
        rows.append(rec)
    hem_root = EXT / "hem_jobbert3m"
    hem_cfg = EXT / "HEM_CONFIG.json"
    names = []
    if hem_cfg.is_file():
        names = loadj(hem_cfg).get("conditions") or []
    for cond in names:
        for seed in (42, 43, 44):
            out_dir = hem_root / cond / f"seed{seed}"
            scp = out_dir / "score_gold150.json"
            if not scp.is_file():
                continue
            sc = loadj(scp)
            rec = {
                "family": "jobbert3m_reinit_crf",
                "condition": cond,
                "seed": seed,
                "gold150_exact_f1": sc["gold150"]["typed_exact_f1"],
                "gold150_relaxed_f1": sc["gold150"]["typed_relaxed_f1"],
                "challenge100_exact_f1": sc["challenge100"]["typed_exact_f1"],
                "audit50_exact_f1": sc["audit50"]["typed_exact_f1"],
                "per_type_exact": sc["gold150"].get("per_type_exact"),
                "complete_150": sc.get("coverage", {}).get("complete_150"),
            }
            rc = out_dir / "run_config.json"
            if rc.is_file():
                rec["resource"] = loadj(rc)
            res = out_dir / "RESOURCE.json"
            if res.is_file():
                rec["resource"] = {**(rec.get("resource") or {}), **loadj(res)}
            rows.append(rec)
    summary = {}
    by = {}
    for r in rows:
        by.setdefault((r["family"], r["condition"]), []).append(r)
    for key, rs in by.items():
        m, sd = mean_sd([x["gold150_exact_f1"] for x in rs])
        summary[f"{key[0]}|{key[1]}"] = {
            "n_seeds": len(rs),
            "gold150_exact_mean": m,
            "gold150_exact_sample_sd": sd,
            "seeds": [x["seed"] for x in rs],
            "sample_sd_is_not_test_ci": True,
        }
    payload = {
        "rows": rows,
        "summary": summary,
        "jobbert1m": "skipped_not_comparable_pretrain_stage",
        "official_qwen_condition": "SFT",
        "knn_random_abc_not_official": True,
        "not_compared_to_0.4331": True,
        "not_compared_to_0.1724": True,
        "qwen_b2_only_not_b2_vs_b1_validation": True,
        "old_json_offset_v3_retained_separately": True,
        "vs_v3_not_all_attributed_to_data_volume": True,
        "slurm_job_id": os.environ.get("SLURM_JOB_ID", "7349"),
    }
    (EXT / "EXTENSION_RESULTS.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    csv_path = EXT / "EXTENSION_RESULTS.csv"
    fields = [
        "family",
        "condition",
        "seed",
        "gold150_exact_f1",
        "gold150_relaxed_f1",
        "challenge100_exact_f1",
        "audit50_exact_f1",
        "empty_label_fp",
        "parse_fail",
        "complete_150",
        "mean_input_tokens",
        "mean_output_tokens",
        "mean_seconds",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    repro = {
        "data": "v6a_nocross_20260908 from v6a without editing v6a",
        "gold150_sha256": "ca8db0bc386c24543fec845d42ea8e24883eb67b8ce75129ac1768c5c0310fd0",
        "scripts": [
            "scripts/qwen_ext_protocol.py",
            "scripts/test_qwen_ext_parser.py",
            "scripts/train_qwen_ext_sft.py",
            "scripts/infer_qwen_ext_sft.py",
            "scripts/eval_gold150_ext.py",
            "scripts/sample_hem_ext.py",
            "scripts/train_jobbert_ext.py",
            "scripts/run_extension_chain.sh",
            "scripts/extension_chain.sbatch",
        ],
        "superseded_not_official": [
            "scripts/infer_qwen_ext_abc.py",
            "scripts/build_qwen_knn_index.py",
            "knn_index/",
        ],
        "max_official_trains_this_round": 12,
        "gpu_cap": 2,
        "jobbert1m": "skipped",
        "slurm_job_id": os.environ.get("SLURM_JOB_ID", "7349"),
    }
    (EXT / "REPRODUCTION_MANIFEST.json").write_text(json.dumps(repro, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"n_rows": len(rows), "summary_keys": list(summary)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
