#!/usr/bin/env python3
"""Emit verified machine-readable results from completed cells. Means live only in summaries, not results.jsonl."""
from __future__ import annotations

import csv
import hashlib
import json
import statistics
from pathlib import Path

ROOT = Path("/home/guojingli3/cnss_external_benchmarks_20260921")
sys_path_note = ROOT
import sys

sys.path.insert(0, str(ROOT))
from audit_and_lexicon import entities, read, score  # noqa: E402

PINS = {r["model"]: r["revision"] for r in json.loads((ROOT / "models.json").read_text())}
SOURCES = {r["dataset"]: r["revision"] for r in json.loads((ROOT / "sources.json").read_text()) if "dataset" in r}
MODEL_HF = {
    "xlm-roberta-large": "FacebookAI/xlm-roberta-large",
    "esco-xlm-roberta-large": "jjzha/esco-xlm-roberta-large",
}


def sha256(path: Path | None):
    if path is None or not path.exists():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(path: Path | None):
    if path is None:
        return None
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_jsonl(path: Path, rows):
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def common_rows():
    rows = []
    datasets = ["skillspan", "kompetencer", "gnehm", "green", "sayfullina", "fijo"]
    for ds in datasets:
        heads = ["tags_skill", "tags_knowledge"] if ds in ("skillspan", "kompetencer") else ["tags_skill"]
        for head in heads:
            for short, hf in MODEL_HF.items():
                for seed in (42, 43, 44):
                    cell = ROOT / "runs" / "full" / ds / head / short / str(seed)
                    result_p = cell / "result.json"
                    pred_p = cell / "test_predictions.jsonl"
                    cfg_p = cell / "config.json"
                    r = json.loads(result_p.read_text()) if result_p.exists() else None
                    status = "completed" if r and r.get("status") == "completed" and "test" in (r or {}) else ("failed" if r else "not_started")
                    test = (r or {}).get("test") or {}
                    rec = {
                        "track": "common",
                        "dataset": ds,
                        "subset": "public_release" if ds != "gnehm" else "public_ict",
                        "task": head,
                        "model": hf,
                        "protocol_id": "common_encoder_linear_20260921",
                        "seed": seed,
                        "status": status,
                        "metric": "typed_exact_micro_f1",
                        "scale": "0-1",
                        "value": test.get("f1") if status == "completed" else None,
                        "precision": test.get("precision") if status == "completed" else None,
                        "recall": test.get("recall") if status == "completed" else None,
                        "eval_split": "test",
                        "eval_n": sum(1 for _ in pred_p.open()) if pred_p.exists() else None,
                        "eval_unit": "sentence",
                        "selection_split": "dev",
                        "checkpoint_epoch": r.get("best_epoch") if r else None,
                        "dataset_revision": SOURCES.get(ds),
                        "model_revision": PINS[hf],
                        "code_revision": "run_common_encoder.py",
                        "scorer_revision": "audit_and_lexicon.entities",
                        "config_file": rel(cfg_p) if cfg_p.exists() else None,
                        "predictions_file": rel(pred_p) if pred_p.exists() else None,
                        "metrics_file": rel(result_p) if result_p.exists() else None,
                        "config_sha256": sha256(cfg_p),
                        "predictions_sha256": sha256(pred_p),
                        "metrics_sha256": sha256(result_p),
                        "notes": "New linear first-subword BIO head; not MaChAmp-CRF/NNOSE. IEEE 10-epoch dumps are historical_reference_only.",
                    }
                    rows.append(rec)
    return rows


