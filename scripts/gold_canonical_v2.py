#!/usr/bin/env python3
"""Build gold_canonical_v2 from raw Gold + 18 adjudicated conflict IDs.

Does not modify raw Gold. v1 files are left as an audit trail.
"""
from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/home/guojingli3/SCESC-LLM-skill-extraction")
PAPER = ROOT / "Chinese_skill_benchmark_Paper"
RAW = ROOT / "chinese_skillspan_preprocessing/data/doccano_to_baseline_file/admin_Baseline_test.jsonl"
sys_path_scorer = str(PAPER / "scorer")

import sys

sys.path.insert(0, sys_path_scorer)
from score_lskt import GOLD_FIELDS, extract_spans, sha256_file  # noqa: E402

# Human Gold: Doubao draft + three revisions (2026-08-22).
# Empty list = no candidate competency span.
DECISIONS: dict[str, list[tuple[int, int, str]]] = {
    "1987-s0045": [],  # exam format; not 试讲/答辩 as job skills
    "1987-s0059": [],
    "1988-s0026": [(37, 54, "K")],
    "1988-s0027": [],
    "1988-s0063": [],
    "1988-s0085": [],
    "1988-s0107": [
        (38, 42, "K"),
        (43, 47, "T"),
        (48, 52, "T"),
        (53, 57, "T"),
        (58, 64, "T"),
        (66, 70, "T"),
    ],
    "1988-s0113": [],  # tie-break rule, not a degree requirement
    "1988-s0154": [],
    "1988-s0161": [],
    "1989-s0001": [],
    "1989-s0023": [],
    "1991-s0006": [(4, 14, "T")],
    "1991-s0033": [],
    "1991-s0042": [(12, 16, "K")],  # 医学专业 only
    "1995-s0036": [],
    "1995-s0037": [],
    "1999-s0072": [],
}

DOUBAO_OVERRIDES = {
    "1987-s0045": "empty_not_试讲答辩",
    "1988-s0113": "empty_not_学历_tiebreak",
    "1991-s0042": "keep_医学专业_K_only",
}


def spans_to_bio4(n: int, spans: list[tuple[int, int, str]]) -> list[str]:
    tags = ["O"] * n
    for a, b, typ in spans:
        if a < 0 or a >= n or b <= a:
            raise ValueError(f"bad span {(a, b, typ)} n={n}")
        tags[a] = f"B-{typ}"
        for i in range(a + 1, min(b, n)):
            tags[i] = f"I-{typ}"
    return tags


def bio4_to_untyped(tags: list[str]) -> list[str]:
    out = []
    for t in tags:
        if t.startswith("B-"):
            out.append("B")
        elif t.startswith("I-"):
            out.append("I")
        else:
            out.append("O")
    return out


def markup(tokens: list[str], spans: list[tuple[int, int, str]]) -> tuple[str, str]:
    marked = list(tokens)
    four = list(tokens)
    for a, b, typ in sorted(spans, key=lambda x: -x[0]):
        if a < len(marked) and b <= len(marked) + 1:
            four[a] = "@@" + four[a]
            four[b - 1] = four[b - 1] + f"##[{typ}]"
            marked[a] = "@@" + marked[a]
            marked[b - 1] = marked[b - 1] + "##"
    return "".join(marked), "".join(four)


def apply_decision(rec: dict, spans: list[tuple[int, int, str]], raw_line: int, dropped: list[int]) -> dict:
    rec = json.loads(json.dumps(rec, ensure_ascii=False))
    n = len(rec.get("tokens") or [])
    bio = spans_to_bio4(n, spans)
    rec["list_of_selection_bio4"] = bio
    rec["list_of_selection"] = bio4_to_untyped(bio)
    rec["tags_skill"] = list(bio)
    rec["tags_skill_clean"] = list(bio)
    rec["skill_spans"] = [[a, b] for a, b, _ in spans]
    sw, sw4 = markup(rec.get("tokens") or [], spans)
    rec["sentence_with_tags"] = sw
    rec["sentence_with_tags_4d"] = sw4
    rec["_canon"] = {
        "source_id": rec["id"],
        "kept_raw_line": raw_line,
        "dropped_raw_lines": dropped,
        "rule": "adjudicated_v2",
        "adjudication": "doubao_plus_human_20260822",
        "human_overrides": DOUBAO_OVERRIDES.get(str(rec["id"])),
    }
    return rec


def classify_group(group: list[tuple[int, dict]]) -> str:
    texts = {(r.get("sentence") or r.get("text") or "") for _, r in group}
    labs = {json.dumps(extract_spans(r, GOLD_FIELDS), ensure_ascii=False) for _, r in group}
    if len(group) == 1:
        return "unique"
    if len(texts) == 1 and len(labs) == 1:
        return "exact_duplicate"
    if len(texts) == 1 and len(labs) > 1:
        return "annotation_conflict"
    if len(texts) > 1:
        return "id_collision"
    return "other"


def span_count(path: Path) -> dict:
    types: Counter[str] = Counter()
    ids = []
    n = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        ids.append(str(rec["id"]))
        for *_, t in extract_spans(rec, GOLD_FIELDS):
            types[t] += 1
            n += 1
    return {
        "path": str(path),
        "sha256": sha256_file(str(path)),
        "n_rows": len(ids),
        "n_unique_ids": len(set(ids)),
        "n_spans": n,
        "L": types.get("L", 0),
        "K": types.get("K", 0),
        "S": types.get("S", 0),
        "T": types.get("T", 0),
    }


