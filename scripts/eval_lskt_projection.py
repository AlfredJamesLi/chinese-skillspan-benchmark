#!/usr/bin/env python3
"""LSKT multi-granularity projection audit (read-only).

Computes native 4-way, SkillSpan-compatible 2-way (L/K→KNOWLEDGE, S/T→SKILL),
and boundary-only exact-span micro F1 on frozen Gold v2 dumps.

Does not train, modify Gold/dumps/scorer, or write paper tables.
"""
from __future__ import annotations

import csv
import hashlib
import json
import random
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
ROOT = PAPER.parent
sys.path.insert(0, str(PAPER / "scorer"))
from score_lskt import (  # noqa: E402
    GOLD_FIELDS,
    PRED_FIELDS,
    SCORER_VERSION,
    extract_spans,
    git_commit,
    index_by_id,
    load_records,
    match_exact,
    rec_id,
    score as official_score,
    sha256_file,
)

GOLD_PATH = PAPER / "data/gold_canonical_v2.jsonl"
OUT_DIR = PAPER / "output/lskt_projection_audit"
N_BOOT = 2000
BOOT_SEED = 42
EPS = 1e-6
MONO_EPS = 1e-12

MAP_2WAY = {"L": "KNOWLEDGE", "K": "KNOWLEDGE", "S": "SKILL", "T": "SKILL"}
KNOWLEDGE = frozenset({"L", "K"})
SKILL_GROUP = frozenset({"S", "T"})
TYPES4 = ("L", "K", "S", "T")

# Reference 4-way typed F1 from confirmed Gold-v2 unique-first scores (file check only).
REF_4WAY = {
    "GPT-4o": 0.6364783609234652,
    "DeepSeek": 0.13265225933202357,
    "Qwen2.5-14B": 0.07905138339920947,
    "JobBERT-en-skill_head-transfer": 0.0,
    "JobBERT-en-knowledge_head-transfer": 0.0,
}
REF_BOUNDARY = {
    "GPT-4o": 0.6403385049365303,
}


def project_2way(spans: list[tuple[int, int, str]]) -> list[tuple[int, int, str]]:
    out = []
    for a, b, t in spans:
        lab = MAP_2WAY.get(t, t)
        if lab not in {"KNOWLEDGE", "SKILL"}:
            lab = "SKILL" if t.upper() == "SKILL" else lab
        out.append((a, b, lab))
    return out


def project_boundary(spans: list[tuple[int, int, str]]) -> list[tuple[int, int, str]]:
    return [(a, b, "COMPETENCY") for a, b, _ in spans]


def prf_from_counts(tp: int, pred_n: int, gold_n: int) -> dict[str, float]:
    p = tp / pred_n if pred_n else 0.0
    r = tp / gold_n if gold_n else 0.0
    f = 2 * p * r / (p + r) if (p + r) else 0.0
    return {
        "precision": p,
        "recall": r,
        "f1": f,
        "tp": tp,
        "fp": pred_n - tp,
        "fn": gold_n - tp,
        "pred": pred_n,
        "gold": gold_n,
    }


def micro_pairs(pairs) -> dict[str, float]:
    tp = pred_n = gold_n = 0
    for gs, ps in pairs:
        m = match_exact(gs, ps)
        tp += int(m["tp"])
        pred_n += int(m["pred"])
        gold_n += int(m["gold"])
    return prf_from_counts(tp, pred_n, gold_n)


def bootstrap_deltas(
    triples: list[tuple[list, list, list]],
    n_boot: int = N_BOOT,
    seed: int = BOOT_SEED,
) -> dict[str, float]:
    """triples: list of (spans4_gold/pred unused; we pass count triples).

    Each item is (c4, c2, cb) where each c is (tp, pred, gold) for one sentence.
    """
    rng = random.Random(seed)
    n = len(triples)
    if n == 0:
        z = {
            "delta_2_vs_4": 0.0,
            "delta_2_vs_4_ci_low": 0.0,
            "delta_2_vs_4_ci_high": 0.0,
            "delta_boundary_vs_2": 0.0,
            "delta_boundary_vs_2_ci_low": 0.0,
            "delta_boundary_vs_2_ci_high": 0.0,
        }
        return z

    d24, db2 = [], []
    for _ in range(n_boot):
        t4 = p4 = g4 = 0
        t2 = p2 = g2 = 0
        tb = pb = gb = 0
        for _i in range(n):
            c4, c2, cb = triples[rng.randrange(n)]
            t4 += c4[0]
            p4 += c4[1]
            g4 += c4[2]
            t2 += c2[0]
            p2 += c2[1]
            g2 += c2[2]
            tb += cb[0]
            pb += cb[1]
            gb += cb[2]
        f4 = prf_from_counts(t4, p4, g4)["f1"]
        f2 = prf_from_counts(t2, p2, g2)["f1"]
        fb = prf_from_counts(tb, pb, gb)["f1"]
        d24.append(f2 - f4)
        db2.append(fb - f2)
    d24.sort()
    db2.sort()
    lo = int(0.025 * (n_boot - 1))
    hi = int(0.975 * (n_boot - 1))
    return {
        "delta_2_vs_4_ci_low": d24[lo],
        "delta_2_vs_4_ci_high": d24[hi],
        "delta_boundary_vs_2_ci_low": db2[lo],
        "delta_boundary_vs_2_ci_high": db2[hi],
        "delta_2_vs_4_boot_mean": sum(d24) / n_boot,
        "delta_boundary_vs_2_boot_mean": sum(db2) / n_boot,
    }


