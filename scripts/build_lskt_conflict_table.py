#!/usr/bin/env python3
"""Build Codex vs Doubao vs Kimi test conflict table. Does not touch Gold v2.

Kimi is optional: if no dump yet, every row is kimi_pending.
"""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
PACK = PAPER / "reports/sandbox_lskt_v4_silver/codex_pack"
B52 = PACK / "batches_52"
CODEX = PAPER / "data/test_lskt_v4_silver_g2ids.jsonl"
DOUBAO = PAPER / "data/test_lskt_v4_doubao_g2ids.jsonl"
DOUBAO_RAW = PACK / "outputs_doubao/lskt_all_results.json"
KIMI_CANDIDATES = [
    PAPER / "data/test_lskt_v4_kimi_g2ids.jsonl",
    PACK / "outputs_kimi/lskt_all_results.json",
]
OUT_DIR = PACK / "conflict_v1"
SOURCE = "sandbox v4 · Codex 2601 + Doubao 2601 + Kimi k2.6 2601 · 2026-08-25"


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def load_json(path: Path):
    raw = path.read_text(encoding="utf-8")
    if raw.lstrip().startswith("["):
        return json.loads(raw)
    return load_jsonl(path)


def spans_of(rec: dict) -> list[tuple[int, int, str]]:
    out = []
    for item in rec.get("v4_spans") or rec.get("spans") or []:
        if isinstance(item, dict):
            if "start" in item:
                out.append((int(item["start"]), int(item["end"]), str(item.get("type") or "S")))
            else:
                continue
        else:
            a, b, t = item
            out.append((int(a), int(b), str(t)))
    return out


def fmt(spans: list[tuple[int, int, str]], toks: list[str] | None, rec: dict | None = None) -> str:
    parts = []
    for a, b, t in spans:
        if toks:
            text = "".join(toks[a:b])
        elif rec is not None:
            text = (rec.get("sentence") or "")[a:b] if False else ""
            # prefer stored text in compact spans
        else:
            text = ""
        if rec:
            for s in rec.get("spans") or []:
                if isinstance(s, dict) and s.get("start") == a and s.get("end") == b:
                    text = s.get("text") or text
        parts.append(f"{text}/{t}" if text else f"[{a}:{b}]/{t}")
    return " | ".join(parts) if parts else "[]"


def fmt_from_rec(rec: dict) -> str:
    toks = [str(t) for t in (rec.get("tokens") or [])]
    spans = spans_of(rec)
    if toks:
        return " | ".join(f"{''.join(toks[a:b])}/{t}" for a, b, t in spans) or "[]"
    parts = []
    for s in rec.get("spans") or []:
        if isinstance(s, dict) and "text" in s:
            parts.append(f"{s.get('text')}/{s.get('type')}")
    if parts:
        return " | ".join(parts)
    return " | ".join(f"[{a}:{b}]/{t}" for a, b, t in spans) or "[]"


def classify(c: list[tuple[int, int, str]], d: list[tuple[int, int, str]]) -> str:
    cs, ds = tuple(sorted(c)), tuple(sorted(d))
    if cs == ds:
        return "agree_empty" if not cs else "agree_spans"
    cb = tuple(sorted((a, b) for a, b, _ in c))
    db = tuple(sorted((a, b) for a, b, _ in d))
    if cb == db and cb:
        return "type_only"
    if (not c) != (not d):
        return "empty_mismatch"
    return "span_mismatch"


