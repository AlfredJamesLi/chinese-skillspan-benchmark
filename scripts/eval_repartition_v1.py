#!/usr/bin/env python3
"""Score one repartition_v1 CRF run. Appends CSVs. Does not overwrite old benchmarks."""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
sys.path.insert(0, str(PAPER / "scorer"))
from score_lskt import rec_id, score  # noqa: E402

SOURCE_MAP = {
    "人工智能招聘": "AI",
    "应届生招聘": "Grad",
    "阿里云公开数据集": "Cloud",
    "事业单位招聘": "Public",
}
REP = PAPER / "reports/repartition_v1"
GOLD = PAPER / "data/repartition_v1/test.jsonl"


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_jsonl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def append_csv(path: Path, row: dict, fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    new = not path.exists()
    with path.open("a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        if new:
            w.writeheader()
        w.writerow({k: row.get(k, "") for k in fields})


def pack(report: dict) -> dict:
    te, tr = report["typed_exact"], report["typed_relaxed"]
    pt = report.get("per_type_exact") or {}
    out = {
        "typed_exact_p": te["precision"],
        "typed_exact_r": te["recall"],
        "typed_exact_f1": te["f1"],
        "typed_relaxed_p": tr["precision"],
        "typed_relaxed_r": tr["recall"],
        "typed_relaxed_f1": tr["f1"],
        "gold_spans": te.get("gold"),
        "pred_spans": te.get("pred"),
        "alignment_ok": int(bool(report.get("alignment_ok"))),
    }
    for k in "LKST":
        v = pt.get(k) or {}
        out[f"{k}_f1"] = v.get("f1", 0.0)
        out[f"{k}_gold"] = v.get("gold", 0)
        out[f"{k}_pred"] = v.get("pred", 0)
    return out


def empty_fp_rate(gold_rows: list[dict], pred_rows: list[dict]) -> float:
    gmap = {rec_id(r): r for r in gold_rows}
    n_empty, fp = 0, 0
    for pr in pred_rows:
        g = gmap.get(rec_id(pr))
        if not g:
            continue
        gtags = g.get("list_of_selection_bio4") or []
        empty = not any(str(t).startswith("B-") for t in gtags)
        if not empty:
            continue
        n_empty += 1
        pt = pr.get("pred_tags") or pr.get("list_of_selection_bio4") or []
        if any(str(t).startswith("B-") for t in pt):
            fp += 1
    return fp / n_empty if n_empty else 0.0


def main() -> None:
    pred = Path(sys.argv[1])
    model = sys.argv[2]
    seed = sys.argv[3]
    ckpt = sys.argv[4] if len(sys.argv) > 4 else ""
    gold_rows = load_jsonl(GOLD)
    pred_rows = load_jsonl(pred)
    gmap = {rec_id(r): r for r in gold_rows}
    tmp = Path("/tmp") / f"rep_v1_{model}_{seed}.jsonl"
    ordered = []
    for g in gold_rows:
        gid = rec_id(g)
        pr = next((p for p in pred_rows if rec_id(p) == gid), None)
        if pr is None:
            toks = g.get("tokens") or []
            ordered.append({"id": gid, "tokens": toks, "pred_tags": ["O"] * len(toks), "list_of_selection_bio4": ["O"] * len(toks)})
        else:
            ordered.append(pr)
    tmp.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in ordered) + "\n", encoding="utf-8")
    rep = score(str(GOLD), str(tmp), align_mode="official", n_boot=0)
    base = pack(rep)
    base.update({
        "model": model,
        "seed": seed,
        "checkpoint": ckpt,
        "pred_path": str(pred),
        "test_manifest_sha256": sha256_file(PAPER / "manifests/repartition_v1/test_manifest.jsonl"),
        "test_jsonl_sha256": sha256_file(GOLD),
        "scorer_version": "cnss-lskt-1.2.0",
        "id_coverage": sum(1 for p in pred_rows if rec_id(p) in gmap) / len(gold_rows),
        "empty_sentence_fp_rate": empty_fp_rate(gold_rows, pred_rows),
        "n_test": len(gold_rows),
    })
    src_f1 = {}
    pmap = {rec_id(p): p for p in pred_rows}
    by_src = defaultdict(list)
    for g in gold_rows:
        by_src[SOURCE_MAP.get(str(g.get("source_domain") or ""), "UNK")].append(g)
    src_vals = []
    for src, grows in sorted(by_src.items()):
        gp = Path("/tmp") / f"rep_v1_g_{src}.jsonl"
        pp = Path("/tmp") / f"rep_v1_p_{src}.jsonl"
        gp.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in grows) + "\n", encoding="utf-8")
        prows = []
        for x in grows:
            pr = pmap.get(rec_id(x))
            if pr is None:
                toks = x.get("tokens") or []
                pr = {"id": rec_id(x), "tokens": toks, "pred_tags": ["O"] * len(toks)}
            prows.append(pr)
        pp.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in prows) + "\n", encoding="utf-8")
        sr = pack(score(str(gp), str(pp), align_mode="official", n_boot=0))
        src_f1[src] = sr["typed_exact_f1"]
        src_vals.append(sr["typed_exact_f1"])
        append_csv(
            REP / "per_source_results.csv",
            {"model": model, "seed": seed, "source": src, "n": len(grows), **sr,
             "test_jsonl_sha256": base["test_jsonl_sha256"], "scorer_version": "cnss-lskt-1.2.0"},
            ["model", "seed", "source", "n", "typed_exact_f1", "typed_relaxed_f1", "typed_exact_p", "typed_exact_r",
             "test_jsonl_sha256", "scorer_version"],
        )
    base["source_macro_f1"] = sum(src_vals) / len(src_vals) if src_vals else 0.0
    for src, v in src_f1.items():
        base[f"exact_{src}"] = v
    fields = [
        "model", "seed", "typed_exact_p", "typed_exact_r", "typed_exact_f1",
        "typed_relaxed_p", "typed_relaxed_r", "typed_relaxed_f1", "source_macro_f1",
        "exact_AI", "exact_Grad", "exact_Cloud", "exact_Public",
        "L_f1", "K_f1", "S_f1", "T_f1", "gold_spans", "pred_spans",
        "empty_sentence_fp_rate", "id_coverage", "alignment_ok", "n_test",
        "test_manifest_sha256", "test_jsonl_sha256", "scorer_version", "checkpoint", "pred_path",
    ]
    append_csv(REP / "main_results_by_seed.csv", base, fields)
    append_csv(
        REP / "per_label_results.csv",
        {"model": model, "seed": seed, **{f"{k}_f1": base[f"{k}_f1"] for k in "LKST"},
         "test_jsonl_sha256": base["test_jsonl_sha256"], "scorer_version": "cnss-lskt-1.2.0"},
        ["model", "seed", "L_f1", "K_f1", "S_f1", "T_f1", "test_jsonl_sha256", "scorer_version"],
    )
    print(json.dumps({k: base[k] for k in ("model", "seed", "typed_exact_f1", "typed_relaxed_f1", "source_macro_f1", "id_coverage")}, indent=2))


if __name__ == "__main__":
    main()
