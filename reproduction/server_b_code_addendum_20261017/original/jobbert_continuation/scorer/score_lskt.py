#!/usr/bin/env python3
"""Unified LSKT span scorer (cnss-lskt-1.2.0).

Official: Gold IDs unique; each Gold ID needs exactly one prediction.
Predictions outside Gold are counted, not scored, and do not fail unless
--require-exact-id-set. Missing Gold IDs or duplicate Gold-ID predictions fail.
Legacy: last-wins, intersection only.

Micro F1 is summed over sentences. Do not put (start, end, type) into a
global set: identical offsets in different sentences are different spans.
v1.0–v1.1 used a global set and inflated F1 (JobBERT ~0.46 instead of ~0.0045).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCORER_VERSION = "cnss-lskt-1.2.0"
TYPES = ("L", "K", "S", "T")
PRED_FIELDS = (
    "pred_tags",
    "list_of_selection_bio4",
    "list_of_selection",
    "pred",
)
GOLD_FIELDS = ("list_of_selection_bio4", "list_of_selection", "tags_skill_clean", "gold")


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git_commit(repo: Path) -> str:
    try:
        out = subprocess.check_output(
            ["git", "-C", str(repo), "rev-parse", "HEAD"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        return out or "NO_GIT_HEAD"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "NO_GIT_HEAD"


def load_records(path: str) -> list[dict[str, Any]]:
    raw = Path(path).read_text(encoding="utf-8")
    if raw.lstrip().startswith("["):
        data = json.loads(raw)
        if not isinstance(data, list):
            raise ValueError(f"{path}: JSON root is not a list")
        return data
    rows = []
    for i, line in enumerate(raw.splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as e:
            raise ValueError(f"{path}:{i}: {e}") from e
    return rows


def rec_id(rec: dict[str, Any]) -> str:
    if rec.get("id") is None:
        raise ValueError("record missing id")
    return str(rec["id"]).strip()


def _norm_tag(t: Any) -> str:
    t = ("" if t is None else str(t)).strip()
    if not t:
        return "O"
    u = t.upper()
    if u in {"B", "I", "O"}:
        return u if u == "O" else f"{u}-SKILL"
    if u.startswith("B-") or u.startswith("I-") or u == "O":
        lab = u.split("-", 1)[1] if "-" in u else ""
        if u != "O" and lab in {"SKILL", "L", "K", "S", "T"}:
            return f"{u[0]}-{lab}"
        if u != "O" and lab:
            return f"{u[0]}-SKILL"
        return "O"
    return "O"


def pick_tags(rec: dict[str, Any], fields: tuple[str, ...]) -> list[str]:
    """First field with a B/I tag; else first non-empty list (may be all O).

    LLM dumps often store an all-O `list_of_selection_bio4` next to a filled
    untyped `list_of_selection`. Treating all-O as empty avoids blocking the
    actual prediction.
    """
    empty_fallback: list[str] | None = None
    for f in fields:
        v = rec.get(f)
        if not isinstance(v, list) or not v:
            continue
        tags = [_norm_tag(x) for x in v]
        if any(t != "O" for t in tags):
            return tags
        if empty_fallback is None:
            empty_fallback = tags
    return empty_fallback or []


def align_len(tags: list[str], n: int) -> list[str]:
    if n <= 0:
        return list(tags)
    if len(tags) < n:
        return tags + ["O"] * (n - len(tags))
    return tags[:n]


def seqeval_entities(tags: list[str]) -> list[tuple[int, int, str]]:
    """seqeval-style chunks: I-without-B starts an entity (matches old JobBERT 0.0045)."""
    chunks: list[tuple[int, int, str]] = []
    typ, start = None, None
    seq = list(tags) + ["O"]
    for i, tok in enumerate(seq):
        if tok == "O" or not tok:
            if typ is not None:
                chunks.append((start, i, typ))
                typ = None
            continue
        prefix, lab = (tok[0], tok[2:]) if tok.startswith(("B-", "I-")) else ("O", "")
        if prefix == "B" or typ is None or lab != typ:
            if typ is not None:
                chunks.append((start, i, typ))
            typ, start = lab or "SKILL", i
    return chunks


def tags_to_spans(tags: list[str]) -> list[tuple[int, int, str]]:
    spans: list[tuple[int, int, str]] = []
    i, n = 0, len(tags)
    while i < n:
        t = tags[i]
        if t.startswith("B-"):
            typ = t[2:]
            j = i + 1
            while j < n and tags[j] == f"I-{typ}":
                j += 1
            spans.append((i, j, typ))
            i = j
        else:
            i += 1
    return spans


def collapse(spans: list[tuple[int, int, str]]) -> list[tuple[int, int, str]]:
    return [(a, b, "SKILL") for a, b, _ in spans]


def iou_token(a: tuple[int, int, str], b: tuple[int, int, str]) -> float:
    if a[2] != b[2]:
        return 0.0
    inter = max(0, min(a[1], b[1]) - max(a[0], b[0]))
    union = max(a[1], b[1]) - min(a[0], b[0])
    return inter / union if union else 0.0


def prf(tp: int, pred_n: int, gold_n: int) -> dict[str, float]:
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


def match_exact(gs, ps):
    g, p = set(gs), set(ps)
    return prf(len(g & p), len(p), len(g))


def match_relaxed(gs, ps, thr: float = 0.5):
    used = set()
    tp = 0
    for g in gs:
        best_i, best = -1, 0.0
        for i, p in enumerate(ps):
            if i in used:
                continue
            v = iou_token(g, p)
            if v > best:
                best, best_i = v, i
        if best >= thr and best_i >= 0:
            tp += 1
            used.add(best_i)
    return prf(tp, len(ps), len(gs))


def per_type(gs, ps, fn):
    out = {}
    for typ in TYPES:
        out[typ] = fn([x for x in gs if x[2] == typ], [x for x in ps if x[2] == typ])
    return out


def _acc(dst: dict[str, int], m: dict) -> None:
    dst["tp"] += int(m["tp"])
    dst["pred"] += int(m["pred"])
    dst["gold"] += int(m["gold"])


def _from_acc(dst: dict[str, int]) -> dict[str, float]:
    return prf(dst["tp"], dst["pred"], dst["gold"])


def micro_over_sentences(pairs, fn) -> dict[str, float]:
    dst = {"tp": 0, "pred": 0, "gold": 0}
    for gs, ps in pairs:
        _acc(dst, fn(gs, ps))
    return _from_acc(dst)


def bootstrap_f1(pairs, mode: str, n_boot: int, seed: int) -> dict[str, float]:
    import random

    rng = random.Random(seed)
    if not pairs:
        return {"low": 0.0, "high": 0.0, "mean": 0.0}
    fn = match_relaxed if mode == "relaxed" else match_exact
    scores = []
    n = len(pairs)
    for _ in range(n_boot):
        sample = [pairs[rng.randrange(n)] for _ in range(n)]
        scores.append(micro_over_sentences(sample, fn)["f1"])
    scores.sort()
    lo = scores[int(0.025 * (n_boot - 1))]
    hi = scores[int(0.975 * (n_boot - 1))]
    return {"low": lo, "high": hi, "mean": sum(scores) / n_boot}


def index_by_id(rows: list[dict], policy: str) -> tuple[dict[str, dict], dict]:
    counts: Counter[str] = Counter()
    first: dict[str, dict] = {}
    last: dict[str, dict] = {}
    order: list[str] = []
    for rec in rows:
        i = rec_id(rec)
        counts[i] += 1
        last[i] = rec
        if i not in first:
            first[i] = rec
            order.append(i)
    chosen = last if policy == "last" else first
    info = {
        "n_rows": len(rows),
        "n_unique_ids": len(counts),
        "n_duplicate_ids": sum(1 for c in counts.values() if c > 1),
        "n_extra_rows": len(rows) - len(counts),
        "duplicate_ids": sorted(i for i, c in counts.items() if c > 1),
        "id_order": order,
    }
    return chosen, info


def sentence_n(rec: dict) -> int:
    toks = rec.get("tokens")
    if isinstance(toks, list) and toks:
        return len(toks)
    return 0


def extract_spans(rec: dict, fields: tuple[str, ...]) -> list[tuple[int, int, str]]:
    n = sentence_n(rec)
    tags = align_len(pick_tags(rec, fields), n or len(pick_tags(rec, fields)))
    return tags_to_spans(tags)


def align_sets(gold_ids: set[str], pred_ids: set[str]) -> dict:
    return {
        "missing_in_pred": sorted(gold_ids - pred_ids),
        "extra_in_pred": sorted(pred_ids - gold_ids),
        "n_gold": len(gold_ids),
        "n_pred": len(pred_ids),
        "n_intersection": len(gold_ids & pred_ids),
    }


def score(
    gold_path: str,
    pred_path: str,
    *,
    align_mode: str = "official",
    pred_fields: tuple[str, ...] = PRED_FIELDS,
    gold_fields: tuple[str, ...] = GOLD_FIELDS,
    relaxed_thr: float = 0.5,
    n_boot: int = 1000,
    boot_seed: int = 20260822,
    require_exact_id_set: bool = False,
    repo: Path | None = None,
) -> dict[str, Any]:
    gold_rows = load_records(gold_path)
    pred_rows = load_records(pred_path)
    gold_counts = Counter(rec_id(r) for r in gold_rows)
    pred_counts = Counter(rec_id(r) for r in pred_rows)
    g_policy = "last" if align_mode == "legacy" else "first"
    gold_map, gold_info = index_by_id(gold_rows, g_policy)
    pred_map, pred_info = index_by_id(pred_rows, g_policy)
    gold_ids = set(gold_map)
    pred_ids = set(pred_map)

    missing = sorted(i for i in gold_ids if pred_counts.get(i, 0) == 0)
    dup_gold_preds = sorted(i for i in gold_ids if pred_counts.get(i, 0) > 1)
    extra = sorted(i for i in pred_ids if i not in gold_ids)
    matched = sorted(i for i in gold_info["id_order"] if pred_counts.get(i, 0) == 1)

    errors = []
    if align_mode == "official":
        if gold_info["n_duplicate_ids"]:
            errors.append(f"gold IDs not unique ({gold_info['n_duplicate_ids']} duplicated)")
        if missing:
            errors.append(f"missing {len(missing)} gold IDs in predictions")
        if dup_gold_preds:
            errors.append(f"duplicate predictions for {len(dup_gold_preds)} gold IDs")
        if require_exact_id_set and extra:
            errors.append(f"--require-exact-id-set: {len(extra)} extra pred IDs")

    alignment_ok = not errors if align_mode == "official" else True
    if align_mode == "legacy":
        ids = sorted(gold_ids & pred_ids)
    else:
        ids = matched if not alignment_ok else gold_info["id_order"]

    typed_pairs = []
    coll_pairs = []
    n_pred_nonempty = 0
    n_gold_nonempty = 0
    typed_acc = {"tp": 0, "pred": 0, "gold": 0}
    coll_acc = {"tp": 0, "pred": 0, "gold": 0}
    typed_r_acc = {"tp": 0, "pred": 0, "gold": 0}
    coll_r_acc = {"tp": 0, "pred": 0, "gold": 0}
    per_exact_acc = {t: {"tp": 0, "pred": 0, "gold": 0} for t in TYPES}
    per_relax_acc = {t: {"tp": 0, "pred": 0, "gold": 0} for t in TYPES}
    for i in ids:
        gsp = extract_spans(gold_map[i], gold_fields)
        psp = extract_spans(pred_map[i], pred_fields)
        if gsp:
            n_gold_nonempty += 1
        if psp:
            n_pred_nonempty += 1
        typed_pairs.append((gsp, psp))
        coll_pairs.append((collapse(gsp), collapse(psp)))
        _acc(typed_acc, match_exact(gsp, psp))
        _acc(coll_acc, match_exact(collapse(gsp), collapse(psp)))
        _acc(typed_r_acc, match_relaxed(gsp, psp, relaxed_thr))
        _acc(coll_r_acc, match_relaxed(collapse(gsp), collapse(psp), relaxed_thr))
        for typ in TYPES:
            gt = [x for x in gsp if x[2] == typ]
            pt = [x for x in psp if x[2] == typ]
            _acc(per_exact_acc[typ], match_exact(gt, pt))
            _acc(per_relax_acc[typ], match_relaxed(gt, pt, relaxed_thr))

    typed_exact = _from_acc(typed_acc)
    coll_exact = _from_acc(coll_acc)
    typed_relax = _from_acc(typed_r_acc)
    coll_relax = _from_acc(coll_r_acc)
    per_exact = {t: _from_acc(per_exact_acc[t]) for t in TYPES}
    per_relax = {t: _from_acc(per_relax_acc[t]) for t in TYPES}
    n = len(ids)
    n_gold = len(gold_ids)
    report = {
        "scorer_version": SCORER_VERSION,
        "align_mode": align_mode,
        "alignment_ok": alignment_ok,
        "eligible_for_main_table": bool(alignment_ok and align_mode == "official"),
        "error": "; ".join(errors) if errors else None,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": git_commit(repo or Path(__file__).resolve().parents[2]),
        "gold_path": os.path.abspath(gold_path),
        "pred_path": os.path.abspath(pred_path),
        "gold_sha256": sha256_file(gold_path),
        "pred_sha256": sha256_file(pred_path),
        "config": {
            "gold_id_policy": g_policy,
            "pred_fields": list(pred_fields),
            "gold_fields": list(gold_fields),
            "relaxed_iou": relaxed_thr,
            "bootstrap_n": n_boot,
            "bootstrap_seed": boot_seed,
            "require_exact_id_set": require_exact_id_set,
            "metrics_aggregation": "micro_over_sentences",
            "pred_field_policy": "first_field_with_entity_else_first_nonempty",
        },
        "gold_n_rows": gold_info["n_rows"],
        "gold_n_unique_ids": gold_info["n_unique_ids"],
        "pred_n_rows": pred_info["n_rows"],
        "pred_n_unique_ids": pred_info["n_unique_ids"],
        "n_matched": len(matched),
        "n_missing": len(missing),
        "n_extra": len(extra),
        "n_duplicate_gold_preds": len(dup_gold_preds),
        "gold": gold_info,
        "pred": pred_info,
        "id_sets": {
            "n_missing_in_pred": len(missing),
            "n_extra_in_pred": len(extra),
            "n_duplicate_gold_preds": len(dup_gold_preds),
            "n_matched_exactly_one": len(matched),
            "n_gold": n_gold,
            "n_pred_unique": pred_info["n_unique_ids"],
            "n_scored": n,
            "metrics_on_complete_gold": alignment_ok if align_mode == "official" else False,
        },
        "coverage": {
            "gold_ids_scored": n,
            "frac_gold_ids_scored": n / n_gold if n_gold else 0.0,
            "frac_gold_sents_with_span": n_gold_nonempty / n if n else 0.0,
            "frac_pred_sents_with_span": n_pred_nonempty / n if n else 0.0,
        },
        "primary_metric": "typed_exact_micro_f1",
        "typed_exact": typed_exact,
        "collapsed_exact": coll_exact,
        "typed_relaxed": typed_relax,
        "collapsed_relaxed": coll_relax,
        "per_type_exact": per_exact,
        "per_type_relaxed": per_relax,
        "bootstrap_95ci": {
            "typed_exact_f1": bootstrap_f1(typed_pairs, "exact", n_boot, boot_seed) if n_boot > 0 else None,
            "collapsed_exact_f1": bootstrap_f1(coll_pairs, "exact", n_boot, boot_seed + 1) if n_boot > 0 else None,
        },
    }
    return report


def write_report(report: dict, out: str | None) -> None:
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if out:
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        Path(out).write_text(text, encoding="utf-8")
    else:
        print(text)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Unified Chinese-SkillSpan LSKT scorer")
    ap.add_argument("--gold", required=True)
    ap.add_argument("--pred", required=True)
    ap.add_argument("--align-mode", choices=("official", "legacy"), default="official")
    ap.add_argument("--require-exact-id-set", action="store_true")
    ap.add_argument("--pred-field", action="append", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--n-boot", type=int, default=1000)
    args = ap.parse_args(argv)
    pred_fields = tuple(args.pred_field) if args.pred_field else PRED_FIELDS
    report = score(
        args.gold,
        args.pred,
        align_mode=args.align_mode,
        pred_fields=pred_fields,
        n_boot=args.n_boot,
        require_exact_id_set=args.require_exact_id_set,
    )
    write_report(report, args.out)
    if args.align_mode == "official" and not report.get("alignment_ok"):
        print(report.get("error"), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
