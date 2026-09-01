#!/usr/bin/env python3
"""Diagnostic: typed F1 by gold/pred surface character length (short <=5 vs long >5).

Does not train. Does not overwrite Gold. Scorer match_exact/match_relaxed from cnss-lskt-1.2.0.
Write reports/span_length_char5/ only. Numbers are 待验证 until copied into confirmed-results.
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
sys.path.insert(0, str(PAPER / "scorer"))
from score_lskt import (  # noqa: E402
    GOLD_FIELDS,
    PRED_FIELDS,
    extract_spans,
    index_by_id,
    load_records,
    match_exact,
    match_relaxed,
    prf,
    rec_id,
)

OUT = PAPER / "reports/span_length_char5"
SHORT_MAX = 5
TYPES = ("L", "K", "S", "T")


def span_chars(rec: dict, start: int, end: int) -> int:
    toks = rec.get("tokens") or []
    if toks and 0 <= start <= end <= len(toks):
        return len("".join(str(t) for t in toks[start:end]))
    sent = str(rec.get("sentence") or "")
    if sent and 0 <= start <= end <= len(sent):
        return len(sent[start:end])
    return max(0, int(end) - int(start))


def band(n: int) -> str:
    if n <= 0:
        return "empty"
    return "short<=5" if n <= SHORT_MAX else "long>5"


def hist_rows(name: str, rows: list[dict], fields) -> list[dict]:
    char_c = Counter()
    tok_c = Counter()
    type_band = Counter()
    n_span = 0
    for rec in rows:
        for a, b, t in extract_spans(rec, fields):
            n_span += 1
            cl = span_chars(rec, a, b)
            tl = b - a
            char_c[cl] += 1
            tok_c[tl] += 1
            type_band[(t, band(cl))] += 1
    out = []
    for cl in range(1, 21):
        out.append(
            {
                "split": name,
                "kind": "char_len",
                "key": str(cl),
                "n": char_c.get(cl, 0),
                "frac": round(char_c.get(cl, 0) / max(n_span, 1), 4),
            }
        )
    out.append(
        {
            "split": name,
            "kind": "char_len",
            "key": "21+",
            "n": sum(v for k, v in char_c.items() if k >= 21),
            "frac": round(sum(v for k, v in char_c.items() if k >= 21) / max(n_span, 1), 4),
        }
    )
    for lab in ("short<=5", "long>5"):
        n = sum(v for k, v in char_c.items() if band(k) == lab)
        out.append(
            {
                "split": name,
                "kind": "char_band",
                "key": lab,
                "n": n,
                "frac": round(n / max(n_span, 1), 4),
            }
        )
    for t in TYPES:
        for lab in ("short<=5", "long>5"):
            n = type_band.get((t, lab), 0)
            out.append(
                {
                    "split": name,
                    "kind": f"type_{t}",
                    "key": lab,
                    "n": n,
                    "frac": round(n / max(n_span, 1), 4),
                }
            )
    out.append({"split": name, "kind": "total_spans", "key": "all", "n": n_span, "frac": 1.0})
    mean_c = sum(k * v for k, v in char_c.items()) / max(n_span, 1)
    mean_t = sum(k * v for k, v in tok_c.items()) / max(n_span, 1)
    out.append({"split": name, "kind": "mean_char", "key": "all", "n": round(mean_c, 4), "frac": ""})
    out.append({"split": name, "kind": "mean_tok", "key": "all", "n": round(mean_t, 4), "frac": ""})
    return out


def score_bands(gold_rows, pred_by, typed: bool) -> list[dict]:
    bands = ("all", "short<=5", "long>5")
    acc = {b: {"tp": 0, "pred": 0, "gold": 0, "tp_rel": 0} for b in bands}
    type_acc = {
        (t, b): {"tp": 0, "pred": 0, "gold": 0} for t in TYPES for b in ("short<=5", "long>5")
    }
    for g in gold_rows:
        iid = rec_id(g)
        gs = extract_spans(g, GOLD_FIELDS)
        p = pred_by.get(iid)
        ps = extract_spans(p, PRED_FIELDS) if p is not None else []
        g_ann = [(a, b, t, span_chars(g, a, b)) for a, b, t in gs]
        p_ann = [(a, b, t, span_chars(p if p is not None else g, a, b)) for a, b, t in ps]

        def keep(ann, lab):
            if lab == "all":
                return [(a, b, t) for a, b, t, _ in ann]
            return [(a, b, t) for a, b, t, cl in ann if band(cl) == lab]

        for lab in bands:
            g_s = keep(g_ann, lab)
            p_s = keep(p_ann, lab)
            if typed:
                m = match_exact(g_s, p_s)
                r = match_relaxed(g_s, p_s, 0.5)
            else:
                g_c = [(a, b, "X") for a, b, _ in g_s]
                p_c = [(a, b, "X") for a, b, _ in p_s]
                m = match_exact(g_c, p_c)
                r = match_relaxed(g_c, p_c, 0.5)
            acc[lab]["tp"] += m["tp"]
            acc[lab]["pred"] += m["pred"]
            acc[lab]["gold"] += m["gold"]
            acc[lab]["tp_rel"] += r["tp"]
        for t in TYPES:
            for lab in ("short<=5", "long>5"):
                g_s = [(a, b, tt) for a, b, tt, cl in g_ann if tt == t and band(cl) == lab]
                p_s = [(a, b, tt) for a, b, tt, cl in p_ann if tt == t and band(cl) == lab]
                m = match_exact(g_s, p_s)
                type_acc[(t, lab)]["tp"] += m["tp"]
                type_acc[(t, lab)]["pred"] += m["pred"]
                type_acc[(t, lab)]["gold"] += m["gold"]
    rows = []
    for lab in bands:
        s = acc[lab]
        exact = prf(s["tp"], s["pred"], s["gold"])
        rel = prf(s["tp_rel"], s["pred"], s["gold"])
        rows.append(
            {
                "band": lab,
                "type": "micro",
                "exact_p": round(exact["precision"], 4),
                "exact_r": round(exact["recall"], 4),
                "exact_f1": round(exact["f1"], 4),
                "relaxed_f1": round(rel["f1"], 4),
                "tp": s["tp"],
                "pred": s["pred"],
                "gold": s["gold"],
            }
        )
    for t in TYPES:
        for lab in ("short<=5", "long>5"):
            s = type_acc[(t, lab)]
            exact = prf(s["tp"], s["pred"], s["gold"])
            rows.append(
                {
                    "band": lab,
                    "type": t,
                    "exact_p": round(exact["precision"], 4),
                    "exact_r": round(exact["recall"], 4),
                    "exact_f1": round(exact["f1"], 4),
                    "relaxed_f1": "",
                    "tp": s["tp"],
                    "pred": s["pred"],
                    "gold": s["gold"],
                }
            )
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    gold_v2 = load_records(str(PAPER / "data/gold_canonical_v2.jsonl"))
    gold_v4 = load_records(str(PAPER / "data/test_lskt_v4_cws_simhuman980_hybrid.jsonl"))
    train_v4 = load_records(str(PAPER / "data/train_lskt_v4_silver.jsonl"))
    goldstyle = PAPER / "data/train_goldstyle_v3.jsonl"
    train_gs = load_records(str(goldstyle)) if goldstyle.exists() else []

    dist = []
    dist += hist_rows("gold_v2_test", gold_v2, GOLD_FIELDS)
    dist += hist_rows("v4_hybrid_test", gold_v4, GOLD_FIELDS)
    dist += hist_rows("train_v4_silver", train_v4, GOLD_FIELDS)
    if train_gs:
        dist += hist_rows("train_goldstyle_v3", train_gs, GOLD_FIELDS)
    write_csv(OUT / "span_char_hist.csv", dist)

    jobs = [
        (
            "gold_v2",
            gold_v2,
            "ChatGPT_gpt-4o",
            PAPER / "reports/views/ChatGPT_unique_first_v2.jsonl",
        ),
        (
            "gold_v2",
            gold_v2,
            "JobBERT_1M_goldstyle_s42",
            PAPER / "output/jobbert_zh_1m/crf_v3_seed42/test_pred.jsonl",
        ),
        (
            "gold_v2",
            gold_v2,
            "RoBERTa_wwm_v3_s42",
            PAPER / "output/cn_roberta_wwm_crf/smoke_goldstyle_v3_seed42/test_pred.jsonl",
        ),
        (
            "v4_hybrid",
            gold_v4,
            "JobBERT_3M_v4_cws",
            PAPER
            / "reports/sandbox_lskt_v4_silver/hybrid_cws_eval/preds_cws/JobBERT_3M_v4.jsonl",
        ),
        (
            "v4_hybrid",
            gold_v4,
            "JobBERT_1M_v4_cws",
            PAPER
            / "reports/sandbox_lskt_v4_silver/hybrid_cws_eval/preds_cws/JobBERT_1M_v4.jsonl",
        ),
        (
            "v4_hybrid",
            gold_v4,
            "ChatGPT_gpt-4o_cws",
            PAPER / "reports/sandbox_lskt_v4_silver/hybrid_cws_eval/preds_cws/ChatGPT.jsonl",
        ),
    ]
    score_rows = []
    for protocol, gold_rows, name, pred_path in jobs:
        if not pred_path.exists():
            print("MISSING", pred_path)
            continue
        pred_by, _ = index_by_id(load_records(str(pred_path)), "first")
        for row in score_bands(gold_rows, pred_by, typed=True):
            score_rows.append({"protocol": protocol, "system": name, **row})
        print(protocol, name, "done")
    write_csv(OUT / "f1_short_long.csv", score_rows)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
