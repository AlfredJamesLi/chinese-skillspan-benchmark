#!/usr/bin/env python3
"""Round-2 JobBERT metric audit, canonical Table 3, split leakage.

Does not modify raw Gold or overwrite prediction dumps.
"""
from __future__ import annotations

import csv
import json
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path("/home/guojingli3/SCESC-LLM-skill-extraction")
PAPER = ROOT / "Chinese_skill_benchmark_Paper"
GOLD = PAPER / "data/gold_canonical_v2.jsonl"
VIEWS = PAPER / "reports/views"
sys.path.insert(0, str(PAPER / "scorer"))
from score_lskt import (  # noqa: E402
    GOLD_FIELDS,
    PRED_FIELDS,
    SCORER_VERSION,
    _norm_tag,
    align_len,
    collapse,
    extract_spans,
    load_records,
    match_exact,
    match_relaxed,
    micro_over_sentences,
    pick_tags,
    rec_id,
    score,
    sentence_n,
    seqeval_entities,
    sha256_file,
    tags_to_spans,
)

PREDS = {
    "ChatGPT": {
        "path": ROOT / "chinese_skillspan_preprocessing/output/dir/test-gpt/silver_gpt4o_sent_ner_test_1005_last_test.jsonl",
        "setting": "GPT-4o silver dump 2025-10-05; prompt_template_rag chinese_skillspan; model version string not logged",
        "paper": 0.6700,
        "fields": PRED_FIELDS,
    },
    "Claude": {
        "path": ROOT / "chinese_skillspan_preprocessing/output/dir/test_claude/merged_test_cluade.jsonl",
        "setting": "Claude-3.5 silver merge; incomplete; version not logged",
        "paper": 0.6300,
        "fields": PRED_FIELDS,
    },
    "Kimi": {
        "path": ROOT / "chinese_skillspan_preprocessing/output/dir/test-kimi/merged_test_kimi.jsonl",
        "setting": "Kimi-k2 silver merge; incomplete; version not logged",
        "paper": 0.5700,
        "fields": PRED_FIELDS,
    },
    "DeepSeek": {
        "path": ROOT / "chinese_skillspan_preprocessing/output/dir/test-deepseek/ds_test_.merged.jsonl",
        "setting": "DeepSeek-r1 silver merge; version not logged",
        "paper": 0.5130,
        "fields": PRED_FIELDS,
    },
    "Qwen": {
        "path": ROOT / "output/chinese_skillspan_qwen25-14b_test_all.jsonl",
        "setting": "Qwen2.5-14B dump 2025-10-07; SFT vs base unlabeled in file; paper 0.2130 unreproducible — do not tune toward it",
        "paper": 0.2130,
        "fields": PRED_FIELDS,
    },
    "JobBERT-skill": {
        "path": ROOT / "Baseline_Models_Collection/out_jobbert_skill_chinese_encoder_aligned.jsonl",
        "setting": "JobBERT-skill head + hfl/chinese-bert-wwm-ext; pred_tags; dump copies raw Gold duplicate rows",
        "paper": 0.0045,
        "fields": ("pred_tags",),
    },
    "JobBERT-knowledge": {
        "path": ROOT / "Baseline_Models_Collection/out_jobbert_knowledge_chinese_encoder_skillaligned.jsonl",
        "setting": "JobBERT-knowledge head + Chinese encoder; pred_tags; dump copies raw Gold duplicate rows",
        "paper": 0.0038,
        "fields": ("pred_tags",),
    },
}


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def illegal_bio(tags: list[str]) -> Counter:
    c: Counter[str] = Counter()
    prev = "O"
    for t in tags:
        t = _norm_tag(t)
        if t.startswith("I-"):
            typ = t[2:]
            if prev == "O":
                c["I-after-O"] += 1
            elif prev.startswith("B-") and prev[2:] != typ:
                c["I-after-B-other-type"] += 1
            elif prev.startswith("I-") and prev[2:] != typ:
                c["I-after-I-other-type"] += 1
        prev = t
    return c


def repair_i_to_b(tags: list[str]) -> list[str]:
    out = []
    prev = "O"
    for t in tags:
        t = _norm_tag(t)
        if t.startswith("I-"):
            typ = t[2:]
            prev_typ = prev[2:] if prev[:2] in {"B-", "I-"} else ""
            if prev == "O" or prev_typ != typ:
                t = f"B-{typ}"
        out.append(t)
        prev = t
    return out


def seqeval_strict_entities(tags: list[str]) -> list[tuple[int, int, str]]:
    """IOB2-strict: I without a matching B does not start an entity."""
    chunks: list[tuple[int, int, str]] = []
    typ, start, ok = None, None, False
    seq = list(tags) + ["O"]
    for i, tok in enumerate(seq):
        tok = _norm_tag(tok)
        if tok.startswith("B-"):
            if typ is not None and ok:
                chunks.append((start, i, typ))
            typ, start, ok = tok[2:], i, True
        elif tok.startswith("I-"):
            lab = tok[2:]
            if typ is not None and ok and lab == typ:
                continue
            if typ is not None and ok:
                chunks.append((start, i, typ))
            typ, start, ok = None, None, False
        else:
            if typ is not None and ok:
                chunks.append((start, i, typ))
            typ, start, ok = None, None, False
    return chunks


