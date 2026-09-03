#!/usr/bin/env python3
"""Map page-1 200 human labels, write scoring gold, score frozen preds.

Does not overwrite gold_canonical_v2.jsonl or the V4 hybrid 2601 file.
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
sys.path.insert(0, str(PAPER / "scorer"))
from score_lskt import GOLD_FIELDS, PRED_FIELDS, score  # noqa: E402

SRC = PAPER / "gold_page1_200.compact.jsonl"
H980 = PAPER / "reports/human980_doccano/doccano/human980.jsonl"
G2 = PAPER / "data/gold_canonical_v2.jsonl"
HY = PAPER / "data/test_lskt_v4_cws_simhuman980_hybrid.jsonl"
OUT_GOLD = PAPER / "data/human_gold_page1_200.jsonl"
OUT_COMPACT = PAPER / "data/human_gold_page1_200.compact.jsonl"
OUT_QA = PAPER / "reports/human980_doccano/page1_200_QA.json"
OUT_CSV = PAPER / "tables/human200_page1_scores.csv"
OUT_JSON = PAPER / "reports/human980_doccano/page1_200_scores.json"

TYPES = {"L", "K", "S", "T"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def char_spans_to_bio(tokens: list[str], spans: list[tuple[int, int, str]]) -> list[str]:
    offs = []
    i = 0
    for tok in tokens:
        offs.append((i, i + len(tok)))
        i += len(tok)
    bio = ["O"] * len(tokens)
    for a, b, typ in spans:
        first = True
        for ti, (s, e) in enumerate(offs):
            if e <= a or s >= b:
                continue
            bio[ti] = f"B-{typ}" if first else f"I-{typ}"
            first = False
    return bio


def midword_flags(text: str, spans: list[dict], jieba_mod) -> list[dict]:
    flags = []
    cuts = []
    if jieba_mod is not None:
        pos = 0
        for w in jieba_mod.cut(text, cut_all=False):
            cuts.append((pos, pos + len(w), w))
            pos += len(w)
    for s in spans:
        a, b, tx = s["start"], s["end"], s.get("text") or ""
        flag = None
        if tx and tx[-1].isdigit():
            flag = "swallowed_digit"
        if jieba_mod is not None:
            for cs, ce, w in cuts:
                if cs < a < ce or cs < b < ce:
                    flag = flag or "mid_jieba_token"
                    flags.append(
                        {
                            "kind": flag,
                            "span": tx,
                            "start": a,
                            "end": b,
                            "jieba_word": w,
                        }
                    )
                    break
            else:
                if flag:
                    flags.append({"kind": flag, "span": tx, "start": a, "end": b})
        elif flag:
            flags.append({"kind": flag, "span": tx, "start": a, "end": b})
        verb = ("熟悉", "掌握", "了解", "精通", "具备", "具有")
        if any(tx.startswith(v) or tx.startswith(" " + v) for v in verb):
            flags.append({"kind": "includes_ability_verb", "span": tx, "start": a, "end": b})
        if (b - a) > 14:
            flags.append({"kind": "long_gt14", "span": tx, "start": a, "end": b, "n": b - a})
    return flags


def main() -> int:
    raw = load_jsonl(SRC)
    if len(raw) != 200:
        raise SystemExit(f"expected 200 rows, got {len(raw)}")
    q980 = load_jsonl(H980)[:200]
    g2 = {r["id"]: r for r in load_jsonl(G2)}
    hy = {r["id"]: r for r in load_jsonl(HY)}

    try:
        import jieba
    except ImportError:
        jieba = None

    gold_rows = []
    compact_rows = []
    qa_rows = []
    n_flagged = 0
    n_same_pre = 0
    n_same_g2 = 0
    n_same_hy = 0

    for page_i, (h, p) in enumerate(zip(raw, q980), 1):
        sid = str(p["id"])
        g = g2[sid]
        tokens = list(g["tokens"])
        sent = g.get("sentence") or "".join(tokens)
        if h["text"] != sent:
            raise SystemExit(f"text mismatch {sid}")
        if "".join(tokens) != sent:
            raise SystemExit(f"token concat mismatch {sid}")
        spans = []
        for s in h.get("spans") or []:
            typ = s["label"]
            if typ not in TYPES:
                raise SystemExit(f"bad type {sid} {typ}")
            if sent[s["start"] : s["end"]] != s["text"]:
                raise SystemExit(f"offset mismatch {sid}")
            spans.append((s["start"], s["end"], typ, s.get("user") or "", s["text"]))
        char_t = [(a, b, t) for a, b, t, _, _ in spans]
        bio = char_spans_to_bio(tokens, char_t)
        pre = tuple((x[0], x[1], x[2]) for x in (p.get("label") or []))
        now = tuple((a, b, t) for a, b, t, _, _ in spans)
        if pre == now:
            n_same_pre += 1

        def bio_to_char(toks, tags):
            out = []
            i = 0
            while i < len(tags):
                t = tags[i]
                if isinstance(t, str) and t.startswith("B-"):
                    typ = t[2:]
                    j = i + 1
                    while j < len(tags) and tags[j] == f"I-{typ}":
                        j += 1
                    a = sum(len(toks[k]) for k in range(i))
                    b = sum(len(toks[k]) for k in range(j))
                    out.append((a, b, typ))
                    i = j
                else:
                    i += 1
            return tuple(out)

        if bio_to_char(tokens, g["list_of_selection_bio4"]) == now:
            n_same_g2 += 1
        if sid in hy and bio_to_char(hy[sid]["tokens"], hy[sid]["list_of_selection_bio4"]) == now:
            n_same_hy += 1

        flags = midword_flags(
            sent,
            [{"start": a, "end": b, "text": tx} for a, b, _, _, tx in spans],
            jieba,
        )
        if flags:
            n_flagged += 1
        rec = {
            "id": sid,
            "global_id": g.get("global_id"),
            "sentence": sent,
            "tokens": tokens,
            "source_domain": g.get("source_domain") or p.get("meta", {}).get("source_domain"),
            "title": g.get("title") or p.get("meta", {}).get("title"),
            "list_of_selection_bio4": bio,
            "char_spans": [
                {"start": a, "end": b, "type": t, "text": tx, "user": u}
                for a, b, t, u, tx in spans
            ],
            "page": h.get("page", page_i),
            "example_id": h.get("example_id"),
            "queue": "human980_page1_200",
            "annotators": sorted({u for *_, u, _ in spans if u}),
            "conflict_kind": (p.get("meta") or {}).get("conflict_kind"),
            "do_not_overwrite_gold_v2": True,
            "do_not_replace_v4_hybrid_2601": True,
            "protocol_note": "human labels on 980-queue page 1; not dual-blind IAA; QA flags logged",
        }
        gold_rows.append(rec)
        compact_rows.append(
            {
                "id": sid,
                "page": rec["page"],
                "example_id": rec["example_id"],
                "text": sent,
                "spans": rec["char_spans"],
                "source_domain": rec["source_domain"],
                "conflict_kind": rec["conflict_kind"],
            }
        )
        qa_rows.append(
            {
                "id": sid,
                "page": rec["page"],
                "n_spans": len(spans),
                "annotators": rec["annotators"],
                "same_as_980_prelabel": pre == now,
                "n_flags": len(flags),
                "flags": flags,
            }
        )

    write_jsonl(OUT_GOLD, gold_rows)
    write_jsonl(OUT_COMPACT, compact_rows)
    qa = {
        "n": 200,
        "src_sha256": sha256_file(SRC),
        "gold_sha256": sha256_file(OUT_GOLD),
        "n_empty": sum(1 for r in gold_rows if not r["char_spans"]),
        "n_spans": sum(len(r["char_spans"]) for r in gold_rows),
        "types": dict(Counter(s["type"] for r in gold_rows for s in r["char_spans"])),
        "domains": dict(Counter(r["source_domain"] for r in gold_rows)),
        "same_as_980_prelabel": n_same_pre,
        "same_as_gold_v2": n_same_g2,
        "same_as_v4_hybrid": n_same_hy,
        "n_sentences_with_qa_flag": n_flagged,
        "flag_kinds": dict(
            Counter(f["kind"] for q in qa_rows for f in q["flags"])
        ),
        "annotator_sentences": dict(
            Counter(
                tuple(r["annotators"]) if r["annotators"] else ("EMPTY",)
                for r in gold_rows
            )
        ),
        "rows": qa_rows,
    }
    # Counter keys that are tuples: stringify
    qa["annotator_sentences"] = {
        "+".join(k) if isinstance(k, tuple) else str(k): v
        for k, v in qa["annotator_sentences"].items()
    }
    OUT_QA.write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding="utf-8")

    pred_specs = [
        ("JobBERT 3M v4 (frozen)", PAPER / "data/frozen_preds/jobbert_3m_v4.jsonl"),
        ("JobBERT 1M v4 (frozen)", PAPER / "data/frozen_preds/jobbert_1m_v4.jsonl"),
        ("JobBERT 1M CWS retrain (frozen)", PAPER / "data/frozen_preds/jobbert_1m_v4_cws_retrain.jsonl"),
        ("ChatGPT gpt-4o dump", PAPER / "reports/views/ChatGPT_unique_first_v2.jsonl"),
        ("DeepSeek deepseek-r1 dump", PAPER / "reports/views/DeepSeek_unique_first_v2.jsonl"),
        ("Qwen Qwen2.5-14B-Instruct dump", PAPER / "reports/views/Qwen_unique_first_v2.jsonl"),
        ("Claude haiku dump", PAPER / "reports/views/Claude_unique_first_v2.jsonl"),
        ("Kimi k2 dump", PAPER / "reports/views/Kimi_unique_first_v2.jsonl"),
        ("Gold v2 (agreement, not a system)", G2),
        ("V4 hybrid (agreement, not a system)", HY),
    ]
    rows_out = []
    reports = {}
    for name, path in pred_specs:
        if not path.exists():
            rows_out.append({"system": name, "path": str(path), "status": "missing"})
            continue
        rep = score(
            str(OUT_GOLD),
            str(path),
            align_mode="official",
            pred_fields=PRED_FIELDS if "Gold v2" not in name and "hybrid" not in name else GOLD_FIELDS,
            n_boot=0,
            require_exact_id_set=False,
        )
        te = rep["typed_exact"]
        tr = rep["typed_relaxed"]
        rows_out.append(
            {
                "system": name,
                "n_gold": rep["gold_n_unique_ids"],
                "n_matched": rep["n_matched"],
                "n_missing": rep["n_missing"],
                "alignment_ok": rep.get("alignment_ok"),
                "typed_exact_p": float(f"{te['precision']:.4f}"),
                "typed_exact_r": float(f"{te['recall']:.4f}"),
                "typed_exact_f1": float(f"{te['f1']:.4f}"),
                "typed_relaxed_f1": float(f"{tr['f1']:.4f}"),
                "collapsed_exact_f1": float(f"{rep['collapsed_exact']['f1']:.4f}"),
            }
        )
        reports[name] = {
            "typed_exact": te,
            "typed_relaxed": tr,
            "per_type_exact": rep["per_type_exact"],
            "alignment_ok": rep.get("alignment_ok"),
            "n_missing": rep["n_missing"],
            "n_matched": rep["n_matched"],
        }
        print(
            f"{name:42s} exact={te['f1']:.4f} relaxed={tr['f1']:.4f} "
            f"miss={rep['n_missing']} ok={rep.get('alignment_ok')}"
        )

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    cols = [
        "system",
        "n_gold",
        "n_matched",
        "n_missing",
        "alignment_ok",
        "typed_exact_p",
        "typed_exact_r",
        "typed_exact_f1",
        "typed_relaxed_f1",
        "collapsed_exact_f1",
    ]
    with OUT_CSV.open("w", encoding="utf-8") as f:
        f.write(",".join(cols) + "\n")
        for r in rows_out:
            f.write(",".join(str(r.get(c, "")) for c in cols) + "\n")
    OUT_JSON.write_text(
        json.dumps(
            {
                "gold": str(OUT_GOLD),
                "gold_sha256": sha256_file(OUT_GOLD),
                "scorer": "cnss-lskt-1.2.0",
                "n": 200,
                "note": "n=200 analysis only; do not replace V4 hybrid 0.4331 or Gold v2 0.6365",
                "rows": rows_out,
                "reports": reports,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print("wrote", OUT_GOLD)
    print("wrote", OUT_CSV)
    print("QA flagged sentences", n_flagged, "same_pre", n_same_pre, "same_g2", n_same_g2, "same_hy", n_same_hy)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
