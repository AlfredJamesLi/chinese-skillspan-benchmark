#!/usr/bin/env python3
"""SkillSpan-style appendix tables from existing Gold v2 predictions.

No new training. Scorer cnss-lskt-1.2.0. Writes CSVs under tables/ and
paper_results/repo/. Round-to-4-decimal printout is for confirmed-results.md.
"""
from __future__ import annotations

import csv
import json
import math
import shutil
import statistics
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path("/home/guojingli3/SCESC-LLM-skill-extraction")
PAPER = ROOT / "Chinese_skill_benchmark_Paper"
sys.path.insert(0, str(PAPER / "scorer"))
from score_lskt import (  # noqa: E402
    GOLD_FIELDS,
    PRED_FIELDS,
    collapse,
    extract_spans,
    index_by_id,
    load_records,
    match_exact,
    match_relaxed,
    prf,
    rec_id,
)

GOLD = PAPER / "data/gold_canonical_v2.jsonl"
TEST = ROOT / "data/annotated/processed/chinese_skillspan/test.json"
TABLES = PAPER / "tables"
OUT = PAPER / "paper_results/repo"
BUNDLE_TABLES = PAPER / "overleaf_cursor_bundle/tables"
SEEDS = (42, 123, 2026)

ENCODERS = {
    "JobBERT 1M goldstyle v3": {
        42: PAPER / "output/jobbert_zh_1m/crf_v3_seed42",
        123: PAPER / "output/encoder_3seed/jobbert_zh_1m/seed_123",
        2026: PAPER / "output/encoder_3seed/jobbert_zh_1m/seed_2026",
    },
    "domain-mix 1M": {
        42: PAPER / "output/jobbert_zh_domain_1m/crf_v3_seed42",
        123: PAPER / "output/jobbert_zh_domain_1m/crf_v3_seed123",
        2026: PAPER / "output/jobbert_zh_domain_1m/crf_v3_seed2026",
    },
    "JobBERT 3M ckpt65000": {
        42: PAPER / "output/jobbert_zh_3m/crf_ckpt65000_ep1",
        123: PAPER / "output/encoder_3seed/jobbert_zh_3m_ckpt65000/seed_123",
        2026: PAPER / "output/encoder_3seed/jobbert_zh_3m_ckpt65000/seed_2026",
    },
    "RoBERTa-wwm v3": {
        42: PAPER / "output/cn_roberta_wwm_crf/smoke_goldstyle_v3_seed42",
        123: PAPER / "output/encoder_3seed/cn_roberta_wwm_v3/seed_123",
        2026: PAPER / "output/encoder_3seed/cn_roberta_wwm_v3/seed_2026",
    },
}

LLM_PREDS = {
    "ChatGPT (gpt-4o)": PAPER / "reports/views/ChatGPT_unique_first_v2.jsonl",
    "Claude filled (haiku+98 sonnet-4-6)": PAPER / "reports/views/Claude_filled_v2.jsonl",
    "Kimi (kimi-k2-0711-preview, 293 missing)": PAPER / "reports/views/Kimi_unique_first_v2.jsonl",
    "DeepSeek (deepseek-r1)": PAPER / "reports/views/DeepSeek_unique_first_v2.jsonl",
    "Qwen (Qwen2.5-14B-Instruct)": PAPER / "reports/views/Qwen_unique_first_v2.jsonl",
}

SPAN_SYSTEMS = {
    "ChatGPT (gpt-4o)": PAPER / "reports/views/ChatGPT_unique_first_v2.jsonl",
    "JobBERT 1M seed42": PAPER / "output/jobbert_zh_1m/crf_v3_seed42/test_pred.jsonl",
    "JobBERT 1M seed123": PAPER / "output/encoder_3seed/jobbert_zh_1m/seed_123/test_pred.jsonl",
    "RoBERTa-wwm v3 seed42": PAPER
    / "output/cn_roberta_wwm_crf/smoke_goldstyle_v3_seed42/test_pred.jsonl",
}

DOMAIN_ORDER = ("人工智能招聘", "阿里云公开数据集", "事业单位招聘")
BUCKETS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def r4(x: float | None) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return ""
    return f"{x:.4f}"