def chinese_rows():
    rows = []
    for short, hf in MODEL_HF.items():
        for seed in (42, 43, 44):
            cell = ROOT / "runs" / "chinese" / "full" / short / str(seed)
            result_p = cell / "result.json"
            off_p = cell / "gold150_official.json"
            pred_p = cell / "gold150_predictions.jsonl"
            r = json.loads(result_p.read_text()) if result_p.exists() else None
            off = json.loads(off_p.read_text()) if off_p.exists() else None
            status = "completed" if off and off.get("typed_exact") else ("running" if r else "not_started")
            te = (off or {}).get("typed_exact") or {}
            tr = (off or {}).get("typed_relaxed") or {}
            ce = (off or {}).get("collapsed_exact") or {}
            per = (off or {}).get("per_type_exact") or {}
            macro = None
            if per:
                fs = []
                for k in ("L", "K", "S", "T"):
                    fs.append((per.get(k) or {}).get("f1") or 0.0)
                macro = sum(fs) / 4.0
            base = {
                "track": "chinese",
                "dataset": "cnss_lskt",
                "subset": "gold150_human_reference",
                "task": "lskt_span",
                "model": hf,
                "protocol_id": "chinese_lskt_linear_b2_20260921",
                "seed": seed,
                "status": status,
                "scale": "0-1",
                "eval_split": "gold150",
                "eval_n": (off or {}).get("gold_n_rows"),
                "eval_unit": "record",
                "selection_split": "dev_b2",
                "checkpoint_epoch": (r or {}).get("best_epoch"),
                "dataset_revision": "frozen_b2_gold150_sha_in_receipt",
                "model_revision": PINS[hf],
                "code_revision": "run_chinese_encoder.py",
                "scorer_revision": (off or {}).get("scorer_version"),
                "config_file": rel(cell / "config.json") if (cell / "config.json").exists() else None,
                "predictions_file": rel(pred_p) if pred_p.exists() else None,
                "metrics_file": rel(off_p) if off_p.exists() else None,
                "config_sha256": sha256(cell / "config.json"),
                "predictions_sha256": sha256(pred_p),
                "metrics_sha256": sha256(off_p),
                "notes": "Gold150 diagnostic human reference, not a fresh blind test. n=3 required for main table. Do not mix with JobBERT-zh CRF.",
            }
            for metric, value in [
                ("typed_exact_micro_f1", te.get("f1")),
                ("typed_relaxed_micro_f1", tr.get("f1")),
                ("collapsed_exact_boundary_f1", ce.get("f1")),
                ("macro_f1_LKST", macro),
            ]:
                rec = dict(base)
                rec["metric"] = metric
                rec["value"] = value if status == "completed" else None
                rows.append(rec)
    return rows


def native_rows():
    rows = []
    ss = ROOT / "runs" / "native" / "skillspan"
    if ss.exists():
        for result_p in sorted(ss.glob("*/*/*/result.json")):
            r = json.loads(result_p.read_text())
            rec = {
                "track": "native",
                "dataset": "skillspan",
                "subset": r.get("subset", "public_house_tech"),
                "task": r.get("task"),
                "model": r.get("model"),
                "protocol_id": r.get("protocol_id"),
                "seed": r.get("seed"),
                "status": r.get("status"),
                "metric": "span_f1_pooled_house_tech",
                "scale": "0-1",
                "value": (r.get("test") or {}).get("f1"),
                "eval_split": "test",
                "eval_n": (r.get("test") or {}).get("n_sents"),
                "eval_unit": "sentence",
                "selection_split": "dev",
                "checkpoint_epoch": r.get("best_epoch"),
                "metrics_file": rel(result_p),
                "metrics_sha256": sha256(result_p),
                "notes": r.get("notes"),
            }
            rows.append(rec)
    g = ROOT / "runs" / "native" / "gnehm_ict"
    if g.exists():
        for result_p in sorted(g.glob("*/*/result.json")):
            r = json.loads(result_p.read_text())
            rec = {
                "track": "native",
                "dataset": "gnehm",
                "subset": "public_ict",
                "task": "ict_span",
                "model": r.get("model"),
                "protocol_id": r.get("protocol_id"),
                "seed": r.get("seed"),
                "status": r.get("status"),
                "metric": "span_f1",
                "scale": "0-1",
                "value": (r.get("test") or {}).get("f1"),
                "eval_split": "test",
                "eval_n": (r.get("test") or {}).get("n_sents"),
                "eval_unit": "sentence",
                "selection_split": "dev",
                "checkpoint_epoch": r.get("best_epoch"),
                "metrics_file": rel(result_p),
                "metrics_sha256": sha256(result_p),
                "notes": r.get("notes"),
            }
            rows.append(rec)
    return rows


def mean_sd(vals):
    if len(vals) < 2:
        return (None, None, len(vals))
    return (statistics.mean(vals), statistics.stdev(vals), len(vals))


