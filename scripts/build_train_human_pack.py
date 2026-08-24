#!/usr/bin/env python3
"""Pack locked human-80 + train IAA-300 into one Gold-style train worksheet.

Does not overwrite train.json or Gold v2. 80 rows are prefilled; 300 are blank.
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from goldstyle_empty_rules import empty_hint

ROOT = Path("/home/guojingli3/SCESC-LLM-skill-extraction")
PAPER = ROOT / "Chinese_skill_benchmark_Paper"
TRAIN = ROOT / "data/annotated/processed/chinese_skillspan/train.json"
FINAL80 = PAPER / "reports/gold_style_relabel/sample80_final.json"
IAA300 = PAPER / "reports/iaa300/iaa300_manifest.json"
OUT = PAPER / "reports/gold_style_relabel/train_human_80_300"


def load_json(path: Path):
    raw = path.read_text(encoding="utf-8")
    if raw.lstrip().startswith("["):
        return json.loads(raw)
    return [json.loads(l) for l in raw.splitlines() if l.strip()]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    train = {r["id"]: r for r in load_json(TRAIN)}
    locked80 = load_json(FINAL80)
    iaa300 = load_json(IAA300)
    lock_ids = {r["id"] for r in locked80}
    overlap = [r["id"] for r in iaa300 if r["id"] in lock_ids]
    pack = []
    for rec in locked80:
        tr = train.get(rec["id"], {})
        sent = tr.get("sentence") or rec.get("sentence") or ""
        d = tr.get("source_domain") or ""
        pack.append(
            {
                "id": rec["id"],
                "role": "lock80",
                "decision": rec.get("decision"),
                "source_domain": d,
                "empty_hint": empty_hint(sent, d),
                "sentence": sent,
                "spans": rec.get("spans") or [],
                "comment": rec.get("comment") or "",
                "status": "locked",
            }
        )
    for rec in iaa300:
        tr = train.get(rec["id"], {})
        sent = rec.get("sentence") or tr.get("sentence") or ""
        d = rec.get("source_domain") or tr.get("source_domain") or ""
        pack.append(
            {
                "id": rec["id"],
                "role": "train300",
                "decision": "",
                "source_domain": d,
                "empty_hint": empty_hint(sent, d),
                "sentence": sent,
                "spans": [],
                "comment": "",
                "status": "todo",
                "bucket_silver": rec.get("bucket"),
                "n_silver_spans": rec.get("n_silver_spans"),
            }
        )
    (OUT / "pack.json").write_text(json.dumps(pack, ensure_ascii=False, indent=2), encoding="utf-8")
    fields = ["id", "role", "status", "source_domain", "empty_hint", "sentence", "spans_json", "comment"]
    with (OUT / "worksheet.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in pack:
            w.writerow(
                {
                    "id": row["id"],
                    "role": row["role"],
                    "status": row["status"],
                    "source_domain": row["source_domain"],
                    "empty_hint": row["empty_hint"],
                    "sentence": row["sentence"],
                    "spans_json": json.dumps(row["spans"], ensure_ascii=False) if row["role"] == "lock80" else "",
                    "comment": row.get("comment") or "",
                }
            )
    meta = {
        "n": len(pack),
        "n_lock80": sum(1 for r in pack if r["role"] == "lock80"),
        "n_train300_todo": sum(1 for r in pack if r["role"] == "train300"),
        "overlap_80_300": overlap,
        "domains": dict(Counter(r["source_domain"] for r in pack)),
        "empty_hint_n": sum(1 for r in pack if r["empty_hint"]),
        "overwrote_train": False,
        "touched_gold_v2": False,
        "note": "80 locked from sample80_final.json. 300 need human Gold-style labels. Do not invent labels in scripts.",
    }
    (OUT / "pack_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(meta, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
