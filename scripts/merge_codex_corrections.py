#!/usr/bin/env python3
"""Merge Codex span corrections into LSKT v4 silver JSONL. Does not touch Gold v2."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
TYPES = {"L", "K", "S", "T"}


def load_json(path: Path):
    raw = path.read_text(encoding="utf-8")
    if raw.lstrip().startswith("["):
        data = json.loads(raw)
        if not isinstance(data, list):
            raise ValueError(f"{path}: JSON root is not a list")
        return data
    rows = []
    for line in raw.splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for rec in rows:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def spans_to_bio(n: int, spans: list[tuple[int, int, str]]) -> list[str]:
    tags = ["O"] * n
    for a, b, t in sorted(spans, key=lambda x: (x[0], x[1])):
        t = t if t in TYPES else "S"
        a, b = max(0, a), min(n, b)
        if a >= b:
            continue
        tags[a] = f"B-{t}"
        for i in range(a + 1, b):
            tags[i] = f"I-{t}"
    return tags


def locate_all(tokens: list[str], text: str) -> list[tuple[int, int]]:
    needle = (text or "").strip()
    if not needle:
        return []
    flat = "".join(tokens)
    out = []
    start_char = 0
    while True:
        pos = flat.find(needle, start_char)
        if pos < 0:
            break
        acc = 0
        tok_start = None
        for i, tok in enumerate(tokens):
            nxt = acc + len(tok)
            if tok_start is None and acc <= pos < nxt:
                tok_start = i
            if tok_start is not None and nxt >= pos + len(needle):
                out.append((tok_start, i + 1))
                break
            acc = nxt
        start_char = pos + 1
    return out


def align_record(tokens: list[str], sentence: str, items: list[dict]) -> tuple[list[tuple[int, int, str]], list[str]]:
    errs: list[str] = []
    kept: list[tuple[int, int, str]] = []
    for item in items:
        text = str(item.get("text") or "").strip()
        typ = str(item.get("type") or "").strip()
        if typ not in TYPES:
            errs.append(f"bad_type:{typ}:{text}")
            continue
        if text not in (sentence or ""):
            errs.append(f"not_in_sentence:{text}")
            continue
        cands = locate_all(tokens, text)
        if not cands:
            errs.append(f"not_in_tokens:{text}")
            continue
        picked = None
        for a, b in cands:
            if any(not (b <= k[0] or a >= k[1]) for k in kept):
                continue
            picked = (a, b, typ)
            break
        if picked is None:
            errs.append(f"overlap:{text}")
            continue
        kept.append(picked)
    kept.sort(key=lambda x: (x[0], x[1]))
    return kept, errs


def compact_of(rec: dict) -> dict:
    toks = rec.get("tokens") or []
    spans = []
    for a, b, t in rec.get("v4_spans") or []:
        if isinstance(a, list):
            a, b, t = a
        spans.append({"start": a, "end": b, "type": t, "text": "".join(toks[a:b])})
    return {
        "id": rec.get("id"),
        "sentence": rec.get("sentence") or "",
        "domain": rec.get("source_domain") or rec.get("domain") or "",
        "spans": spans,
        "v4_source": rec.get("v4_source"),
    }


def patch_file(path: Path, aligned: dict[str, list[tuple[int, int, str]]], source: str) -> dict:
    if not path.is_file():
        return {"path": str(path), "skipped": True}
    rows = load_json(path)
    n_hit = 0
    out = []
    for rec in rows:
        rid = str(rec.get("id"))
        if rid not in aligned:
            out.append(rec)
            continue
        toks = [str(t) for t in (rec.get("tokens") or list(rec.get("sentence") or ""))]
        spans = aligned[rid]
        rec = dict(rec)
        rec["tokens"] = toks
        rec["v4_spans"] = [[a, b, t] for a, b, t in spans]
        rec["list_of_selection_bio4"] = spans_to_bio(len(toks), spans)
        rec["v4_source"] = source
        out.append(rec)
        n_hit += 1
    write_jsonl(path, out)
    return {"path": str(path), "n_rows": len(out), "n_patched": n_hit}


def patch_compact(path: Path, patched_full: list[dict]) -> dict:
    by_id = {str(r["id"]): compact_of(r) for r in patched_full}
    rows = load_json(path)
    n_hit = 0
    out = []
    for rec in rows:
        rid = str(rec.get("id"))
        if rid in by_id:
            out.append(by_id[rid])
            n_hit += 1
        else:
            out.append(rec)
    write_jsonl(path, out)
    return {"path": str(path), "n_rows": len(out), "n_patched": n_hit}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--corrections",
        default=str(PAPER / "reports/sandbox_lskt_v4_silver/sample_50_corrected.json"),
    )
    ap.add_argument(
        "--sample",
        default=str(PAPER / "reports/sandbox_lskt_v4_silver/codex_pack/sample_50.jsonl"),
    )
    ap.add_argument("--source", default="codex_sample50")
    args = ap.parse_args()

    corr_path = Path(args.corrections)
    sample_path = Path(args.sample)
    corrections = load_json(corr_path)
    sample = {str(r["id"]): r for r in load_json(sample_path)}
    corr_ids = [str(r["id"]) for r in corrections]
    sample_ids = list(sample)
    report: dict = {
        "gold_v2_untouched": True,
        "corrections": str(corr_path),
        "n_corrections": len(corrections),
        "n_sample": len(sample),
        "id_match": corr_ids == sample_ids,
        "missing_ids": sorted(set(sample_ids) - set(corr_ids)),
        "extra_ids": sorted(set(corr_ids) - set(sample_ids)),
        "align_errors": [],
        "n_empty": 0,
        "n_changed": 0,
        "type_counts": {},
        "span_len": Counter(),
        "n_over_cap8": 0,
        "patched": [],
    }
    if corr_ids != sample_ids:
        print(json.dumps({k: report[k] for k in ("id_match", "missing_ids", "extra_ids")}, ensure_ascii=False, indent=2))
        return 2

    types: Counter[str] = Counter()
    aligned: dict[str, list[tuple[int, int, str]]] = {}
    test_full = {str(r["id"]): r for r in load_json(PAPER / "data/test_lskt_v4_silver.jsonl")}
    for rec in corrections:
        rid = str(rec["id"])
        base = test_full.get(rid) or sample[rid]
        toks = [str(t) for t in (base.get("tokens") or list(base.get("sentence") or ""))]
        sent = base.get("sentence") or sample[rid].get("sentence") or ""
        spans, errs = align_record(toks, sent, rec.get("spans") or [])
        if errs:
            report["align_errors"].append({"id": rid, "errs": errs})
        aligned[rid] = spans
        old = sample[rid].get("spans") or []
        new_txt = [(a, b, t) for a, b, t in spans]
        old_txt = [(s["start"], s["end"], s["type"]) for s in old]
        if new_txt != old_txt:
            report["n_changed"] += 1
        if not spans:
            report["n_empty"] += 1
        for a, b, t in spans:
            types[t] += 1
            ln = b - a
            report["span_len"][str(ln)] += 1
            if ln > 8:
                report["n_over_cap8"] += 1
    report["type_counts"] = dict(types)
    report["span_len"] = dict(report["span_len"])

    report["patched"].append(
        patch_file(PAPER / "data/test_lskt_v4_silver.jsonl", aligned, args.source)
    )
    report["patched"].append(
        patch_file(PAPER / "data/test_lskt_v4_silver_g2ids.jsonl", aligned, args.source)
    )
    patched_rows = [r for r in load_json(PAPER / "data/test_lskt_v4_silver.jsonl") if str(r["id"]) in aligned]
    for name in ("test_compact.jsonl", "test_g2ids_compact.jsonl"):
        report["patched"].append(patch_compact(PAPER / "reports/sandbox_lskt_v4_silver/codex_pack" / name, patched_rows))
    chunk0 = PAPER / "reports/sandbox_lskt_v4_silver/codex_pack/chunks_test_g2ids/test_g2ids_part_00.jsonl"
    if chunk0.is_file():
        report["patched"].append(patch_compact(chunk0, patched_rows))

    out_json = PAPER / "reports/sandbox_lskt_v4_silver/codex_pack/MERGE_sample50.json"
    out_md = PAPER / "reports/sandbox_lskt_v4_silver/codex_pack/MERGE_sample50.md"
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# Codex sample_50 merge (sandbox)",
        "",
        "Gold v2 untouched. Train/dev silver untouched. No retrain.",
        "",
        f"- corrections: `{corr_path}`",
        f"- ids: {report['n_corrections']} matched sample_50",
        f"- sentences changed vs rule_v4: {report['n_changed']}",
        f"- empty after Codex: {report['n_empty']}",
        f"- align errors: {len(report['align_errors'])}",
        f"- spans longer than 8 tokens (kept, not recapped): {report['n_over_cap8']}",
        f"- type counts: {report['type_counts']}",
        "",
        "Next: remaining 27 chunks. Do not copy into confirmed-results.md.",
    ]
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("id_match", "n_changed", "n_empty", "align_errors", "n_over_cap8", "type_counts", "patched")}, ensure_ascii=False, indent=2))
    return 0 if not report["align_errors"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
