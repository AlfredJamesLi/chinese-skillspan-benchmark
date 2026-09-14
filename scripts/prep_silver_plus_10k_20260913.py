#!/usr/bin/env python3
"""Prepare Chinese-SkillSpan Silver top-up to 10,000 unique valid sentences.

Does not call model APIs, does not rewrite Gold150 / V4 hybrid / manifests /
scorer, and does not change paper counts.

Repro:
  python3 scripts/prep_silver_plus_10k_20260913.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
import sys
import unicodedata
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
ROOT = PAPER.parent
PRE = PAPER / "chineseskillspan-jobert-pretrain"
OUT = PAPER / "data/silver_plus_10k_prep_20260913"

TARGET_UNIQUE = 10_000
SEED = 20260913
SALT_TOPUP = "CNSS_SP_10K_TOPUP"
SALT_QA150 = "CNSS_SP_NEW150_QA"
BATCH_SIZE = 20
LO, HI = 8, 400

# Documented 2451 ledger = v5 records 2369 + hold82. Frozen labeled file here is v6a_nocross.
DOCUMENTED_LEDGER_N = 2451

ALI_XLSX = PRE / "aliyun_天池公开数据集" / "only_yun_wei-预处理-James-0928.xlsx"
SY_XLSX = PRE / "0930-事业单位-LLM-软硬技能-提取-结果汇总编码文档-James.xlsx"
LISTED_YEARLY = PRE / "上市公司招聘大数据2014-2026.3" / "分年份保存数据"
CNSS_ZIP = PAPER / "CNSS_LabelData_Release_20260909.zip"
PILOT_ZIP = PAPER / "Silver_plus_pilot100_Doccano_review_20260908.zip"
PROMPT_REV2 = (
    PAPER
    / "output/gold150_codex_review_rev2_20260910/rev2_source"
    / "PROMPT_silver_plus_v4212_rev2.frozen.txt"
)
PROMPT_HANDBOOK = PAPER / "notes/handbooks/PROMPT_silver_plus_v4212.txt"

SENT_SPLIT = re.compile(r"[。！？；;\n]+|(?:\d+[\.、．])|<br\s*/?>", re.I)
HTML = re.compile(r"<[^>]+>|&nbsp;|&amp;|&lt;|&gt;")
BOILER = re.compile(
    r"(网上报名|资格审查|资格审核|准考证|缴费|咨询电话|联系电话|笔试时间|面试时间|"
    r"招聘公告|体检|公示|工作日|报名条件|报名办法|考试安排|应聘人员可拨打|"
    r"关注公众号|马克数据网|macrodatas|更多数据请)"
)
JUNK = re.compile(
    r"""\\xa0|\\n|\\t|','|'\s*,\s*'|&[a-z]+;|mso-|font-size|span style""",
    re.I,
)
SKILL = re.compile(
    r"(任职|岗位职责|专业|学历|技能|熟练|掌握|具备|能力|资格|证书|"
    r"本科|研究生|工程师|计算机|软件|要求|熟悉|精通|负责)"
)
TINY_BOILER = {"。", "！", "？", "';", "']", "]", "'", "；", "，"}

csv.field_size_limit(min(sys.maxsize, 16 * 1024 * 1024))

STRATUM_FRAC = {
    "阿里云公开数据集": 0.40,
    "事业单位招聘": 0.30,
    "上市公司招聘": 0.30,
}


def nfc(s: str) -> str:
    t = unicodedata.normalize("NFC", str(s or ""))
    t = re.sub(r"[\s\u3000]+", "", t)
    return t.strip(" ，,、:：;；")


def nfc_sha1(s: str) -> str:
    return hashlib.sha1(nfc(s).encode("utf-8")).hexdigest()


def rank_key(salt: str, text_nfc: str) -> str:
    return hashlib.sha256(f"{salt}|{SEED}|{text_nfc}".encode("utf-8")).hexdigest()


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def load_json_rows(path: Path) -> list[dict]:
    raw = path.read_text(encoding="utf-8")
    if raw.lstrip().startswith("["):
        return json.loads(raw)
    return load_jsonl(path)


def rec_text(o: dict) -> str:
    t = o.get("sentence") or o.get("text") or ""
    if isinstance(t, list):
        t = "".join(t)
    return str(t)


def rec_id(o: dict) -> str | None:
    meta = o.get("meta") or {}
    for blob in (o, meta):
        for k in ("id", "source_id", "example_id", "global_id"):
            v = blob.get(k)
            if v not in (None, ""):
                return str(v)
    return None


def is_valid_old_silver(text: str) -> tuple[bool, str]:
    """Keep already-labeled teacher rows unless the whole sentence is empty/punct."""
    nt = nfc(text)
    if not nt:
        return False, "empty"
    if nt in TINY_BOILER or len(nt) < 6:
        return False, "too_short_or_punct"
    return True, "ok"


def is_valid_sent(text: str) -> tuple[bool, str]:
    """Filter for NEW source-pool sentences (not used to drop old Silver)."""
    nt = nfc(text)
    if not nt:
        return False, "empty"
    if nt in TINY_BOILER or len(nt) < LO:
        return False, "too_short_or_punct"
    if len(nt) > HI:
        return False, "too_long"
    if BOILER.search(nt):
        return False, "boilerplate"
    if JUNK.search(text) or JUNK.search(nt):
        return False, "export_artifact"
    if nt.count("'") >= 2 or nt.count("\\") >= 2:
        return False, "export_artifact"
    return True, "ok"


def split_sents(text: str) -> list[str]:
    t = HTML.sub("", text or "")
    out = []
    for x in SENT_SPLIT.split(t):
        s = re.sub(r"\s+", "", x).strip(" ，,、:：")
        ok, _ = is_valid_sent(s)
        if ok:
            out.append(s)
    return out


def dump_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _zip_jsonl(zf: zipfile.ZipFile, suffix: str) -> list[dict]:
    name = next(n for n in zf.namelist() if n.replace("\\", "/").endswith(suffix))
    raw = zf.read(name).decode("utf-8")
    return [json.loads(line) for line in raw.splitlines() if line.strip()]


def extract_cnss_human350(tmp: Path) -> tuple[set[str], set[str], dict]:
    tmp.mkdir(parents=True, exist_ok=True)
    gold = load_jsonl(PAPER / "data/gold150_test.jsonl")
    with zipfile.ZipFile(CNSS_ZIP) as zf:
        a100 = _zip_jsonl(zf, "02_HumanReviewed_Silver_A100/a100_reviewed_sp.doccano.jsonl")
        qa = _zip_jsonl(zf, "03_QA100_SpotCheck/qa100_machine_frozen.jsonl")
    ids: set[str] = set()
    nfcs: set[str] = set()
    rows = []
    for src, recs, id_field in (
        ("gold150", gold, "source_id"),
        ("a100", a100, None),
        ("qa100", qa, None),
    ):
        for o in recs:
            i = str(o[id_field]) if id_field else rec_id(o)
            t = rec_text(o)
            nt = nfc(t)
            if i:
                ids.add(i)
            if nt:
                nfcs.add(nt)
            rows.append({"role": src, "id": i, "nfc_sha1": nfc_sha1(t), "nchars": len(nt)})
    return ids, nfcs, {
        "n_ids": len(ids),
        "n_nfc": len(nfcs),
        "n_gold150": len(gold),
        "n_a100": len(a100),
        "n_qa100": len(qa),
        "rows": rows,
    }


def load_block_texts() -> tuple[set[str], dict]:
    """Exact NFC blocklist from existing labeled / eval / human files (not 3M)."""
    blocked: set[str] = set()
    stats = Counter()
    files = [
        ("v6a_train", PAPER / "data/silver_plus_v6a_nocross/train_b2.jsonl"),
        ("v6a_dev", PAPER / "data/silver_plus_v6a_nocross/dev_b2.jsonl"),
        ("gold150", PAPER / "data/gold150_test.jsonl"),
        ("human200", PAPER / "data/human_gold_page1_200.jsonl"),
        ("hold82", PAPER / "notes/silver_plus_hold82_process_proof_20260908/HOLD82_WITH_TEXT.jsonl"),
        ("gold_v2", PAPER / "data/gold_canonical_v2.jsonl"),
        ("hybrid_v4", PAPER / "data/test_lskt_v4_cws_simhuman980_hybrid.jsonl"),
    ]
    for name, path in files:
        n = 0
        for o in load_jsonl(path):
            nt = nfc(rec_text(o))
            if nt:
                blocked.add(nt)
                n += 1
        stats[name] = n
    for split in ("train", "dev", "test"):
        path = PAPER / "data/corpus_splits" / f"{split}.json"
        n = 0
        for o in load_json_rows(path):
            nt = nfc(rec_text(o))
            if nt:
                blocked.add(nt)
                n += 1
        stats[f"corpus_{split}"] = n
    if PILOT_ZIP.is_file():
        with zipfile.ZipFile(PILOT_ZIP) as zf:
            with zf.open("silver_plus_pilot100_doccano.jsonl") as f:
                n = 0
                for line in f:
                    line = line.decode("utf-8").strip()
                    if not line:
                        continue
                    nt = nfc(rec_text(json.loads(line)))
                    if nt:
                        blocked.add(nt)
                        n += 1
                stats["pilot100"] = n
    return blocked, dict(stats)


def load_3m_nfc(paths: list[Path]) -> tuple[set[bytes], dict]:
    """SHA1 digest set of NFC texts in available DAPT dumps."""
    digests: set[bytes] = set()
    meta = []
    for path in paths:
        if not path.is_file():
            meta.append({"path": str(path), "exists": False})
            continue
        n = 0
        with path.open(encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                o = json.loads(line)
                nt = nfc(o.get("text") or o.get("sentence") or "")
                if nt:
                    digests.add(hashlib.sha1(nt.encode("utf-8")).digest())
                    n += 1
        meta.append({
            "path": str(path),
            "exists": True,
            "n_lines_with_text": n,
            "bytes": path.stat().st_size,
            "size_bytes": path.stat().st_size,
            "file_sha256": "omitted_large_dapt_dump",
        })
        print(f"[3M-check] loaded {n} texts from {path.name}", flush=True)
    return digests, {"files": meta, "unique_digests": len(digests)}


def in_3m(nt: str, digests: set[bytes]) -> bool:
    return hashlib.sha1(nt.encode("utf-8")).digest() in digests


def collect_aliyun(blocked: set[str], dapt: set[bytes]) -> list[dict]:
    import pandas as pd

    df = pd.read_excel(ALI_XLSX, sheet_name="only_yun_wei", engine="openpyxl")
    id_col = "ID" if "ID" in df.columns else df.columns[0]
    jd_col = "工作描述"
    out = []
    seen = set()
    n_raw = n_block = n_dapt = n_dup = 0
    for _, row in df.iterrows():
        src_id = row.get(id_col)
        jd = "" if pd.isna(row.get(jd_col)) else str(row.get(jd_col))
        for si, s in enumerate(split_sents(jd)):
            n_raw += 1
            nt = nfc(s)
            if nt in blocked:
                n_block += 1
                continue
            if in_3m(nt, dapt):
                n_dapt += 1
                continue
            if nt in seen:
                n_dup += 1
                continue
            seen.add(nt)
            out.append({
                "text": s,
                "source_domain": "阿里云公开数据集",
                "source_file": ALI_XLSX.name,
                "source_row_id": str(src_id),
                "sent_index": si,
                "skillish": bool(SKILL.search(s)),
            })
    print(
        f"[aliyun] raw={n_raw} block={n_block} dapt={n_dapt} dup={n_dup} unique={len(out)}",
        flush=True,
    )
    return out


def collect_shiye(blocked: set[str], dapt: set[bytes]) -> list[dict]:
    import pandas as pd

    df = pd.read_excel(
        SY_XLSX, sheet_name="all-result-0925-6k", engine="openpyxl",
        usecols=lambda c: c in {"ID", "cleaned_text", "title"},
    )
    out = []
    seen = set()
    n_raw = n_block = n_dapt = n_dup = n_boiler = 0
    for _, row in df.iterrows():
        src_id = row.get("ID")
        jd = "" if pd.isna(row.get("cleaned_text")) else str(row.get("cleaned_text"))
        for si, s in enumerate(split_sents(jd)):
            n_raw += 1
            nt = nfc(s)
            if BOILER.search(s):
                n_boiler += 1
                continue
            if nt in blocked:
                n_block += 1
                continue
            if in_3m(nt, dapt):
                n_dapt += 1
                continue
            if nt in seen:
                n_dup += 1
                continue
            seen.add(nt)
            out.append({
                "text": s,
                "source_domain": "事业单位招聘",
                "source_file": SY_XLSX.name,
                "source_row_id": str(src_id),
                "sent_index": si,
                "skillish": bool(SKILL.search(s)),
                "title": "" if pd.isna(row.get("title")) else str(row.get("title"))[:120],
            })
    print(
        f"[shiye] raw={n_raw} block={n_block} dapt={n_dapt} boiler={n_boiler} dup={n_dup} unique={len(out)}",
        flush=True,
    )
    return out


def collect_listed(blocked: set[str], dapt: set[bytes], cap: int) -> list[dict]:
    """Stream yearly listed CSVs until `cap` unique NFC sentences (skillish first)."""
    years = sorted(LISTED_YEARLY.glob("上市公司招聘数据*.csv"), reverse=True)
    out_skill: list[dict] = []
    out_other: list[dict] = []
    seen = set()
    n_raw = n_block = n_dapt = n_dup = 0
    for path in years:
        print(f"[listed] scanning {path.name}", flush=True)
        with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if not header:
                continue
            i_jd = header.index("职位描述") if "职位描述" in header else 12
            i_year = header.index("招聘发布年份") if "招聘发布年份" in header else -1
            i_name = header.index("企业名称") if "企业名称" in header else -1
            for ri, row in enumerate(reader, start=2):
                if not row or (row[0] or "").startswith("更多数据"):
                    continue
                jd = row[i_jd] if i_jd < len(row) else ""
                year = ""
                if i_year >= 0 and i_year < len(row):
                    year = str(row[i_year]).strip()[:4]
                company = ""
                if i_name >= 0 and i_name < len(row):
                    company = str(row[i_name])[:80]
                for si, s in enumerate(split_sents(jd)):
                    n_raw += 1
                    nt = nfc(s)
                    if nt in blocked:
                        n_block += 1
                        continue
                    if in_3m(nt, dapt):
                        n_dapt += 1
                        continue
                    if nt in seen:
                        n_dup += 1
                        continue
                    seen.add(nt)
                    rec = {
                        "text": s,
                        "source_domain": "上市公司招聘",
                        "source_file": path.name,
                        "source_row_id": f"{path.stem}-r{ri}",
                        "sent_index": si,
                        "skillish": bool(SKILL.search(s)),
                        "year": year,
                        "company": company,
                    }
                    if rec["skillish"]:
                        out_skill.append(rec)
                    else:
                        out_other.append(rec)
                    if len(out_skill) + len(out_other) >= cap:
                        print(
                            f"[listed] hit cap raw={n_raw} unique={len(seen)} skillish={len(out_skill)}",
                            flush=True,
                        )
                        return out_skill + out_other
        if len(out_skill) + len(out_other) >= cap:
            break
    print(
        f"[listed] done raw={n_raw} block={n_block} dapt={n_dapt} dup={n_dup} unique={len(seen)}",
        flush=True,
    )
    return out_skill + out_other


def hamilton(counts: dict[str, int], total: int, fracs: dict[str, float]) -> dict[str, int]:
    raw = {k: total * fracs.get(k, 0.0) for k in counts}
    alloc = {k: min(counts[k], int(raw[k])) for k in counts}
    remain = total - sum(alloc.values())
    # largest remainder among strata that still have leftover candidates
    rem = sorted(
        ((raw[k] - int(raw[k]), k) for k in counts if alloc[k] < counts[k]),
        reverse=True,
    )
    i = 0
    while remain > 0 and rem:
        k = rem[i % len(rem)][1]
        if alloc[k] < counts[k]:
            alloc[k] += 1
            remain -= 1
        i += 1
        if i > total * 3:
            break
    # leftover capacity from short strata
    if remain > 0:
        for k, n in sorted(counts.items(), key=lambda kv: kv[1], reverse=True):
            take = min(remain, counts[k] - alloc[k])
            alloc[k] += take
            remain -= take
            if remain <= 0:
                break
    return alloc


def audit_old_silver() -> dict:
    train = load_jsonl(PAPER / "data/silver_plus_v6a_nocross/train_b2.jsonl")
    dev = load_jsonl(PAPER / "data/silver_plus_v6a_nocross/dev_b2.jsonl")
    hold = load_jsonl(PAPER / "notes/silver_plus_hold82_process_proof_20260908/HOLD82_WITH_TEXT.jsonl")
    rows = []
    nfc_first: dict[str, str] = {}
    invalid = Counter()
    for split, recs in (("train", train), ("dev", dev)):
        for o in recs:
            t = rec_text(o)
            nt = nfc(t)
            ok, why = is_valid_old_silver(t)
            if not ok:
                invalid[why] += 1
            rec = {
                "id": o.get("id"),
                "split": split,
                "cohort": o.get("cohort"),
                "nchars": len(nt),
                "nfc_sha1": nfc_sha1(t),
                "valid": ok,
                "valid_reason": why,
                "v5_added_exact_dup": o.get("v5_added_exact_dup"),
            }
            rows.append(rec)
            nfc_first.setdefault(nt, o.get("id"))
    unique_valid = []
    seen = set()
    for rec, o in zip(rows, train + dev):
        nt = nfc(rec_text(o))
        if rec["valid"] and nt not in seen:
            seen.add(nt)
            unique_valid.append(rec)
    hold_ids = {r["id"] for r in hold}
    v6a_ids = {r["id"] for r in train + dev}
    return {
        "documented_ledger_n": DOCUMENTED_LEDGER_N,
        "documented_ledger_note": (
            "CNSS 2026-09-09 pack: 2451 = A100+QA100+REST. "
            "Equivalent reconstruction: v5 2200+169=2369 records + hold82. "
            "Full 2451 jsonl is not in this working tree (private REST pack omitted)."
        ),
        "v6a_nocross_records": len(train) + len(dev),
        "v6a_train": len(train),
        "v6a_dev": len(dev),
        "v6a_unique_ids": len(v6a_ids),
        "v6a_unique_nfc": len({nfc(rec_text(o)) for o in train + dev}),
        "v6a_unique_valid_nfc": len(unique_valid),
        "v6a_invalid_by_reason": dict(invalid),
        "hold82_records": len(hold),
        "hold82_ids_in_v6a": len(hold_ids & v6a_ids),
        "punct_or_tiny_in_v6a": invalid.get("too_short_or_punct", 0),
        "unique_valid_rows": unique_valid,
        "all_row_flags": rows,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "annotation_input" / "batches").mkdir(parents=True, exist_ok=True)
    (OUT / "human_qa150").mkdir(parents=True, exist_ok=True)
    (OUT / "old_silver").mkdir(parents=True, exist_ok=True)
    (OUT / "human350").mkdir(parents=True, exist_ok=True)
    (OUT / "new_unlabeled").mkdir(parents=True, exist_ok=True)

    print("== audit old silver ==", flush=True)
    audit = audit_old_silver()
    unique_valid_n = audit["v6a_unique_valid_nfc"]
    # Primary accounting: unique valid sentences in the frozen labeled Silver-plus.
    # 2451 is the documented ledger (records, including dups + pending 82).
    gap = TARGET_UNIQUE - unique_valid_n
    if gap < 0:
        gap = 0
    write_jsonl(OUT / "old_silver/unique_valid.jsonl", audit.pop("unique_valid_rows"))
    write_jsonl(OUT / "old_silver/record_flags.jsonl", audit.pop("all_row_flags"))
    dump_json(OUT / "old_silver/retained_v6a_nocross_pointer.json", {
        "train": "data/silver_plus_v6a_nocross/train_b2.jsonl",
        "dev": "data/silver_plus_v6a_nocross/dev_b2.jsonl",
        "do_not_rewrite": True,
        "n_train": audit["v6a_train"],
        "n_dev": audit["v6a_dev"],
        "sha256_train": sha256_file(PAPER / "data/silver_plus_v6a_nocross/train_b2.jsonl"),
        "sha256_dev": sha256_file(PAPER / "data/silver_plus_v6a_nocross/dev_b2.jsonl"),
    })
    dump_json(OUT / "AUDIT_OLD_SILVER.json", {
        **audit,
        "target_unique": TARGET_UNIQUE,
        "gap_from_unique_valid": gap,
        "gap_if_2451_all_unique_valid": TARGET_UNIQUE - DOCUMENTED_LEDGER_N,
        "accounting_used": "unique_valid_nfc_of_v6a_nocross",
        "why_not_2451": (
            "2451 is the Silver-plus registry/ledger (records). "
            "v6a_nocross unique NFC is lower because of exact-duplicate extras; "
            "hold82 is pending and not labeled teacher Silver. "
            "Top-up uses unique valid sentences, not extra duplicate records."
        ),
    })

    print("== human 350 ==", flush=True)
    cnss_tmp = OUT / "_cnss_unpack"
    h_ids, h_nfc, h_meta = extract_cnss_human350(cnss_tmp)
    write_jsonl(OUT / "human350/ids.jsonl", h_meta.pop("rows"))
    dump_json(OUT / "human350/SUMMARY.json", {
        **h_meta,
        "definition": "Gold150 + A100 + QA100 = 350 human-coded or checked sentences",
        "new_150_must_not_overlap": True,
        "after_new_150_human_cover_sentences": 500,
        "status": "new_150_pending_ai_labels_and_human_check",
    })

    print("== local blocklist ==", flush=True)
    blocked, block_stats = load_block_texts()
    blocked |= h_nfc
    print(f"blocked unique NFC (no 3M): {len(blocked)}", flush=True)

    print("== 3M list (paper-main jobbert_3m_sents.jsonl) ==", flush=True)
    dapt_3m_path = PAPER / "data/jobbert_3m_sents.jsonl"
    extra_dapt_paths = [
        PAPER / "data/jobbert_1m_sents.jsonl",
        PAPER / "data/jobbert_listed_mix_1m_sents.jsonl",
        PAPER / "data/jobbert_domain_mix_1m_sents.jsonl",
    ]
    # Hard exclusion = obtainable paper-main 3M list only (应届生+人工智能).
    # Other local DAPT dumps are reported after sampling, not used to drop Aliyun/listed/事业单位.
    dapt, dapt_meta = load_3m_nfc([dapt_3m_path])
    print(f"3M unique NFC digests: {len(dapt)}", flush=True)

    print("== collect candidates (prefer non-3M sources) ==", flush=True)
    ali = collect_aliyun(blocked, dapt)
    sy = collect_shiye(blocked, dapt)
    listed_need = int(gap * STRATUM_FRAC["上市公司招聘"] * 4) + 500
    listed = collect_listed(blocked, dapt, cap=max(listed_need, 8000))

    pools = {
        "阿里云公开数据集": ali,
        "事业单位招聘": sy,
        "上市公司招聘": listed,
    }
    # Prefer skill-bearing inside each source, but do not drop the rest until SRS.
    by_src_counts = {k: len(v) for k, v in pools.items()}
    alloc = hamilton(by_src_counts, gap, STRATUM_FRAC)
    print("stratum counts", by_src_counts, "alloc", alloc, flush=True)

    selected: list[dict] = []
    selected_nfc: set[str] = set()
    stratum_report = {}
    for src, recs in pools.items():
        ranked = sorted(
            recs,
            key=lambda r: (not r.get("skillish"), rank_key(SALT_TOPUP, nfc(r["text"]))),
        )
        take_n = alloc.get(src, 0)
        taken = []
        for r in ranked:
            nt = nfc(r["text"])
            if nt in selected_nfc:
                continue
            taken.append(r)
            selected_nfc.add(nt)
            if len(taken) >= take_n:
                break
        stratum_report[src] = {
            "pool": len(recs),
            "pool_skillish": sum(1 for r in recs if r.get("skillish")),
            "allocated": take_n,
            "taken": len(taken),
        }
        selected.extend(taken)

    # Fill any remaining gap from leftover ranked pool (still unique).
    if len(selected) < gap:
        leftover = []
        for recs in pools.values():
            leftover.extend(recs)
        leftover.sort(key=lambda r: rank_key(SALT_TOPUP, nfc(r["text"])))
        for r in leftover:
            if len(selected) >= gap:
                break
            nt = nfc(r["text"])
            if nt in selected_nfc:
                continue
            selected.append(r)
            selected_nfc.add(nt)

    selected.sort(key=lambda r: rank_key(SALT_TOPUP, nfc(r["text"])))
    actual_new = len(selected)
    shortfall = max(0, gap - actual_new)

    new_rows = []
    for i, r in enumerate(selected, start=1):
        nt = nfc(r["text"])
        sid = f"sp10k-{i:05d}"
        new_rows.append({
            "id": sid,
            "source_id": sid,
            "example_id": None,
            "seq": i,
            "text": r["text"],
            "source_domain": r["source_domain"],
            "source_file": r["source_file"],
            "source_row_id": r.get("source_row_id"),
            "sent_index": r.get("sent_index"),
            "year": r.get("year") or "",
            "title": r.get("title") or r.get("company") or "",
            "skillish_source_filter": bool(r.get("skillish")),
            "nfc_sha1": nfc_sha1(r["text"]),
            "nchars": len(nt),
            "not_gold": True,
            "split": "silver_plus_10k_new",
            "protocol": "B.sop_v4.2.14",
            "prompt_id": "silver_plus_v4212_rev2",
            "annotation_version": "silver_plus_10k_topup_20260913",
            "label_status": "pending_ai",
            "gpt6_label": None,
            "gpt6_why": None,
            "model": None,
            "gpt6_remark": None,
        })

    write_jsonl(OUT / "new_unlabeled/new_sentences.jsonl", new_rows)
    dump_json(OUT / "new_unlabeled/sampling_manifest.json", {
        "seed": SEED,
        "salt": SALT_TOPUP,
        "method": (
            "Within each source, rank by (not skillish, sha256(salt|seed|nfc)); "
            "take Hamilton-allocated n; then fill remainder from global rank. "
            "Not conditioned on model errors or label difficulty."
        ),
        "stratum_frac": STRATUM_FRAC,
        "stratum_report": stratum_report,
        "need": gap,
        "actual_new": actual_new,
        "shortfall": shortfall,
        "lo_hi": [LO, HI],
        "skillish_in_selected": sum(1 for r in new_rows if r["skillish_source_filter"]),
        "source_counts": dict(Counter(r["source_domain"] for r in new_rows)),
    })

    # Annotation input = new sentences only (old silver already labeled).
    work = new_rows
    write_jsonl(OUT / "annotation_input/work.jsonl", work)
    n_batch = 0
    for i in range(0, len(work), BATCH_SIZE):
        n_batch += 1
        write_jsonl(
            OUT / "annotation_input" / "batches" / f"batch_{n_batch:04d}.jsonl",
            work[i : i + BATCH_SIZE],
        )
    if PROMPT_REV2.is_file():
        shutil.copyfile(PROMPT_REV2, OUT / "annotation_input/PROMPT_silver_plus_v4212_rev2.txt")
    elif PROMPT_HANDBOOK.is_file():
        shutil.copyfile(PROMPT_HANDBOOK, OUT / "annotation_input/PROMPT_silver_plus_v4212_rev2.txt")

    extra_overlap = []
    selected_digests = {
        hashlib.sha1(nfc(r["text"]).encode("utf-8")).digest() for r in new_rows
    }
    for path in extra_dapt_paths:
        if not path.is_file():
            extra_overlap.append({"path": str(path), "exists": False})
            continue
        n = 0
        hit_ids = set()
        with path.open(encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                o = json.loads(line)
                nt = nfc(o.get("text") or o.get("sentence") or "")
                if not nt:
                    continue
                n += 1
                dg = hashlib.sha1(nt.encode("utf-8")).digest()
                if dg in selected_digests:
                    hit_ids.add(dg)
        extra_overlap.append({
            "path": str(path),
            "n_texts": n,
            "n_selected_nfc_also_in_dump": len(hit_ids),
            "used_as_hard_exclusion": False,
            "note": "Reported only. These dumps are not the paper-main 3M list.",
        })
        print(f"[extra-dapt report] {path.name} overlap_selected={len(hit_ids)}", flush=True)

    dump_json(OUT / "DEDUP_AND_SOURCE_VERIFICATION.json", {
        "local_block_files": block_stats,
        "local_blocked_unique_nfc": len(blocked),
        "paper_main_3m_check": dapt_meta,
        "paper_main_3m_hard_exclusion": True,
        "other_local_dapt_overlap_on_selected": extra_overlap,
        "dapt_scope_note": (
            "Hard-excluded exact NFC matches in data/jobbert_3m_sents.jsonl "
            "(paper-main 3.2M DAPT: 应届生招聘 + 人工智能招聘). "
            "Also blocked existing Silver, Gold150, A100, QA100, human200, hold82, "
            "Gold v2, V4 hybrid, corpus_splits, and pilot100. "
            "Other local DAPT dumps (1M / listed-mix / domain-mix) are reported "
            "on the selected set only and were NOT used to drop Aliyun or listed "
            "candidates. This does not claim exclusion from unpublished dumps, "
            "near-duplicates, or whitespace/tokenization variants beyond NFC."
        ),
        "new_vs_human350_id_overlap": 0,
        "new_vs_human350_nfc_overlap": sum(1 for r in new_rows if nfc(r["text"]) in h_nfc),
        "new_vs_old_valid_nfc_overlap": 0,
        "sources_used": dict(Counter(r["source_domain"] for r in new_rows)),
        "not_used": [
            "synthetic job sentences",
            "duplicate records of the same NFC text",
            "corpus_splits train/dev/test sentences (blocked; includes eval test 阿里云/事业单位)",
        ],
    })

    dump_json(OUT / "human_qa150/STATUS.json", {
        "status": "pending_ai_labels",
        "n_requested": 150,
        "seed": SEED,
        "salt": SALT_QA150,
        "frame": "new unlabeled/AI-labeled silver only; not old 2451/v6a",
        "exclude": "Gold150 + A100 + QA100 (350) by id and NFC",
        "do_not_replace_after_draw": True,
        "not_independent_blind_gold": True,
        "quality_stats_scope": "new silver portion only, not the full 10,000",
        "script": "scripts/sample_silver_plus_new150_qa.py",
    })

    n_old_valid = unique_valid_n
    n_new = actual_new
    projected_unique = n_old_valid + n_new
    dump_json(OUT / "COUNTS.json", {
        "paper_numbers_updated": False,
        "status": "pending_ai_annotation_and_human_qa150",
        "documented_old_ledger_records": DOCUMENTED_LEDGER_N,
        "old_labeled_records_retained": audit["v6a_nocross_records"],
        "old_unique_valid_sentences": n_old_valid,
        "need_if_old_unique_valid": gap,
        "need_if_2451_all_kept_as_unique": TARGET_UNIQUE - DOCUMENTED_LEDGER_N,
        "actual_new_unique_sentences": n_new,
        "shortfall": shortfall,
        "projected_unique_after_topup_unlabeled": projected_unique,
        "human350": 350,
        "new_human_qa150": "pending",
        "human_cover_sentences_after_qa": "500_only_after_new_150_checked",
        "do_not_write_10000_or_500_in_paper_yet": True,
    })

    print(
        json.dumps(
            {
                "old_unique_valid": n_old_valid,
                "gap": gap,
                "actual_new": n_new,
                "shortfall": shortfall,
                "batches": n_batch,
            },
            ensure_ascii=False,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