def main() -> int:
    raw_rows = []
    with RAW.open(encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            if line.strip():
                raw_rows.append((lineno, json.loads(line)))
    by_id: dict[str, list[tuple[int, dict]]] = defaultdict(list)
    for lineno, rec in raw_rows:
        by_id[str(rec["id"]).strip()].append((lineno, rec))

    missing = sorted(set(DECISIONS) - set(by_id))
    extra_dec = sorted(i for i, g in by_id.items() if classify_group(g) == "annotation_conflict" and i not in DECISIONS)
    if missing or extra_dec:
        raise SystemExit(f"decision/id mismatch missing={missing} extra_conflicts={extra_dec}")

    canonical = []
    log_rows = []
    for iid, group in by_id.items():
        kind = classify_group(group)
        first_line, first = group[0]
        dropped = [n for n, _ in group[1:]]
        if kind == "annotation_conflict":
            rec = apply_decision(first, DECISIONS[iid], first_line, dropped)
            canonical.append(rec)
            log_rows.append({
                "id": iid,
                "n_raw": len(group),
                "kept_raw_line": first_line,
                "dropped_raw_lines": "|".join(str(x) for x in dropped),
                "spans": json.dumps(DECISIONS[iid], ensure_ascii=False),
                "human_override": DOUBAO_OVERRIDES.get(iid, ""),
            })
            continue
        rec = json.loads(json.dumps(first, ensure_ascii=False))
        rec["_canon"] = {
            "source_id": iid,
            "kept_raw_line": first_line,
            "dropped_raw_lines": dropped,
            "rule": "keep_first_exact" if kind == "exact_duplicate" else "unique",
        }
        canonical.append(rec)

    ids = [str(r["id"]) for r in canonical]
    if len(ids) != len(set(ids)):
        raise SystemExit("canonical v2 IDs not unique")
    if set(DECISIONS) - set(ids):
        raise SystemExit("adjudicated IDs missing from v2")

    out = PAPER / "data/gold_canonical_v2.jsonl"
    with out.open("w", encoding="utf-8") as f:
        for rec in canonical:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    adj_path = PAPER / "data/gold_adjudication_v2.json"
    adj_path.write_text(
        json.dumps(
            {
                "created_utc": datetime.now(timezone.utc).isoformat(),
                "source": "doubao_draft_plus_human_review",
                "human_confirmed": True,
                "overrides": DOUBAO_OVERRIDES,
                "decisions": {k: v for k, v in DECISIONS.items()},
                "rows": log_rows,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    raw_m = span_count(RAW)
    v2_m = span_count(out)
    v1 = PAPER / "data/gold_canonical_v1.jsonl"
    v1_m = span_count(v1) if v1.is_file() else {}
    man = PAPER / "manifests/gold_canonical_v2_manifest.csv"
    with man.open("w", encoding="utf-8", newline="") as f:
        fields = ["role", "path", "sha256", "n_rows", "n_unique_ids", "n_spans", "L", "K", "S", "T"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerow({"role": "raw_gold", **raw_m})
        if v1_m:
            w.writerow({"role": "canonical_v1_held_out_conflicts", **v1_m})
        w.writerow({"role": "canonical_v2", **v2_m})

    md = [
        "# Gold canonicalization v2",
        "",
        "**18 annotation conflicts adjudicated (Doubao draft + human).** Unique IDs restored to 2601.",
        "Raw Gold was not modified.",
        "",
        "This uniqueifies Gold. Do **not** yet write Table 3 into the PDF: most dumps still have duplicate or missing IDs.",
        "Score with `data/gold_canonical_v2.jsonl` and unique-first prediction views.",
        "",
        "## Counts",
        "",
        f"| role | rows | unique IDs | spans | L | K | S | T | SHA256 |",
        f"|---|---:|---:|---:|---:|---:|---:|---:|---|",
        f"| raw | {raw_m['n_rows']} | {raw_m['n_unique_ids']} | {raw_m['n_spans']} | {raw_m['L']} | {raw_m['K']} | {raw_m['S']} | {raw_m['T']} | `{raw_m['sha256']}` |",
        f"| v1 (conflicts held out) | {v1_m.get('n_rows','')} | {v1_m.get('n_unique_ids','')} | {v1_m.get('n_spans','')} | {v1_m.get('L','')} | {v1_m.get('K','')} | {v1_m.get('S','')} | {v1_m.get('T','')} | `{v1_m.get('sha256','')}` |",
        f"| **v2** | {v2_m['n_rows']} | {v2_m['n_unique_ids']} | {v2_m['n_spans']} | {v2_m['L']} | {v2_m['K']} | {v2_m['S']} | {v2_m['T']} | `{v2_m['sha256']}` |",
        "",
        "Human overrides vs Doubao: `1987-s0045` empty; `1988-s0113` empty; `1991-s0042` only `医学专业`[K].",
        "Log: `data/gold_adjudication_v2.json`.",
        "",
    ]
    (PAPER / "notes/GOLD_CANONICALIZATION.md").write_text("\n".join(md), encoding="utf-8")
    print("v2", v2_m)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