def bootstrap_comparisons(n_boot=2000, seed=20260921):
    import random

    rng = random.Random(seed)
    out = []
    datasets = ["skillspan", "kompetencer", "gnehm", "green", "sayfullina", "fijo"]
    for ds in datasets:
        heads = ["tags_skill", "tags_knowledge"] if ds in ("skillspan", "kompetencer") else ["tags_skill"]
        gold_rows = read(ROOT / "data" / ds / "test.json")
        for head in heads:
            gold = [entities(r[head]) for r in gold_rows]
            n = len(gold)
            per_seed = {}
            for s in (42, 43, 44):
                preds = {}
                for short in MODEL_HF:
                    p = ROOT / "runs" / "full" / ds / head / short / str(s) / "test_predictions.jsonl"
                    tags = [entities(json.loads(line)["predicted_tags"]) for line in p.read_text().splitlines() if line.strip()]
                    if len(tags) != n:
                        raise SystemExit(f"pred/gold length mismatch {ds} {head} {short} {s}: {len(tags)} vs {n}")
                    preds[short] = tags
                per_seed[s] = preds

            def f1_idx(pred_sents, idx):
                tp = gold_n = pred_n = 0
                for i in idx:
                    g, p = gold[i], pred_sents[i]
                    tp += len(g & p)
                    gold_n += len(g)
                    pred_n += len(p)
                return (2 * tp / (gold_n + pred_n)) if (gold_n + pred_n) else 0.0

            deltas = []
            for _ in range(n_boot):
                idx = [rng.randrange(n) for _ in range(n)]
                d = []
                for s in (42, 43, 44):
                    fe = f1_idx(per_seed[s]["esco-xlm-roberta-large"], idx)
                    fx = f1_idx(per_seed[s]["xlm-roberta-large"], idx)
                    d.append(fe - fx)
                deltas.append(sum(d) / 3.0)
            deltas.sort()
            lo = deltas[int(0.025 * n_boot)]
            hi = deltas[int(0.975 * n_boot)]
            observed = []
            for s in (42, 43, 44):
                fe = score(gold, per_seed[s]["esco-xlm-roberta-large"])["f1"]
                fx = score(gold, per_seed[s]["xlm-roberta-large"])["f1"]
                observed.append(fe - fx)
            out.append(
                {
                    "track": "common",
                    "dataset": ds,
                    "task": head,
                    "pair": "esco-xlm-roberta-large minus xlm-roberta-large",
                    "metric": "typed_exact_micro_f1",
                    "seeds": [42, 43, 44],
                    "observed_per_seed": observed,
                    "observed_mean": sum(observed) / 3.0,
                    "bootstrap_n": n_boot,
                    "bootstrap_seed": seed,
                    "resample_unit": "sentence",
                    "ci_2.5": lo,
                    "ci_97.5": hi,
                    "notes": "Sentence-level paired bootstrap of the three-seed mean difference. Not a substitute for seed SD. No multiple-comparison claim from CI excluding 0.",
                }
            )
    return out


def main():
    receipts = ROOT / "receipts"
    receipts.mkdir(exist_ok=True)
    rows = common_rows() + chinese_rows() + native_rows()
    write_jsonl(ROOT / "results.jsonl", rows)
    write_jsonl(receipts / "results.jsonl", rows)
    fields = sorted({k for r in rows for k in r})
    with (ROOT / "raw_metrics.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    (receipts / "raw_metrics.csv").write_text((ROOT / "raw_metrics.csv").read_text())

    summary = []
    for ds in ["skillspan", "kompetencer", "gnehm", "green", "sayfullina", "fijo"]:
        heads = ["tags_skill", "tags_knowledge"] if ds in ("skillspan", "kompetencer") else ["tags_skill"]
        for head in heads:
            for short, hf in MODEL_HF.items():
                vals = [r["value"] for r in rows if r["track"] == "common" and r["dataset"] == ds and r["task"] == head and r["model"] == hf and r["metric"] == "typed_exact_micro_f1" and r["status"] == "completed" and r["value"] is not None]
                m, sd, n = mean_sd(vals)
                summary.append({"dataset": ds, "task": head, "model": hf, "n": n, "mean": m, "sd": sd, "seeds": vals})
    (receipts / "common_mean_sd.json").write_text(json.dumps(summary, indent=2))

    print("running sentence-level paired bootstrap (2000, seed=20260921)", flush=True)
    comps = bootstrap_comparisons()
    write_jsonl(ROOT / "comparisons.jsonl", comps)
    write_jsonl(receipts / "comparisons.jsonl", comps)
    print(json.dumps({"n_result_rows": len(rows), "n_comparisons": len(comps), "common_completed": sum(1 for r in rows if r["track"] == "common" and r["status"] == "completed")}, indent=2))


if __name__ == "__main__":
    main()