def counts_one(gs, ps) -> tuple[int, int, int]:
    m = match_exact(gs, ps)
    return int(m["tp"]), int(m["pred"]), int(m["gold"])


def label_set_from_spans(spans) -> set[str]:
    return {t for _, _, t in spans}


def span_overlap_stats(spans: list[tuple[int, int, str]]) -> dict[str, int]:
    n_dup = len(spans) - len(set(spans))
    n_overlap = 0
    for i, (a1, b1, _t1) in enumerate(spans):
        for a2, b2, _t2 in spans[i + 1 :]:
            if a1 == a2 and b1 == b2:
                continue
            if min(b1, b2) > max(a1, a2):
                n_overlap += 1
    return {"n_duplicate_span_tuples": n_dup, "n_overlapping_span_pairs": n_overlap}


def audit_records(path: Path) -> dict[str, Any]:
    rows = load_records(str(path))
    ids = [rec_id(r) for r in rows]
    counts = Counter(ids)
    first, info = index_by_id(rows, "first")
    labels = Counter()
    n_overlap = 0
    n_dup_span = 0
    n_empty = 0
    n_nonempty = 0
    for rec in first.values():
        sp = extract_spans(rec, PRED_FIELDS if "pred" in path.name.lower() or True else GOLD_FIELDS)
        if not sp:
            n_empty += 1
        else:
            n_nonempty += 1
        for _a, _b, t in sp:
            labels[t] += 1
        st = span_overlap_stats(sp)
        n_dup_span += st["n_duplicate_span_tuples"]
        n_overlap += st["n_overlapping_span_pairs"]
    return {
        "path": str(path.resolve()),
        "exists": path.is_file(),
        "bytes": path.stat().st_size if path.is_file() else 0,
        "sha256": sha256_file(str(path)) if path.is_file() else None,
        "n_rows": len(rows),
        "n_unique_ids": len(counts),
        "n_duplicate_ids": sum(1 for c in counts.values() if c > 1),
        "n_extra_rows": len(rows) - len(counts),
        "label_counts": dict(labels),
        "n_sents_empty_span": n_empty,
        "n_sents_nonempty_span": n_nonempty,
        "n_duplicate_span_tuples": n_dup_span,
        "n_overlapping_span_pairs": n_overlap,
        "id_set": set(counts),
    }


def greedy_type_pairs(g_types: list[str], p_types: list[str]):
    gt = list(g_types)
    pt = list(p_types)
    same = []
    diff = []
    leftover_g = []
    leftover_p = []
    for t in list(gt):
        if t in pt:
            gt.remove(t)
            pt.remove(t)
            same.append((t, t))
    while gt and pt:
        g = gt.pop(0)
        p = pt.pop(0)
        diff.append((g, p))
    leftover_g.extend(gt)
    leftover_p.extend(pt)
    return same, diff, leftover_g, leftover_p


def error_breakdown_sentence(gsp, psp) -> dict[str, Any]:
    g_bounds: dict[tuple[int, int], list[str]] = defaultdict(list)
    p_bounds: dict[tuple[int, int], list[str]] = defaultdict(list)
    for a, b, t in gsp:
        g_bounds[(a, b)].append(t)
    for a, b, t in psp:
        p_bounds[(a, b)].append(t)
    gb, pb = set(g_bounds), set(p_bounds)
    matched = gb & pb
    missed_b = gb - pb
    extra_b = pb - gb

    n_gold_spans = len(gsp)
    n_pred_spans = len(psp)
    n_miss_spans = sum(len(g_bounds[b]) for b in missed_b)
    n_extra_spans = sum(len(p_bounds[b]) for b in extra_b)

    conf4: Counter[tuple[str, str]] = Counter()
    conf2: Counter[tuple[str, str]] = Counter()
    n_same = n_diff = n_lk = n_st = n_cross = 0
    n_bound_leftover_g = n_bound_leftover_p = 0

    for b in matched:
        same, diff, lg, lp = greedy_type_pairs(g_bounds[b], p_bounds[b])
        for g, p in same:
            n_same += 1
            conf4[(g, p)] += 1
            conf2[(MAP_2WAY.get(g, g), MAP_2WAY.get(p, p))] += 1
        for g, p in diff:
            n_diff += 1
            conf4[(g, p)] += 1
            gg = {g}
            pp = {p}
            if gg <= KNOWLEDGE and pp <= KNOWLEDGE:
                n_lk += 1
            elif gg <= SKILL_GROUP and pp <= SKILL_GROUP:
                n_st += 1
            else:
                n_cross += 1
            g2, p2 = MAP_2WAY.get(g, g), MAP_2WAY.get(p, p)
            conf2[(g2, p2)] += 1
        for g in lg:
            n_bound_leftover_g += 1
            conf4[(g, "NONE")] += 1
            conf2[(MAP_2WAY.get(g, g), "NONE")] += 1
        for p in lp:
            n_bound_leftover_p += 1
            conf4[("NONE", p)] += 1
            conf2[("NONE", MAP_2WAY.get(p, p))] += 1

    for b in missed_b:
        for g in g_bounds[b]:
            conf4[(g, "NONE")] += 1
            conf2[(MAP_2WAY.get(g, g), "NONE")] += 1
    for b in extra_b:
        for p in p_bounds[b]:
            conf4[("NONE", p)] += 1
            conf2[("NONE", MAP_2WAY.get(p, p))] += 1

    n_boundary_matched_pairs = n_same + n_diff
    cond_acc = (n_same / n_boundary_matched_pairs) if n_boundary_matched_pairs else None
    return {
        "n_gold_spans": n_gold_spans,
        "n_pred_spans": n_pred_spans,
        "n_boundary_matched_gold_bounds": len(matched),
        "n_miss_bounds": len(missed_b),
        "n_extra_bounds": len(extra_b),
        "n_miss_spans": n_miss_spans,
        "n_extra_spans": n_extra_spans,
        "n_type_same": n_same,
        "n_type_diff": n_diff,
        "n_recoverable_L_K": n_lk,
        "n_recoverable_S_T": n_st,
        "n_cross_group": n_cross,
        "n_bound_leftover_gold": n_bound_leftover_g,
        "n_bound_leftover_pred": n_bound_leftover_p,
        "conditional_type_accuracy": cond_acc,
        "conf4": conf4,
        "conf2": conf2,
    }


