#!/usr/bin/env python3
"""Simulate SOP-v4 human labels on the 980 must-human test sentences.

Does not overwrite Gold v2, train.json, Codex test silver, or train/dev v4.
Does not add the 980 IDs to the CRF train set (test leakage).

Simulated labels = rule_v4 (same SOP the CRF was trained on). Rescue only when
rule_v4 is empty on a non-welfare sentence and ≥2 LLMs agree on a SOP-valid span.
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
sys.path.insert(0, str(PAPER / "scripts"))
sys.path.insert(0, str(PAPER / "scorer"))

import rewrite_train_goldstyle_v3 as g  # noqa: E402
import rewrite_train_lskt_v4 as v4  # noqa: E402
from goldstyle_empty_rules import empty_hint  # noqa: E402
from score_lskt import score  # noqa: E402

G2 = PAPER / "data/gold_canonical_v2.jsonl"
CODEX = PAPER / "data/test_lskt_v4_silver_g2ids.jsonl"
DOUBAO = PAPER / "data/test_lskt_v4_doubao_g2ids.jsonl"
KIMI = PAPER / "data/test_lskt_v4_kimi_g2ids.jsonl"
CSV980 = PAPER / "reports/sandbox_lskt_v4_silver/codex_pack/conflict_v1/human_must_review.csv"
PRED = PAPER / "output/jobbert_zh_1m/crf_lskt_v4_silver_seed42/test_pred.jsonl"
OUT_DIR = PAPER / "reports/sandbox_lskt_v4_silver/simhuman980"
OUT_980 = PAPER / "data/test_lskt_v4_simhuman980.jsonl"
OUT_PATCH = PAPER / "data/test_lskt_v4_simhuman_patched_g2ids.jsonl"
OUT_RULE = PAPER / "data/test_lskt_v4_rule_g2ids.jsonl"

LEAD = ("熟悉", "掌握", "了解", "精通", "具备", "具有")


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def load_json_any(path: Path) -> list[dict]:
    raw = path.read_text(encoding="utf-8")
    if raw.lstrip().startswith("["):
        return json.loads(raw)
    return load_jsonl(path)


def by_id(rows: list[dict]) -> dict[str, dict]:
    return {str(r["id"]): r for r in rows}


def spans_of(rec: dict) -> list[tuple[int, int, str]]:
    out = []
    for item in rec.get("v4_spans") or []:
        if isinstance(item, dict):
            out.append((int(item["start"]), int(item["end"]), str(item.get("type") or "S")))
        else:
            a, b, t = item
            out.append((int(a), int(b), str(t)))
    if out:
        return out
    tags = rec.get("list_of_selection_bio4") or []
    return g.bio_spans(tags)


def fmt_spans(toks: list[str], spans: list[tuple[int, int, str]]) -> str:
    if not spans:
        return "[]"
    return " | ".join(f"{''.join(toks[a:b])}/{t}" for a, b, t in spans)


def map_spans(src_toks: list[str], spans: list[tuple[int, int, str]], dst_toks: list[str]) -> list[tuple[int, int, str]]:
    if src_toks == dst_toks:
        return list(spans)
    mapped = []
    for a, b, t in spans:
        text = "".join(src_toks[a:b])
        loc = g.find_span(dst_toks, text)
        if loc is None:
            continue
        mapped.append((loc[0], loc[1], t))
    return mapped


def sop_span(toks: list[str], a: int, b: int, typ: str, sent: str) -> tuple[int, int, str] | None:
    n = len(toks)
    a = max(0, a)
    b = min(n, b)
    while a < b and toks[a] in g.PUNCT_TOK:
        a += 1
    while b > a and toks[b - 1] in g.PUNCT_TOK:
        b -= 1
    text = "".join(toks[a:b])
    for lead in LEAD:
        if text.startswith(lead) and len(text) > len(lead) + 1:
            loc = g.find_span(toks[a:b], text[len(lead) :])
            if loc is not None:
                a, b = a + loc[0], a + loc[1]
                text = "".join(toks[a:b])
            break
    if (b - a) > g.HARD_CAP:
        b = a + g.HARD_CAP
        while b > a and toks[b - 1] in g.PUNCT_TOK:
            b -= 1
        text = "".join(toks[a:b])
    if (b - a) < g.MIN_LEN or g.should_drop_span(text, sent):
        return None
    typ = typ if typ in g.TYPES else g.assign_type(text, "S")
    return (a, b, typ)


def greedy(spans: list[tuple[int, int, str]]) -> list[tuple[int, int, str]]:
    spans = sorted(spans, key=lambda x: (x[0], -(x[1] - x[0])))
    kept = []
    for sp in spans:
        if any(not (sp[1] <= k[0] or sp[0] >= k[1]) for k in kept):
            continue
        kept.append(sp)
    return kept


def llm_valid(rec: dict, toks: list[str], sent: str) -> list[tuple[int, int, str]]:
    out = []
    for a, b, t in spans_of(rec):
        clean = sop_span(toks, a, b, t, sent)
        if clean:
            out.append(clean)
    return out


def agreed_spans(cands: list[list[tuple[int, int, str]]]) -> list[tuple[int, int, str]]:
    votes: Counter[tuple[int, int]] = Counter()
    types: dict[tuple[int, int], Counter[str]] = {}
    for spans in cands:
        seen = set()
        for a, b, t in spans:
            key = (a, b)
            if key in seen:
                continue
            seen.add(key)
            votes[key] += 1
            types.setdefault(key, Counter())[t] += 1
    out = []
    for key, n in votes.items():
        if n >= 2:
            typ = types[key].most_common(1)[0][0]
            out.append((key[0], key[1], typ))
    return greedy(out)


def pack(template: dict, spans: list[tuple[int, int, str]], source: str) -> dict:
    toks = g.tokens_of(template)
    rec = dict(template)
    rec["v4_spans"] = [[a, b, t] for a, b, t in spans]
    rec["list_of_selection_bio4"] = g.spans_to_bio(len(toks), spans)
    rec["v4_source"] = source
    rec.pop("comment", None)
    return rec


def simulate_one(corpus: dict | None, tmpl: dict, doubao: dict | None, kimi: dict | None) -> tuple[list[tuple[int, int, str]], str]:
    sent = tmpl.get("sentence") or ""
    domain = tmpl.get("source_domain") or ""
    toks = g.tokens_of(tmpl)
    hint = empty_hint(sent, domain)
    if hint.startswith("empty_"):
        return [], hint
    src = corpus or tmpl
    src_toks = g.tokens_of(src)
    rule = map_spans(src_toks, v4.rule_v4(src), toks)
    rule = [s for s in (sop_span(toks, a, b, t, sent) for a, b, t in rule) if s]
    rule = greedy(rule)
    if rule:
        return rule, "rule_v4"
    c_ok = llm_valid(tmpl, toks, sent)
    d_ok = llm_valid(doubao, toks, sent) if doubao else []
    k_ok = llm_valid(kimi, toks, sent) if kimi else []
    agreed = agreed_spans([c_ok, d_ok, k_ok])
    if agreed:
        return agreed, "rescue_llm_agree2"
    return [], "rule_empty"


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def one_score(name: str, gold: Path) -> dict:
    r = score(str(gold), str(PRED), align_mode="official", n_boot=0)
    te, ce = r["typed_exact"], r["collapsed_exact"]
    return {
        "name": name,
        "gold": str(gold),
        "alignment_ok": r.get("alignment_ok"),
        "n_gold": r.get("gold_n_unique_ids"),
        "n_missing": r.get("n_missing"),
        "typed_p": te["precision"],
        "typed_r": te["recall"],
        "typed_f1": te["f1"],
        "collapsed_f1": ce["f1"],
        "error": r.get("error"),
    }


def main() -> int:
    ids980 = [row["id"] for row in csv.DictReader(CSV980.open(encoding="utf-8-sig"))]
    idset = set(ids980)
    if len(ids980) != 980:
        raise SystemExit(f"expected 980 ids, got {len(ids980)}")

    corpus_all = by_id(load_json_any(v4.TEST))
    g2_ids = {str(json.loads(l)["id"]) for l in G2.read_text(encoding="utf-8").splitlines() if l.strip()}
    codex_rows = load_jsonl(CODEX)
    codex = by_id(codex_rows)
    doubao = by_id(load_jsonl(DOUBAO))
    kimi = by_id(load_jsonl(KIMI))

    rule_g2 = []
    for rec in codex_rows:
        rid = str(rec["id"])
        src = corpus_all.get(rid, rec)
        spans = map_spans(g.tokens_of(src), v4.rule_v4(src), g.tokens_of(rec))
        spans = greedy(
            [s for s in (sop_span(g.tokens_of(rec), a, b, t, rec.get("sentence") or "") for a, b, t in spans) if s]
        )
        hint = empty_hint(rec.get("sentence") or "", rec.get("source_domain") or "")
        src_name = hint if hint.startswith("empty_") else "rule_v4"
        if hint.startswith("empty_"):
            spans = []
        rule_g2.append(pack(rec, spans, src_name))
    write_jsonl(OUT_RULE, rule_g2)

    rows980 = []
    src_count = Counter()
    n_empty = 0
    for rid in ids980:
        tmpl = codex[rid]
        spans, source = simulate_one(corpus_all.get(rid), tmpl, doubao.get(rid), kimi.get(rid))
        rec = pack(tmpl, spans, f"simhuman_{source}")
        rec["review_bucket"] = "must_human_split"
        rows980.append(rec)
        src_count[source] += 1
        if not spans:
            n_empty += 1
    write_jsonl(OUT_980, rows980)

    patched = []
    for rec in codex_rows:
        rid = str(rec["id"])
        if rid in idset:
            sim = by_id(rows980)[rid]
            patched.append(pack(rec, [(a, b, t) for a, b, t in sim["v4_spans"]], sim["v4_source"]))
        else:
            keep = dict(rec)
            keep["v4_source"] = rec.get("v4_source") or "codex_kept"
            patched.append(keep)
    write_jsonl(OUT_PATCH, patched)

    examples = []
    for rec, raw in zip(rows980[:20], csv.DictReader(CSV980.open(encoding="utf-8-sig"))):
        toks = rec["tokens"]
        examples.append(
            {
                "id": rec["id"],
                "source": rec["v4_source"],
                "sentence": rec["sentence"],
                "simhuman": fmt_spans(toks, [(a, b, t) for a, b, t in rec["v4_spans"]]),
                "codex": raw["codex"],
                "doubao": raw["doubao"],
                "kimi": raw["kimi"],
            }
        )

    scores = []
    if PRED.is_file():
        scores = [
            one_score("Gold v2 (frozen official)", G2),
            one_score("Codex test silver (current g2ids)", CODEX),
            one_score("rule_v4 recomputed on 2601", OUT_RULE),
            one_score("patched 2601 (980 simhuman, rest Codex)", OUT_PATCH),
            one_score("simhuman 980 only", OUT_980),
        ]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    summary = {
        "gold_v2_untouched": True,
        "codex_test_untouched": True,
        "train_untouched": True,
        "n_980": len(rows980),
        "n_empty_980": n_empty,
        "source_980": dict(src_count),
        "note": "Simulated SOP labels, not human Gold. 980 are test IDs; not used for CRF train.",
        "paths": {
            "simhuman980": str(OUT_980),
            "patched2601": str(OUT_PATCH),
            "rule2601": str(OUT_RULE),
        },
        "scores": scores,
        "examples20": examples,
    }
    (OUT_DIR / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    md = [
        "# Simulated SOP-v4 labels on 980 (sandbox)",
        "",
        "Gold v2 / Codex test / train.json / train_lskt_v4 未改。不是人工 Gold，不进论文。",
        "",
        "模拟规则：先 empty-lock，再 **rule_v4**（CRF 训练 SOP：2–8 token、完整词、熟悉/掌握只标对象）。",
        "仅当规则把技能句放空、且至少两家 LLM 跨度 SOP 合法且一致时，才 rescue。",
        "980 是 Gold v2 测试 ID，**没有**并进 CRF 训练集。现有 `crf_lskt_v4_silver_seed42` 预测直接重打分。",
        "",
        f"- 980 空句: **{n_empty}**",
        f"- 来源: `{dict(src_count)}`",
        "",
        "| Gold | typed P/R/F1 | collapsed | align |",
        "|---|---|---:|---|",
    ]
    for s in scores:
        prf = f"{s['typed_p']:.4f}/{s['typed_r']:.4f}/{s['typed_f1']:.4f}"
        md.append(f"| {s['name']} | {prf} | {s['collapsed_f1']:.4f} | {s['alignment_ok']} |")
    md += ["", "前 20 条见 `summary.json` → examples20。", ""]
    (OUT_DIR / "SIMHUMAN980.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps({k: summary[k] for k in ("n_980", "n_empty_980", "source_980", "scores")}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
