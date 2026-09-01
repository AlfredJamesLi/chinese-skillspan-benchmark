#!/usr/bin/env python3
"""Build Doccano + worksheet packs for human SOP-v4 labeling on repartition_v1.

Does not overwrite Gold v2, V4 hybrid, old human980_pack, or train/test jsonl.
Sample IDs ranked by source / empty / L presence only — no model F1.
"""
from __future__ import annotations

import csv
import hashlib
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
sys.path.insert(0, str(PAPER / "scripts"))
sys.path.insert(0, str(PAPER / "scorer"))
from goldstyle_empty_rules import empty_hint  # noqa: E402
from score_lskt import rec_id  # noqa: E402

TEST = PAPER / "data/repartition_v1/test.jsonl"
TRAIN = PAPER / "data/repartition_v1/train.jsonl"
DEV = PAPER / "data/repartition_v1/dev.jsonl"
SIM980 = PAPER / "data/test_lskt_v4_simhuman980_cws.jsonl"
OUT = PAPER / "reports/repartition_v1/human_pack"
SAMPLE_SEED = 13  # official seed set; not split seed 7, not CRF 42/123/2026
IAA_N = 300
IAA100_N = 100
BATCH = 50
TYPES = {"L", "K", "S", "T"}
SRC = {
    "人工智能招聘": "AI",
    "应届生招聘": "Grad",
    "阿里云公开数据集": "Cloud",
    "事业单位招聘": "Public",
}


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_jsonl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def token_char_map(sentence: str, tokens: list) -> list[tuple[int, int]]:
    pos = 0
    out: list[tuple[int, int]] = []
    for tok in tokens:
        t = str(tok)
        idx = sentence.find(t, pos)
        if idx < 0:
            idx = pos
            end = pos + len(t)
        else:
            end = idx + len(t)
        out.append((idx, end))
        pos = end
    return out


def bio_to_char_spans(sentence: str, tokens: list, tags: list) -> list[list]:
    mapping = token_char_map(sentence, tokens)
    n = min(len(tokens), len(tags), len(mapping))
    spans: list[list] = []
    i = 0
    while i < n:
        tag = str(tags[i] or "O")
        if tag.startswith("B-"):
            typ = tag[2:]
            a, b = mapping[i]
            j = i + 1
            while j < n and str(tags[j]) == f"I-{typ}":
                b = mapping[j][1]
                j += 1
            if typ in TYPES and b > a:
                spans.append([int(a), int(b), typ])
            i = j
        else:
            i += 1
    return spans


def has_l(tags: list) -> bool:
    return any(str(t).endswith("-L") for t in tags)


def is_empty(tags: list) -> bool:
    return not any(str(t).startswith("B-") for t in tags)


def enrich(rec: dict) -> dict:
    sent = rec.get("sentence") or ""
    toks = [str(t) for t in (rec.get("tokens") or list(sent))]
    tags = rec.get("list_of_selection_bio4") or ["O"] * len(toks)
    if len(tags) != len(toks):
        tags = (list(tags) + ["O"] * len(toks))[: len(toks)]
    domain = str(rec.get("source_domain") or "")
    spans = bio_to_char_spans(sent, toks, tags)
    return {
        "id": rec_id(rec),
        "global_id": str(rec.get("global_id") or ""),
        "sentence": sent,
        "tokens": toks,
        "source_domain": domain,
        "src": SRC.get(domain, "UNK"),
        "title": rec.get("title") or "",
        "repartition_split": rec.get("repartition_split") or "",
        "empty_hint": empty_hint(sent, domain),
        "empty": is_empty(tags),
        "has_L": has_l(tags),
        "silver_spans": spans,
        "n_silver": len(spans),
        "annotation_provenance": rec.get("annotation_provenance") or "",
        "human_verification_status": rec.get("human_verification_status") or "",
    }


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")


def doccano_blank(row: dict, track: str) -> dict:
    return {
        "id": row["id"],
        "text": row["sentence"],
        "label": [],
        "labels": [],
        "meta": {
            "id": row["id"],
            "global_id": row["global_id"],
            "source_domain": row["source_domain"],
            "title": row["title"],
            "repartition_split": "test",
            "empty_hint": row["empty_hint"],
            "track": track,
            "prelabel": "none_dual_blind",
            "do_not_train": True,
            "do_not_overwrite_gold_v2": True,
        },
    }


def doccano_prelabel(row: dict, track: str) -> dict:
    rec = doccano_blank(row, track)
    rec["label"] = row["silver_spans"]
    rec["labels"] = row["silver_spans"]
    rec["meta"]["prelabel"] = "v4_silver_draft"
    rec["meta"]["annotation_provenance"] = row["annotation_provenance"]
    rec["meta"]["human_verification_status"] = row["human_verification_status"]
    rec["meta"]["n_silver"] = row["n_silver"]
    return rec


