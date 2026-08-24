#!/usr/bin/env python3
"""Build JobBERT-zh MLM corpus: 上市公司 (yearly stream) + 人工智能 + 应届生.

Gold-aligned mix default: listed 40% / AI 35% / 应届生 25%.
Listed rows: industry-stratified sampling, per-company JD cap, sentence dedup,
blocklist on train/dev/test/Gold v2. Reads yearly CSVs only (not the 10GB monolith).

Example:
  python prepare_jobbert_listed_mix_corpus.py --n 1000000 \\
    --out data/jobbert_listed_mix_1m_sents.jsonl
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
ROOT = PAPER.parent
PRE = PAPER / "chineseskillspan-jobert-pretrain"
AI_CSV = PRE / "人工智能招聘大数据2014-2025.3" / "人工智能招聘大数据.csv"
YJ_CSV = PRE / "应届生招聘大数据（2014-2025.6）" / "应届生招聘大数据（2014-2025.6）.csv"
LISTED_YEARLY = PRE / "上市公司招聘大数据2014-2026.3" / "分年份保存数据"
TEST = ROOT / "data/annotated/processed/chinese_skillspan/test.json"
TRAIN = ROOT / "data/annotated/processed/chinese_skillspan/train.json"
DEV = ROOT / "data/annotated/processed/chinese_skillspan/dev.json"
GOLD = PAPER / "data/gold_canonical_v2.jsonl"

SENT_SPLIT = re.compile(r"[。！？；;\n]+|(?:\d+[\.、．])|<br\s*/?>", re.I)
HTML = re.compile(r"<[^>]+>|&nbsp;|&amp;|&lt;|&gt;")

# Listed industry strata (within the listed share)
LISTED_STRATA = {
    "it_software": {
        "weight": 0.20,
        "industries": ("软件和信息技术服务业", "研究和试验发展", "互联网和相关服务"),
    },
    "it_hardware": {
        "weight": 0.20,
        "industries": ("计算机、通信和其他电子设备制造业",),
    },
    "public_state": {
        "weight": 0.15,
        "industries": (
            "资本市场服务",
            "商务服务业",
            "专业技术服务业",
            "公共设施管理业",
            "生态保护和环境治理业",
        ),
        "jd_keywords": ("事业单位", "编制", "国企", "央企", "政府机关", "公务员"),
    },
    "cloud_ops": {
        "weight": 0.05,
        "industries": (),
        "jd_keywords": ("云计算", "阿里云", "运维", "docker", "kubernetes", "devops", "saas", "paas"),
    },
    "mfg_engineering": {
        "weight": 0.25,
        "industries": (
            "汽车制造业",
            "专用设备制造业",
            "通用设备制造业",
            "电气机械和器材制造业",
            "医药制造业",
            "化学原料和化学制品制造业",
        ),
        "role_keywords": ("工程师", "研发", "工艺", "质量", "机械", "电气", "自动化"),
    },
    "other": {"weight": 0.15, "industries": (), "jd_keywords": (), "role_keywords": ()},
}

csv.field_size_limit(min(sys.maxsize, 16 * 1024 * 1024))


def load_json_rows(path: Path) -> list[dict]:
    raw = path.read_text(encoding="utf-8")
    if raw.lstrip().startswith("["):
        return json.loads(raw)
    return [json.loads(line) for line in raw.splitlines() if line.strip()]


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


def jd_fingerprint(jd: str) -> str:
    norm = re.sub(r"\s+", "", jd)[:240]
    return hashlib.md5(norm.encode("utf-8")).hexdigest()


def classify_listed_row(industry: str, role: str, jd: str) -> str:
    industry = (industry or "").strip()
    role = (role or "").strip()
    jd_l = (jd or "").lower()
    for name in ("it_software", "it_hardware", "public_state", "mfg_engineering"):
        spec = LISTED_STRATA[name]
        if any(ind in industry for ind in spec.get("industries", ())):
            return name
        for kw in spec.get("jd_keywords", ()):
            if kw.lower() in jd_l:
                return name
        for kw in spec.get("role_keywords", ()):
            if kw in role or kw in jd:
                return name
    cloud_kws = LISTED_STRATA["cloud_ops"].get("jd_keywords", ())
    if any(kw.lower() in jd_l for kw in cloud_kws):
        return "cloud_ops"
    return "other"


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


def stream_listed_yearly(
    yearly_dir: Path,
    years: list[int],
    caps: dict[str, int],
    blocked: set[str],
    seen: set[str],
    *,
    min_jd_len: int,
    max_same_jd_per_company: int,
    seed: int,
) -> tuple[list[dict], dict]:
    """Stream yearly listed-company CSVs with industry-stratified caps."""
    got: list[dict] = []
    remaining = {k: v for k, v in caps.items() if v > 0}
    strata_kept: Counter[str] = Counter()
    year_kept: Counter[str] = Counter()
    stats = {
        "rows_scanned": 0,
        "empty_jd": 0,
        "short_jd": 0,
        "company_jd_capped": 0,
        "blocked_hits": 0,
        "dup_hits": 0,
        "files": [],
    }
    company_jd: dict[str, Counter[str]] = defaultdict(Counter)
    rng = random.Random(seed)
    year_files: list[Path] = []
    for y in years:
        p = yearly_dir / f"上市公司招聘数据{y}.csv"
        if p.is_file():
            year_files.append(p)
    if not year_files:
        raise FileNotFoundError(
            f"No yearly CSV under {yearly_dir}. Run scripts/extract_listed_yearly_csvs.sh first."
        )
    rng.shuffle(year_files)

    def strata_done() -> bool:
        return not remaining or all(v <= 0 for v in remaining.values())

    for path in year_files:
        if strata_done():
            break
        file_rows = 0
        with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if not header:
                continue
            idx = {h: i for i, h in enumerate(header)}
            i_jd = idx.get("职位描述", 12)
            i_year = idx.get("招聘发布年份", idx.get("招聘发布年份", 5))
            i_ind = idx.get("上市公司行业", 4)
            i_role = idx.get("招聘岗位", 7)
            i_co = idx.get("企业名称", 0)
            for row in reader:
                stats["rows_scanned"] += 1
                file_rows += 1
                if is_footer_row(row):
                    continue
                jd = row[i_jd] if i_jd < len(row) else ""
                if not jd.strip():
                    stats["empty_jd"] += 1
                    continue
                if len(jd.strip()) < min_jd_len:
                    stats["short_jd"] += 1
                    continue
                company = (row[i_co] if i_co < len(row) else "").strip() or "NA"
                fp = jd_fingerprint(jd)
                if company_jd[company][fp] >= max_same_jd_per_company:
                    stats["company_jd_capped"] += 1
                    continue
                industry = row[i_ind] if i_ind < len(row) else ""
                role = row[i_role] if i_role < len(row) else ""
                strata = classify_listed_row(industry, role, jd)
                if remaining.get(strata, 0) <= 0:
                    continue
                year = ""
                if i_year >= 0 and i_year < len(row):
                    year = str(row[i_year]).strip()[:4]
                added = 0
                for s in split_sents(jd):
                    if s in blocked:
                        stats["blocked_hits"] += 1
                        continue
                    if s in seen:
                        stats["dup_hits"] += 1
                        continue
                    if remaining.get(strata, 0) <= 0:
                        break
                    seen.add(s)
                    got.append(
                        {
                            "text": s,
                            "source": "上市公司招聘",
                            "year": year,
                            "strata": strata,
                            "industry": (industry or "")[:40],
                        }
                    )
                    remaining[strata] -= 1
                    strata_kept[strata] += 1
                    year_kept[year or "unk"] += 1
                    added += 1
                if added:
                    company_jd[company][fp] += 1
                if strata_done():
                    break
        stats["files"].append({"path": str(path), "rows_scanned": file_rows})
        print(
            json.dumps(
                {
                    "phase": "listed_year",
                    "file": path.name,
                    "kept_total": len(got),
                    "remaining": {k: v for k, v in remaining.items() if v > 0},
                },
                ensure_ascii=False,
            ),
            flush=True,
        )

    stats["strata_kept"] = dict(strata_kept)
    stats["years_kept"] = dict(year_kept)
    stats["remaining_unfilled"] = {k: v for k, v in remaining.items() if v > 0}
    return got, stats


def listed_caps(n_listed: int) -> dict[str, int]:
    caps: dict[str, int] = {}
    assigned = 0
    keys = list(LISTED_STRATA.keys())
    for i, name in enumerate(keys):
        w = LISTED_STRATA[name]["weight"]
        if i == len(keys) - 1:
            caps[name] = max(0, n_listed - assigned)
        else:
            c = int(round(n_listed * w))
            caps[name] = c
            assigned += c
    return caps


def parse_years(s: str) -> list[int]:
    out: list[int] = []
    for part in s.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            out.extend(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return sorted(set(out))


def main() -> None:
    ap = argparse.ArgumentParser(description="Build Gold-aligned JobBERT MLM corpus with listed-company mix.")
    ap.add_argument("--n", type=int, default=1_000_000)
    ap.add_argument("--listed_frac", type=float, default=0.40)
    ap.add_argument("--ai_frac", type=float, default=0.35)
    ap.add_argument("--yj_frac", type=float, default=0.25)
    ap.add_argument("--listed_yearly_dir", type=Path, default=LISTED_YEARLY)
    ap.add_argument("--years", default="2020-2026", help="Comma years or ranges, e.g. 2017-2019,2020-2026")
    ap.add_argument("--min_jd_len", type=int, default=50)
    ap.add_argument("--max_same_jd_per_company", type=int, default=5)
    ap.add_argument("--seed", type=int, default=20260824)
    ap.add_argument("--out", type=Path, default=PAPER / "data/jobbert_listed_mix_1m_sents.jsonl")
    args = ap.parse_args()

    fracs = [args.listed_frac, args.ai_frac, args.yj_frac]
    if abs(sum(fracs) - 1.0) > 1e-6:
        raise SystemExit(f"Fractions must sum to 1.0, got {fracs}")
    n_listed = int(round(args.n * args.listed_frac))
    n_ai = int(round(args.n * args.ai_frac))
    n_yj = args.n - n_listed - n_ai
    years = parse_years(args.years)
    blocked = load_block()
    seen: set[str] = set()

    print(
        json.dumps(
            {
                "phase": "start",
                "n": args.n,
                "n_listed": n_listed,
                "n_ai": n_ai,
                "n_yj": n_yj,
                "years": years,
                "blocked": len(blocked),
            },
            ensure_ascii=False,
        ),
        flush=True,
    )

    listed, listed_stats = stream_listed_yearly(
        args.listed_yearly_dir,
        years,
        listed_caps(n_listed),
        blocked,
        seen,
        min_jd_len=args.min_jd_len,
        max_same_jd_per_company=args.max_same_jd_per_company,
        seed=args.seed,
    )
    print(json.dumps({"phase": "listed_done", "n": len(listed), "stats": listed_stats}, ensure_ascii=False), flush=True)

    ai, ai_stats = stream_flat_csv(AI_CSV, n_ai + max(0, n_listed - len(listed)), blocked, seen, "人工智能招聘")
    print(json.dumps({"phase": "ai_done", "n": len(ai), "stats": ai_stats}, ensure_ascii=False), flush=True)

    yj, yj_stats = stream_flat_csv(
        YJ_CSV,
        n_yj + max(0, n_ai - len(ai)) + max(0, n_listed - len(listed)),
        blocked,
        seen,
        "应届生招聘",
    )
    print(json.dumps({"phase": "yj_done", "n": len(yj), "stats": yj_stats}, ensure_ascii=False), flush=True)

    picked = listed + ai + yj
    rng = random.Random(args.seed)
    rng.shuffle(picked)
    picked = picked[: args.n]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as f:
        for rec in picked:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    src = Counter(r["source"] for r in picked)
    strata = Counter(r.get("strata", "NA") for r in picked if r["source"] == "上市公司招聘")
    meta = {
        "out": str(args.out),
        "n": len(picked),
        "target_n": args.n,
        "mix_policy": "gold_aligned_listed_40_ai_35_yj_25",
        "target_frac": {
            "上市公司招聘": args.listed_frac,
            "人工智能招聘": args.ai_frac,
            "应届生招聘": args.yj_frac,
        },
        "target_n_by_source": {
            "上市公司招聘": n_listed,
            "人工智能招聘": n_ai,
            "应届生招聘": n_yj,
        },
        "actual": dict(src),
        "actual_frac": {k: round(v / len(picked), 4) for k, v in src.items()} if picked else {},
        "listed_strata_actual": dict(strata),
        "listed_strata_target": listed_caps(n_listed),
        "blocked_train_dev_test_gold": len(blocked),
        "years_listed": years,
        "listed_scan": listed_stats,
        "ai_scan": ai_stats,
        "yj_scan": yj_stats,
        "align_gold": True,
        "align_note": (
            "Listed yearly CSVs add 事业单位/制造业/IT diversity missing from AI+应届生 only. "
            "Still block exact Gold/train/dev/test sentences."
        ),
        "overwrote_train": False,
        "touched_gold_v2": False,
    }
    meta_path = args.out.with_suffix(".meta.json")
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(meta, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
