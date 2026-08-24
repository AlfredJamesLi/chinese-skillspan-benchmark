#!/usr/bin/env python3
"""Round-2 Gold duplicate audit + canonicalization. Does not modify raw Gold."""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/home/guojingli3/SCESC-LLM-skill-extraction")
PAPER = ROOT / "Chinese_skill_benchmark_Paper"
RAW = ROOT / "chinese_skillspan_preprocessing/data/doccano_to_baseline_file/admin_Baseline_test.jsonl"
sys.path.insert(0, str(PAPER / "scorer"))
from score_lskt import extract_spans, GOLD_FIELDS, sha256_file  # noqa: E402


def load_jsonl_rows(path: Path) -> list[tuple[int, dict]]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            if not line.strip():
                continue
            rows.append((lineno, json.loads(line)))
    return rows


def spans_key(rec: dict) -> str:
    return json.dumps(extract_spans(rec, GOLD_FIELDS), ensure_ascii=False)


def text_of(rec: dict) -> str:
    return rec.get("sentence") or rec.get("text") or ""


def classify(group: list[tuple[int, dict]]) -> str:
    texts = {text_of(r) for _, r in group}
    labs = {spans_key(r) for _, r in group}
    posts = {str(r.get("global_id", "")) for _, r in group}
    if len(texts) == 1 and len(labs) == 1:
        return "exact_duplicate"
    if len(texts) == 1 and len(labs) > 1:
        return "annotation_conflict"
    if len(texts) > 1:
        return "id_collision"
    return "other"