def mean_std(xs: list[float]) -> tuple[float, float]:
    if not xs:
        return float("nan"), float("nan")
    if len(xs) == 1:
        return xs[0], 0.0
    return statistics.mean(xs), statistics.stdev(xs)


def load_summary(run_dir: Path) -> dict:
    p = run_dir / "run_summary.json"
    if not p.is_file():
        raise FileNotFoundError(p)
    return json.loads(p.read_text())


def pred_path(run_dir: Path, summary: dict) -> Path:
    listed = summary.get("pred_path")
    if listed:
        q = Path(listed)
        if q.is_file():
            return q
    q = run_dir / "test_pred.jsonl"
    if q.is_file():
        return q
    raise FileNotFoundError(f"no pred in {run_dir}")


def score_subset(gold_rows: list[dict], pred_by: dict[str, dict], ids: list[str]) -> dict:
    te_tp = te_p = te_g = 0
    re_tp = re_p = re_g = 0
    n_missing = 0
    g_by = {rec_id(r): r for r in gold_rows}
    for iid in ids:
        g = g_by[iid]
        p = pred_by.get(iid)
        gs = extract_spans(g, GOLD_FIELDS)
        if p is None:
            n_missing += 1
            ps = []
        else:
            ps = extract_spans(p, PRED_FIELDS)
        te = match_exact(gs, ps)
        re = match_relaxed(gs, ps, 0.5)
        te_tp += te["tp"]
        te_p += te["pred"]
        te_g += te["gold"]
        re_tp += re["tp"]
        re_p += re["pred"]
        re_g += re["gold"]
    return {
        "n": len(ids),
        "n_missing": n_missing,
        "typed_exact": prf(te_tp, te_p, te_g),
        "typed_relaxed": prf(re_tp, re_p, re_g),
    }


def load_test_domains() -> dict[str, str]:
    raw = TEST.read_text(encoding="utf-8")
    rows = json.loads(raw) if raw.lstrip().startswith("[") else [
        json.loads(l) for l in raw.splitlines() if l.strip()
    ]
    return {str(r["id"]): str(r.get("source_domain") or "UNKNOWN") for r in rows}


def bucket_of(length: int) -> str:
    if length >= 10:
        return "10+"
    return str(length)


def span_len_f1(gold_rows: list[dict], pred_by: dict[str, dict]) -> list[dict]:
    """Exact typed F1 using gold and pred spans whose token length falls in the bucket."""
    acc: dict[str, dict[str, int]] = {
        bucket_of(k): {"tp": 0, "pred": 0, "gold": 0} for k in BUCKETS
    }
    for g in gold_rows:
        iid = rec_id(g)
        gs = extract_spans(g, GOLD_FIELDS)
        p = pred_by.get(iid)
        ps = extract_spans(p, PRED_FIELDS) if p is not None else []
        g_by_b: dict[str, list] = defaultdict(list)
        p_by_b: dict[str, list] = defaultdict(list)
        for s in gs:
            g_by_b[bucket_of(s[1] - s[0])].append(s)
        for s in ps:
            p_by_b[bucket_of(s[1] - s[0])].append(s)
        for b in acc:
            m = match_exact(g_by_b[b], p_by_b[b])
            acc[b]["tp"] += m["tp"]
            acc[b]["pred"] += m["pred"]
            acc[b]["gold"] += m["gold"]
    rows = []
    for b in [str(k) for k in range(1, 10)] + ["10+"]:
        s = acc[b]
        rows.append({"bucket": b, **prf(s["tp"], s["pred"], s["gold"]), **s})
    return rows


