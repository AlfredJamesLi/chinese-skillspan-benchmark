#!/usr/bin/env python3
"""Merge train-300 Gold-style draft with locked 80. New file only."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from goldstyle_empty_rules import empty_hint
from project_gold_style_spans import find_span

ROOT = Path("/home/guojingli3/SCESC-LLM-skill-extraction")
PAPER = ROOT / "Chinese_skill_benchmark_Paper"
TRAIN = ROOT / "data/annotated/processed/chinese_skillspan/train.json"
PACK = PAPER / "reports/gold_style_relabel/train_human_80_300/pack.json"
W = PAPER / "reports/gold_style_relabel/train_human_80_300/work"
OUT = PAPER / "data/train_goldstyle_human380.jsonl"
OUT_JSON = PAPER / "reports/gold_style_relabel/train_human_80_300/human380.json"


def load_json(path: Path):
    raw = path.read_text(encoding="utf-8")
    if raw.lstrip().startswith("["):
        return json.loads(raw)
    return [json.loads(l) for l in raw.splitlines() if l.strip()]


def bio(tokens, aligned):
    tags = ["O"] * len(tokens)
    for s, e, typ in aligned:
        if 0 <= s < e <= len(tokens):
            tags[s] = f"B-{typ}"
            for i in range(s + 1, e):
                tags[i] = f"I-{typ}"
    return tags


def main() -> None:
    train = {r["id"]: r for r in load_json(TRAIN)}
    pack = load_json(PACK)
    draft = {}
    for p in (W / "train_part1_labels.json", W / "train_part2_labels.json"):
        if not p.is_file():
            raise FileNotFoundError(p)
        for rec in load_json(p):
            draft[rec["id"]] = rec
    rows = []
    n_lock = n_draft = n_empty_lock = n_miss = 0
    missing = []
    for rec in pack:
        iid = rec["id"]
        src = train[iid]
        toks = src.get("tokens") or []
        sent = src.get("sentence") or rec.get("sentence") or ""
        domain = src.get("source_domain") or rec.get("source_domain") or ""
        if rec["role"] == "lock80":
            spans = rec.get("spans") or []
            n_lock += 1
            source = "human80"
        else:
            d = draft.get(iid)
            if d is None:
                missing.append(iid)
                spans = []
                source = "missing"
            else:
                spans = d.get("spans") or []
                n_draft += 1
                source = "draft300"
        if empty_hint(sent, domain) in {"empty_process", "empty_welfare", "empty_shiye_process"}:
            spans = []
            n_empty_lock += 1
            source = source + "+empty_lock"
        aligned = []
        for sp in spans:
            text = (sp.get("text") if isinstance(sp, dict) else "") or ""
            typ = str((sp.get("type") if isinstance(sp, dict) else "S") or "S").upper()[:1]
            if typ not in {"L", "K", "S", "T"}:
                typ = "S"
            hit = find_span(toks, text)
            if hit is None:
                n_miss += 1
            else:
                aligned.append((hit[0], hit[1], typ, text))
        tags = bio(toks, [(a, b, t) for a, b, t, _ in aligned])
        out = dict(src)
        out["list_of_selection_bio4"] = tags
        out["_goldstyle"] = {
            "source": source,
            "spans_text": [{"text": tx, "type": t} for _, _, t, tx in aligned],
            "decision": rec.get("decision") or (draft.get(iid) or {}).get("decision") or "draft",
        }
        rows.append(out)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    meta = {
        "n": len(rows),
        "n_lock80": n_lock,
        "n_draft300": n_draft,
        "missing_draft_ids": missing,
        "empty_lock": n_empty_lock,
        "unaligned_spans": n_miss,
        "out": str(OUT),
        "overwrote_train": False,
        "touched_gold_v2": False,
        "note": "Draft human-style 380. Remaining train rows still use goldstyle v3. Not paper numbers.",
    }
    OUT_JSON.write_text(json.dumps({"meta": meta, "ids": [r["id"] for r in rows]}, ensure_ascii=False, indent=2), encoding="utf-8")
    (W / "merge_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(meta, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
