#!/usr/bin/env python3
"""LSKT v4 silver: shorter complete spans, keep L/K/S/T. No Gold v2 / train.json overwrite.

Starts from corpus silver BIO, applies goldstyle helpers with HARD_CAP=8 and
empty-sentence lock. Cursor rule silver, not human Gold.
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
sys.path.insert(0, str(PAPER / "scripts"))
import rewrite_train_goldstyle_v3 as g  # noqa: E402
from goldstyle_empty_rules import empty_hint  # noqa: E402

g.HARD_CAP = 8
g.MIN_LEN = 2

ROOT = PAPER.parent
TEST = ROOT / "data/annotated/processed/chinese_skillspan/test.json"
GOLD_V2 = PAPER / "data/gold_canonical_v2.jsonl"
OUT_TRAIN = PAPER / "data/train_lskt_v4_silver.jsonl"
OUT_DEV = PAPER / "data/dev_lskt_v4_silver.jsonl"
OUT_TEST = PAPER / "data/test_lskt_v4_silver.jsonl"
OUT_TEST_G2 = PAPER / "data/test_lskt_v4_silver_g2ids.jsonl"
OUT_META = PAPER / "reports/sandbox_lskt_v4_silver/silver_meta.json"


def rule_v4(rec: dict) -> list[tuple[int, int, str]]:
    sent = rec.get("sentence") or ""
    domain = rec.get("source_domain") or ""
    hint = empty_hint(sent, domain)
    if hint.startswith("empty_"):
        return []
    spans = g.rule_spans(rec)
    toks = g.tokens_of(rec)
    kept = []
    for a, b, t in spans:
        if (b - a) > g.HARD_CAP:
            b = a + g.HARD_CAP
            while b > a and toks[b - 1] in g.PUNCT_TOK:
                b -= 1
        text = "".join(toks[a:b])
        if g.should_drop_span(text, sent) or (b - a) < g.MIN_LEN:
            continue
        if any(not (b <= k[0] or a >= k[1]) for k in kept):
            continue
        kept.append((a, b, t if t in g.TYPES else "S"))
    return kept


def rewrite(rows: list[dict]) -> tuple[list[dict], dict]:
    out = []
    src = Counter()
    n_empty = n_span = n_forced_empty = 0
    lens = []
    types = Counter()
    for rec in rows:
        hint = empty_hint(rec.get("sentence") or "", rec.get("source_domain") or "")
        if hint.startswith("empty_"):
            spans = []
            source = hint
            n_forced_empty += 1
        else:
            spans = rule_v4(rec)
            source = "rule_v4"
        toks = g.tokens_of(rec)
        tags = g.spans_to_bio(len(toks), spans)
        if any(t != "O" for t in tags):
            n_span += 1
        else:
            n_empty += 1
        src[source] += 1
        for a, b, t in spans:
            lens.append(b - a)
            types[t] += 1
        out.append(
            {
                "id": rec.get("id"),
                "global_id": rec.get("global_id"),
                "sentence_order": rec.get("sentence_order"),
                "sentence": rec.get("sentence"),
                "tokens": toks,
                "source_domain": rec.get("source_domain"),
                "title": rec.get("title"),
                "list_of_selection_bio4": tags,
                "v4_spans": [[a, b, t] for a, b, t in spans],
                "v4_source": source,
            }
        )
    stats = {
        "n": len(out),
        "n_empty": n_empty,
        "n_with_span": n_span,
        "n_forced_empty": n_forced_empty,
        "source": dict(src),
        "type_counts": dict(types),
        "span_len": g.pcts(lens) if lens else {"n": 0},
    }
    return out, stats


def main() -> int:
    test = g.load_json(TEST)
    te, te_s = rewrite(test)
    g.write_jsonl(OUT_TEST, te)
    if OUT_TRAIN.is_file() and OUT_DEV.is_file():
        tr_s = {"skipped_existing": True, "path": str(OUT_TRAIN)}
        dv_s = {"skipped_existing": True, "path": str(OUT_DEV)}
        tr = []
    else:
        train = g.load_json(g.TRAIN)
        dev = g.load_json(g.DEV)
        tr, tr_s = rewrite(train)
        dv, dv_s = rewrite(dev)
        g.write_jsonl(OUT_TRAIN, tr)
        g.write_jsonl(OUT_DEV, dv)
    g2_ids = set()
    with GOLD_V2.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                g2_ids.add(str(json.loads(line)["id"]))
    te_g2 = [r for r in te if str(r.get("id")) in g2_ids]
    g.write_jsonl(OUT_TEST_G2, te_g2)
    meta = {
        "hard_cap_tokens": g.HARD_CAP,
        "gold_v2_untouched": True,
        "train_json_untouched": True,
        "label_scheme": "LSKT",
        "how": "rule_v4 on corpus silver BIO (empty lock + cap 8). Not human Gold. Not Codex dump.",
        "train": tr_s,
        "dev": dv_s,
        "test": te_s,
        "test_g2ids": {"n": len(te_g2), "n_gold_v2": len(g2_ids)},
        "train_path": str(OUT_TRAIN),
        "dev_path": str(OUT_DEV),
        "test_path": str(OUT_TEST),
        "test_g2ids_path": str(OUT_TEST_G2),
        "examples": g.example_spans(
            [{**r, "goldstyle_spans": r.get("v4_spans")} for r in (tr or te)[:80]],
            k=15,
        ),
    }
    OUT_META.parent.mkdir(parents=True, exist_ok=True)
    OUT_META.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"train": tr_s, "dev": dv_s, "out_train": str(OUT_TRAIN)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