def add_counter(dst: Counter, src: Counter) -> None:
    dst.update(src)


MODELS: list[dict[str, Any]] = [
    {
        "model": "GPT-4o",
        "family": "llm",
        "path": PAPER / "reports/views/ChatGPT_unique_first_v2.jsonl",
        "include": True,
        "note": "Official Gold-v2 unique-first view of GPT-4o dump (raw dump has duplicate gold IDs).",
        "raw_dump": str(
            ROOT
            / "chinese_skillspan_preprocessing/output/dir/test-gpt/silver_gpt4o_sent_ner_test_1005_last_test.jsonl"
        ),
    },
    {
        "model": "DeepSeek",
        "family": "llm",
        "path": ROOT / "chinese_skillspan_preprocessing/output/dir/test-deepseek/ds_test_.merged.jsonl",
        "include": True,
    },
    {
        "model": "Qwen2.5-14B",
        "family": "llm",
        "path": ROOT / "output/chinese_skillspan_qwen25-14b_test_all.jsonl",
        "include": True,
    },
    {
        "model": "Claude",
        "family": "llm",
        "path": ROOT / "chinese_skillspan_preprocessing/output/dir/test_claude/merged_test_cluade.jsonl",
        "include": False,
        "skip_reason": "incomplete dump (missing Gold IDs)",
    },
    {
        "model": "Kimi",
        "family": "llm",
        "path": ROOT / "chinese_skillspan_preprocessing/output/dir/test-kimi/merged_test_kimi.jsonl",
        "include": False,
        "skip_reason": "incomplete dump (missing Gold IDs)",
    },
    {
        "model": "RoBERTa-wwm_goldstyle-v3_seed42",
        "family": "encoder",
        "path": PAPER / "output/cn_roberta_wwm_crf/smoke_goldstyle_v3_seed42/test_pred.jsonl",
        "include": True,
    },
    {
        "model": "JobBERT-zh_1M_goldstyle-v3_seed42",
        "family": "encoder",
        "path": PAPER / "output/jobbert_zh_1m/crf_v3_seed42/test_pred.jsonl",
        "include": True,
    },
    {
        "model": "JobBERT-zh_1M_seed123",
        "family": "encoder",
        "path": PAPER / "output/encoder_3seed/jobbert_zh_1m/seed_123/test_pred.jsonl",
        "include": True,
    },
    {
        "model": "JobBERT-zh_1M_seed2026",
        "family": "encoder",
        "path": PAPER / "output/encoder_3seed/jobbert_zh_1m/seed_2026/test_pred.jsonl",
        "include": True,
    },
    {
        "model": "JobBERT-zh_3M_ckpt65000_seed42",
        "family": "encoder",
        "path": PAPER / "output/jobbert_zh_3m/crf_ckpt65000_ep1/test_pred.jsonl",
        "include": True,
    },
    {
        "model": "JobBERT-zh_3M_ckpt65000_seed123",
        "family": "encoder",
        "path": PAPER / "output/encoder_3seed/jobbert_zh_3m_ckpt65000/seed_123/test_pred.jsonl",
        "include": True,
    },
    {
        "model": "JobBERT-zh_3M_crf-v3_seed42",
        "family": "encoder",
        "path": PAPER / "output/jobbert_zh_3m/crf_v3_seed42/test_pred.jsonl",
        "include": True,
    },
    {
        "model": "JobBERT-zh_3M_ckpt100000_seed42",
        "family": "encoder",
        "path": PAPER / "output/jobbert_zh_3m_ckpt_sweep/crf_ckpt100000/test_pred.jsonl",
        "include": True,
    },
    {
        "model": "JobBERT-zh_listed-mix_1M_seed42",
        "family": "encoder",
        "path": PAPER / "output/jobbert_zh_listed_1m/crf_v3_seed42/test_pred.jsonl",
        "include": True,
    },
    {
        "model": "JobBERT-zh_domain-mix_1M_seed42",
        "family": "encoder",
        "path": PAPER / "output/jobbert_zh_domain_1m/crf_v3_seed42/test_pred.jsonl",
        "include": True,
    },
    {
        "model": "JobBERT-zh_domain-mix_1M_seed123",
        "family": "encoder",
        "path": PAPER / "output/jobbert_zh_domain_1m/crf_v3_seed123/test_pred.jsonl",
        "include": True,
    },
    {
        "model": "JobBERT-zh_1M_human380-v3_seed42",
        "family": "encoder",
        "path": PAPER / "output/jobbert_1m_human380_v3merge_seed42/test_pred.jsonl",
        "include": True,
    },
    {
        "model": "JobBERT-en-skill_head-transfer",
        "family": "encoder_transfer",
        "path": PAPER / "reports/views/JobBERT-skill_unique_first_v2.jsonl",
        "include": True,
        "pred_fields": ("pred_tags",),
        "note": "English JobBERT skill head; unique-first view; score pred_tags only (file also copies Gold BIO4)",
        "raw_dump": str(
            ROOT / "Baseline_Models_Collection/out_jobbert_skill_chinese_encoder_aligned.jsonl"
        ),
    },
    {
        "model": "JobBERT-en-knowledge_head-transfer",
        "family": "encoder_transfer",
        "path": PAPER / "reports/views/JobBERT-knowledge_unique_first_v2.jsonl",
        "include": True,
        "pred_fields": ("pred_tags",),
        "note": "English JobBERT knowledge head; unique-first view; score pred_tags only (file also copies Gold BIO4)",
        "raw_dump": str(
            ROOT / "Baseline_Models_Collection/out_jobbert_knowledge_chinese_encoder_skillaligned.jsonl"
        ),
    },
    {
        "model": "RoBERTa-wwm_goldstyle-v2_seed42",
        "family": "encoder_excluded",
        "path": PAPER / "output/cn_roberta_wwm_crf/smoke_goldstyle_v2_seed42/test_pred.jsonl",
        "include": False,
        "skip_reason": "not a formal run (failed goldstyle-v2 SOP)",
    },
    {
        "model": "RoBERTa-wwm_goldstyle-v1_seed42",
        "family": "encoder_excluded",
        "path": PAPER / "output/cn_roberta_wwm_crf/smoke_goldstyle_seed42/test_pred.jsonl",
        "include": False,
        "skip_reason": "not a formal run (failed goldstyle-v1 SOP)",
    },
    {
        "model": "RoBERTa-wwm_smoke_seed42",
        "family": "encoder_excluded",
        "path": PAPER / "output/cn_roberta_wwm_crf/smoke_seed42_gpu1/test_pred.jsonl",
        "include": False,
        "skip_reason": "not a formal run (smoke)",
    },
    {
        "model": "JobBERT-zh_demo80k_seed42",
        "family": "encoder_excluded",
        "path": PAPER / "output/jobbert_zh_demo/crf_v3_seed42/test_pred.jsonl",
        "include": False,
        "skip_reason": "demo 80k, not a main-table encoder",
    },
]


