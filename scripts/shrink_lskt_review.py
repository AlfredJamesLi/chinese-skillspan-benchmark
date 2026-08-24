#!/usr/bin/env python3
"""Shrink LSKT v4 human review using 3-way overlap. Does not touch Gold v2."""
from __future__ import annotations

import csv
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
PACK = PAPER / "reports/sandbox_lskt_v4_silver/codex_pack"
OUT = PACK / "conflict_v1"
SEED = 42
FIELDS = [
    "id",
    "domain",
    "review_bucket",
    "status",
    "codex",
    "doubao",
    "kimi",
    "sentence",
]


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def spans_of(rec: dict) -> tuple[tuple[int, int, str], ...]:
    out = []
    for item in rec.get("v4_spans") or rec.get("spans") or []:
        if isinstance(item, dict):
            if "start" in item:
                out.append((int(item["start"]), int(item["end"]), str(item.get("type") or "S")))
        else:
            a, b, t = item
            out.append((int(a), int(b), str(t)))
    return tuple(sorted(out))


def fmt(rec: dict) -> str:
    toks = [str(t) for t in (rec.get("tokens") or [])]
    spans = spans_of(rec)
    if toks:
        return " | ".join(f"{''.join(toks[a:b])}/{t}" for a, b, t in spans) or "[]"
    return "[]"


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def main() -> int:
    codex = {str(r["id"]): r for r in load_jsonl(PAPER / "data/test_lskt_v4_silver_g2ids.jsonl")}
    doubao = {str(r["id"]): r for r in load_jsonl(PAPER / "data/test_lskt_v4_doubao_g2ids.jsonl")}
    kimi = {str(r["id"]): r for r in load_jsonl(PAPER / "data/test_lskt_v4_kimi_g2ids.jsonl")}
    conflict = load_jsonl(OUT / "conflict_table.jsonl")
    by: dict[str, list[dict]] = defaultdict(list)
    for rec in conflict:
        rid = rec["id"]
        c, d, k = spans_of(codex[rid]), spans_of(doubao[rid]), spans_of(kimi[rid])
        if c == d == k:
            bucket = "three_agree"
        elif c != d and k == c:
            bucket = "kimi_backs_codex"
        elif c != d and k == d:
            bucket = "kimi_backs_doubao"
        elif c != d:
            bucket = "must_human_split"
        elif k != c:
            bucket = "pair_agree_kimi_diff"
        else:
            bucket = "other"
        row = {
            "id": rid,
            "domain": rec.get("domain") or "",
            "review_bucket": bucket,
            "status": rec.get("status") or "",
            "codex": fmt(codex[rid]),
            "doubao": fmt(doubao[rid]),
            "kimi": fmt(kimi[rid]),
            "sentence": rec.get("sentence") or "",
        }
        by[bucket].append(row)

    rng = random.Random(SEED)
    sample: list[dict] = []
    plan = [
        ("must_human_split", 50),
        ("kimi_backs_codex", 15),
        ("kimi_backs_doubao", 15),
        ("pair_agree_kimi_diff", 20),
    ]
    for bucket, n in plan:
        pool = list(by[bucket])
        rng.shuffle(pool)
        sample.extend(pool[:n])

    files = {
        "auto_accept_three_agree.csv": by["three_agree"],
        "kimi_suggest_codex.csv": by["kimi_backs_codex"],
        "kimi_suggest_doubao.csv": by["kimi_backs_doubao"],
        "human_must_review.csv": by["must_human_split"],
        "pair_agree_kimi_diff.csv": by["pair_agree_kimi_diff"],
        "sample100_kimi_vs_codex.csv": sample,
    }
    for name, rows in files.items():
        write_csv(OUT / name, rows)

    summary = {
        "gold_v2_untouched": True,
        "seed": SEED,
        "n": 2601,
        "buckets": {k: len(v) for k, v in by.items()},
        "must_human_status": dict(Counter(r["status"] for r in by["must_human_split"])),
        "sample_n": len(sample),
        "sample_bucket": dict(Counter(r["review_bucket"] for r in sample)),
        "sample_status": dict(Counter(r["status"] for r in sample)),
        "note": "939 three-way identical labels are agreement, not majority vote. 520 Kimi-tiebreak rows are suggestions only.",
    }
    (OUT / "review_queue_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "sample100_kimi_vs_codex.jsonl").write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in sample),
        encoding="utf-8",
    )
    md = [
        "# LSKT v4 人工范围缩小（sandbox）",
        "",
        "Gold v2 未改。Kimi 是 `kimi-k2.6`，不是多数决 Gold。",
        "",
        "| 队列 | 句数 | 用法 |",
        "|---|---:|---|",
        f"| 三家完全一致 | **{len(by['three_agree'])}** | 批量接受 |",
        f"| Codex≠豆包，Kimi=豆包 | {len(by['kimi_backs_doubao'])} | 建议跟豆包，有空再抽查 |",
        f"| Codex≠豆包，Kimi=Codex | {len(by['kimi_backs_codex'])} | 建议跟 Codex，有空再抽查 |",
        f"| Codex=豆包，Kimi不同 | {len(by['pair_agree_kimi_diff'])} | 次优先：两家已同，看 Kimi 是否多标/少标 |",
        f"| **三家各不相同** | **{len(by['must_human_split'])}** | **现在人工主队列** |",
        "",
        f"原先 Codex↔豆包 1500 句。用 Kimi 站边后，主队列从 1500 收到 **{len(by['must_human_split'])}**。",
        f"抽查 100 句（seed={SEED}）：三家分裂 50 + 站边各 15 + 两家同Kimi异 20。",
        "",
        "- 主队列: `human_must_review.csv`",
        "- 100 句对照: `sample100_kimi_vs_codex.csv`",
        "- 批量接受: `auto_accept_three_agree.csv`",
        "",
        "不要写入 confirmed-results.md。不要用这些 test 句训练。",
        "",
    ]
    (OUT / "REVIEW_QUEUE.md").write_text("\n".join(md), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