def find_kimi() -> tuple[dict[str, dict], str]:
    for p in KIMI_CANDIDATES:
        if p.is_file():
            rows = load_json(p)
            return {str(r["id"]): r for r in rows}, str(p)
    return {}, ""


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rule_rows = []
    for b in range(0, 52):
        rule_rows.extend(load_jsonl(B52 / f"batch_{b:02d}.jsonl"))
    rule = {str(r["id"]): r for r in rule_rows}
    codex = {str(r["id"]): r for r in load_jsonl(CODEX)}
    doubao = {str(r["id"]): r for r in load_jsonl(DOUBAO)}
    raw_db = {str(r["id"]): r for r in load_json(DOUBAO_RAW)}
    kimi_map, kimi_path = find_kimi()

    ids = [str(r["id"]) for r in load_jsonl(CODEX)]
    status_n = Counter()
    rows = []
    for rid in ids:
        cr, dr, rr = codex[rid], doubao[rid], rule[rid]
        csp, dsp = spans_of(cr), spans_of(dr)
        st = classify(csp, dsp)
        n_raw = len(raw_db.get(rid, {}).get("spans") or [])
        n_keep = len(dsp)
        n_drop = max(0, n_raw - n_keep)
        km = kimi_map.get(rid)
        kimi_status = "ready" if km is not None else "pending"
        ksp = spans_of(km) if km is not None else None
        rec = {
            "id": rid,
            "sentence": cr.get("sentence") or rr.get("sentence") or "",
            "domain": cr.get("source_domain") or rr.get("domain") or "",
            "status": st,
            "kimi_status": kimi_status,
            "human_priority": st not in {"agree_empty", "agree_spans"},
            "doubao_n_dropped": n_drop,
            "rule": fmt_from_rec(rr),
            "codex": fmt_from_rec(cr),
            "doubao": fmt_from_rec(dr),
            "kimi": fmt_from_rec(km) if km is not None else "",
            "n_codex": len(csp),
            "n_doubao": len(dsp),
        }
        if ksp is not None:
            ks, cs, ds = tuple(sorted(ksp)), tuple(sorted(csp)), tuple(sorted(dsp))
            if ks == cs:
                status_n["kimi_codex"] += 1
            if ks == ds:
                status_n["kimi_doubao"] += 1
            if ks == cs == ds:
                status_n["three_agree"] += 1
        rows.append(rec)
        status_n[st] += 1

    jsonl_path = OUT_DIR / "conflict_table.jsonl"
    csv_path = OUT_DIR / "conflict_table.csv"
    review_path = OUT_DIR / "human_review_priority.csv"
    with jsonl_path.open("w", encoding="utf-8") as f:
        for rec in rows:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    fields = ["id", "domain", "status", "kimi_status", "human_priority", "doubao_n_dropped", "codex", "doubao", "kimi", "rule", "sentence"]
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    pri = [r for r in rows if r["human_priority"]]
    with review_path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(pri)

    # samples per class for canvas (cap 25 each)
    samples: dict[str, list] = {}
    for rec in rows:
        bucket = samples.setdefault(rec["status"], [])
        if len(bucket) < 25:
            samples[rec["status"]].append(
                {
                    "id": rec["id"],
                    "domain": rec["domain"],
                    "sentence": (rec["sentence"] or "")[:160],
                    "codex": rec["codex"],
                    "doubao": rec["doubao"],
                    "dropped": rec["doubao_n_dropped"],
                }
            )

    summary = {
        "gold_v2_untouched": True,
        "n": len(rows),
        "kimi_n": len(kimi_map),
        "kimi_path": kimi_path or None,
        "status_counts": dict(status_n),
        "n_agree": status_n["agree_empty"] + status_n["agree_spans"],
        "n_disagree": len(pri),
        "n_doubao_any_drop": sum(1 for r in rows if r["doubao_n_dropped"] > 0),
        "source": SOURCE,
        "files": {
            "jsonl": str(jsonl_path),
            "csv": str(csv_path),
            "priority_csv": str(review_path),
        },
        "samples": samples,
    }
    (OUT_DIR / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    md = [
        "# LSKT v4 冲突表初版（sandbox）",
        "",
        "Gold v2 未改。Kimi 列为官方 `kimi-k2.6`（思考关闭）test 52 批。",
        "",
        f"- 句子: **{len(rows)}**（Gold v2 ID）",
        f"- Codex ↔ 豆包 一致: **{summary['n_agree']}**（空句一致 {status_n['agree_empty']}，有跨度一致 {status_n['agree_spans']}）",
        f"- 不一致（建议人工先看 Codex↔豆包）: **{summary['n_disagree']}**",
        f"  - 跨度边界不同: {status_n['span_mismatch']}",
        f"  - 一边空一边非空: {status_n['empty_mismatch']}",
        f"  - 边界相同类型不同: {status_n['type_only']}",
        f"- 三家跨度+类型完全一致: **{status_n['three_agree']}**",
        f"- Kimi↔Codex 一致: {status_n['kimi_codex']}；Kimi↔豆包 一致: {status_n['kimi_doubao']}",
        f"- 豆包有跨度对不上原文被丢掉: {summary['n_doubao_any_drop']} 句",
        f"- Kimi: {summary['kimi_n']}/2601",
        "",
        "全表: `conflict_table.csv`  |  人工优先: `human_review_priority.csv`",
        "不要写入 confirmed-results.md。不要用 test 冲突表训练。",
    ]
    (OUT_DIR / "README.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps({k: summary[k] for k in ("n", "kimi_n", "status_counts", "n_agree", "n_disagree", "n_doubao_any_drop")}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