def mean_span_stats(gold_rows: list[dict], pred_by: dict[str, dict], fb: dict[str, str]) -> list[dict]:
    def lengths(spans):
        return [s[1] - s[0] for s in spans]

    rows = []
    by_dom: dict[str, list[dict]] = defaultdict(list)
    for g in gold_rows:
        d = g.get("source_domain") or fb.get(rec_id(g), "UNKNOWN")
        by_dom[str(d)].append(g)
    for domain, recs in [("ALL", gold_rows)] + [(d, by_dom[d]) for d in DOMAIN_ORDER]:
        gl: list[int] = []
        pl: list[int] = []
        n_g = n_p = 0
        for g in recs:
            gs = extract_spans(g, GOLD_FIELDS)
            p = pred_by.get(rec_id(g))
            ps = extract_spans(p, PRED_FIELDS) if p is not None else []
            gl.extend(lengths(gs))
            pl.extend(lengths(ps))
            n_g += len(gs)
            n_p += len(ps)
        rows.append(
            {
                "domain": domain,
                "n_gold_spans": n_g,
                "n_pred_spans": n_p,
                "mean_gold_len": statistics.mean(gl) if gl else 0.0,
                "mean_pred_len": statistics.mean(pl) if pl else 0.0,
            }
        )
    return rows


def pairwise_winrate(a: list[float], b: list[float]) -> float:
    """P(a_i > b_j) + 0.5 P(equal) over seed pairs. n=3 is under-powered."""
    hits = 0.0
    n = 0
    for x in a:
        for y in b:
            n += 1
            if x > y:
                hits += 1.0
            elif x == y:
                hits += 0.5
    return hits / n if n else float("nan")


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def copy_to_bundle(src: Path) -> None:
    BUNDLE_TABLES.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, BUNDLE_TABLES / src.name)


