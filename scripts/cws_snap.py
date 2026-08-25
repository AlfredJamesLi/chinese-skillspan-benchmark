#!/usr/bin/env python3
"""Snap LSKT spans to jieba word boundaries (禁半词).

Does not overwrite Gold v2, corpus train.json, or LSKT v4 silver/CRF dirs.
Hard cap stays 8 tokens. Completes mid-word edges; if that exceeds the cap,
trims the incomplete edge instead of growing into a long NP.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from pathlib import Path

import jieba

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
sys.path.insert(0, str(PAPER / "scripts"))
import rewrite_train_goldstyle_v3 as g  # noqa: E402

HARD_CAP = 8
MIN_LEN = 2
USERDICT = PAPER / "data/cws_userdict.txt"
USERDICT_WORDS = PAPER / "data/cws_userdict_words.txt"
PKUSEG_HOME = PAPER / ".cache/pkuseg"
HANLP_HOME = PAPER / ".cache/hanlp"
PUNCT = g.PUNCT_TOK | set("（）()【】[]《》<>/\\|")

# jieba remains the default engineering baseline. Other names are snap-only.
BACKENDS = (
    "jieba",
    "pkuseg_mixed",
    "pkuseg_news",
    "pkuseg_web",
    "pkuseg_news_nodict",
)

_JIEBA_READY = False
_PKU: dict[str, object] = {}
_HANLP = None


def _ensure_jieba() -> None:
    global _JIEBA_READY
    if _JIEBA_READY:
        return
    jieba.initialize()
    if USERDICT.is_file():
        jieba.load_userdict(str(USERDICT))
    _JIEBA_READY = True


def _ensure_pkuseg(model_name: str, use_userdict: bool):
    key = f"{model_name}:{int(use_userdict)}"
    if key in _PKU:
        return _PKU[key]
    os.environ.setdefault("PKUSEG_HOME", str(PKUSEG_HOME))
    PKUSEG_HOME.mkdir(parents=True, exist_ok=True)
    import spacy_pkuseg as pkuseg  # Python 3.11 wheel; original pkuseg fails to compile

    ud = str(USERDICT_WORDS) if use_userdict and USERDICT_WORDS.is_file() else "default"
    seg = pkuseg.pkuseg(model_name=model_name, user_dict=ud)
    _PKU[key] = seg
    return seg


def _cut_to_spans(sent: str, pieces: list[str]) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    i = 0
    n = len(sent)
    for w in pieces:
        if not w:
            continue
        pos = sent.find(w, i)
        if pos < 0:
            continue
        if pos > i:
            out.append((i, pos))
        out.append((pos, pos + len(w)))
        i = pos + len(w)
    if i < n:
        out.append((i, n))
    return out or ([(0, n)] if n else [])


def token_char_spans(toks: list[str]) -> list[tuple[int, int]]:
    out = []
    i = 0
    for t in toks:
        out.append((i, i + len(t)))
        i += len(t)
    return out


def jieba_word_spans(sent: str) -> list[tuple[int, int]]:
    _ensure_jieba()
    return _cut_to_spans(sent, jieba.lcut(sent, cut_all=False, HMM=True))


def word_spans(sent: str, backend: str = "jieba") -> list[tuple[int, int]]:
    """Char-offset word bounds. Does not choose span types or emptiness."""
    if backend == "jieba":
        return jieba_word_spans(sent)
    if backend.startswith("pkuseg_"):
        name = backend[len("pkuseg_") :]
        use_dict = True
        if name.endswith("_nodict"):
            name = name[: -len("_nodict")]
            use_dict = False
        if name not in {"mixed", "news", "web", "medicine", "tourism"}:
            raise ValueError(f"unknown pkuseg domain: {backend}")
        seg = _ensure_pkuseg(name, use_dict)
        return _cut_to_spans(sent, list(seg.cut(sent)))
    if backend.startswith("hanlp"):
        raise RuntimeError(
            "HanLP 2.1.3 tok is incompatible with this env's transformers "
            "(encode_plus removed). Use pkuseg_* backends."
        )
    raise ValueError(f"unknown CWS backend: {backend}")


def _word_at(words: list[tuple[int, int]], c: int) -> tuple[int, int] | None:
    for a, b in words:
        if a <= c < b:
            return a, b
    return None


def _tok_containing(tok_cs: list[tuple[int, int]], c: int) -> int:
    for i, (a, b) in enumerate(tok_cs):
        if a <= c < b:
            return i
    if tok_cs and c >= tok_cs[-1][1]:
        return len(tok_cs) - 1
    return 0


def _tok_end_exclusive(tok_cs: list[tuple[int, int]], c_end: int) -> int:
    """Map exclusive char offset to exclusive token index."""
    for i, (a, b) in enumerate(tok_cs):
        if b == c_end:
            return i + 1
        if a < c_end <= b:
            return i + 1
    return len(tok_cs)


def _is_punct_span(sent: str, a: int, b: int) -> bool:
    t = sent[a:b]
    return bool(t) and all(ch in PUNCT or ch.isspace() for ch in t)


def snap_span(
    toks: list[str],
    a: int,
    b: int,
    words: list[tuple[int, int]] | None = None,
    hard_cap: int = HARD_CAP,
    backend: str = "jieba",
) -> tuple[int, int]:
    n = len(toks)
    a = max(0, min(a, n))
    b = max(a, min(b, n))
    if a >= b:
        return a, b
    sent = "".join(toks)
    tok_cs = token_char_spans(toks)
    words = words if words is not None else word_spans(sent, backend)

    def apply(na: int, nb: int) -> tuple[int, int]:
        na = max(0, min(na, n))
        nb = max(na, min(nb, n))
        while nb > na and toks[nb - 1] in g.PUNCT_TOK:
            nb -= 1
        while na < nb and toks[na] in g.PUNCT_TOK:
            na += 1
        return na, nb

    c0, c1 = tok_cs[a][0], tok_cs[b - 1][1]
    w0 = _word_at(words, c0)
    w1 = _word_at(words, c1 - 1)
    start_inc = bool(w0 and w0[0] < c0 and not _is_punct_span(sent, *w0))
    end_inc = bool(w1 and w1[1] > c1 and not _is_punct_span(sent, *w1))
    if not start_inc and not end_inc:
        return apply(a, b)

    na, nb = a, b
    if start_inc:
        na = _tok_containing(tok_cs, w0[0])
    if end_inc:
        nb = _tok_end_exclusive(tok_cs, w1[1])
    na, nb = apply(na, nb)
    if MIN_LEN <= (nb - na) <= hard_cap:
        return na, nb

    # Over cap: drop the incomplete edge instead of keeping a half word.
    na, nb = a, b
    if end_inc and w1[0] > tok_cs[a][0]:
        nb = _tok_containing(tok_cs, w1[0])
    if start_inc and w0[1] < tok_cs[b - 1][1]:
        na = _tok_end_exclusive(tok_cs, w0[1])
    na, nb = apply(na, nb)
    if (nb - na) > hard_cap:
        nb = na + hard_cap
        na, nb = apply(na, nb)
    return na, nb


def snap_spans(
    toks: list[str],
    spans: list[tuple[int, int, str]],
    hard_cap: int = HARD_CAP,
    backend: str = "jieba",
) -> list[tuple[int, int, str]]:
    if not spans:
        return []
    sent = "".join(toks)
    words = word_spans(sent, backend)
    kept: list[tuple[int, int, str]] = []
    for a, b, t in sorted(spans, key=lambda x: (x[0], x[1])):
        na, nb = snap_span(toks, a, b, words=words, hard_cap=hard_cap, backend=backend)
        if (nb - na) < MIN_LEN:
            continue
        text = "".join(toks[na:nb])
        if g.should_drop_span(text, sent):
            continue
        if any(not (nb <= k[0] or na >= k[1]) for k in kept):
            continue
        kept.append((na, nb, t if t in g.TYPES else "S"))
    return kept


def _pad_tags(raw: list, n: int) -> list[str]:
    tags = [str(t) if t is not None else "O" for t in raw]
    if len(tags) < n:
        tags = tags + ["O"] * (n - len(tags))
    return tags[:n]


def tags_of(rec: dict, field: str | None = None) -> list[str]:
    n = len(g.tokens_of(rec))
    if field:
        return _pad_tags(rec.get(field) or [], n)
    for f in ("pred_tags", "list_of_selection_bio4", "list_of_selection"):
        raw = rec.get(f)
        if isinstance(raw, list) and raw:
            return _pad_tags(raw, n)
    return ["O"] * n


def rewrite_record(
    rec: dict,
    tag_field: str | None = None,
    hard_cap: int = HARD_CAP,
    backend: str = "jieba",
) -> dict:
    toks = g.tokens_of(rec)
    tags = tags_of(rec, tag_field)
    spans = g.bio_spans(tags)
    snapped = snap_spans(toks, spans, hard_cap=hard_cap, backend=backend)
    bio = g.spans_to_bio(len(toks), snapped)
    out = dict(rec)
    out["tokens"] = toks
    out["list_of_selection_bio4"] = bio
    if "pred_tags" in rec:
        out["pred_tags"] = bio
    out["cws_spans"] = [[a, b, t] for a, b, t in snapped]
    out["cws_n_changed"] = int(spans != snapped)
    out["cws_backend"] = backend
    return out


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as f:
        raw = f.read()
    if raw.lstrip().startswith("["):
        return json.loads(raw)
    for line in raw.splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for rec in rows:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def spans_of(rec: dict, field: str = "cws_spans") -> list[tuple[int, int, str]]:
    if field == "cws_spans" and rec.get("cws_spans") is not None:
        return [(int(a), int(b), str(t)) for a, b, t in rec["cws_spans"]]
    return g.bio_spans(tags_of(rec, None if field == "cws_spans" else field))


def is_incomplete_text(text: str) -> bool:
    t = (text or "").strip(" ，,、;；。：:")
    if not t:
        return True
    if t[-1] in g.INCOMPLETE_END:
        return True
    return not g.looks_complete(t)


def span_stats(rows: list[dict], field: str = "cws_spans", backend: str = "jieba") -> dict:
    n_empty = n_inc_span = n_inc_sent = n_changed = 0
    n_mid = n_mid_sent = 0
    lens: list[int] = []
    types: Counter[str] = Counter()
    n_spans = 0
    for rec in rows:
        toks = g.tokens_of(rec)
        spans = spans_of(rec, field)
        n_changed += int(rec.get("cws_n_changed") or 0)
        n_spans += len(spans)
        if not spans:
            n_empty += 1
            continue
        inc_sent = False
        mid_sent = False
        sent = "".join(toks)
        words = word_spans(sent, backend)
        tok_cs = token_char_spans(toks)
        for a, b, t in spans:
            text = "".join(toks[a:b])
            lens.append(b - a)
            types[str(t)] += 1
            if is_incomplete_text(text):
                n_inc_span += 1
                inc_sent = True
            if 0 <= a < b <= len(toks):
                c0, c1 = tok_cs[a][0], tok_cs[b - 1][1]
                w0 = _word_at(words, c0)
                w1 = _word_at(words, c1 - 1)
                if (w0 and w0[0] < c0) or (w1 and w1[1] > c1):
                    n_mid += 1
                    mid_sent = True
        if inc_sent:
            n_inc_sent += 1
        if mid_sent:
            n_mid_sent += 1
    n = max(1, len(rows))
    return {
        "n": len(rows),
        "empty_sent_rate": n_empty / n,
        "n_spans": n_spans,
        "mean_len": (sum(lens) / len(lens)) if lens else 0.0,
        "n_incomplete_spans": n_inc_span,
        "pct_incomplete_spans": (n_inc_span / n_spans) if n_spans else 0.0,
        "pct_sents_with_incomplete": n_inc_sent / n,
        "n_midword_spans": n_mid,
        "pct_midword_spans": (n_mid / n_spans) if n_spans else 0.0,
        "pct_sents_with_midword": n_mid_sent / n,
        "n_sents_changed": n_changed,
        "pct_sents_changed": n_changed / n,
        "type_counts": dict(types),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["rewrite", "snap-one"])
    ap.add_argument("--in_path", dest="in_path")
    ap.add_argument("--out_path", dest="out_path")
    ap.add_argument("--tag_field", default=None)
    ap.add_argument("--hard_cap", type=int, default=HARD_CAP)
    ap.add_argument("--backend", default="jieba", choices=list(BACKENDS))
    ap.add_argument("--sentence")
    ap.add_argument("--span_text")
    args = ap.parse_args()
    if args.mode == "snap-one":
        toks = list(args.sentence or "")
        sent = args.sentence or ""
        needle = args.span_text or ""
        pos = sent.find(needle)
        if pos < 0:
            print("span not in sentence")
            return 2
        a = pos
        b = pos + len(needle)
        na, nb = snap_span(toks, a, b, hard_cap=args.hard_cap, backend=args.backend)
        print(json.dumps({"before": needle, "after": "".join(toks[na:nb]), "a": na, "b": nb, "backend": args.backend}, ensure_ascii=False))
        return 0
    src = Path(args.in_path)
    dst = Path(args.out_path)
    forbidden = {
        PAPER / "data/gold_canonical_v2.jsonl",
        PAPER / "data/train_lskt_v4_silver.jsonl",
        PAPER / "data/dev_lskt_v4_silver.jsonl",
        PAPER / "data/test_lskt_v4_rule_g2ids.jsonl",
        Path("/home/guojingli3/SCESC-LLM-skill-extraction/data/annotated/processed/chinese_skillspan/train.json"),
    }
    if dst.resolve() in {p.resolve() for p in forbidden}:
        print("refusing to overwrite", dst)
        return 2
    rows = [
        rewrite_record(r, tag_field=args.tag_field, hard_cap=args.hard_cap, backend=args.backend)
        for r in load_jsonl(src)
    ]
    write_jsonl(dst, rows)
    print(json.dumps({"n": len(rows), "backend": args.backend, "out": str(dst), **span_stats(rows, backend=args.backend)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