def score_model(gold_map, gold_order, gold_ids, spec, gold_audit) -> dict[str, Any]:
    pred_path = Path(spec["path"])
    model = spec["model"]
    row: dict[str, Any] = {
        "model": model,
        "family": spec["family"],
        "prediction_path": str(pred_path.resolve()),
        "n_gold_sentences": len(gold_ids),
        "include_requested": spec["include"],
    }
    if not pred_path.is_file():
        row["validation_status"] = "SKIPPED_MISSING_FILE"
        row["skip_reason"] = "prediction file not found"
        return row

    pred_audit = audit_records(pred_path)
    # Re-extract pred spans with PRED_FIELDS (audit_records used PRED_FIELDS already).
    pred_rows = load_records(str(pred_path))
    pred_counts = Counter(rec_id(r) for r in pred_rows)
    pred_map, pred_info = index_by_id(pred_rows, "first")
    pred_ids = set(pred_map)
    missing = sorted(i for i in gold_ids if pred_counts.get(i, 0) == 0)
    dup_gold_preds = sorted(i for i in gold_ids if pred_counts.get(i, 0) > 1)
    extra = sorted(i for i in pred_ids if i not in gold_ids)

    row.update(
        {
            "n_prediction_sentences": pred_info["n_rows"],
            "n_prediction_unique_ids": pred_info["n_unique_ids"],
            "missing_ids": len(missing),
            "extra_ids": len(extra),
            "duplicate_gold_pred_ids": len(dup_gold_preds),
            "pred_duplicate_ids": pred_info["n_duplicate_ids"],
            "pred_sha256": pred_audit["sha256"],
            "pred_label_counts": pred_audit["label_counts"],
            "pred_n_overlapping_span_pairs": pred_audit["n_overlapping_span_pairs"],
            "pred_n_duplicate_span_tuples": pred_audit["n_duplicate_span_tuples"],
        }
    )

    if not spec["include"]:
        row["validation_status"] = "SKIPPED"
        row["skip_reason"] = spec.get("skip_reason", "excluded")
        return row
    if missing or dup_gold_preds:
        row["validation_status"] = "SKIPPED_INCOMPLETE"
        row["skip_reason"] = (
            f"missing {len(missing)} gold IDs, duplicate preds for {len(dup_gold_preds)} gold IDs"
        )
        return row

    pred_fields = tuple(spec.get("pred_fields") or PRED_FIELDS)
    official = official_score(
        str(GOLD_PATH),
        str(pred_path),
        align_mode="official",
        pred_fields=pred_fields,
        n_boot=0,
    )
    if not official.get("alignment_ok"):
        row["validation_status"] = "SKIPPED_OFFICIAL_ALIGN_FAIL"
        row["skip_reason"] = official.get("error")
        row["official_f1_4way"] = (official.get("typed_exact") or {}).get("f1")
        return row

    ids = gold_order
    pairs4, pairs2, pairsb = [], [], []
    triples = []
    br_acc = {
        "n_gold_spans": 0,
        "n_pred_spans": 0,
        "n_miss_spans": 0,
        "n_extra_spans": 0,
        "n_type_same": 0,
        "n_type_diff": 0,
        "n_recoverable_L_K": 0,
        "n_recoverable_S_T": 0,
        "n_cross_group": 0,
        "n_bound_leftover_gold": 0,
        "n_bound_leftover_pred": 0,
        "n_boundary_matched_gold_bounds": 0,
        "n_miss_bounds": 0,
        "n_extra_bounds": 0,
    }
    conf4: Counter[tuple[str, str]] = Counter()
    conf2: Counter[tuple[str, str]] = Counter()
    gold_span_labels = Counter()
    pred_span_labels = Counter()

    for i in ids:
        gsp = extract_spans(gold_map[i], GOLD_FIELDS)
        psp = extract_spans(pred_map[i], pred_fields)
        for _a, _b, t in gsp:
            gold_span_labels[t] += 1
        for _a, _b, t in psp:
            pred_span_labels[t] += 1
        g2, p2 = project_2way(gsp), project_2way(psp)
        gb, pb = project_boundary(gsp), project_boundary(psp)
        pairs4.append((gsp, psp))
        pairs2.append((g2, p2))
        pairsb.append((gb, pb))
        triples.append((counts_one(gsp, psp), counts_one(g2, p2), counts_one(gb, pb)))
        eb = error_breakdown_sentence(gsp, psp)
        for k in br_acc:
            br_acc[k] += eb[k]
        add_counter(conf4, eb["conf4"])
        add_counter(conf2, eb["conf2"])

    m4 = micro_pairs(pairs4)
    m2 = micro_pairs(pairs2)
    mb = micro_pairs(pairsb)
    off4 = official["typed_exact"]
    offb = official["collapsed_exact"]

    ok_4 = abs(m4["f1"] - off4["f1"]) < EPS and abs(m4["precision"] - off4["precision"]) < EPS and abs(
        m4["recall"] - off4["recall"]
    ) < EPS
    ok_b = abs(mb["f1"] - offb["f1"]) < EPS and abs(mb["precision"] - offb["precision"]) < EPS and abs(
        mb["recall"] - offb["recall"]
    ) < EPS

    status = "OK"
    fail_reasons = []
    if not ok_4:
        status = "FAILED VALIDATION"
        fail_reasons.append(
            f"4-way mismatch vs official scorer: script F1={m4['f1']:.10f} official={off4['f1']:.10f}"
        )
    if not ok_b:
        status = "FAILED VALIDATION"
        fail_reasons.append(
            f"boundary mismatch vs official collapsed: script F1={mb['f1']:.10f} official={offb['f1']:.10f}"
        )
    if not (m4["f1"] <= m2["f1"] + MONO_EPS and m2["f1"] <= mb["f1"] + MONO_EPS):
        status = "FAILED VALIDATION"
        fail_reasons.append(
            f"monotonicity failed: F1_4={m4['f1']:.10f} F1_2={m2['f1']:.10f} F1_b={mb['f1']:.10f}"
        )

    if model in REF_4WAY and abs(m4["f1"] - REF_4WAY[model]) >= EPS:
        status = "FAILED VALIDATION"
        fail_reasons.append(
            f"4-way F1 {m4['f1']:.10f} != reference {REF_4WAY[model]:.10f} (wrong dump/Gold?)"
        )
    if model == "GPT-4o":
        if not (m4["f1"] - 1e-4 <= m2["f1"] <= mb["f1"] + 1e-4):
            status = "FAILED VALIDATION"
            fail_reasons.append("GPT-4o 2-way not between this run's 4-way and boundary")
        if abs(m4["f1"] - 0.6365) < 5e-4 and abs(mb["f1"] - 0.6403) < 5e-4:
            if not (0.6365 - 5e-4 <= m2["f1"] <= 0.6403 + 5e-4):
                status = "FAILED VALIDATION"
                fail_reasons.append(
                    f"GPT-4o 2-way {m2['f1']:.6f} outside reference band 0.6365–0.6403"
                )

    n_bound_pairs = br_acc["n_type_same"] + br_acc["n_type_diff"]
    cond_acc = (br_acc["n_type_same"] / n_bound_pairs) if n_bound_pairs else None
    n_type_err = br_acc["n_type_diff"]
    n_recov = br_acc["n_recoverable_L_K"] + br_acc["n_recoverable_S_T"]
    recov_frac_of_type_err = (n_recov / n_type_err) if n_type_err else None
    recov_frac_of_fn_fp = None
    denom = br_acc["n_miss_spans"] + br_acc["n_extra_spans"] + n_type_err
    if denom:
        recov_frac_of_fn_fp = n_recov / denom

    boot = bootstrap_deltas(triples, N_BOOT, BOOT_SEED) if status == "OK" else {}
    d24 = m2["f1"] - m4["f1"]
    db2 = mb["f1"] - m2["f1"]

    primary_cause = diagnose_cause(m4, br_acc, n_type_err, n_recov)

    row.update(
        {
            "validation_status": status,
            "fail_reasons": fail_reasons,
            "official_align_ok": True,
            "scorer_version": official["scorer_version"],
            "P_4way": m4["precision"],
            "R_4way": m4["recall"],
            "F1_4way": m4["f1"],
            "tp_4way": m4["tp"],
            "fp_4way": m4["fp"],
            "fn_4way": m4["fn"],
            "P_2way": m2["precision"],
            "R_2way": m2["recall"],
            "F1_2way": m2["f1"],
            "tp_2way": m2["tp"],
            "fp_2way": m2["fp"],
            "fn_2way": m2["fn"],
            "P_boundary": mb["precision"],
            "R_boundary": mb["recall"],
            "F1_boundary": mb["f1"],
            "tp_boundary": mb["tp"],
            "fp_boundary": mb["fp"],
            "fn_boundary": mb["fn"],
            "delta_2_vs_4": d24,
            "delta_boundary_vs_2": db2,
            "official_F1_4way": off4["f1"],
            "official_F1_collapsed": offb["f1"],
            "official_4way_match": ok_4,
            "official_boundary_match": ok_b,
            "n_type_same": br_acc["n_type_same"],
            "n_type_diff": n_type_err,
            "n_recoverable_L_K": br_acc["n_recoverable_L_K"],
            "n_recoverable_S_T": br_acc["n_recoverable_S_T"],
            "n_cross_group": br_acc["n_cross_group"],
            "n_miss_spans": br_acc["n_miss_spans"],
            "n_extra_spans": br_acc["n_extra_spans"],
            "n_miss_bounds": br_acc["n_miss_bounds"],
            "n_extra_bounds": br_acc["n_extra_bounds"],
            "n_gold_spans": br_acc["n_gold_spans"],
            "n_pred_spans": br_acc["n_pred_spans"],
            "conditional_type_accuracy": cond_acc,
            "recoverable_frac_of_type_errors": recov_frac_of_type_err,
            "recoverable_frac_of_all_span_errors": recov_frac_of_fn_fp,
            "primary_error_cause": primary_cause,
            "gold_span_label_counts": dict(gold_span_labels),
            "pred_span_label_counts": dict(pred_span_labels),
            "conf4": {f"{a}->{b}": v for (a, b), v in sorted(conf4.items())},
            "conf2": {f"{a}->{b}": v for (a, b), v in sorted(conf2.items())},
            "conf4_raw": conf4,
            "conf2_raw": conf2,
            "note": spec.get("note"),
        }
    )
    row.update(boot)
    return row