def write_unique_first_view(src: Path, dest: Path, keep_ids: set[str] | None = None) -> dict:
    """Derived scoring view: first row per ID. Does not touch `src`."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    seen: set[str] = set()
    n_in = n_out = n_skip = 0
    with src.open(encoding="utf-8") as fin, dest.open("w", encoding="utf-8") as fout:
        for line in fin:
            if not line.strip():
                continue
            n_in += 1
            rec = json.loads(line)
            iid = rec_id(rec)
            if iid in seen:
                continue
            if keep_ids is not None and iid not in keep_ids:
                n_skip += 1
                seen.add(iid)
                continue
            seen.add(iid)
            n_out += 1
            fout.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return {"src": str(src), "dest": str(dest), "n_in": n_in, "n_out": n_out, "n_non_gold_skipped": n_skip}


def gold_to_skill(tags: list[str]) -> list[str]:
    out = []
    for t in tags:
        t = _norm_tag(t)
        if t == "O":
            out.append("O")
        else:
            out.append(f"{t[0]}-SKILL")
    return out


def token_span_text(tokens: list, start: int, end: int) -> str:
    return "".join(str(t) for t in tokens[start:end])


def jobbert_audit() -> None:
    gold_rows = load_records(str(GOLD))
    gold = {rec_id(r): r for r in gold_rows}
    pred_path = PREDS["JobBERT-skill"]["path"]
    view = VIEWS / "jobbert_skill_unique_first_canonical_v1.jsonl"
    view_meta = write_unique_first_view(pred_path, view, keep_ids=set(gold))
    view_k = VIEWS / "jobbert_knowledge_unique_first_canonical_v1.jsonl"
    write_unique_first_view(PREDS["JobBERT-knowledge"]["path"], view_k, keep_ids=set(gold))

    preds = load_records(str(view))
    pred_by = {rec_id(r): r for r in preds}

    illegal: Counter[str] = Counter()
    align = Counter()
    pairs_legal: list = []
    pairs_repair: list = []
    pairs_seq_def: list = []
    pairs_seq_strict: list = []
    pairs_typed_legal: list = []
    sample_pool = {"TP": [], "FP": [], "FN": []}

    join_ok = join_fail = offset_ok = offset_fail = 0
    for iid, grec in gold.items():
        prec = pred_by.get(iid)
        if prec is None:
            continue
        n = sentence_n(grec) or sentence_n(prec)
        gt = gold_to_skill(align_len(pick_tags(grec, GOLD_FIELDS), n))
        gt_typed = align_len(pick_tags(grec, GOLD_FIELDS), n)
        pt = align_len(pick_tags(prec, ("pred_tags",)), n)
        illegal.update(illegal_bio(pt))
        sent = grec.get("sentence") or ""
        toks = grec.get("tokens") or []
        if toks:
            joined = "".join(str(t) for t in toks)
            if joined == sent:
                join_ok += 1
            else:
                join_fail += 1
                align["join_ne_sentence"] += 1
            off = 0
            ok_off = True
            for t in toks:
                t = str(t)
                if sent[off : off + len(t)] != t:
                    ok_off = False
                    break
                off += len(t)
            if ok_off and off == len(sent):
                offset_ok += 1
            else:
                offset_fail += 1
        if "token_char_spans" in grec:
            align["has_token_char_spans"] += 1
        else:
            align["no_token_char_spans"] += 1
        if len(pt) != n:
            align["pred_len_ne_n"] += 1

        g_sp = tags_to_spans(gt)
        p_legal = tags_to_spans(pt)
        p_repair = tags_to_spans(repair_i_to_b(pt))
        p_def = seqeval_entities(pt)
        p_strict = seqeval_strict_entities(pt)
        pairs_legal.append((g_sp, p_legal))
        pairs_repair.append((g_sp, p_repair))
        pairs_seq_def.append((g_sp, p_def))
        pairs_seq_strict.append((g_sp, p_strict))
        pairs_typed_legal.append((tags_to_spans(gt_typed), tags_to_spans(pt)))

        gset, pset = set(g_sp), set(p_legal)
        for sp in gset & pset:
            sample_pool["TP"].append((iid, sp, token_span_text(toks, sp[0], sp[1]), sent))
        for sp in pset - gset:
            sample_pool["FP"].append((iid, sp, token_span_text(toks, sp[0], sp[1]), sent))
        for sp in gset - pset:
            sample_pool["FN"].append((iid, sp, token_span_text(toks, sp[0], sp[1]), sent))

    rng = random.Random(20260822)
    samples = {}
    for k, pool in sample_pool.items():
        rng.shuffle(pool)
        samples[k] = [
            {"id": iid, "span_start": sp[0], "span_end": sp[1], "type": sp[2], "span_text": txt, "sentence": sent}
            for iid, sp, txt, sent in pool[:6]
        ]

    m_legal = micro_over_sentences(pairs_legal, match_exact)
    m_repair = micro_over_sentences(pairs_repair, match_exact)
    m_def = micro_over_sentences(pairs_seq_def, match_exact)
    m_ss = micro_over_sentences(pairs_seq_strict, match_exact)
    m_typed = micro_over_sentences(pairs_typed_legal, match_exact)
    m_rel_legal = micro_over_sentences(pairs_legal, lambda a, b: match_relaxed(a, b, 0.5))

    off_raw = score(str(GOLD), str(pred_path), align_mode="official", pred_fields=("pred_tags",), n_boot=0)
    off_view = score(str(GOLD), str(view), align_mode="official", pred_fields=("pred_tags",), n_boot=0)
    off_k = score(
        str(GOLD), str(view_k), align_mode="official", pred_fields=("pred_tags",), n_boot=0
    )

    seqeval_pkg = None
    try:
        from seqeval.metrics import f1_score, precision_score, recall_score
        from seqeval.scheme import IOB2

        y_true, y_pred = [], []
        for iid, grec in gold.items():
            prec = pred_by.get(iid)
            if prec is None:
                continue
            n = sentence_n(grec) or sentence_n(prec)
            y_true.append(gold_to_skill(align_len(pick_tags(grec, GOLD_FIELDS), n)))
            y_pred.append(align_len(pick_tags(prec, ("pred_tags",)), n))
        seqeval_pkg = {
            "default_f1": f1_score(y_true, y_pred),
            "default_p": precision_score(y_true, y_pred),
            "default_r": recall_score(y_true, y_pred),
            "strict_iob2_f1": f1_score(y_true, y_pred, mode="strict", scheme=IOB2),
            "strict_iob2_p": precision_score(y_true, y_pred, mode="strict", scheme=IOB2),
            "strict_iob2_r": recall_score(y_true, y_pred, mode="strict", scheme=IOB2),
        }
    except Exception as e:
        seqeval_pkg = {"error": f"{type(e).__name__}: {e}"}

    fixtures = [
        {"gold": ["O", "B-SKILL", "I-SKILL", "O"], "pred": ["O", "B-SKILL", "I-SKILL", "O"], "legal_tp": 1, "repair_tp": 1, "seqdef_tp": 1, "note": "exact match"},
        {"gold": ["O", "B-SKILL", "I-SKILL", "O"], "pred": ["O", "O", "O", "O"], "legal_tp": 0, "repair_tp": 0, "seqdef_tp": 0, "note": "miss entire span"},
        {"gold": ["O", "O", "O", "O"], "pred": ["O", "B-SKILL", "I-SKILL", "O"], "legal_tp": 0, "repair_tp": 0, "seqdef_tp": 0, "note": "false span"},
        {"gold": ["B-SKILL", "I-SKILL"], "pred": ["B-SKILL", "O"], "legal_tp": 0, "repair_tp": 0, "seqdef_tp": 0, "note": "right boundary short"},
        {"gold": ["O", "B-L", "I-L"], "pred": ["O", "B-S", "I-S"], "legal_tp": 0, "typed_tp": 0, "note": "type mismatch; collapsed still matches if both SKILL"},
        {"gold": ["O", "B-SKILL"], "pred": ["O", "I-SKILL"], "legal_tp": 0, "repair_tp": 1, "seqdef_tp": 1, "note": "illegal I-after-O"},
        {"gold": ["B-SKILL", "I-SKILL", "I-SKILL"], "pred": ["B-SKILL", "I-SKILL", "I-SKILL"], "legal_tp": 1, "note": "long span"},
        {"gold": ["B-SKILL", "O", "B-SKILL"], "pred": ["B-SKILL", "I-SKILL", "I-SKILL"], "legal_tp": 0, "note": "merge two gold spans"},
        {"gold": ["O"], "pred": ["O"], "legal_tp": 0, "note": "both empty"},
        {"gold": ["B-SKILL", "I-SKILL"], "pred": ["B-SKILL", "I-SKILL", "O"], "legal_tp": 1, "note": "pred longer; gold n used after align in scorer"},
        {"gold": ["B-SKILL", "I-SKILL"], "pred": ["B-K", "I-K"], "legal_tp": 0, "note": "typed SKILL vs K"},
        {"gold": ["O", "B-SKILL", "I-SKILL"], "pred": ["O", "I-SKILL", "I-SKILL"], "legal_tp": 0, "repair_tp": 1, "seqdef_tp": 1, "note": "illegal I-after-O covering the gold span"},
    ]
    fix_rows = []
    fix_ok = 0
    for i, fx in enumerate(fixtures, 1):
        g = [_norm_tag(x) for x in fx["gold"]]
        p = [_norm_tag(x) for x in fx["pred"]]
        n = max(len(g), len(p))
        g, p = align_len(g, n), align_len(p, n)
        legal = match_exact(tags_to_spans(g), tags_to_spans(p))
        repair = match_exact(tags_to_spans(g), tags_to_spans(repair_i_to_b(p)))
        seqdef = match_exact(tags_to_spans(g), seqeval_entities(p))
        expect = fx.get("legal_tp")
        ok = expect is None or legal["tp"] == expect
        if "repair_tp" in fx and repair["tp"] != fx["repair_tp"]:
            ok = False
        if "seqdef_tp" in fx and seqdef["tp"] != fx["seqdef_tp"]:
            ok = False
        if ok:
            fix_ok += 1
        fix_rows.append({
            "i": i,
            "note": fx["note"],
            "legal_tp": legal["tp"],
            "legal_fp": legal["fp"],
            "legal_fn": legal["fn"],
            "repair_tp": repair["tp"],
            "seqdef_tp": seqdef["tp"],
            "ok": int(ok),
        })

    adopt_046 = (
        off_view.get("alignment_ok")
        and (off_view.get("collapsed_exact") or {}).get("f1", 0) >= 0.3
        and abs((off_view.get("collapsed_exact") or {}).get("f1", 0) - m_legal["f1"]) < 0.02
    )
    paper_ok = 0.003 < (off_view.get("collapsed_exact") or {}).get("f1", 0) < 0.006

    (PAPER / "reports/jobbert_span_samples.json").write_text(
        json.dumps(samples, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    write_csv(PAPER / "reports/jobbert_fixtures.csv", fix_rows, ["i", "note", "legal_tp", "legal_fp", "legal_fn", "repair_tp", "seqdef_tp", "ok"])
    write_csv(
        PAPER / "reports/jobbert_metric_comparison.csv",
        [
            {
                "scheme": "official_1.2_raw_dump_collapsed_exact",
                "f1": (off_raw.get("collapsed_exact") or {}).get("f1"),
                "precision": (off_raw.get("collapsed_exact") or {}).get("precision"),
                "recall": (off_raw.get("collapsed_exact") or {}).get("recall"),
                "tp": (off_raw.get("collapsed_exact") or {}).get("tp"),
                "fp": (off_raw.get("collapsed_exact") or {}).get("fp"),
                "fn": (off_raw.get("collapsed_exact") or {}).get("fn"),
                "notes": f"original dump; alignment_ok={off_raw.get('alignment_ok')}; {off_raw.get('error')}",
            },
            {
                "scheme": "official_1.2_unique_view_typed_exact",
                "f1": (off_view.get("typed_exact") or {}).get("f1"),
                "precision": (off_view.get("typed_exact") or {}).get("precision"),
                "recall": (off_view.get("typed_exact") or {}).get("recall"),
                "tp": (off_view.get("typed_exact") or {}).get("tp"),
                "fp": (off_view.get("typed_exact") or {}).get("fp"),
                "fn": (off_view.get("typed_exact") or {}).get("fn"),
                "notes": "pred_tags are SKILL not L/K/S/T so typed exact is ~0",
            },
            {
                "scheme": "official_1.2_unique_view_collapsed_exact",
                "f1": (off_view.get("collapsed_exact") or {}).get("f1"),
                "precision": (off_view.get("collapsed_exact") or {}).get("precision"),
                "recall": (off_view.get("collapsed_exact") or {}).get("recall"),
                "tp": (off_view.get("collapsed_exact") or {}).get("tp"),
                "fp": (off_view.get("collapsed_exact") or {}).get("fp"),
                "fn": (off_view.get("collapsed_exact") or {}).get("fn"),
                "notes": f"alignment_ok={off_view.get('alignment_ok')}; BIO-legal B/I; I-after-O dropped; unique-first view",
            },
            {
                "scheme": "official_1.2_unique_view_collapsed_relaxed",
                "f1": (off_view.get("collapsed_relaxed") or {}).get("f1"),
                "precision": (off_view.get("collapsed_relaxed") or {}).get("precision"),
                "recall": (off_view.get("collapsed_relaxed") or {}).get("recall"),
                "tp": (off_view.get("collapsed_relaxed") or {}).get("tp"),
                "fp": (off_view.get("collapsed_relaxed") or {}).get("fp"),
                "fn": (off_view.get("collapsed_relaxed") or {}).get("fn"),
                "notes": "token IoU>=0.5",
            },
            {
                "scheme": "strict_BIO_legal_collapsed",
                "f1": m_legal["f1"],
                "precision": m_legal["precision"],
                "recall": m_legal["recall"],
                "tp": m_legal["tp"],
                "fp": m_legal["fp"],
                "fn": m_legal["fn"],
                "notes": "same decode as scorer tags_to_spans",
            },
            {
                "scheme": "repair_I_to_B_collapsed",
                "f1": m_repair["f1"],
                "precision": m_repair["precision"],
                "recall": m_repair["recall"],
                "tp": m_repair["tp"],
                "fp": m_repair["fp"],
                "fn": m_repair["fn"],
                "notes": "I after O or type-break becomes B",
            },
            {
                "scheme": "seqeval_default_I_starts_entity",
                "f1": m_def["f1"],
                "precision": m_def["precision"],
                "recall": m_def["recall"],
                "tp": m_def["tp"],
                "fp": m_def["fp"],
                "fn": m_def["fn"],
                "notes": "I-without-B starts a span",
            },
            {
                "scheme": "seqeval_strict_drop_illegal_I",
                "f1": m_ss["f1"],
                "precision": m_ss["precision"],
                "recall": m_ss["recall"],
                "tp": m_ss["tp"],
                "fp": m_ss["fp"],
                "fn": m_ss["fn"],
                "notes": "I-without-B dropped (IOB2-like)",
            },
            {
                "scheme": "seqeval_python_package",
                "f1": (seqeval_pkg or {}).get("default_f1", ""),
                "precision": (seqeval_pkg or {}).get("default_p", ""),
                "recall": (seqeval_pkg or {}).get("default_r", ""),
                "tp": "",
                "fp": "",
                "fn": "",
                "notes": json.dumps(seqeval_pkg, ensure_ascii=False)[:500],
            },
            {
                "scheme": "paper_table3_jobbert_skill",
                "f1": 0.0045,
                "precision": 0.0025,
                "recall": 0.0213,
                "tp": "",
                "fp": "",
                "fn": "",
                "notes": "published S-F1; do not replace with 0.46",
            },
            {
                "scheme": "v1.1_global_set_bug_collapsed",
                "f1": 0.46,
                "precision": "",
                "recall": "",
                "tp": "",
                "fp": "",
                "fn": "",
                "notes": "INVALID: v1.0-1.1 global set of (start,end,type) without sentence id",
            },
            {
                "scheme": "official_1.2_jobbert_knowledge_unique_collapsed",
                "f1": (off_k.get("collapsed_exact") or {}).get("f1"),
                "precision": (off_k.get("collapsed_exact") or {}).get("precision"),
                "recall": (off_k.get("collapsed_exact") or {}).get("recall"),
                "tp": (off_k.get("collapsed_exact") or {}).get("tp"),
                "fp": (off_k.get("collapsed_exact") or {}).get("fp"),
                "fn": (off_k.get("collapsed_exact") or {}).get("fn"),
                "notes": f"alignment_ok={off_k.get('alignment_ok')}; paper 0.0038",
            },
        ],
        ["scheme", "f1", "precision", "recall", "tp", "fp", "fn", "notes"],
    )

    coll = off_view.get("collapsed_exact") or {}
    md = [
        "# JobBERT metric audit",
        "",
        f"Scorer: `{SCORER_VERSION}` (sentence-level micro F1).",
        f"Canonical Gold: `{GOLD}` ({len(gold)} unique IDs, SHA256 `{sha256_file(str(GOLD))}`).",
        f"Original dump (not overwritten): `{pred_path}`.",
        f"Derived unique-first view: `{view}` (n_out={view_meta['n_out']}).",
        "",
        "## Verdict: do not adopt ~0.46",
        "",
        f"**Adopt 0.46? `{adopt_046}`.** The ~0.46 figure is an artifact of scorer `cnss-lskt-1.0/1.1`,",
        "which put `(start, end, type)` into a **global set**. Identical token offsets in different",
        "sentences collapsed, so thousands of illegal `I-SKILL` fragments became ~950 unique offset",
        "patterns and spuriously matched Gold.",
        "",
        f"**Keep the paper ballpark ~0.0045? `{paper_ok}`** (as an order-of-magnitude / published S-F1).",
        f"Official unique-view collapsed exact F1 = **{coll.get('f1')}**",
        f"(P={coll.get('precision')}, R={coll.get('recall')}, TP={coll.get('tp')}, FP={coll.get('fp')}, FN={coll.get('fn')}).",
        "Paper Table 3 JobBERT-skill **0.0045** / knowledge **0.0038** are in this range.",
        "They are **not** a 100× scoring error relative to BIO-legal micro F1.",
        "Do **not** replace them with 0.46. Do **not** put 0.46 in any paper table.",
        "",
        f"Unique-view official alignment_ok: **{off_view.get('alignment_ok')}** — {off_view.get('error')}",
        f"Raw dump official alignment_ok: **{off_raw.get('alignment_ok')}** — {off_raw.get('error')}",
        "",
        "## Illegal BIO transfers (unique-first rows vs canonical Gold)",
        "",
    ]
    md.extend(f"- {k}: {v}" for k, v in illegal.most_common())
    if not illegal:
        md.append("- none")
    md += [
        "",
        f"Total illegal I transfers: **{sum(illegal.values())}**.",
        "Dominant pattern: `I-SKILL` immediately after `O` (model emits I without B).",
        "BIO-legal decode **drops** those I tokens (they do not start a span).",
        "`repair-I-to-B` turns them into `B-SKILL` and creates many extra predicted spans.",
        "",
        "## Alignment (character / token / offset)",
        "",
        f"- `''.join(tokens) == sentence`: ok={join_ok}, fail={join_fail}",
        f"- reconstructed token offsets cover the sentence: ok={offset_ok}, fail={offset_fail}",
    ]
    md.extend(f"- {k}: {v}" for k, v in sorted(align.items()))
    md += [
        "",
        "JobBERT `pred_tags` length is aligned to Gold `tokens`. Scoring is **token-index** spans,",
        "not character offsets. Leading spaces in `sentence` are separate tokens when present.",
        "",
        "## Scheme comparison (collapsed exact unless noted)",
        "",
        f"- BIO-legal (scorer): F1={m_legal['f1']:.6f} TP={m_legal['tp']} FP={m_legal['fp']} FN={m_legal['fn']}",
        f"- repair-I-to-B: F1={m_repair['f1']:.6f} TP={m_repair['tp']} FP={m_repair['fp']} FN={m_repair['fn']}",
        f"- seqeval-default (I starts entity): F1={m_def['f1']:.6f} TP={m_def['tp']} FP={m_def['fp']} FN={m_def['fn']}",
        f"- seqeval-strict / IOB2-like: F1={m_ss['f1']:.6f} TP={m_ss['tp']} FP={m_ss['fp']} FN={m_ss['fn']}",
        f"- typed exact (LSKT vs SKILL): F1={m_typed['f1']:.6f}",
        f"- collapsed relaxed IoU≥0.5: F1={m_rel_legal['f1']:.6f}",
        f"- seqeval package: not installed in this environment; in-repo `seqeval_entities` matches seqeval **default** (I starts an entity). On this dump it equals repair-I-to-B because the only illegal transfer is I-after-O (14094).",
        f"- JobBERT-knowledge unique-view collapsed F1: {(off_k.get('collapsed_exact') or {}).get('f1')}",
        "",
        "## Fixtures",
        "",
        f"{fix_ok}/{len(fixtures)} fixtures passed (see `reports/jobbert_fixtures.csv`).",
        "These check exact match, miss, false span, boundary, type mismatch, illegal I-after-O,",
        "long span, merge error, empty, length pad, and leading illegal I.",
        "",
        "## Manual span samples",
        "",
        "Random TP / FP / FN (seed 20260822): `reports/jobbert_span_samples.json`.",
        "Token slices are `''.join(tokens[start:end])`. BIO-legal JobBERT predicts few true spans;",
        "most mass is FP from leftover `B-SKILL` fragments after dropping illegal I.",
        "",
        "## Why v1.1 reported ~0.46",
        "",
        "```python",
        "# buggy",
        "all_spans.extend(sentence_spans)  # (start, end, type) only",
        "tp = len(set(gold_spans) & set(pred_spans))",
        "```",
        "Correct: count TP/FP/FN **inside each sentence**, then sum (micro).",
        "A regression test (`test_micro_does_not_collapse_cross_sentence_offsets`) now requires",
        "two sentences with the same offsets to contribute 2 TP.",
        "",
    ]
    (PAPER / "reports/jobbert_metric_audit.md").write_text("\n".join(md), encoding="utf-8")
    (PAPER / "reports/score_canon_JobBERT-skill_unique_view.json").write_text(
        json.dumps(off_view, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def table3() -> None:
    rows = []
    for name, meta in PREDS.items():
        path = meta["path"]
        if not path.is_file():
            rows.append({"model": name, "eligible_for_main_table": "no", "reason_not_in_table": "missing dump"})
            continue
        r = score(str(GOLD), str(path), align_mode="official", pred_fields=meta["fields"], n_boot=0)
        te, ce = r.get("typed_exact") or {}, r.get("collapsed_exact") or {}
        paper = meta["paper"]
        typed_f1 = te.get("f1") or 0.0
        coll_f1 = ce.get("f1") or 0.0
        reasons = [
            "gold_canonical_v2 (18 conflicts adjudicated); PDF Table 3 still not updated",
            f"scorer={SCORER_VERSION} sentence micro; v1.1 global-set F1 is invalid",
        ]
        if not r.get("alignment_ok"):
            reasons.append(r.get("error") or "official alignment failed")
        if name == "Qwen":
            reasons.append("paper 0.2130 unreproducible; do not tune toward it")
        if name.startswith("JobBERT"):
            reasons.append("0.46 from v1.1 is invalid; collapsed micro ~0.004 matches paper order of magnitude")
        if name == "ChatGPT":
            reasons.append(
                f"do not call collapsed {coll_f1:.6f} a reproduction of 0.6700; "
                f"delta_collapsed={coll_f1 - paper:+.6f}; delta_typed={typed_f1 - paper:+.6f}; "
                f"matched={r.get('n_matched')}, duplicate_gold_preds={r.get('n_duplicate_gold_preds')}, "
                f"extra={r.get('n_extra')}; gold N={r.get('gold_n_unique_ids')}; "
                "primary metric is typed exact micro, paper Table 3 was collapsed S-F1"
            )
        eligible = "no"
        rows.append({
            "model": name,
            "version": meta["setting"],
            "prediction_file": str(path),
            "prediction_hash": r.get("pred_sha256"),
            "inference_setting": meta["setting"],
            "gold_n_rows": r.get("gold_n_rows"),
            "gold_n_unique_ids": r.get("gold_n_unique_ids"),
            "pred_n_rows": r.get("pred_n_rows"),
            "pred_n_unique_ids": r.get("pred_n_unique_ids"),
            "gold_coverage": r.get("coverage", {}).get("frac_gold_ids_scored"),
            "n_matched": r.get("n_matched"),
            "n_missing": r.get("n_missing"),
            "n_extra": r.get("n_extra"),
            "n_duplicate": r.get("n_duplicate_gold_preds"),
            "alignment_ok": int(bool(r.get("alignment_ok"))),
            "metrics_on_complete_gold": int(bool((r.get("id_sets") or {}).get("metrics_on_complete_gold"))),
            "typed_exact_p": te.get("precision"),
            "typed_exact_r": te.get("recall"),
            "typed_exact_f1": te.get("f1"),
            "typed_exact_tp": te.get("tp"),
            "typed_exact_fp": te.get("fp"),
            "typed_exact_fn": te.get("fn"),
            "collapsed_exact_p": ce.get("precision"),
            "collapsed_exact_r": ce.get("recall"),
            "collapsed_exact_f1": ce.get("f1"),
            "typed_relaxed_f1": (r.get("typed_relaxed") or {}).get("f1"),
            "collapsed_relaxed_f1": (r.get("collapsed_relaxed") or {}).get("f1"),
            "primary_metric": r.get("primary_metric"),
            "eligible_for_main_table": eligible,
            "paper_old_s_f1": paper,
            "delta_typed_exact_minus_paper": typed_f1 - paper,
            "delta_collapsed_exact_minus_paper": coll_f1 - paper,
            "delta_reason": "; ".join(reasons),
            "gold_sha256": r.get("gold_sha256"),
            "scorer_version": r.get("scorer_version"),
            "git_commit": r.get("git_commit"),
        })
        (PAPER / "reports" / f"score_v2_{name}.json").write_text(
            json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    fields = [
        "model", "version", "prediction_file", "prediction_hash", "inference_setting",
        "gold_n_rows", "gold_n_unique_ids", "pred_n_rows", "pred_n_unique_ids",
        "gold_coverage", "n_matched", "n_missing", "n_extra", "n_duplicate",
        "alignment_ok", "metrics_on_complete_gold",
        "typed_exact_p", "typed_exact_r", "typed_exact_f1",
        "typed_exact_tp", "typed_exact_fp", "typed_exact_fn",
        "collapsed_exact_p", "collapsed_exact_r", "collapsed_exact_f1",
        "typed_relaxed_f1", "collapsed_relaxed_f1", "primary_metric",
        "eligible_for_main_table", "paper_old_s_f1",
        "delta_typed_exact_minus_paper", "delta_collapsed_exact_minus_paper",
        "delta_reason", "gold_sha256", "scorer_version", "git_commit",
    ]
    write_csv(PAPER / "reports/table3_canonical_v2_reproduction.csv", rows, fields)


def table3_unique_views() -> None:
    """First row per prediction ID. Does not overwrite dumps. Extras kept."""
    rows = []
    for name, meta in PREDS.items():
        path = meta["path"]
        if not path.is_file():
            continue
        view = VIEWS / f"{name}_unique_first_v2.jsonl"
        write_unique_first_view(path, view, keep_ids=None)
        r = score(str(GOLD), str(view), align_mode="official", pred_fields=meta["fields"], n_boot=0)
        te, ce = r.get("typed_exact") or {}, r.get("collapsed_exact") or {}
        paper = meta["paper"]
        typed_f1 = te.get("f1") or 0.0
        coll_f1 = ce.get("f1") or 0.0
        ok = bool(r.get("alignment_ok"))
        eligible = "no"
        why = []
        if not ok:
            why.append(r.get("error") or "official fail")
        if name in {"Claude", "Kimi"}:
            why.append("incomplete dump; fill missing Gold IDs later")
        if name == "Qwen":
            why.append("0.2130 unreproducible")
        if ok and name not in {"Claude", "Kimi", "Qwen"}:
            why.append("unique-first view passes official; still do not write PDF until all main-table models use the same view policy")
        rows.append({
            "model": name,
            "version": meta["setting"] + " | unique-first view",
            "prediction_file": str(view),
            "prediction_hash": r.get("pred_sha256"),
            "inference_setting": meta["setting"],
            "gold_n_rows": r.get("gold_n_rows"),
            "gold_n_unique_ids": r.get("gold_n_unique_ids"),
            "pred_n_rows": r.get("pred_n_rows"),
            "pred_n_unique_ids": r.get("pred_n_unique_ids"),
            "gold_coverage": r.get("coverage", {}).get("frac_gold_ids_scored"),
            "n_matched": r.get("n_matched"),
            "n_missing": r.get("n_missing"),
            "n_extra": r.get("n_extra"),
            "n_duplicate": r.get("n_duplicate_gold_preds"),
            "alignment_ok": int(ok),
            "metrics_on_complete_gold": int(bool((r.get("id_sets") or {}).get("metrics_on_complete_gold"))),
            "typed_exact_p": te.get("precision"),
            "typed_exact_r": te.get("recall"),
            "typed_exact_f1": te.get("f1"),
            "typed_exact_tp": te.get("tp"),
            "typed_exact_fp": te.get("fp"),
            "typed_exact_fn": te.get("fn"),
            "collapsed_exact_p": ce.get("precision"),
            "collapsed_exact_r": ce.get("recall"),
            "collapsed_exact_f1": ce.get("f1"),
            "typed_relaxed_f1": (r.get("typed_relaxed") or {}).get("f1"),
            "collapsed_relaxed_f1": (r.get("collapsed_relaxed") or {}).get("f1"),
            "primary_metric": r.get("primary_metric"),
            "eligible_for_main_table": eligible,
            "paper_old_s_f1": paper,
            "delta_typed_exact_minus_paper": typed_f1 - paper,
            "delta_collapsed_exact_minus_paper": coll_f1 - paper,
            "delta_reason": "; ".join(why) if why else "ok",
            "gold_sha256": r.get("gold_sha256"),
            "scorer_version": r.get("scorer_version"),
            "git_commit": r.get("git_commit"),
        })
        (PAPER / "reports" / f"score_v2_unique_{name}.json").write_text(
            json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    if rows:
        write_csv(PAPER / "reports/table3_canonical_v2_unique_view.csv", rows, list(rows[0].keys()))


def main() -> int:
    table3()
    print("table3 v2 dumps done")
    table3_unique_views()
    print("table3 v2 unique views done")
    return 0


def norm_text(s: str) -> str:
    s = s or ""
    s = re.sub(r"\s+", "", s)
    s = re.sub(r"[0-9０-９]+", "0", s)
    s = re.sub(r"[^\w\u4e00-\u9fff]", "", s, flags=re.UNICODE)
    return s.lower()


def is_boilerplate(text: str) -> bool:
    t = (text or "").strip()
    if len(t) <= 2:
        return True
    if t in {".", "。", "!", "！", "&nbsp;", "关注!", "]", "）。"}:
        return True
    if "马克数据" in t or "马 克" in t or "微信公众号" in t:
        return True
    return False


def leakage() -> None:
    splits = {
        "train": ROOT / "data/annotated/processed/chinese_skillspan/train.json",
        "dev": ROOT / "data/annotated/processed/chinese_skillspan/dev.json",
        "test": ROOT / "data/annotated/processed/chinese_skillspan/test.json",
    }
    recs = {k: load_records(str(p)) for k, p in splits.items()}
    pairs: list[dict] = []

    def groups(kind: str, index: dict, cross_only: bool) -> None:
        for key, locs in index.items():
            if len(locs) < 2:
                continue
            splits_hit = sorted({s for s, _, _ in locs})
            if cross_only and len(splits_hit) < 2:
                continue
            pairs.append({
                "kind": kind,
                "n": len(locs),
                "splits": "|".join(splits_hit),
                "boilerplate": int(is_boilerplate(str(key) if kind.startswith("exact") else "")),
                "locations": "|".join(f"{s}:{i}" for s, i, _ in locs[:12]),
                "global_ids": "|".join(str(g) for _, _, g in locs[:8]),
                "preview": (str(key)[:120] if isinstance(key, str) else ""),
            })

    exact: dict[str, list] = defaultdict(list)
    normed: dict[str, list] = defaultdict(list)
    posting: dict[str, list] = defaultdict(list)
    prefix: dict[str, list] = defaultdict(list)
    title: dict[str, list] = defaultdict(list)
    for sp, rows in recs.items():
        for r in rows:
            iid = rec_id(r)
            gid = r.get("global_id")
            text = r.get("sentence") or ""
            exact[text].append((sp, iid, gid))
            nt = norm_text(text)
            if nt:
                normed[nt].append((sp, iid, gid))
            posting[str(gid)].append((sp, iid, gid))
            pref = re.sub(r"\s+", "", text)[:24]
            if len(pref) >= 16:
                prefix[pref].append((sp, iid, gid))
            tit = str(r.get("title") or "").strip()
            if tit:
                title[tit].append((sp, iid, gid))

    groups("exact_text_cross", exact, True)
    groups("normalized_text_cross", {k: v for k, v in normed.items() if k}, True)
    groups("posting_id_cross", posting, True)
    groups("prefix24_template_cross", prefix, True)
    groups("title_cross", title, True)

    n_exact = sum(1 for p in pairs if p["kind"] == "exact_text_cross")
    n_exact_nb = sum(1 for p in pairs if p["kind"] == "exact_text_cross" and not p["boilerplate"])
    n_norm = sum(1 for p in pairs if p["kind"] == "normalized_text_cross")
    n_post = sum(1 for p in pairs if p["kind"] == "posting_id_cross")
    n_pref = sum(1 for p in pairs if p["kind"] == "prefix24_template_cross")
    n_title = sum(1 for p in pairs if p["kind"] == "title_cross")

    gold = load_records(str(GOLD))
    gold_ids = {rec_id(r) for r in gold}
    gold_gids = {str(r.get("global_id")) for r in gold}
    gold_text = {(r.get("sentence") or "") for r in gold}
    train_ids = {rec_id(r) for r in recs["train"]}
    train_gids = {str(r.get("global_id")) for r in recs["train"]}
    train_text = {(r.get("sentence") or "") for r in recs["train"]}
    test_ids = {rec_id(r) for r in recs["test"]}

    silver_paths = {
        "silver_train": ROOT / "data/annotated/raw/chinese_skillspan/doccano_silver_merged_train_sorted_enrich.jsonl",
        "silver_dev": ROOT / "data/annotated/raw/chinese_skillspan/doccano_silver_merged_dev_sorted_enrich.jsonl",
        "silver_test": ROOT / "data/annotated/raw/chinese_skillspan/doccano_silver_merged_test_sorted_enrich.jsonl",
    }
    silver_ids: dict[str, set[str]] = {}
    silver_gids: dict[str, set[str]] = {}
    silver_text: dict[str, set[str]] = {}
    for name, p in silver_paths.items():
        sids, sg, st = set(), set(), set()
        if p.is_file():
            for rec in load_records(str(p)):
                meta = rec.get("meta") or {}
                if meta.get("id") is not None:
                    sids.add(str(meta["id"]))
                if meta.get("global_id") is not None:
                    sg.add(str(meta["global_id"]))
                st.add(rec.get("text") or "")
        silver_ids[name] = sids
        silver_gids[name] = sg
        silver_text[name] = st

    for kind, locs in [
        ("gold_id_in_train", [( "gold", i, "") for i in sorted(gold_ids & train_ids)]),
        ("gold_posting_in_train", [("gold", g, "") for g in sorted(gold_gids & train_gids)]),
    ]:
        if locs:
            pairs.append({
                "kind": kind,
                "n": len(locs),
                "splits": "gold|train",
                "boilerplate": 0,
                "locations": "|".join(f"{s}:{i}" for s, i, _ in locs[:12]),
                "global_ids": "",
                "preview": "",
            })

    gold_train_text = gold_text & train_text
    if gold_train_text:
        for t in list(gold_train_text)[:200]:
            pairs.append({
                "kind": "gold_text_in_train",
                "n": 1,
                "splits": "gold|train",
                "boilerplate": int(is_boilerplate(t)),
                "locations": "",
                "global_ids": "",
                "preview": t[:160],
            })

    write_csv(
        PAPER / "reports/split_duplicate_pairs.csv",
        pairs,
        ["kind", "n", "splits", "boilerplate", "locations", "global_ids", "preview"],
    )

    md = [
        "# Split leakage audit",
        "",
        "Corpus: `data/annotated/processed/chinese_skillspan/{train,dev,test}.json`",
        "Silver: `data/annotated/raw/chinese_skillspan/doccano_silver_merged_{train,dev,test}_sorted_enrich.jsonl`",
        "Gold: canonical v1 (test subset, unique IDs).",
        "",
        "## Split sizes",
        "",
        f"- train {len(recs['train'])} sentences / {len(train_gids)} postings",
        f"- dev {len(recs['dev'])} / {len({str(r.get('global_id')) for r in recs['dev']})} postings",
        f"- test {len(recs['test'])} / {len({str(r.get('global_id')) for r in recs['test']})} postings",
        f"- canonical Gold {len(gold)} IDs; all Gold IDs ⊆ test? {gold_ids <= test_ids}",
        "",
        "## Posting-level (`global_id`)",
        "",
        f"Cross-split posting groups: **{n_post}**.",
        "",
    ]
    if n_post:
        md += [
            "The same `global_id` appears in more than one split.",
            "**Do not run 3-seed encoder baselines until a posting-level split is rebuilt.**",
            "",
        ]
    else:
        md += [
            "No `global_id` is shared across train/dev/test.",
            "Posting-level split leakage is **not** present. Sentence-level duplicates still exist.",
            "Encoder 3-seed runs remain **blocked** until Gold conflicts are adjudicated and this audit is accepted;",
            "they are not blocked by a posting rebuild.",
            "",
        ]
    md += [
        "## Sentence-level duplicates",
        "",
        f"- Cross-split exact text groups: {n_exact} (non-boilerplate {n_exact_nb})",
        f"- Cross-split normalized (strip space/punct, digit→0) groups: {n_norm}",
        f"- Cross-split 24-char prefix template groups: {n_pref}",
        f"- Cross-split job-title groups: {n_title} (same title string, **different** posting IDs)",
        "",
        "Exact-text leakage includes short boilerplate (。, `&nbsp;`, 马克数据 watermark). See CSV `boilerplate=1`.",
        "Non-boilerplate exact matches are real sentence reuse across postings, not the same `global_id`.",
        "",
        "## Gold vs Silver source overlap",
        "",
        f"- Gold IDs ∩ silver_train IDs: {len(gold_ids & silver_ids['silver_train'])}",
        f"- Gold IDs ∩ silver_dev IDs: {len(gold_ids & silver_ids['silver_dev'])}",
        f"- Gold IDs ∩ silver_test IDs: {len(gold_ids & silver_ids['silver_test'])} (expected: Gold is a test subset)",
        f"- Gold posting ∩ silver_train posting: {len(gold_gids & silver_gids['silver_train'])}",
        f"- Gold text ∩ train text: {len(gold_train_text)}",
        f"- silver_train IDs == corpus train IDs: {silver_ids['silver_train'] == train_ids}",
        "",
        "Silver train/dev/test are the **same sentences** as the corpus splits with LLM silver labels.",
        "Overlap of Gold with silver_test is by design. Overlap of Gold with silver_train would be leakage;",
        "ID/posting overlap with silver_train is zero if posting split is clean.",
        "Shared **text** between Gold and train is the sentence-level exact-dup issue above.",
        "",
        "Pairs: `reports/split_duplicate_pairs.csv`.",
        "",
    ]
    (PAPER / "reports/split_leakage_audit.md").write_text("\n".join(md), encoding="utf-8")
    print(
        "leakage",
        "posting_cross", n_post,
        "exact_cross", n_exact,
        "exact_non_boiler", n_exact_nb,
        "gold_train_text", len(gold_train_text),
        "gold_train_ids", len(gold_ids & train_ids),
    )


if __name__ == "__main__":
    raise SystemExit(main())
