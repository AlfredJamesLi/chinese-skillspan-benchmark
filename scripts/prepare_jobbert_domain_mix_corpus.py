#!/usr/bin/env python3
"""Build JobBERT-zh domain-mix MLM corpus (no listed companies).

Target mix (remainder filled from 人工智能 then 应届生):
  人工智能 35% / 应届生 25% / 阿里云 22% / 事业单位 14%

Aliyun: only_yun_wei 工作描述, sentence split, exact train/dev/test/Gold blocklist.
事业单位: all-result-0925-6k cleaned_text; drop whole announcements that contain
Gold/test/train/dev 事业单位 sentences as substrings; drop exam-process boiler;
prefer skill-bearing sentences; exact sentence blocklist.
Do not MLM the LLM 软/硬技能 columns.

Example:
  python prepare_jobbert_domain_mix_corpus.py --n 1000000 \\
    --out data/jobbert_domain_mix_1m_sents.jsonl
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
ALI_XLSX = PRE / "aliyun_天池公开数据集" / "only_yun_wei-预处理-James-0928.xlsx"
SY_XLSX = PRE / "0930-事业单位-LLM-软硬技能-提取-结果汇总编码文档-James.xlsx"
TEST = ROOT / "data/annotated/processed/chinese_skillspan/test.json"
TRAIN = ROOT / "data/annotated/processed/chinese_skillspan/train.json"
DEV = ROOT / "data/annotated/processed/chinese_skillspan/dev.json"
GOLD = PAPER / "data/gold_canonical_v2.jsonl"

SENT_SPLIT = re.compile(r"[。！？；;\n]+|(?:\d+[\.、．])|<br\s*/?>", re.I)
HTML = re.compile(r"<[^>]+>|&nbsp;|&amp;|&lt;|&gt;")
BOILER = re.compile(
    r"(网上报名|资格审查|准考证|缴费|咨询电话|笔试时间|面试时间|"
    r"招聘公告|体检|公示|工作日|报名条件|报名办法|考试安排)"
)
SKILL = re.compile(
    r"(任职|岗位职责|专业|学历|技能|熟练|掌握|具备|能力|资格|证书|"
    r"本科|研究生|工程师|计算机|软件|要求)"
)

csv.field_size_limit(min(sys.maxsize, 16 * 1024 * 1024))


def load_json_rows(path: Path) -> list[dict]:
    raw = path.read_text(encoding="utf-8")
    if raw.lstrip().startswith("["):
        return json.loads(raw)
    return [json.loads(line) for line in raw.splitlines() if line.strip()]


def domain_of(row: dict) -> str:
    return str(row.get("source_domain") or row.get("domain") or "")


def norm_sent(s: str) -> str:
    return re.sub(r"\s+", "", str(s or "")).strip(" ，,、:：")


def load_block() -> tuple[set[str], set[str]]:
    """Exact sentences to drop, plus 事业单位 needles for document-level drop."""
    blocked: set[str] = set()
    sy_needles: set[str] = set()
    for path in (TRAIN, DEV, TEST):
        if not path.is_file():
            continue
        for row in load_json_rows(path):
            s = (row.get("sentence") or "").strip()
            if s:
                blocked.add(s)
                ns = norm_sent(s)
                if ns:
                    blocked.add(ns)
                if "事业单位" in domain_of(row) and len(ns) >= 12:
                    sy_needles.add(ns)
    if GOLD.is_file():
        for line in GOLD.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            s = (row.get("sentence") or "").strip()
            if not s:
                continue
            blocked.add(s)
            ns = norm_sent(s)
            if ns:
                blocked.add(ns)
            if "事业单位" in domain_of(row) and len(ns) >= 12:
                sy_needles.add(ns)
    blocked.discard("")
    sy_needles.discard("")
    return blocked, sy_needles


def split_sents(text: str, lo: int = 6, hi: int = 200) -> list[str]:
    t = HTML.sub("", text or "")
    out = []
    for x in SENT_SPLIT.split(t):
        s = re.sub(r"\s+", "", x).strip(" ，,、:：")
        if lo <= len(s) <= hi:
            out.append(s)
    return out


def is_footer_row(row: list[str]) -> bool:
    if not row:
        return True
    head = row[0] or ""
    return head.startswith("更多数据") or "macrodatas" in "".join(row[:2])


def stream_flat_csv(
    path: Path,
    cap: int,
    blocked: set[str],
    seen: set[str],
    source: str,
) -> tuple[list[dict], dict]:
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
            return got, {"rows_scanned": 0}
        i_jd = header.index("职位描述") if "职位描述" in header else 6
        i_year = header.index("招聘发布年份") if "招聘发布年份" in header else -1
        for row in reader:
            n_rows += 1
            if is_footer_row(row):
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
                    return got, {
                        "rows_scanned": n_rows,
                        "empty_jd": n_empty_jd,
                        "hit_cap": True,
                        "years": dict(years),
                    }
    return got, {
        "rows_scanned": n_rows,
        "empty_jd": n_empty_jd,
        "hit_cap": False,
        "years": dict(years),
    }


def doc_has_needle(text: str, needles: set[str]) -> bool:
    nt = norm_sent(text)
    if not nt:
        return False
    return any(n and n in nt for n in needles)


def sent_leaks(s: str, needles: set[str]) -> bool:
    return any(n and n in s for n in needles)


def collect_aliyun(blocked: set[str], seen: set[str], cap: int, rng: random.Random) -> tuple[list[dict], dict]:
    import pandas as pd

    if not ALI_XLSX.is_file():
        raise FileNotFoundError(ALI_XLSX)
    df = pd.read_excel(ALI_XLSX, sheet_name="only_yun_wei", engine="openpyxl", usecols=["工作描述"])
    pool: list[dict] = []
    n_raw = 0
    n_block = 0
    n_dup = 0
    for t in df["工作描述"].fillna("").astype(str):
        for s in split_sents(t):
            n_raw += 1
            if s in blocked:
                n_block += 1
                continue
            if s in seen:
                n_dup += 1
                continue
            seen.add(s)
            pool.append({"text": s, "source": "阿里云公开数据集", "year": ""})
    rng.shuffle(pool)
    kept = pool[:cap]
    stats = {
        "rows": int(len(df)),
        "path": str(ALI_XLSX),
        "raw_sents": n_raw,
        "blocked_exact": n_block,
        "dup": n_dup,
        "unique_pool": len(pool),
        "kept": len(kept),
        "hit_cap": len(pool) >= cap,
    }
    return kept, stats


def collect_shiye(
    blocked: set[str],
    sy_needles: set[str],
    seen: set[str],
    cap: int,
    rng: random.Random,
) -> tuple[list[dict], dict]:
    import pandas as pd

    if not SY_XLSX.is_file():
        raise FileNotFoundError(SY_XLSX)
    df = pd.read_excel(
        SY_XLSX,
        sheet_name="all-result-0925-6k",
        engine="openpyxl",
        usecols=["cleaned_text"],
    )
    n_docs = len(df)
    n_drop_doc = 0
    n_raw = 0
    n_block = 0
    n_leak = 0
    n_boiler = 0
    n_dup = 0
    skillish: list[dict] = []
    other: list[dict] = []
    for t in df["cleaned_text"].fillna("").astype(str):
        if doc_has_needle(t, sy_needles):
            n_drop_doc += 1
            continue
        for s in split_sents(t):
            n_raw += 1
            if s in blocked:
                n_block += 1
                continue
            if sent_leaks(s, sy_needles):
                n_leak += 1
                continue
            if BOILER.search(s):
                n_boiler += 1
                continue
            if s in seen:
                n_dup += 1
                continue
            seen.add(s)
            rec = {"text": s, "source": "事业单位招聘", "year": ""}
            if SKILL.search(s):
                skillish.append(rec)
            else:
                other.append(rec)
    rng.shuffle(skillish)
    rng.shuffle(other)
    pool = skillish + other
    kept = pool[:cap]
    stats = {
        "rows": n_docs,
        "path": str(SY_XLSX),
        "sheet": "all-result-0925-6k",
        "docs_dropped_gold_overlap": n_drop_doc,
        "docs_kept": n_docs - n_drop_doc,
        "raw_sents_from_kept_docs": n_raw,
        "blocked_exact": n_block,
        "blocked_sy_span": n_leak,
        "dropped_boiler": n_boiler,
        "dup": n_dup,
        "skillish_pool": len(skillish),
        "other_nonskill_pool": len(other),
        "unique_pool": len(pool),
        "kept": len(kept),
        "kept_skillish": sum(1 for r in kept if SKILL.search(r["text"])),
        "hit_cap": len(pool) >= cap,
    }
    return kept, stats


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=1_000_000)
    ap.add_argument("--ai_frac", type=float, default=0.35)
    ap.add_argument("--yj_frac", type=float, default=0.25)
    ap.add_argument("--ali_frac", type=float, default=0.22)
    ap.add_argument("--sy_frac", type=float, default=0.14)
    ap.add_argument("--seed", type=int, default=20260824)
    ap.add_argument("--out", type=Path, default=PAPER / "data/jobbert_domain_mix_1m_sents.jsonl")
    args = ap.parse_args()
    total_frac = args.ai_frac + args.yj_frac + args.ali_frac + args.sy_frac
    if total_frac > 1.0 + 1e-6:
        raise SystemExit(f"fractions must sum to <= 1, got {total_frac}")

    n_ai = int(round(args.n * args.ai_frac))
    n_yj = int(round(args.n * args.yj_frac))
    n_ali = int(round(args.n * args.ali_frac))
    n_sy = int(round(args.n * args.sy_frac))
    # Remainder (e.g. 4% when 35/25/22/14) is filled from 人工智能 then 应届生.

    blocked, sy_needles = load_block()
    seen: set[str] = set()
    rng = random.Random(args.seed)
    print(
        json.dumps(
            {
                "phase": "start",
                "n": args.n,
                "n_ai": n_ai,
                "n_yj": n_yj,
                "n_ali": n_ali,
                "n_sy": n_sy,
                "blocked": len(blocked),
                "sy_needles": len(sy_needles),
            },
            ensure_ascii=False,
        ),
        flush=True,
    )

    ali, ali_stats = collect_aliyun(blocked, seen, n_ali, rng)
    print(json.dumps({"phase": "aliyun_done", "n": len(ali), "stats": ali_stats}, ensure_ascii=False), flush=True)

    sy, sy_stats = collect_shiye(blocked, sy_needles, seen, n_sy, rng)
    print(json.dumps({"phase": "shiye_done", "n": len(sy), "stats": sy_stats}, ensure_ascii=False), flush=True)

    short_ali = max(0, n_ali - len(ali))
    short_sy = max(0, n_sy - len(sy))
    ai, ai_stats = stream_flat_csv(AI_CSV, n_ai + short_ali + short_sy, blocked, seen, "人工智能招聘")
    print(json.dumps({"phase": "ai_done", "n": len(ai), "stats": ai_stats}, ensure_ascii=False), flush=True)

    # Fill whatever is still missing to hit --n. Do not add n_yj on top of the remainder
    # (that over-collects, and shuffle[:n] would randomly shrink 阿里云/事业单位).
    still_short = max(0, args.n - (len(ali) + len(sy) + len(ai)))
    yj, yj_stats = stream_flat_csv(YJ_CSV, still_short, blocked, seen, "应届生招聘")
    print(json.dumps({"phase": "yj_done", "n": len(yj), "stats": yj_stats}, ensure_ascii=False), flush=True)

    picked = ali + sy + ai + yj
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
        "mix_policy": "domain_mix_ai35_yj25_aliyun22_shiye14_no_listed",
        "remainder_fill": "人工智能 then 应届生",
        "target_frac": {
            "人工智能招聘": args.ai_frac,
            "应届生招聘": args.yj_frac,
            "阿里云公开数据集": args.ali_frac,
            "事业单位招聘": args.sy_frac,
        },
        "target_n_by_source": {
            "人工智能招聘": n_ai,
            "应届生招聘": n_yj,
            "阿里云公开数据集": n_ali,
            "事业单位招聘": n_sy,
        },
        "actual": dict(src),
        "actual_frac": {k: round(v / len(picked), 4) for k, v in src.items()} if picked else {},
        "blocked_train_dev_test_gold": len(blocked),
        "sy_doc_needles": len(sy_needles),
        "aliyun_scan": ali_stats,
        "shiye_scan": sy_stats,
        "ai_scan": ai_stats,
        "yj_scan": yj_stats,
        "align_gold": True,
        "align_note": (
            "Raises 事业单位 (encoder failure mode ~0.015) and 阿里云 share. "
            "Drops listed mix (1M lost to 0.1224). "
            "事业单位: drop gold-overlapping announcements; drop exam boiler; "
            "prefer skill-bearing sentences. Aliyun: exact sentence blocklist only."
        ),
        "overwrote_train": False,
        "touched_gold_v2": False,
        "used_llm_skill_columns": False,
    }
    meta_path = args.out.with_suffix(".meta.json")
    # with_suffix on .jsonl → .json ; we want .meta.json
    meta_path = Path(str(args.out).replace(".jsonl", ".meta.json"))
    if meta_path == args.out:
        meta_path = args.out.with_name(args.out.name + ".meta.json")
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    meta["meta_path"] = str(meta_path)
    print(json.dumps(meta, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
