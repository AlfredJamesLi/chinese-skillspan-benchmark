#!/usr/bin/env python3
"""Sandbox v4: unlabeled export, v3→2way seed, Doccano JSONL, optional LLM apply + smoke score.

Does not write gold_canonical_v2.jsonl, train.json, or paper tables.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
sys.path.insert(0, str(PAPER / "scorer"))
sys.path.insert(0, str(PAPER / "scripts"))
from project_gold_style_spans import find_span  # noqa: E402
from score_lskt import load_records, score as official_score, sha256_file  # noqa: E402

GOLD_V2 = PAPER / "data/gold_canonical_v2.jsonl"
PILOT_MANIFEST = PAPER / "reports/gold_eval_v3/pilot300_manifest.json"
V3_JSONL = PAPER / "data/gold_eval_v3_pilot300.jsonl"
OUT = PAPER / "reports/sandbox_v4_prelabel"
PRED_JB = PAPER / "output/encoder_3seed/jobbert_zh_1m/seed_2026/test_pred.jsonl"
CHUNK = 25
TWO_WAY = {"L": "K", "K": "K", "S": "S", "T": "S"}


def recs_by_id(path: Path) -> dict[str, dict]:
    return {str(r["id"]): r for r in load_records(str(path))}


def map_bio2(tags: list[str]) -> list[str]:
    out = []
    for t in tags:
        t = (t or "O").strip()
        if t == "O" or not t.startswith(("B-", "I-")):
            out.append("O")
            continue
        p, lab = t[0], t[2:].upper()
        lab = TWO_WAY.get(lab, "S" if lab in {"SKILL"} else "K" if lab in {"KNOWLEDGE"} else lab)
        if lab not in {"K", "S"}:
            lab = "S"
        out.append(f"{p}-{lab}")
    return out


def bio_from_token_spans(n: int, spans: list[list]) -> list[str]:
    tags = ["O"] * n
    for sp in spans:
        a, b, typ = int(sp[0]), int(sp[1]), str(sp[2]).upper()[:1]
        typ = typ if typ in {"L", "K", "S", "T"} else "S"
        if a < 0 or b > n or a >= b:
            continue
        tags[a] = f"B-{typ}"
        for i in range(a + 1, b):
            tags[i] = f"I-{typ}"
    return tags


def token_char_spans(sentence: str, tokens: list[str]) -> list[tuple[int, int]]:
    spans = []
    cursor = 0
    for tok in tokens:
        if not tok:
            spans.append((cursor, cursor))
            continue
        pos = sentence.find(tok, cursor)
        if pos < 0:
            pos = cursor
            end = min(len(sentence), cursor + len(tok))
        else:
            end = pos + len(tok)
        spans.append((pos, end))
        cursor = end
    return spans


def to_doccano(rec: dict, tags: list[str]) -> dict:
    sent = rec["sentence"]
    toks = rec["tokens"]
    char_of = token_char_spans(sent, toks)
    labels = []
    i, n = 0, len(tags)
    while i < n:
        t = tags[i] if i < len(tags) else "O"
        if t.startswith("B-"):
            lab = t[2:]
            j = i + 1
            while j < n and (tags[j] if j < len(tags) else "O") == f"I-{lab}":
                j += 1
            cs, _ = char_of[i]
            _, ce = char_of[j - 1]
            labels.append([cs, ce, lab if lab in {"L", "K", "S", "T"} else "S"])
            i = j
        else:
            i += 1
    return {
        "text": sent,
        "labels": labels,
        "meta": {
            "id": rec["id"],
            "global_id": rec.get("global_id"),
            "source_domain": rec.get("source_domain"),
            "sandbox": "v4_lskt",
        },
    }


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def export_unlabeled(v2: dict[str, dict], ids: list[str]) -> list[dict]:
    rows = []
    for i in ids:
        g = v2[i]
        rows.append(
            {
                "id": i,
                "global_id": g.get("global_id"),
                "source_domain": g.get("source_domain"),
                "sentence": g["sentence"],
                "tokens": g["tokens"],
            }
        )
    return rows


def norm_lskt(typ: str) -> str:
    u = str(typ or "S").strip().upper()
    if u in {"L", "LANGUAGE"}:
        return "L"
    if u in {"K", "KNOWLEDGE"}:
        return "K"
    if u in {"T", "TRAIT", "TRANSVERSAL"}:
        return "T"
    return "S"


def apply_llm(llm_path: Path, unlabeled: list[dict]) -> tuple[list[dict], dict]:
    items = {r["id"]: r for r in unlabeled}
    raw = json.loads(llm_path.read_text(encoding="utf-8"))
    if isinstance(raw, dict):
        raw = raw.get("items") or raw.get("data") or []
    gold_rows = []
    n_miss = 0
    n_ok = 0
    for rec in raw:
        iid = str(rec.get("id", ""))
        src = items.get(iid)
        if src is None:
            continue
        toks = src["tokens"]
        aligned = []
        for sp in rec.get("spans") or []:
            text = sp.get("text") if isinstance(sp, dict) else ""
            typ = norm_lskt(sp.get("type") if isinstance(sp, dict) else "S")
            hit = find_span(toks, str(text or ""))
            if hit is None:
                n_miss += 1
            else:
                aligned.append([hit[0], hit[1], typ])
                n_ok += 1
        tags = bio_from_token_spans(len(toks), aligned)
        row = dict(src)
        row["list_of_selection_bio4"] = tags
        row["list_of_selection"] = ["O" if t == "O" else t[0] for t in tags]
        gold_rows.append(row)
    stats = {"n_rows": len(gold_rows), "aligned_spans": n_ok, "unaligned_spans": n_miss}
    return gold_rows, stats


def smoke_score(gold_path: Path, pred_path: Path, name: str) -> dict:
    if not pred_path.is_file():
        return {"name": name, "error": "pred missing"}
    rep = official_score(str(gold_path), str(pred_path), align_mode="official", n_boot=0)
    te, ce = rep["typed_exact"], rep["collapsed_exact"]
    return {
        "name": name,
        "alignment_ok": rep.get("alignment_ok"),
        "n_gold": rep.get("gold_n_unique_ids"),
        "n_missing": rep.get("n_missing"),
        "typed_p": te["precision"],
        "typed_r": te["recall"],
        "typed_f1": te["f1"],
        "collapsed_f1": ce["f1"],
        "error": rep.get("error"),
    }


def cmd_export() -> None:
    v2 = recs_by_id(GOLD_V2)
    man = json.loads(PILOT_MANIFEST.read_text(encoding="utf-8"))
    ids = [str(x["id"]) for x in man]
    unlabeled = export_unlabeled(v2, ids)
    OUT.mkdir(parents=True, exist_ok=True)
    write_jsonl(OUT / "unlabeled_pilot300.jsonl", unlabeled)
    chunk_dir = OUT / "gpt56_chunks"
    chunk_dir.mkdir(exist_ok=True)
    slim = [{"id": r["id"], "sentence": r["sentence"]} for r in unlabeled]
    for i in range(0, len(slim), CHUNK):
        part = slim[i : i + CHUNK]
        idx = i // CHUNK + 1
        (chunk_dir / f"part_{idx:02d}.json").write_text(
            json.dumps(part, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    v3_rows = load_records(str(V3_JSONL)) if V3_JSONL.is_file() else []
    seed, docc = [], []
    for r in v3_rows:
        tags = map_bio2(r.get("list_of_selection_bio4") or [])
        row = {
            "id": r["id"],
            "global_id": r.get("global_id"),
            "source_domain": r.get("source_domain"),
            "sentence": r["sentence"],
            "tokens": r["tokens"],
            "title": r.get("title"),
            "list_of_selection_bio4": tags,
            "list_of_selection": ["O" if t == "O" else t[0] for t in tags],
            "_sandbox": "v3_projected_2way_seed_only",
        }
        seed.append(row)
        docc.append(to_doccano(row, tags))
    write_jsonl(OUT / "seed_from_v3_2way.jsonl", seed)
    write_jsonl(OUT / "doccano_seed_v3_2way.jsonl", docc)
    lskt_docc = []
    for r in v3_rows:
        tags = list(r.get("list_of_selection_bio4") or [])
        lskt_docc.append(to_doccano(r, tags))
    write_jsonl(OUT / "doccano_seed_v3_lskt.jsonl", lskt_docc)

    v2_300 = [v2[i] for i in ids]
    write_jsonl(OUT / "gold_v2_pilot300_subset.jsonl", v2_300)

    print(
        json.dumps(
            {
                "unlabeled": len(unlabeled),
                "chunks": (len(slim) + CHUNK - 1) // CHUNK,
                "doccano_seed": len(docc),
                "gold_v2_sha": sha256_file(str(GOLD_V2)),
                "out": str(OUT),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def cmd_apply(llm_json: Path) -> None:
    unlabeled = load_records(str(OUT / "unlabeled_pilot300.jsonl"))
    gold_rows, stats = apply_llm(llm_json, unlabeled)
    write_jsonl(OUT / "gpt56_aligned.jsonl", gold_rows)
    write_jsonl(OUT / "doccano_gpt56.jsonl", [to_doccano(r, r["list_of_selection_bio4"]) for r in gold_rows])
    print(json.dumps(stats, ensure_ascii=False, indent=2))


def cmd_smoke() -> None:
    jobs = [
        ("JobBERT-zh_1M_s2026 vs Gold-v2 300-subset", OUT / "gold_v2_pilot300_subset.jsonl"),
        ("JobBERT-zh_1M_s2026 vs eval-v3 LLM-adjudicated 300", V3_JSONL),
        ("JobBERT-zh_1M_s2026 vs v3→2way seed 300", OUT / "seed_from_v3_2way.jsonl"),
    ]
    gpt = OUT / "gpt56_aligned.jsonl"
    if gpt.is_file():
        jobs.append(("JobBERT-zh_1M_s2026 vs GPT-5.6 aligned 300", gpt))
    lines = [
        "# Sandbox smoke scores (NOT for the paper)",
        "",
        "Predictor: `encoder_3seed/jobbert_zh_1m/seed_2026/test_pred.jsonl` (Gold-v2 typed F1 0.1348 on 2601).",
        "Gold files below are **300-id subsets or v3/sandbox labels**. Do not copy into confirmed-results.md.",
        "",
        "| Setting | typed P/R/F1 | collapsed F1 | align_ok | missing |",
        "|---|---|---:|---|---:|",
    ]
    rows = []
    for name, gpath in jobs:
        if not gpath.is_file():
            continue
        s = smoke_score(gpath, PRED_JB, name)
        rows.append(s)
        if s.get("typed_f1") is None:
            lines.append(f"| {name} | {s.get('error')} | | | |")
            continue
        prf = f"{s['typed_p']:.4f}/{s['typed_r']:.4f}/{s['typed_f1']:.4f}"
        lines.append(
            f"| {name} | {prf} | {s['collapsed_f1']:.4f} | {s['alignment_ok']} | {s['n_missing']} |"
        )
    (OUT / "smoke_scores.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    (OUT / "SMOKE_SCORE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--export", action="store_true")
    ap.add_argument("--llm_json", default=None)
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    if args.export:
        cmd_export()
    if args.llm_json:
        cmd_apply(Path(args.llm_json))
    if args.smoke:
        cmd_smoke()
    if not (args.export or args.llm_json or args.smoke):
        cmd_export()
        cmd_smoke()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
