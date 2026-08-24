#!/usr/bin/env python3
"""Build a 1M-sentence JobBERTa-zh mid-rung MLM corpus from the two JD totals.

Mix follows corpus train (应届生 59% / 人工智能 41%), not Gold/test
(those contain 事业单位 / 阿里云, which are absent here).
Drops exact train/dev/test/Gold sentences. Does not overwrite train.json or Gold v2.
"""
from __future__ import annotations

import argparse
import csv
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
ROOT = PAPER.parent
PRE = PAPER / "chineseskillspan-jobert-pretrain"
AI_CSV = PRE / "人工智能招聘大数据2014-2025.3" / "人工智能招聘大数据.csv"
YJ_CSV = PRE / "应届生招聘大数据（2014-2025.6）" / "应届生招聘大数据（2014-2025.6）.csv"
TEST = ROOT / "data/annotated/processed/chinese_skillspan/test.json"
TRAIN = ROOT / "data/annotated/processed/chinese_skillspan/train.json"
DEV = ROOT / "data/annotated/processed/chinese_skillspan/dev.json"
GOLD = PAPER / "data/gold_canonical_v2.jsonl"

SENT_SPLIT = re.compile(r"[。！？；;\n]+|(?:\d+[\.、．])|<br\s*/?>", re.I)
HTML = re.compile(r"<[^>]+>|&nbsp;|&amp;|&lt;|&gt;")

csv.field_size_limit(min(sys.maxsize, 16 * 1024 * 1024))


def load_json_rows(path: Path) -> list[dict]:
    raw = path.read_text(encoding="utf-8")
    if raw.lstrip().startswith("["):
        return json.loads(raw)
    return [json.loads(l) for l in raw.splitlines() if l.strip()]


def load_block() -> set[str]:
    blocked: set[str] = set()
    for path in (TRAIN, DEV, TEST):
        if path.is_file():
            blocked.update((r.get("sentence") or "").strip() for r in load_json_rows(path))
    if GOLD.is_file():
        for line in GOLD.read_text(encoding="utf-8").splitlines():
            if line.strip():
                blocked.add((json.loads(line).get("sentence") or "").strip())
    blocked.discard("")
    return blocked


def split_sents(text: str) -> list[str]:
    t = HTML.sub("", text or "")
    out = []
    for x in SENT_SPLIT.split(t):
        s = re.sub(r"\s+", "", x).strip(" ，,、:：")
        if 6 <= len(s) <= 200:
            out.append(s)
    return out


def stream_sents(path: Path, cap: int, blocked: set[str], seen: set[str], source: str) -> list[dict]:
    got: list[dict] = []
    n_rows = 0
    n_empty_jd = 0
    years: Counter[str] = Counter()
    if not path.is_file():
        raise FileNotFoundError(path)
    with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if not header:
            return got
        try:
            i_jd = header.index("职位描述")
        except ValueError:
            i_jd = 6
        i_year = header.index("招聘发布年份") if "招聘发布年份" in header else -1
        for row in reader:
            n_rows += 1
            if not row:
                continue
            head = row[0] if row else ""
            if head.startswith("更多数据") or "macrodatas" in "".join(row[:2]):
                continue
            jd = row[i_jd] if i_jd < len(row) else ""
            if not jd.strip():
                n_empty_jd += 1
                continue
            year = ""
            if i_year >= 0 and i_year < len(row):
                year = str(row[i_year]).strip()[:4]
            for s in split_sents(jd):
                if s in blocked or s in seen:
                    continue
                seen.add(s)
                got.append({"text": s, "source": source, "year": year})
                years[year or "unk"] += 1
                if len(got) >= cap:
                    stream_sents.last_stats = {
                        "rows_scanned": n_rows,
                        "empty_jd": n_empty_jd,
                        "hit_cap": True,
                        "years": dict(years),
                    }
                    return got
    stream_sents.last_stats = {
        "rows_scanned": n_rows,
        "empty_jd": n_empty_jd,
        "hit_cap": False,
        "years": dict(years),
    }
    return got


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=1_000_000)
    ap.add_argument("--yj_frac", type=float, default=0.5906, help="应届生 share; default = corpus train")
    ap.add_argument("--seed", type=int, default=20260823)
    ap.add_argument("--out", type=Path, default=PAPER / "data/jobbert_1m_sents.jsonl")
    args = ap.parse_args()
    n_yj = int(round(args.n * args.yj_frac))
    n_ai = args.n - n_yj
    blocked = load_block()
    seen: set[str] = set()
    print(json.dumps({"phase": "start", "n": args.n, "n_yj": n_yj, "n_ai": n_ai, "blocked": len(blocked)}, ensure_ascii=False), flush=True)

    ai = stream_sents(AI_CSV, n_ai, blocked, seen, "人工智能招聘")
    ai_stats = getattr(stream_sents, "last_stats", {"rows_scanned": "cap_hit"})
    print(json.dumps({"phase": "ai_done", "n": len(ai), "stats": ai_stats, "file_bytes": AI_CSV.stat().st_size}, ensure_ascii=False), flush=True)

    yj = stream_sents(YJ_CSV, n_yj + max(0, n_ai - len(ai)), blocked, seen, "应届生招聘")
    yj_stats = getattr(stream_sents, "last_stats", {"rows_scanned": "cap_hit"})
    print(json.dumps({"phase": "yj_done", "n": len(yj), "stats": yj_stats, "file_bytes": YJ_CSV.stat().st_size}, ensure_ascii=False), flush=True)

    picked = ai + yj
    rng = random.Random(args.seed)
    rng.shuffle(picked)
    picked = picked[: args.n]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as f:
        for rec in picked:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    src = Counter(r["source"] for r in picked)
    meta = {
        "out": str(args.out),
        "n": len(picked),
        "target_n": args.n,
        "mix_policy": "corpus_train_59_41",
        "target": {"应届生招聘": n_yj, "人工智能招聘": n_ai},
        "actual": dict(src),
        "actual_frac": {k: round(v / len(picked), 4) for k, v in src.items()} if picked else {},
        "blocked_train_dev_test_gold": len(blocked),
        "files": {
            "人工智能": {"path": str(AI_CSV), "bytes": AI_CSV.stat().st_size, "scan": ai_stats, "kept": len(ai)},
            "应届生": {"path": str(YJ_CSV), "bytes": YJ_CSV.stat().st_size, "scan": yj_stats, "kept": len(yj)},
        },
        "align_gold": False,
        "align_note": (
            "Gold/test are 人工智能+阿里云+事业单位 (no 应届生). "
            "These two CSVs cannot match Gold. Mid-rung follows train 59:41. "
            "事业单位/阿里云 DAPT is a later corpus-construction step."
        ),
        "overwrote_train": False,
        "touched_gold_v2": False,
    }
    (args.out.with_suffix(".meta.json")).write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(meta, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