def batches(rows: list, prefix: Path, n: int = BATCH) -> list[Path]:
    paths = []
    for i in range(0, len(rows), n):
        chunk = rows[i : i + n]
        p = prefix / f"batch_{i // n + 1:02d}.jsonl"
        write_jsonl(p, chunk)
        paths.append(p)
    return paths


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def take_forced(pool: list[dict], pred, used: set[str]) -> list[dict]:
    out = []
    for r in pool:
        if r["id"] in used:
            continue
        if pred(r):
            out.append(r)
            used.add(r["id"])
    return out


def fill_quota(pool: list[dict], n: int, used: set[str], rng: random.Random) -> list[dict]:
    cand = [r for r in pool if r["id"] not in used]
    rng.shuffle(cand)
    out = cand[: max(0, int(n))]
    for r in out:
        used.add(r["id"])
    return out


def main() -> int:
    test = [enrich(r) for r in load_jsonl(TEST)]
    train_ids = {rec_id(r) for r in load_jsonl(TRAIN)}
    dev_ids = {rec_id(r) for r in load_jsonl(DEV)}
    sim_ids = {rec_id(r) for r in load_jsonl(SIM980)}
    by_src = defaultdict(list)
    for r in test:
        by_src[r["src"]].append(r)
    rng = random.Random(SAMPLE_SEED)
    used: set[str] = set()
    # All L-bearing test sentences (rare). Then source floors, not "all Public".
    picked: list[dict] = take_forced(test, lambda r: r["has_L"], used)
    quotas300 = {"AI": 120, "Grad": 120, "Cloud": 30, "Public": 30}  # sums to 300
    for src, n in quotas300.items():
        already = sum(1 for r in picked if r["src"] == src)
        picked += fill_quota(by_src[src], n - already, used, rng)
    if len(picked) < IAA_N:
        picked += fill_quota(test, IAA_N - len(picked), used, rng)
    while len(picked) > IAA_N:
        extra = [r for r in picked if (not r["has_L"]) and r["src"] in ("AI", "Grad")]
        if not extra:
            break
        victim = extra[-1]
        picked.remove(victim)
        used.discard(victim["id"])
    picked = picked[:IAA_N]
    picked.sort(key=lambda r: (r["src"], r["id"]))

    rng100 = random.Random(SAMPLE_SEED + 1000)
    iaa100: list[dict] = []
    used100: set[str] = set()
    iaa100 += take_forced(picked, lambda r: r["has_L"], used100)
    quotas100 = {"AI": 40, "Grad": 40, "Cloud": 10, "Public": 10}
    for src, n in quotas100.items():
        pool = [r for r in picked if r["src"] == src]
        already = sum(1 for x in iaa100 if x["src"] == src)
        iaa100 += fill_quota(pool, n - already, used100, rng100)
    if len(iaa100) < IAA100_N:
        iaa100 += fill_quota(picked, IAA100_N - len(iaa100), used100, rng100)
    iaa100 = iaa100[:IAA100_N]
    iaa100.sort(key=lambda r: (r["src"], r["id"]))

    review980 = [r for r in test if r["id"] in sim_ids]
    review980.sort(key=lambda r: (r["src"], r["id"]))

    iaa_blank = [doccano_blank(r, "iaa_dual_blind_300") for r in picked]
    iaa100_blank = [doccano_blank(r, "iaa_dual_blind_100") for r in iaa100]
    review_pre = [doccano_prelabel(r, "simhuman980_in_new_test") for r in review980]
    adj = [
        {
            "id": r["id"],
            "text": r["sentence"],
            "silver_spans": r["silver_spans"],
            "empty_hint": r["empty_hint"],
            "source_domain": r["source_domain"],
            "note": "Adjudicator only. Do not give to annotators A/B.",
        }
        for r in picked
    ]

    # wipe previous generated pack files we own; keep script-created dirs
    if OUT.exists():
        for p in OUT.rglob("*"):
            if p.is_file() and p.suffix in {".jsonl", ".csv", ".json", ".md"}:
                # will overwrite individually
                pass

    labels = [
        {"text": "L", "suffix_key": "l", "background_color": "#2563eb", "text_color": "#ffffff"},
        {"text": "K", "suffix_key": "k", "background_color": "#059669", "text_color": "#ffffff"},
        {"text": "S", "suffix_key": "s", "background_color": "#d97706", "text_color": "#ffffff"},
        {"text": "T", "suffix_key": "t", "background_color": "#7c3aed", "text_color": "#ffffff"},
    ]
    (OUT / "doccano").mkdir(parents=True, exist_ok=True)
    (OUT / "doccano/labels.json").write_text(json.dumps(labels, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    write_jsonl(OUT / "doccano/iaa300_blank.jsonl", iaa_blank)
    write_jsonl(OUT / "doccano/iaa100_blank.jsonl", iaa100_blank)
    write_jsonl(OUT / "doccano/iaa300_annotator_A.jsonl", iaa_blank)
    write_jsonl(OUT / "doccano/iaa300_annotator_B.jsonl", iaa_blank)
    batches(iaa100_blank, OUT / "doccano/iaa100_batches")
    batches(iaa_blank, OUT / "doccano/iaa300_batches")
    write_jsonl(OUT / "doccano/review980_test_prelabel.jsonl", review_pre)
    batches(review_pre, OUT / "doccano/review980_batches")
    write_jsonl(OUT / "adjudicator/iaa300_silver_reference.jsonl", adj)
    (OUT / "adjudicator/README.md").write_text(
        "仅裁决员打开。标注员 A/B 不得看银标。\n不要覆盖 `data/gold_canonical_v2.jsonl`。\n",
        encoding="utf-8",
    )

    csv_fields_iaa = [
        "id", "source_domain", "empty_hint", "sentence", "human_spans", "comment",
    ]
    def csv_rows(rows: list[dict]) -> list[dict]:
        return [
            {
                "id": r["id"],
                "source_domain": r["source_domain"],
                "empty_hint": r["empty_hint"],
                "sentence": r["sentence"],
                "human_spans": "",
                "comment": "",
            }
            for r in rows
        ]

    write_csv(OUT / "worksheets/iaa100_annotator_A.csv", csv_rows(iaa100), csv_fields_iaa)
    write_csv(OUT / "worksheets/iaa100_annotator_B.csv", csv_rows(iaa100), csv_fields_iaa)
    write_csv(OUT / "worksheets/iaa300_annotator_A.csv", csv_rows(picked), csv_fields_iaa)
    write_csv(OUT / "worksheets/iaa300_annotator_B.csv", csv_rows(picked), csv_fields_iaa)
    write_csv(
        OUT / "worksheets/review980_test.csv",
        [
            {
                "id": r["id"],
                "source_domain": r["source_domain"],
                "empty_hint": r["empty_hint"],
                "sentence": r["sentence"],
                "silver_spans": json.dumps(r["silver_spans"], ensure_ascii=False),
                "human_spans": "",
                "comment": "",
            }
            for r in review980
        ],
        ["id", "source_domain", "empty_hint", "sentence", "silver_spans", "human_spans", "comment"],
    )

    def src_counts(rows: list[dict]) -> dict:
        c = defaultdict(int)
        for r in rows:
            c[r["src"]] += 1
        return dict(c)

    sim_split = {"train": 0, "dev": 0, "test": 0, "other": 0}
    test_ids = {r["id"] for r in test}
    for i in sim_ids:
        if i in test_ids:
            sim_split["test"] += 1
        elif i in train_ids:
            sim_split["train"] += 1
        elif i in dev_ids:
            sim_split["dev"] += 1
        else:
            sim_split["other"] += 1

    manifest = {
        "pack": "repartition_v1_human_sop_v4",
        "sample_seed": SAMPLE_SEED,
        "iaa300_n": len(picked),
        "iaa100_n": len(iaa100),
        "iaa100_subset_of_300": all(x["id"] in {r["id"] for r in picked} for x in iaa100),
        "review980_in_new_test_n": len(review980),
        "simhuman980_by_new_split": sim_split,
        "iaa300_by_source": src_counts(picked),
        "iaa100_by_source": src_counts(iaa100),
        "iaa300_n_empty_silver": sum(1 for r in picked if r["empty"]),
        "iaa300_n_has_L": sum(1 for r in picked if r["has_L"]),
        "new_test_n": len(test),
        "new_test_by_source": src_counts(test),
        "test_jsonl_sha256": sha256_file(TEST),
        "no_model_f1_used": True,
        "do_not_overwrite": [
            "data/gold_canonical_v2.jsonl",
            "data/test_lskt_v4_cws_simhuman980_hybrid.jsonl",
            "reports/sandbox_lskt_v4_silver/human980_pack",
        ],
        "iaa300_ids": [r["id"] for r in picked],
        "iaa100_ids": [r["id"] for r in iaa100],
    }
    (OUT / "manifests").mkdir(parents=True, exist_ok=True)
    (OUT / "manifests/sample_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    write_jsonl(
        OUT / "manifests/iaa300_ids.jsonl",
        [{"id": r["id"], "src": r["src"], "empty_hint": r["empty_hint"], "has_L": r["has_L"]} for r in picked],
    )
    write_csv(
        OUT / "manifests/simhuman980_by_new_split.csv",
        [
            {
                "id": i,
                "new_split": (
                    "test" if i in test_ids else "train" if i in train_ids else "dev" if i in dev_ids else "other"
                ),
            }
            for i in sorted(sim_ids)
        ],
        ["id", "new_split"],
    )

    sums = []
    for p in sorted(OUT.rglob("*")):
        if p.is_file() and p.name != "SHA256SUMS":
            sums.append(f"{sha256_file(p)}  {p.relative_to(OUT)}")
    (OUT / "SHA256SUMS").write_text("\n".join(sums) + "\n", encoding="utf-8")
    print(json.dumps({k: manifest[k] for k in manifest if k not in ("iaa300_ids", "iaa100_ids")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
