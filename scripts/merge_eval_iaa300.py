#!/usr/bin/env python3
"""Merge dual eval-300 passes, apply empty lock, adjudicate, project tokens.

Does not overwrite gold_canonical_v2.jsonl. Writes gold_eval_v3_pilot300.jsonl only.
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from goldstyle_empty_rules import empty_hint
from project_gold_style_spans import find_span

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
WORK = PAPER / "reports/gold_eval_v3/work"
GOLD = PAPER / "data/gold_canonical_v2.jsonl"
MAN = PAPER / "reports/gold_eval_v3/pilot300_manifest.json"
OUT_DIR = PAPER / "reports/gold_eval_v3"


def load_arr(*paths: Path) -> list[dict]:
    rows = []
    for p in paths:
        if not p.is_file():
            raise FileNotFoundError(p)
        raw = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(raw, dict):
            raw = raw.get("items") or raw.get("data") or []
        rows.extend(raw)
    return rows


def norm_spans(spans) -> list[tuple[str, str]]:
    out = []
    for sp in spans or []:
        if not isinstance(sp, dict):
            continue
        text = (sp.get("text") or "").strip()
        typ = str(sp.get("type") or "S").strip().upper()[:1]
        if typ not in {"L", "K", "S", "T"}:
            typ = "S"
        if text:
            out.append((text, typ))
    return sorted(set(out))


def force_empty(sentence: str, domain: str, spans: list[tuple[str, str]]) -> list[tuple[str, str]]:
    hint = empty_hint(sentence, domain)
    if hint in {"empty_process", "empty_welfare", "empty_shiye_process"}:
        return []
    return spans


def span_f1(a: list[tuple[str, str]], b: list[tuple[str, str]]) -> tuple[int, int, int]:
    sa, sb = set(a), set(b)
    tp = len(sa & sb)
    return tp, len(sa), len(sb)


def bio(tokens: list[str], aligned: list[tuple[int, int, str]]) -> list[str]:
    tags = ["O"] * len(tokens)
    for s, e, typ in aligned:
        if s < 0 or e > len(tokens) or s >= e:
            continue
        tags[s] = f"B-{typ}"
        for i in range(s + 1, e):
            tags[i] = f"I-{typ}"
    return tags


def main() -> None:
    gold = {}
    for line in GOLD.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            gold[r["id"]] = r
    man = {r["id"]: r for r in json.loads(MAN.read_text(encoding="utf-8"))}
    a = {r["id"]: r for r in load_arr(WORK / "A_part1.json", WORK / "A_part2.json")}
    b = {r["id"]: r for r in load_arr(WORK / "B_part1.json", WORK / "B_part2.json")}
    ids = [r["id"] for r in json.loads(MAN.read_text(encoding="utf-8"))]
    missing_a = [i for i in ids if i not in a]
    missing_b = [i for i in ids if i not in b]

    tp = pred = goldn = 0
    agree = 0
    adj_rows = []
    out_jsonl = []
    n_empty_lock = 0
    n_unaligned = 0
    for iid in ids:
        src = man[iid]
        sent = src["sentence"]
        domain = src["source_domain"]
        sa = force_empty(sent, domain, norm_spans((a.get(iid) or {}).get("spans")))
        sb = force_empty(sent, domain, norm_spans((b.get(iid) or {}).get("spans")))
        if empty_hint(sent, domain) in {"empty_process", "empty_welfare", "empty_shiye_process"}:
            n_empty_lock += 1
        tpi, pa, pb = span_f1(sa, sb)
        tp += tpi
        pred += pa
        goldn += pb
        exact = sa == sb
        if exact:
            agree += 1
            chosen = sa
            how = "exact_agree"
        elif not sa:
            chosen = sb
            how = "take_b_a_empty"
        elif not sb:
            chosen = sa
            how = "take_a_b_empty"
        else:
            inter = sorted(set(sa) & set(sb))
            if inter:
                chosen = inter
                how = "intersection"
            else:
                chosen = sa
                how = "adjudicate_prefer_a"
        rec = gold[iid]
        toks = rec.get("tokens") or []
        aligned = []
        misses = []
        for text, typ in chosen:
            hit = find_span(toks, text)
            if hit is None:
                misses.append(text)
                n_unaligned += 1
            else:
                aligned.append((hit[0], hit[1], typ))
        tags = bio(toks, aligned)
        adj_rows.append(
            {
                "id": iid,
                "source_domain": domain,
                "sentence": sent,
                "A": [{"text": t, "type": y} for t, y in sa],
                "B": [{"text": t, "type": y} for t, y in sb],
                "adjudicated": [{"text": t, "type": y} for t, y in chosen],
                "how": how,
                "exact_agree": exact,
                "unaligned": misses,
                "comment_a": (a.get(iid) or {}).get("comment"),
                "comment_b": (b.get(iid) or {}).get("comment"),
            }
        )
        out = dict(rec)
        out["list_of_selection_bio4"] = tags
        out["_eval_v3"] = {
            "pilot": True,
            "adjudication": how,
            "n_spans": len(aligned),
            "replaced_v2_labels": True,
        }
        out_jsonl.append(out)

    p = tp / pred if pred else 0.0
    r = tp / goldn if goldn else 0.0
    f1 = 2 * p * r / (p + r) if (p + r) else 0.0
    iaa = {
        "n": len(ids),
        "missing_a": missing_a,
        "missing_b": missing_b,
        "exact_sentence_agree": agree,
        "exact_sentence_agree_frac": round(agree / len(ids), 4) if ids else 0,
        "typed_span_micro": {"tp": tp, "pred": pred, "gold": goldn, "p": p, "r": r, "f1": f1},
        "empty_lock_applied": n_empty_lock,
        "unaligned_spans": n_unaligned,
        "how": dict(Counter(x["how"] for x in adj_rows)),
        "overwrote_gold_v2": False,
        "note": "LLM dual pass + empty-lock + heuristic adjudicate. Not human IAA. Not official Gold.",
        "paper_numbers": False,
    }
    OUT_DIR.joinpath("pilot300_adjudicated.json").write_text(
        json.dumps(adj_rows, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    OUT_DIR.joinpath("pilot300_iaa.json").write_text(
        json.dumps(iaa, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    dest = PAPER / "data/gold_eval_v3_pilot300.jsonl"
    with dest.open("w", encoding="utf-8") as f:
        for r in out_jsonl:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    iaa["out_jsonl"] = str(dest)
    OUT_DIR.joinpath("pilot300_iaa.json").write_text(
        json.dumps(iaa, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(iaa, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