def main() -> int:
    TABLES.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    gold = load_records(str(GOLD))
    gold_ids = [rec_id(r) for r in gold]
    fb = load_test_domains()
    for r in gold:
        if not r.get("source_domain"):
            r["source_domain"] = fb.get(rec_id(r), "UNKNOWN")
    by_dom: dict[str, list[str]] = defaultdict(list)
    for r in gold:
        by_dom[str(r.get("source_domain") or fb.get(rec_id(r), "UNKNOWN"))].append(rec_id(r))

    encoder_seed_rows = []
    encoder_f1s: dict[str, list[float]] = {}
    encoder_ps: dict[str, list[float]] = {}
    encoder_rs: dict[str, list[float]] = {}
    encoder_pred_by: dict[str, dict[int, dict[str, dict]]] = {}

    for name, seeds in ENCODERS.items():
        encoder_f1s[name] = []
        encoder_ps[name] = []
        encoder_rs[name] = []
        encoder_pred_by[name] = {}
        for seed in SEEDS:
            run_dir = seeds[seed]
            summary = load_summary(run_dir)
            te = summary["typed_exact"]
            encoder_f1s[name].append(te["f1"])
            encoder_ps[name].append(te["precision"])
            encoder_rs[name].append(te["recall"])
            pp = pred_path(run_dir, summary)
            preds = load_records(str(pp))
            p_by, _ = index_by_id(preds, "first")
            encoder_pred_by[name][seed] = p_by
            encoder_seed_rows.append(
                {
                    "system": name,
                    "seed": seed,
                    "precision": te["precision"],
                    "recall": te["recall"],
                    "f1": te["f1"],
                    "pred_path": str(pp),
                    "scorer": summary.get("scorer_version", "cnss-lskt-1.2.0"),
                }
            )

    pr_rows = []
    for name in ENCODERS:
        mp, sp = mean_std(encoder_ps[name])
        mr, sr = mean_std(encoder_rs[name])
        mf, sf = mean_std(encoder_f1s[name])
        pr_rows.append(
            {
                "system": name,
                "kind": "encoder_3seed",
                "n_seeds": 3,
                "p_seed42": encoder_ps[name][0],
                "p_seed123": encoder_ps[name][1],
                "p_seed2026": encoder_ps[name][2],
                "p_mean": mp,
                "p_std": sp,
                "r_seed42": encoder_rs[name][0],
                "r_seed123": encoder_rs[name][1],
                "r_seed2026": encoder_rs[name][2],
                "r_mean": mr,
                "r_std": sr,
                "f1_seed42": encoder_f1s[name][0],
                "f1_seed123": encoder_f1s[name][1],
                "f1_seed2026": encoder_f1s[name][2],
                "f1_mean": mf,
                "f1_std": sf,
                "n_missing": 0,
                "note": "Gold v2 typed exact; sample std; scorer cnss-lskt-1.2.0",
            }
        )

    llm_overall = []
    for name, path in LLM_PREDS.items():
        preds = load_records(str(path))
        p_by, _ = index_by_id(preds, "first")
        overall = score_subset(gold, p_by, gold_ids)
        te = overall["typed_exact"]
        llm_overall.append({"name": name, "path": path, "overall": overall, "p_by": p_by})
        pr_rows.append(
            {
                "system": name,
                "kind": "llm_dump",
                "n_seeds": 1,
                "p_seed42": te["precision"],
                "p_seed123": "",
                "p_seed2026": "",
                "p_mean": te["precision"],
                "p_std": "",
                "r_seed42": te["recall"],
                "r_seed123": "",
                "r_seed2026": "",
                "r_mean": te["recall"],
                "r_std": "",
                "f1_seed42": te["f1"],
                "f1_seed123": "",
                "f1_seed2026": "",
                "f1_mean": te["f1"],
                "f1_std": "",
                "n_missing": overall["n_missing"],
                "note": "single dump; empty-fill missing Gold IDs",
            }
        )

    pr_fields = [
        "system",
        "kind",
        "n_seeds",
        "p_seed42",
        "p_seed123",
        "p_seed2026",
        "p_mean",
        "p_std",
        "r_seed42",
        "r_seed123",
        "r_seed2026",
        "r_mean",
        "r_std",
        "f1_seed42",
        "f1_seed123",
        "f1_seed2026",
        "f1_mean",
        "f1_std",
        "n_missing",
        "note",
    ]
    pr_path = TABLES / "appendix_pr_gold_v2.csv"
    write_csv(pr_path, pr_rows, pr_fields)
    write_csv(TABLES / "appendix_encoder_seed_pr_gold_v2.csv", encoder_seed_rows,
              ["system", "seed", "precision", "recall", "f1", "pred_path", "scorer"])

    domain_rows = []
    for name in ENCODERS:
        for domain in DOMAIN_ORDER:
            f1s, ps, rs = [], [], []
            for seed in SEEDS:
                sc = score_subset(gold, encoder_pred_by[name][seed], by_dom[domain])
                te = sc["typed_exact"]
                f1s.append(te["f1"])
                ps.append(te["precision"])
                rs.append(te["recall"])
                domain_rows.append(
                    {
                        "system": name,
                        "domain": domain,
                        "n": len(by_dom[domain]),
                        "seed": seed,
                        "precision": te["precision"],
                        "recall": te["recall"],
                        "f1": te["f1"],
                        "n_missing": sc["n_missing"],
                    }
                )
            mf, sf = mean_std(f1s)
            mp, sp = mean_std(ps)
            mr, sr = mean_std(rs)
            domain_rows.append(
                {
                    "system": name,
                    "domain": domain,
                    "n": len(by_dom[domain]),
                    "seed": "mean",
                    "precision": mp,
                    "recall": mr,
                    "f1": mf,
                    "n_missing": 0,
                    "f1_std": sf,
                    "p_std": sp,
                    "r_std": sr,
                }
            )
    for item in llm_overall:
        for domain in DOMAIN_ORDER:
            sc = score_subset(gold, item["p_by"], by_dom[domain])
            te = sc["typed_exact"]
            domain_rows.append(
                {
                    "system": item["name"],
                    "domain": domain,
                    "n": len(by_dom[domain]),
                    "seed": "dump",
                    "precision": te["precision"],
                    "recall": te["recall"],
                    "f1": te["f1"],
                    "n_missing": sc["n_missing"],
                }
            )
    domain_path = TABLES / "appendix_domain_seed_gold_v2.csv"
    write_csv(
        domain_path,
        domain_rows,
        ["system", "domain", "n", "seed", "precision", "recall", "f1", "f1_std", "p_std", "r_std", "n_missing"],
    )

    # Wide domain mean±std table for the paper
    wide = []
    for name in list(ENCODERS) + [x["name"] for x in llm_overall]:
        row = {"system": name}
        for domain in DOMAIN_ORDER:
            cells = [r for r in domain_rows if r["system"] == name and r["domain"] == domain]
            mean_cell = next((c for c in cells if str(c["seed"]) == "mean"), None)
            dump_cell = next((c for c in cells if str(c["seed"]) == "dump"), None)
            use = mean_cell or dump_cell
            key = domain
            if use:
                row[f"{key}_f1"] = use["f1"]
                row[f"{key}_f1_std"] = use.get("f1_std", "")
                row[f"{key}_p"] = use["precision"]
                row[f"{key}_r"] = use["recall"]
        wide.append(row)
    wide_path = TABLES / "appendix_domain_mean_gold_v2.csv"
    wide_fields = ["system"]
    for d in DOMAIN_ORDER:
        wide_fields.extend([f"{d}_f1", f"{d}_f1_std", f"{d}_p", f"{d}_r"])
    write_csv(wide_path, wide, wide_fields)

    span_rows = []
    span_mean_rows = []
    for name, path in SPAN_SYSTEMS.items():
        preds = load_records(str(path))
        p_by, _ = index_by_id(preds, "first")
        for row in span_len_f1(gold, p_by):
            span_rows.append({"system": name, **row})
        for row in mean_span_stats(gold, p_by, fb):
            span_mean_rows.append({"system": name, **row})
    span_path = TABLES / "appendix_span_length_f1_gold_v2.csv"
    write_csv(
        span_path,
        span_rows,
        ["system", "bucket", "precision", "recall", "f1", "tp", "fp", "fn", "pred", "gold"],
    )
    span_mean_path = TABLES / "appendix_span_length_mean_gold_v2.csv"
    write_csv(
        span_mean_path,
        span_mean_rows,
        ["system", "domain", "n_gold_spans", "n_pred_spans", "mean_gold_len", "mean_pred_len"],
    )

    names = list(ENCODERS)
    aso_rows = []
    for ra in names:
        for rb in names:
            wr = 1.0 if ra == rb else pairwise_winrate(encoder_f1s[ra], encoder_f1s[rb])
            aso_rows.append(
                {
                    "row": ra,
                    "col": rb,
                    "p_row_gt_col": wr,
                    "row_dominates": "" if ra == rb else str(wr > 0.5).lower(),
                    "n_seeds": 3,
                    "note": "pairwise seed F1 win-rate; n=3 under-powered vs SkillSpan n=5 ASO",
                }
            )
    aso_path = TABLES / "appendix_aso_encoder_3seed_gold_v2.csv"
    write_csv(aso_path, aso_rows, ["row", "col", "p_row_gt_col", "row_dominates", "n_seeds", "note"])

    # P2 P/R already scored in hybrid CSV — copy a rounded paper-facing slice
    hybrid = TABLES / "hybrid_cws_simhuman980_all_models.csv"
    p2_rows = []
    if hybrid.is_file():
        with hybrid.open(encoding="utf-8") as f:
            for row in csv.DictReader(f):
                p2_rows.append(
                    {
                        "model": row["model"],
                        "kind": row.get("kind", ""),
                        "n_filled_empty": row.get("n_filled_empty", ""),
                        "p": row.get("full2601_typed_exact_p", ""),
                        "r": row.get("full2601_typed_exact_r", ""),
                        "f1": row.get("full2601_typed_exact_f1", ""),
                        "relaxed_f1": row.get("full2601_typed_relaxed_f1", ""),
                        "note": "matched SOP+jieba P2; not Gold v2",
                    }
                )
    p2_path = TABLES / "appendix_pr_p2_matched.csv"
    write_csv(p2_path, p2_rows, ["model", "kind", "n_filled_empty", "p", "r", "f1", "relaxed_f1", "note"])

    inventory = [
        {
            "axis": "Train sentences (paper Table 1)",
            "skillspan_2022": "5866 (200 English JPs in train split)",
            "this_work": "17460",
        },
        {
            "axis": "Dev / test sentences",
            "skillspan_2022": "dev 90 JPs + test 101 JPs; 14.5K sentences total",
            "this_work": "dev 2143 / corpus test 3237; Gold v2 unique 2601",
        },
        {
            "axis": "Label schema",
            "skillspan_2022": "SKILL + KNOWLEDGE (nested allowed)",
            "this_work": "flat LSKT (L/K/S/T, 4 types)",
        },
        {
            "axis": "Human test golds",
            "skillspan_2022": "1 majority-vote gold",
            "this_work": "2 protocols: Doccano Gold v2 and matched SOP+jieba P2",
        },
        {
            "axis": "Unlabeled DAPT",
            "skillspan_2022": "3.2M English JP sentences (one JobBERT)",
            "this_work": "Chinese JD MLM 1M and 3M + domain-mix / listed-mix ablations",
        },
        {
            "axis": "Encoder family (not cloned SpanBERT-from-scratch)",
            "skillspan_2022": "BERT, SpanBERT, JobBERT, JobSpanBERT × STL/MTL × 5 seeds",
            "this_work": "RoBERTa-wwm, JobBERT-zh 1M/3M, domain-mix, listed-mix, goldstyle vs SOP, CWS; 3 seeds (5-seed on 1M goldstyle in progress)",
        },
        {
            "axis": "LLM systems scored",
            "skillspan_2022": "none",
            "this_work": "5 frozen dumps + 6 SOP-extract re-calls on P2-2601",
        },
        {
            "axis": "Significance / analysis tables",
            "skillspan_2022": "5-seed ±std, P/R, ASO, span-length F1",
            "this_work": "3-seed ±std, P/R, domain×seed, span-length F1, pairwise seed win-rate (n=3)",
        },
    ]
    inv_path = TABLES / "appendix_workload_vs_skillspan.csv"
    write_csv(inv_path, inventory, ["axis", "skillspan_2022", "this_work"])

    copies = [
        pr_path,
        TABLES / "appendix_encoder_seed_pr_gold_v2.csv",
        domain_path,
        wide_path,
        span_path,
        span_mean_path,
        aso_path,
        p2_path,
        inv_path,
        TABLES / "encoder_3seed_gold_v2.csv",
    ]
    for p in copies:
        if p.is_file():
            shutil.copy2(p, OUT / p.name)
            copy_to_bundle(p)

    # Print rounded paper cells
    print("=== encoder 3-seed Gold v2 typed exact (sample std) ===")
    for name in ENCODERS:
        mf, sf = mean_std(encoder_f1s[name])
        mp, sp = mean_std(encoder_ps[name])
        mr, sr = mean_std(encoder_rs[name])
        f1s = encoder_f1s[name]
        print(
            f"{name}: F1 {r4(f1s[0])} / {r4(f1s[1])} / {r4(f1s[2])}  "
            f"mean {r4(mf)} ± {r4(sf)}  "
            f"P {r4(mp)} ± {r4(sp)}  R {r4(mr)} ± {r4(sr)}"
        )
    print("=== LLM Gold v2 typed exact P/R (empty-fill missing) ===")
    for item in llm_overall:
        te = item["overall"]["typed_exact"]
        print(
            f"{item['name']}: P {r4(te['precision'])}  R {r4(te['recall'])}  "
            f"F1 {r4(te['f1'])}  missing {item['overall']['n_missing']}"
        )
    print("=== domain mean F1 ± std (encoders) ===")
    for name in ENCODERS:
        bits = []
        for domain in DOMAIN_ORDER:
            cell = next(
                r
                for r in domain_rows
                if r["system"] == name and r["domain"] == domain and str(r["seed"]) == "mean"
            )
            bits.append(f"{domain} {r4(cell['f1'])}±{r4(cell['f1_std'])}")
        print(name + ": " + " | ".join(bits))
    print("=== ASO-style pairwise P(row>col) ===")
    for ra in names:
        vals = []
        for rb in names:
            wr = next(r["p_row_gt_col"] for r in aso_rows if r["row"] == ra and r["col"] == rb)
            vals.append(r4(wr) if ra != rb else "—")
        print(ra + " | " + " ".join(vals))
    print("=== span-length F1 (selected) ===")
    for name in SPAN_SYSTEMS:
        sub = [r for r in span_rows if r["system"] == name]
        compact = " ".join(f"{r['bucket']}={r4(r['f1'])}" for r in sub)
        print(name + ": " + compact)
    print("wrote", pr_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
