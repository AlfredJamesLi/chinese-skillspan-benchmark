#!/usr/bin/env python3
"""Sample unlabeled JD sentences for a small JobBERT-zh MLM demo.

Does not overwrite train.json or Gold v2. Drops exact test/Gold sentences.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import random
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
ROOT = PAPER.parent
TEST = ROOT / "data/annotated/processed/chinese_skillspan/test.json"
GOLD = PAPER / "data/gold_canonical_v2.jsonl"
SENT_SPLIT = re.compile(r"[。！？；;\n]+|(?:\d+[\.、．])|<br\s*/?>", re.I)
HTML = re.compile(r"<[^>]+>|&nbsp;|&amp;|&lt;|&gt;")
NS_C = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def load_block() -> set[str]:
    blocked = set()
    if TEST.is_file():
        raw = json.loads(TEST.read_text(encoding="utf-8"))
        blocked.update((r.get("sentence") or "").strip() for r in raw)
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


def sents_from_csv(path: Path, cap: int, blocked: set[str]) -> list[str]:
    got: list[str] = []
    seen: set[str] = set()
    with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if not header:
            return got
        try:
            i_jd = header.index("职位描述")
        except ValueError:
            i_jd = 6
        for row in reader:
            if not row:
                continue
            if row[0].startswith("更多数据") or "macrodatas" in "".join(row[:2]):
                continue
            jd = row[i_jd] if i_jd < len(row) else ""
            for s in split_sents(jd):
                if s in blocked or s in seen:
                    continue
                seen.add(s)
                got.append(s)
                if len(got) >= cap:
                    return got
    return got


def sents_from_xlsx(path: Path, cap: int, blocked: set[str]) -> list[str]:
    got: list[str] = []
    seen: set[str] = set()
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("xl/sharedStrings.xml"))
        strings = ["".join(t.text or "" for t in si.findall(f".//{NS_C}t")) for si in root.findall(f"{NS_C}si")]
        header = None
        i_jd = 7
        for _ev, el in ET.iterparse(io.BytesIO(z.read("xl/worksheets/sheet1.xml")), events=("end",)):
            if el.tag != f"{NS_C}row":
                continue
            vals = []
            for c in el.findall(f"{NS_C}c"):
                t = c.get("t")
                v = c.find(f"{NS_C}v")
                val = ""
                if t == "s" and v is not None and v.text is not None:
                    val = strings[int(v.text)]
                elif v is not None:
                    val = v.text or ""
                vals.append(val)
            if header is None:
                header = vals
                if "职位描述" in header:
                    i_jd = header.index("职位描述")
            else:
                jd = vals[i_jd] if i_jd < len(vals) else ""
                for s in split_sents(jd):
                    if s in blocked or s in seen:
                        continue
                    seen.add(s)
                    got.append(s)
                    if len(got) >= cap:
                        el.clear()
                        return got
            el.clear()
    return got


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=80000)
    ap.add_argument("--seed", type=int, default=20260823)
    ap.add_argument("--out", type=Path, default=PAPER / "data/jobbert_demo_sents.jsonl")
    args = ap.parse_args()
    blocked = load_block()
    per_file = {
        "应届生招聘大数据2014.csv": 2000,
        "应届生招聘大数据2015.csv": 4000,
        "应届生招聘大数据2016.csv": 35000,
        "应届生招聘大数据2017.csv": 12000,
        "应届生招聘大数据2019.csv": 35000,
        "人工智能招聘大数据2025年.xlsx": 8000,
    }
    picked: list[dict] = []
    sources = {}
    for name, cap in per_file.items():
        path = PAPER / name
        if not path.is_file() or path.stat().st_size < 100:
            continue
        sents = sents_from_xlsx(path, cap, blocked) if path.suffix.lower() == ".xlsx" else sents_from_csv(path, cap, blocked)
        sources[name] = {"n": len(sents), "bytes": path.stat().st_size}
        year = re.search(r"(20\d{2})", name)
        for s in sents:
            picked.append({"text": s, "source": name, "year": year.group(1) if year else ""})
    rng = random.Random(args.seed)
    rng.shuffle(picked)
    # unique again across files
    seen = set()
    uniq = []
    for rec in picked:
        if rec["text"] in seen:
            continue
        seen.add(rec["text"])
        uniq.append(rec)
        if len(uniq) >= args.n:
            break
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as f:
        for rec in uniq:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    meta = {
        "out": str(args.out),
        "n": len(uniq),
        "blocked_test_gold": len(blocked),
        "sources": sources,
        "overwrote_train": False,
        "touched_gold_v2": False,
        "note": "Demo subsample only. Not Zhang-scale 3.2M.",
    }
    (args.out.with_suffix(".meta.json")).write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(meta, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
