#!/usr/bin/env python3
"""Doccano pack for the frozen 980 must-human LLM-disagreement queue.

Uses Gold v2 full sentences (not truncated SimHuman text).
Does not overwrite gold_canonical_v2, V4 hybrid, or repartition splits.
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from goldstyle_empty_rules import empty_hint  # noqa: E402

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
CSV980 = PAPER / "reports/sandbox_lskt_v4_silver/codex_pack/conflict_v1/human_must_review.csv"
GOLD = PAPER / "data/gold_canonical_v2.jsonl"
SIM = PAPER / "data/test_lskt_v4_simhuman980.jsonl"
OUT = PAPER / "reports/human980_doccano"
BATCH = 50
TYPES = {"L", "K", "S", "T"}


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_jsonl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def rec_id(r: dict) -> str:
    return str(r.get("id") or r.get("source_id") or "")


def token_char_map(sentence: str, tokens: list) -> list[tuple[int, int]]:
    pos = 0
    out = []
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
    spans = []
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
            if typ in TYPES and 0 <= a < b <= len(sentence):
                spans.append([int(a), int(b), typ])
            i = j
        else:
            i += 1
    return spans


def drop_overlap(spans: list[list]) -> list[list]:
    spans = sorted(spans, key=lambda x: (x[0], -(x[1] - x[0])))
    kept = []
    occ: set[int] = set()
    for a, b, t in spans:
        ids = set(range(a, b))
        if ids & occ:
            continue
        occ |= ids
        kept.append([a, b, t])
    return kept


def _as_span_list(raw) -> list[list]:
    out = []
    for item in raw or []:
        if isinstance(item, dict):
            a, b, t = int(item["start"]), int(item["end"]), str(item.get("type") or "")
        else:
            a, b, t = int(item[0]), int(item[1]), str(item[2])
        if t in TYPES:
            out.append([a, b, t])
    return out


def shift_spans(spans: list[list], delta: int, n: int) -> list[list]:
    out = []
    for a, b, t in spans:
        a2, b2 = a + delta, b + delta
        if 0 <= a2 < b2 <= n and t in TYPES:
            out.append([a2, b2, t])
    return out


def project_prelabel(gold_sent: str, sim_rec: dict) -> tuple[list[list], str]:
    """Map SimHuman BIO onto Gold v2 text. Never project labels from a different sentence."""
    sim_sent = sim_rec.get("sentence") or ""
    toks = [str(t) for t in (sim_rec.get("tokens") or [])]
    tags = sim_rec.get("list_of_selection_bio4") or []
    raw = _as_span_list(sim_rec.get("v4_spans"))
    if not raw:
        raw = bio_to_char_spans(sim_sent, toks, tags)

    if gold_sent == sim_sent:
        spans = bio_to_char_spans(gold_sent, toks, tags) or raw
        return drop_overlap(spans), "exact"

    if gold_sent and gold_sent in sim_sent:
        idx = sim_sent.find(gold_sent)
        return drop_overlap(shift_spans(raw, -idx, len(gold_sent))), "gold_substring_of_sim"

    if sim_sent.endswith("...") and gold_sent.startswith(sim_sent[:-3]):
        prefix = sim_sent[:-3]
        out = []
        for a, b, t in raw:
            if t not in TYPES or a >= len(gold_sent):
                continue
            if b <= len(prefix):
                out.append([a, b, t])
            elif a < len(prefix):
                # span ran into "..."; keep the rest of the gold token (no punctuation)
                rest = gold_sent[a:]
                cut = len(rest)
                for i, ch in enumerate(rest):
                    if ch in "，。；、,;：:！!？?）)】》\"'":
                        cut = i
                        break
                end = a + max(cut, 1)
                if a < end <= len(gold_sent):
                    out.append([a, end, t])
        return drop_overlap(out), "ellipsis_truncation"

    if sim_sent and sim_sent in gold_sent:
        idx = gold_sent.find(sim_sent)
        return drop_overlap(shift_spans(raw, idx, len(gold_sent))), "sim_substring_of_gold"

    return [], "id_text_mismatch"


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")


def comment_of(row: dict, align: str) -> str:
    warn = ""
    if align == "id_text_mismatch":
        warn = "【预标已清空：SimHuman/三模型建议对应的不是本句 Gold 全文，请按当前句子重标】 "
    bits = [
        warn + f"冲突:{row.get('status') or ''}",
        f"Codex:{row.get('codex') or '[]'}",
        f"豆包:{row.get('doubao') or '[]'}",
        f"Kimi:{row.get('kimi') or '[]'}",
    ]
    return " | ".join(bits)


def main() -> int:
    queue = list(csv.DictReader(CSV980.open(encoding="utf-8-sig")))
    ids = [r["id"] for r in queue]
    if len(ids) != 980 or len(set(ids)) != 980:
        raise SystemExit(f"expected 980 unique IDs, got {len(ids)} unique {len(set(ids))}")
    gold = {rec_id(r): r for r in load_jsonl(GOLD)}
    sim = {rec_id(r): r for r in load_jsonl(SIM)}
    missing_g = [i for i in ids if i not in gold]
    missing_s = [i for i in ids if i not in sim]
    if missing_g or missing_s:
        raise SystemExit(f"missing gold={len(missing_g)} sim={len(missing_s)}")

    docc = []
    n_empty = 0
    type_c: Counter = Counter()
    align_c: Counter = Counter()
    flagged = []
    for row in queue:
        gid = row["id"]
        g = gold[gid]
        s = sim[gid]
        sent = g.get("sentence") or ""
        domain = g.get("source_domain") or row.get("domain") or ""
        spans, align = project_prelabel(sent, s)
        align_c[align] += 1
        if not spans:
            n_empty += 1
        for _a, _b, t in spans:
            type_c[t] += 1
        suggest_ok = align != "id_text_mismatch"
        rec = {
            "id": gid,
            "text": sent,
            "label": spans,
            "labels": spans,
            "Comments": comment_of(row, align),
            "meta": {
                "id": gid,
                "global_id": str(g.get("global_id") or ""),
                "source_domain": domain,
                "title": g.get("title") or "",
                "conflict_kind": row.get("status") or "",
                "review_bucket": row.get("review_bucket") or "must_human_split",
                "prelabel": "none" if align == "id_text_mismatch" else "simhuman_rule_v4_draft",
                "prelabel_align": align,
                "empty_hint": empty_hint(sent, domain),
                "suggest_codex": row.get("codex") or "",
                "suggest_doubao": row.get("doubao") or "",
                "suggest_kimi": row.get("kimi") or "",
                "suggest_applies_to_this_text": suggest_ok,
                "do_not_train": True,
                "do_not_overwrite_gold_v2": True,
                "queue": "human_must_review_980",
            },
        }
        docc.append(rec)
        if align != "exact":
            flagged.append(
                {
                    "id": gid,
                    "align": align,
                    "source_domain": domain,
                    "gold_sentence": sent,
                    "simhuman_sentence": s.get("sentence") or "",
                }
            )

    OUT.mkdir(parents=True, exist_ok=True)
    labels = [
        {"text": "L", "suffix_key": "l", "background_color": "#2563eb", "text_color": "#ffffff"},
        {"text": "K", "suffix_key": "k", "background_color": "#059669", "text_color": "#ffffff"},
        {"text": "S", "suffix_key": "s", "background_color": "#d97706", "text_color": "#ffffff"},
        {"text": "T", "suffix_key": "t", "background_color": "#7c3aed", "text_color": "#ffffff"},
    ]
    (OUT / "doccano").mkdir(parents=True, exist_ok=True)
    labels_txt = json.dumps(labels, ensure_ascii=False, indent=2) + "\n"
    (OUT / "doccano/labels.json").write_text(labels_txt, encoding="utf-8")
    (OUT / "doccano/labels.jsonl").write_text(
        "\n".join(json.dumps(x, ensure_ascii=False) for x in labels) + "\n", encoding="utf-8"
    )
    write_jsonl(OUT / "doccano/human980.jsonl", docc)
    bdir = OUT / "doccano/batches"
    if bdir.exists():
        for p in bdir.glob("*.jsonl"):
            p.unlink()
    bdir.mkdir(parents=True, exist_ok=True)
    for i in range(0, len(docc), BATCH):
        write_jsonl(bdir / f"batch_{i // BATCH + 1:02d}.jsonl", docc[i : i + BATCH])

    blank = []
    for r in docc:
        b = dict(r)
        b["label"] = []
        b["labels"] = []
        meta = dict(r["meta"])
        meta["prelabel"] = "none"
        b["meta"] = meta
        blank.append(b)
    write_jsonl(OUT / "doccano/human980_blank.jsonl", blank)

    mismatch = [x for x in flagged if x["align"] == "id_text_mismatch"]
    write_jsonl(OUT / "doccano/flagged_text_mismatch.jsonl", [r for r in docc if r["meta"]["prelabel_align"] == "id_text_mismatch"])

    ws_path = OUT / "worksheets/human980.csv"
    ws_path.parent.mkdir(parents=True, exist_ok=True)
    with ws_path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "id", "source_domain", "conflict_kind", "prelabel_align",
                "sentence", "prelabel_spans",
                "suggest_codex", "suggest_doubao", "suggest_kimi",
                "human_spans", "comment",
            ],
        )
        w.writeheader()
        for r in docc:
            w.writerow(
                {
                    "id": r["id"],
                    "source_domain": r["meta"]["source_domain"],
                    "conflict_kind": r["meta"]["conflict_kind"],
                    "prelabel_align": r["meta"]["prelabel_align"],
                    "sentence": r["text"],
                    "prelabel_spans": json.dumps(r["label"], ensure_ascii=False),
                    "suggest_codex": r["meta"]["suggest_codex"],
                    "suggest_doubao": r["meta"]["suggest_doubao"],
                    "suggest_kimi": r["meta"]["suggest_kimi"],
                    "human_spans": "",
                    "comment": "",
                }
            )
    flag_path = OUT / "worksheets/flagged_nonexact.csv"
    with flag_path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id", "align", "source_domain", "gold_sentence", "simhuman_sentence"])
        w.writeheader()
        for row in flagged:
            w.writerow(row)

    issues = {
        "n": len(docc),
        "n_empty_prelabel": n_empty,
        "align": dict(align_c),
        "n_id_text_mismatch": len(mismatch),
        "span_types": dict(type_c),
        "gold_sha256": sha256_file(GOLD),
        "queue_csv": str(CSV980),
        "text_source": "gold_canonical_v2.jsonl sentence (full, not truncated)",
        "protocol": "one-pass prelabel correction; not dual-blind",
        "split_deferred": True,
    }
    (OUT / "doccano/convert_issues.json").write_text(json.dumps(issues, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    hashed = [
        OUT / "doccano/human980.jsonl",
        OUT / "doccano/human980_blank.jsonl",
        OUT / "doccano/labels.json",
        GOLD,
        CSV980,
    ]
    sums = OUT / "SHA256SUMS"
    lines = []
    for p in hashed:
        lines.append(f"{sha256_file(p)}  {p.name if p.parent == OUT / 'doccano' else str(p)}")
    sums.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(issues, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