def advise(kind: str) -> str:
    return {
        "exact_duplicate": "keep first row; drop later identical rows; log dropped line numbers",
        "annotation_conflict": "do not auto-merge; hold out for human adjudication",
        "id_collision": "assign stable new IDs to extra texts; record mapping",
        "other": "manual review",
    }[kind]


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def main() -> int:
    raw_rows = load_jsonl_rows(RAW)
    by_id: dict[str, list[tuple[int, dict]]] = defaultdict(list)
    for lineno, rec in raw_rows:
        by_id[str(rec["id"]).strip()].append((lineno, rec))

    counts = Counter({i: len(g) for i, g in by_id.items()})
    n_unique = len(by_id)
    n_rows = len(raw_rows)
    extra = n_rows - n_unique
    n_dup_ids = sum(1 for c in counts.values() if c > 1)
    triples = sorted(i for i, c in counts.items() if c >= 3)
    freq = Counter(counts.values())

    audit = []
    for iid, group in sorted(by_id.items()):
        if len(group) < 2:
            continue
        texts = [text_of(r) for _, r in group]
        labs = [spans_key(r) for _, r in group]
        posts = [str(r.get("global_id", "")) for _, r in group]
        kind = classify(group)
        audit.append({
            "id": iid,
            "n_occurrences": len(group),
            "raw_line_numbers": "|".join(str(n) for n, _ in group),
            "texts_identical": int(len(set(texts)) == 1),
            "labels_identical": int(len(set(labs)) == 1),
            "same_posting": int(len(set(posts)) == 1),
            "global_ids": "|".join(posts),
            "classification": kind,
            "suggested_action": advise(kind),
            "n_distinct_texts": len(set(texts)),
            "n_distinct_label_sets": len(set(labs)),
            "text_preview": texts[0][:160],
        })

    write_csv(
        PAPER / "reports/gold_duplicate_audit.csv",
        audit,
        [
            "id", "n_occurrences", "raw_line_numbers", "texts_identical",
            "labels_identical", "same_posting", "global_ids", "classification",
            "suggested_action", "n_distinct_texts", "n_distinct_label_sets",
            "text_preview",
        ],
    )

    kind_c = Counter(r["classification"] for r in audit)
    summary = [
        "# Gold duplicate audit",
        "",
        f"Raw file: `{RAW}`",
        f"SHA256: `{sha256_file(str(RAW))}`",
        "",
        "## Arithmetic (2676 vs 2601 vs 74)",
        "",
        f"- Raw rows: **{n_rows}**",
        f"- Unique IDs: **{n_unique}**",
        f"- Extra rows = {n_rows} − {n_unique} = **{extra}**",
        f"- IDs with count≥2: **{n_dup_ids}**",
        f"- Frequency of occurrence counts: {dict(sorted(freq.items()))}",
        f"- IDs appearing ≥3 times: **{len(triples)}** → `{triples}`",
        "",
        "If every duplicated ID appeared exactly twice, extra rows would equal",
        f"the number of duplicated IDs ({n_dup_ids}). Extra rows are {extra}, so",
        f"**{extra - n_dup_ids} ID(s) contribute an additional extra copy** (triple or more).",
        "",
        "## Classification of duplicated IDs",
        "",
        f"- exact_duplicate: {kind_c.get('exact_duplicate', 0)}",
        f"- annotation_conflict: {kind_c.get('annotation_conflict', 0)}",
        f"- id_collision: {kind_c.get('id_collision', 0)}",
        f"- other: {kind_c.get('other', 0)}",
        "",
        "Raw Gold was **not** modified.",
        "",
    ]
    (PAPER / "reports/gold_duplicate_summary.md").write_text("\n".join(summary), encoding="utf-8")

    # --- canonicalization ---
    canonical: list[dict] = []
    dropped: list[dict] = []
    conflicts: list[dict] = []
    id_map: list[dict] = []
    seen_canon_ids: set[str] = set()

    for iid, group in by_id.items():
        kind = classify(group) if len(group) > 1 else "unique"
        if len(group) == 1 or kind == "exact_duplicate":
            keep_line, keep = group[0]
            rec = json.loads(json.dumps(keep, ensure_ascii=False))
            rec["_canon"] = {
                "source_id": iid,
                "kept_raw_line": keep_line,
                "dropped_raw_lines": [n for n, _ in group[1:]],
                "rule": "keep_first_exact" if kind == "exact_duplicate" else "unique",
            }
            if iid in seen_canon_ids:
                raise RuntimeError(f"duplicate canonical id {iid}")
            seen_canon_ids.add(iid)
            canonical.append(rec)
            for n, _ in group[1:]:
                dropped.append({"id": iid, "raw_line": n, "reason": "exact_duplicate"})
            continue

        if kind == "annotation_conflict":
            for n, rec in group:
                conflicts.append({
                    "id": iid,
                    "raw_line": n,
                    "global_id": rec.get("global_id"),
                    "text": text_of(rec),
                    "spans": extract_spans(rec, GOLD_FIELDS),
                    "reason": "same_id_same_text_different_labels",
                })
            continue

        # id_collision / other: keep first with original id; remap extras
        keep_line, keep = group[0]
        rec0 = json.loads(json.dumps(keep, ensure_ascii=False))
        rec0["_canon"] = {
            "source_id": iid,
            "kept_raw_line": keep_line,
            "dropped_raw_lines": [],
            "rule": "collision_keep_first_original_id",
        }
        if iid in seen_canon_ids:
            raise RuntimeError(f"duplicate canonical id {iid}")
        seen_canon_ids.add(iid)
        canonical.append(rec0)
        id_map.append({
            "raw_id": iid,
            "raw_line": keep_line,
            "canonical_id": iid,
            "role": "kept_original",
            "text_sha256": hashlib.sha256(text_of(keep).encode()).hexdigest()[:16],
        })
        for extra_i, (n, rec) in enumerate(group[1:], 1):
            tsha = hashlib.sha256(text_of(rec).encode("utf-8")).hexdigest()[:10]
            new_id = f"{iid}#col{extra_i}_{tsha}"
            if new_id in seen_canon_ids:
                raise RuntimeError(f"unstable collision id {new_id}")
            seen_canon_ids.add(new_id)
            rec2 = json.loads(json.dumps(rec, ensure_ascii=False))
            rec2["id_raw"] = iid
            rec2["id"] = new_id
            rec2["_canon"] = {
                "source_id": iid,
                "kept_raw_line": n,
                "dropped_raw_lines": [],
                "rule": "collision_new_id",
                "new_id": new_id,
            }
            canonical.append(rec2)
            id_map.append({
                "raw_id": iid,
                "raw_line": n,
                "canonical_id": new_id,
                "role": "remapped_collision",
                "text_sha256": hashlib.sha256(text_of(rec).encode()).hexdigest()[:16],
            })

    out_dir = PAPER / "data"
    out_dir.mkdir(exist_ok=True)
    canon_path = out_dir / "gold_canonical_v1.jsonl"
    with canon_path.open("w", encoding="utf-8") as f:
        for rec in canonical:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    log = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "raw_path": str(RAW),
        "raw_sha256": sha256_file(str(RAW)),
        "raw_rows": n_rows,
        "raw_unique_ids": n_unique,
        "raw_extra_rows": extra,
        "raw_dup_ids": n_dup_ids,
        "triple_or_more_ids": triples,
        "occurrence_freq": dict(sorted(freq.items())),
        "classification": dict(kind_c),
        "canonical_path": str(canon_path),
        "canonical_rows": len(canonical),
        "canonical_unique_ids": len({r["id"] for r in canonical}),
        "n_dropped_exact": len(dropped),
        "n_conflicts_held_out": len(conflicts),
        "n_collision_remaps": sum(1 for x in id_map if x["role"] == "remapped_collision"),
        "frozen": len(conflicts) == 0,
        "freeze_blocked_reason": (
            None if not conflicts
            else f"{len({c['id'] for c in conflicts})} IDs have annotation conflicts and were held out"
        ),
        "dropped_exact": dropped,
        "id_map": id_map,
    }
    (PAPER / "notes/gold_canonical_v1_transform.json").write_text(
        json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (PAPER / "data/gold_conflicts_v1.jsonl").write_text(
        "".join(json.dumps(c, ensure_ascii=False) + "\n" for c in conflicts),
        encoding="utf-8",
    )
    write_csv(
        PAPER / "manifests/gold_id_remap_v1.csv",
        id_map,
        ["raw_id", "raw_line", "canonical_id", "role", "text_sha256"],
    )

    def span_count(path: Path) -> dict:
        n = 0
        types = Counter()
        ids = []
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

    raw_m = span_count(RAW)
    can_m = span_count(canon_path)
    write_csv(
        PAPER / "manifests/gold_canonical_v1_manifest.csv",
        [
            {"role": "raw_gold", **raw_m},
            {"role": "canonical_v1", **can_m},
            {
                "role": "conflicts_held_out",
                "path": str(PAPER / "data/gold_conflicts_v1.jsonl"),
                "sha256": sha256_file(str(PAPER / "data/gold_conflicts_v1.jsonl")) if conflicts else "",
                "n_rows": len(conflicts),
                "n_unique_ids": len({c["id"] for c in conflicts}),
                "n_spans": "",
                "L": "", "K": "", "S": "", "T": "",
            },
        ],
        ["role", "path", "sha256", "n_rows", "n_unique_ids", "n_spans", "L", "K", "S", "T"],
    )

    md = [
        "# Gold canonicalization v1",
        "",
        "**Status: NOT FROZEN**" if conflicts else "**Status: candidates unique; still not a paper freeze until review.**",
        "",
        f"Raw Gold was not modified: `{RAW}`",
        "",
        "## Counts",
        "",
        f"| | rows | unique IDs | spans |",
        f"|---|---:|---:|---:|",
        f"| raw | {raw_m['n_rows']} | {raw_m['n_unique_ids']} | {raw_m['n_spans']} |",
        f"| canonical v1 | {can_m['n_rows']} | {can_m['n_unique_ids']} | {can_m['n_spans']} |",
        f"| conflicts held out | {len(conflicts)} | {len({c['id'] for c in conflicts})} | — |",
        "",
        f"Raw SHA256: `{raw_m['sha256']}`",
        f"Canonical SHA256: `{can_m['sha256']}`",
        "",
        "## Rules applied",
        "",
        "1. Exact duplicate rows (same ID, text, LSKT spans): keep first raw line; log dropped lines.",
        "2. Same ID + same text + **different** labels: **held out** in `data/gold_conflicts_v1.jsonl`. Not scored.",
        "3. Same ID + different text: first keeps original ID; extras get `{id}#colN_{textsha10}`.",
        "4. Canonical IDs are unique by construction.",
        "",
        f"Triple+ IDs: {triples or 'none'}",
        "",
        "Transform log: `notes/gold_canonical_v1_transform.json`",
        "ID remap: `manifests/gold_id_remap_v1.csv`",
        "",
        "Do not treat this as a frozen public Gold if conflicts remain.",
        "",
    ]
    (PAPER / "notes/GOLD_CANONICALIZATION.md").write_text("\n".join(md), encoding="utf-8")
    print("raw", n_rows, "unique", n_unique, "extra", extra, "dup_ids", n_dup_ids, "triples", triples)
    print("kinds", dict(kind_c))
    print("canonical", len(canonical), "conflicts", len(conflicts), "dropped", len(dropped))
    print("ids unique in canonical", len({r['id'] for r in canonical}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