def diagnose_cause(m4, br_acc, n_type_err, n_recov) -> str:
    miss = br_acc["n_miss_spans"]
    extra = br_acc["n_extra_spans"]
    boundary = miss + extra
    typed_wrong = n_type_err
    recov = n_recov
    cross = br_acc["n_cross_group"]
    if m4["recall"] < 0.25 and boundary > 3 * max(typed_wrong, 1):
        return "A. 边界/漏检"
    if typed_wrong > boundary and recov >= 0.6 * typed_wrong:
        return "B. L-K与S-T细分类"
    if cross > recov and typed_wrong > boundary * 0.5:
        return "C. 跨组类型混淆"
    return "D. 多种因素"


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            out = {}
            for k in fieldnames:
                v = r.get(k)
                if isinstance(v, float):
                    out[k] = f"{v:.10f}"
                elif v is None:
                    out[k] = ""
                else:
                    out[k] = v
            w.writerow(out)


def fmt_prf(p, r, f) -> str:
    if p is None:
        return "—"
    return f"{p:.4f}/{r:.4f}/{f:.4f}"


def main() -> int:
    started = datetime.now(timezone.utc).isoformat()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    gold_rows = load_records(str(GOLD_PATH))
    gold_map, gold_info = index_by_id(gold_rows, "first")
    gold_ids = set(gold_map)
    gold_order = gold_info["id_order"]
    gold_audit = {
        "path": str(GOLD_PATH.resolve()),
        "bytes": GOLD_PATH.stat().st_size,
        "sha256": sha256_file(str(GOLD_PATH)),
        "n_rows": gold_info["n_rows"],
        "n_unique_ids": gold_info["n_unique_ids"],
        "n_duplicate_ids": gold_info["n_duplicate_ids"],
    }
    gold_labels = Counter()
    gold_overlap = 0
    gold_dup_span = 0
    for rec in gold_map.values():
        sp = extract_spans(rec, GOLD_FIELDS)
        for _a, _b, t in sp:
            gold_labels[t] += 1
        st = span_overlap_stats(sp)
        gold_overlap += st["n_overlapping_span_pairs"]
        gold_dup_span += st["n_duplicate_span_tuples"]
    gold_audit["label_counts"] = dict(gold_labels)
    gold_audit["n_overlapping_span_pairs"] = gold_overlap
    gold_audit["n_duplicate_span_tuples"] = gold_dup_span
    gold_audit["offset_convention"] = (
        "half-open token index [start, end) from BIO decoding (cnss-lskt-1.2.0); "
        "not Doccano character offsets. End is exclusive."
    )

    results = []
    for spec in MODELS:
        print(f"[score] {spec['model']} ...", flush=True)
        results.append(score_model(gold_map, gold_order, gold_ids, spec, gold_audit))

    coverage_rows = []
    for spec, res in zip(MODELS, results):
        coverage_rows.append(
            {
                "model": spec["model"],
                "family": spec["family"],
                "prediction_path": res.get("prediction_path"),
                "include_requested": spec["include"],
                "validation_status": res.get("validation_status"),
                "skip_reason": res.get("skip_reason", ""),
                "n_gold_sentences": res.get("n_gold_sentences"),
                "n_prediction_sentences": res.get("n_prediction_sentences", ""),
                "n_prediction_unique_ids": res.get("n_prediction_unique_ids", ""),
                "missing_ids": res.get("missing_ids", ""),
                "extra_ids": res.get("extra_ids", ""),
                "duplicate_gold_pred_ids": res.get("duplicate_gold_pred_ids", ""),
                "pred_duplicate_ids": res.get("pred_duplicate_ids", ""),
                "pred_sha256": res.get("pred_sha256", ""),
                "pred_labels": json.dumps(res.get("pred_label_counts") or {}, ensure_ascii=False),
            }
        )

    ok_rows = [r for r in results if r.get("validation_status") == "OK"]
    failed = [r for r in results if r.get("validation_status") == "FAILED VALIDATION"]

    metric_fields = [
        "model",
        "prediction_path",
        "n_gold_sentences",
        "n_prediction_sentences",
        "missing_ids",
        "extra_ids",
        "P_4way",
        "R_4way",
        "F1_4way",
        "P_2way",
        "R_2way",
        "F1_2way",
        "P_boundary",
        "R_boundary",
        "F1_boundary",
        "delta_2_vs_4",
        "delta_boundary_vs_2",
        "delta_2_vs_4_ci_low",
        "delta_2_vs_4_ci_high",
        "delta_boundary_vs_2_ci_low",
        "delta_boundary_vs_2_ci_high",
        "validation_status",
        "family",
        "official_F1_4way",
        "official_F1_collapsed",
        "primary_error_cause",
    ]
    write_csv(OUT_DIR / "metrics.csv", ok_rows + failed, metric_fields)

    err_fields = [
        "model",
        "n_type_same",
        "n_type_diff",
        "n_recoverable_L_K",
        "n_recoverable_S_T",
        "n_cross_group",
        "n_miss_spans",
        "n_extra_spans",
        "n_miss_bounds",
        "n_extra_bounds",
        "conditional_type_accuracy",
        "recoverable_frac_of_type_errors",
        "recoverable_frac_of_all_span_errors",
        "primary_error_cause",
        "tp_4way",
        "fp_4way",
        "fn_4way",
        "tp_2way",
        "F1_4way",
        "F1_2way",
        "F1_boundary",
        "validation_status",
    ]
    write_csv(OUT_DIR / "error_breakdown.csv", ok_rows, err_fields)
    write_csv(OUT_DIR / "coverage_audit.csv", coverage_rows, list(coverage_rows[0].keys()))

    boot_fields = [
        "model",
        "delta_2_vs_4",
        "delta_2_vs_4_ci_low",
        "delta_2_vs_4_ci_high",
        "delta_2_vs_4_boot_mean",
        "delta_boundary_vs_2",
        "delta_boundary_vs_2_ci_low",
        "delta_boundary_vs_2_ci_high",
        "delta_boundary_vs_2_boot_mean",
        "validation_status",
    ]
    write_csv(OUT_DIR / "bootstrap_ci.csv", ok_rows, boot_fields)

    with (OUT_DIR / "confusion_4way.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["model", "gold_type", "pred_type", "count"])
        w.writeheader()
        for r in ok_rows:
            for (g, p), c in sorted(r["conf4_raw"].items()):
                w.writerow({"model": r["model"], "gold_type": g, "pred_type": p, "count": c})

    with (OUT_DIR / "confusion_2way.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["model", "gold_type", "pred_type", "count"])
        w.writeheader()
        for r in ok_rows:
            for (g, p), c in sorted(r["conf2_raw"].items()):
                w.writerow({"model": r["model"], "gold_type": g, "pred_type": p, "count": c})

    serializable = []
    for r in results:
        x = {k: v for k, v in r.items() if k not in {"conf4_raw", "conf2_raw"}}
        serializable.append(x)

    (OUT_DIR / "metrics.json").write_text(
        json.dumps(serializable, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )

    cmd = "python Chinese_skill_benchmark_Paper/scripts/eval_lskt_projection.py"
    manifest = {
        "created_utc": started,
        "finished_utc": datetime.now(timezone.utc).isoformat(),
        "cwd": str(Path.cwd()),
        "git_head": git_commit(PAPER),
        "scorer_version": SCORER_VERSION,
        "scorer_path": str((PAPER / "scorer/score_lskt.py").resolve()),
        "gold_path": gold_audit["path"],
        "gold_sha256": gold_audit["sha256"],
        "gold_n_rows": gold_audit["n_rows"],
        "gold_n_unique_ids": gold_audit["n_unique_ids"],
        "offset_convention": gold_audit["offset_convention"],
        "label_mapping_2way": MAP_2WAY,
        "boundary_label": "COMPETENCY",
        "match_key": "(sentence_id, start, end, label)",
        "aggregation": "micro_over_sentences",
        "bootstrap_n": N_BOOT,
        "bootstrap_seed": BOOT_SEED,
        "bootstrap_unit": "sentence",
        "command": cmd,
        "predictions": [
            {
                "model": r["model"],
                "path": r.get("prediction_path"),
                "sha256": r.get("pred_sha256"),
                "status": r.get("validation_status"),
            }
            for r in results
        ],
    }
    (OUT_DIR / "source_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    report = build_report(gold_audit, results, ok_rows, failed, started)
    (OUT_DIR / "LSKT_PROJECTION_REPORT.md").write_text(report, encoding="utf-8")
    print(report)
    print(f"\nWrote {OUT_DIR}", flush=True)
    return 1 if failed else 0


def build_report(gold_audit, results, ok_rows, failed, started) -> str:
    lines = []
    a = lines.append
    a("# LSKT projection audit")
    a("")
    a("Read-only. Gold v2 + `cnss-lskt-1.2.0`. Metric name: **Projected SKILL/KNOWLEDGE exact-span F1**.")
    a("Not SkillSpan dataset F1 (evaluation data remain Chinese-SkillSpan).")
    a("")
    a("## A. Data and protocol")
    a("")
    a(f"- Gold: `{gold_audit['path']}`")
    a(f"- Gold SHA-256: `{gold_audit['sha256']}`")
    a(f"- Gold rows / unique IDs: {gold_audit['n_rows']} / {gold_audit['n_unique_ids']}")
    a(f"- Gold labels: `{gold_audit['label_counts']}`")
    a(f"- Gold overlapping span pairs: {gold_audit['n_overlapping_span_pairs']}; duplicate span tuples: {gold_audit['n_duplicate_span_tuples']}")
    a(f"- Scorer: `{SCORER_VERSION}` (`Chinese_skill_benchmark_Paper/scorer/score_lskt.py`)")
    a("- Match key: `(sentence_id, start, end, label)` — **not** a global `(start, end, label)` set")
    a(f"- Offset: {gold_audit['offset_convention']}")
    a("- 2-way map: L→KNOWLEDGE, K→KNOWLEDGE, S→SKILL, T→SKILL (same map on Gold and pred)")
    a("- Boundary map: all types → COMPETENCY (F1 equals official collapsed-to-SKILL)")
    a("- Official 4-way reproduced iff `|F1_script - F1_official| < 1e-6`")
    a("")
    a("## B. Main results (validation_status=OK only)")
    a("")
    a("| Model | 4-way P/R/F1 | 2-way P/R/F1 | Boundary P/R/F1 | Δ 2-way vs 4-way | 95% CI |")
    a("|---|---|---|---|---:|---|")
    for r in ok_rows:
        ci = f"[{r['delta_2_vs_4_ci_low']:.4f}, {r['delta_2_vs_4_ci_high']:.4f}]"
        a(
            f"| {r['model']} | {fmt_prf(r['P_4way'], r['R_4way'], r['F1_4way'])} | "
            f"{fmt_prf(r['P_2way'], r['R_2way'], r['F1_2way'])} | "
            f"{fmt_prf(r['P_boundary'], r['R_boundary'], r['F1_boundary'])} | "
            f"{r['delta_2_vs_4']:+.4f} | {ci} |"
        )
    if not ok_rows:
        a("| _(none)_ | | | | | |")
    a("")
    if failed:
        a("## FAILED VALIDATION (excluded from table)")
        a("")
        for r in failed:
            a(f"- **{r['model']}**: {r.get('fail_reasons')}")
        a("")
    skipped = [r for r in results if str(r.get("validation_status", "")).startswith("SKIPPED")]
    if skipped:
        a("## Skipped")
        a("")
        for r in skipped:
            a(f"- {r['model']}: {r.get('validation_status')} — {r.get('skip_reason', '')}")
        a("")
    a("## C. Error sources (OK models)")
    a("")
    a("| Model | L↔K | S↔T | cross L/K↔S/T | miss (FN bounds) | extra (FP bounds) | type-same | cond. type acc | cause |")
    a("|---|---:|---:|---:|---:|---:|---:|---:|---|")
    for r in ok_rows:
        acc = r.get("conditional_type_accuracy")
        accs = f"{acc:.4f}" if acc is not None else "—"
        a(
            f"| {r['model']} | {r['n_recoverable_L_K']} | {r['n_recoverable_S_T']} | "
            f"{r['n_cross_group']} | {r['n_miss_spans']} | {r['n_extra_spans']} | "
            f"{r['n_type_same']} | {accs} | {r['primary_error_cause']} |"
        )
    a("")
    a("## D. Conclusions")
    a("")
    if ok_rows:
        a("1. Two-way lift per model (F1_2way − F1_4way):")
        a("")
        for r in ok_rows:
            a(f"   - {r['model']}: {r['delta_2_vs_4']:+.4f}")
        a("")
        causes = Counter(r["primary_error_cause"] for r in ok_rows)
        a("2. Recoverable L↔K / S↔T vs cross-group (see table C).")
        a("3. Primary low-F1 cause counts: " + ", ".join(f"{k} n={v}" for k, v in causes.items()))
        a("4. Paper main-table 2-way column: wait for user confirmation; this audit does not edit the paper.")
    else:
        a("No OK models; do not interpret deltas.")
    a("")
    a("## E. Files")
    a("")
    a(f"- Output dir: `{OUT_DIR}`")
    a(f"- Started UTC: {started}")
    a("")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
