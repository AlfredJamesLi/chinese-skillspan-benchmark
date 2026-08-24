#!/usr/bin/env python3
"""Gold-style v1 labels for corpus train/dev. Does not overwrite train.json or Gold v2.

80 human-finals are locked in. Remaining rows use clause-level rewrite
(complete requirement spans, L/K/S/T conventions from the 80-item review).
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path("/home/guojingli3/SCESC-LLM-skill-extraction")
PAPER = ROOT / "Chinese_skill_benchmark_Paper"
TRAIN = ROOT / "data/annotated/processed/chinese_skillspan/train.json"
DEV = ROOT / "data/annotated/processed/chinese_skillspan/dev.json"
FINAL80 = PAPER / "reports/gold_style_relabel/sample80_final.json"
OUT_TRAIN = PAPER / "data/train_goldstyle_v1.jsonl"
OUT_DEV = PAPER / "data/dev_goldstyle_v1.jsonl"
OUT_META = PAPER / "reports/gold_style_relabel/goldstyle_v1_meta.json"

TYPES = {"L", "K", "S", "T"}

ADMIN_RE = re.compile(
    r"五险一金|底薪|提成\d|过节费|生日|带薪年假|法定节假日|工作时间|工作地点|"
    r"股票期权|融资|著名VC|欢迎应届|面试邀约|报名系统|留下姓名|"
    r"水果蛋糕|豪华年度旅游|敬请期待|&nbsp;|晋升空间大|成长迅速"
)
SKILLISH_RE = re.compile(
    r"熟悉|掌握|负责|独立|经验|能力|专业|学历|英语|普通话|编程|开发|设计|"
    r"沟通|团队|责任|证书|资格|框架|算法|销售|管理|分析"
)
L_RE = re.compile(r"英语|英文|普通话|日语|口语|CET|托福|雅思")
K_RE = re.compile(r"学历|专业|本科|硕士|博士|证书|资格考试|理论|思想")
T_RE = re.compile(r"沟通|责任心|团队|抗压|积极|职业道德|服务意识|细心|耐心|开朗|正直|敬业|主动")
S_TECH_RE = re.compile(
    r"框架|Python|JAVA|Java|C\+\+|C#|Office|OFFICE|编程|Spring|MyBatis|Node|"
    r"Web2|MVC|脚本|算法|开发|调试"
)
DROP_RE = re.compile(
    r"身体健康|形象好|气质佳|挑战高薪|留学经验|国外留学|超龄勿扰|"
    r"C1驾照|持有C1|^\d+年以上|^[一二三四五六七八九十]+年以上"
)
NUM_LEAD = re.compile(r"^[\s\d一二三四五六七八九十第（(]+[、.．.）):\：\-—]*")
DUTY_LEAD = re.compile(r"^(负责|任职要求|岗位要求|岗位职责|工作职责|岗位描述)")
CLAUSE_CUT = re.compile(r"[。；;！？]|[（(]?\d+[、.．)）]")
PUNCT_TOK = {"。", "；", ";", "！", "？", "，", ",", "、", "：", ":"}
TIGHT = False
TIGHT_MAX = 16


def load_json(path: Path):
    raw = path.read_text(encoding="utf-8")
    if raw.lstrip().startswith("["):
        return json.loads(raw)
    return [json.loads(l) for l in raw.splitlines() if l.strip()]


def tokens_of(rec: dict) -> list[str]:
    return [str(t) for t in (rec.get("tokens") or list(rec.get("sentence") or ""))]


def find_span(tokens: list[str], text: str) -> tuple[int, int] | None:
    flat = "".join(tokens)
    needle = (text or "").strip()
    if not needle:
        return None
    pos = flat.find(needle)
    if pos < 0:
        return None
    acc = 0
    start = None
    for i, tok in enumerate(tokens):
        nxt = acc + len(tok)
        if start is None and acc <= pos < nxt:
            start = i
        if start is not None and nxt >= pos + len(needle):
            return start, i + 1
        acc = nxt
    return None


def bio_spans(tags: list) -> list[tuple[int, int, str]]:
    out = []
    i, n = 0, len(tags)
    while i < n:
        t = tags[i] or "O"
        if str(t).startswith("B-"):
            typ = t[2:]
            j = i + 1
            while j < n and tags[j] == f"I-{typ}":
                j += 1
            out.append((i, j, typ if typ in TYPES else "S"))
            i = j
        else:
            i += 1
    return out


def spans_to_bio(n: int, spans: list[tuple[int, int, str]]) -> list[str]:
    tags = ["O"] * n
    for a, b, t in sorted(spans, key=lambda x: (x[0], x[1])):
        if t not in TYPES:
            t = "S"
        a = max(0, a)
        b = min(n, b)
        if a >= b:
            continue
        tags[a] = f"B-{t}"
        for i in range(a + 1, b):
            tags[i] = f"I-{t}"
    return tags


def clause_ranges(tokens: list[str]) -> list[tuple[int, int]]:
    acc = []
    ranges = []
    start = 0
    for i, tok in enumerate(tokens):
        acc.append(tok)
        joined = "".join(acc)
        long_enough = (not TIGHT) or (len(acc) >= 8)
        cut_list = tok in {"、"} and TIGHT and long_enough
        if CLAUSE_CUT.search(tok) or cut_list or (i + 1 < len(tokens) and tokens[i + 1] in {"1", "2", "3"} and tok in {" ", "。"}):
            if len(acc) >= 2:
                ranges.append((start, i + 1))
                start = i + 1
                acc = []
        elif tok in {"。", "；", ";", "！", "？"} or (TIGHT and tok in {"，", ","} and long_enough):
            ranges.append((start, i + 1))
            start = i + 1
            acc = []
    if start < len(tokens):
        ranges.append((start, len(tokens)))
    if not ranges:
        ranges = [(0, len(tokens))]
    # merge tiny leftovers into previous
    merged = []
    for a, b in ranges:
        if merged and (b - a) <= 2:
            merged[-1] = (merged[-1][0], b)
        else:
            merged.append((a, b))
    return merged or [(0, len(tokens))]


def assign_type(text: str, fallback: str = "S") -> str:
    if S_TECH_RE.search(text):
        return "S"
    if L_RE.search(text) and not K_RE.search(text):
        return "L"
    if T_RE.search(text) and not S_TECH_RE.search(text) and not K_RE.search(text):
        return "T"
    if K_RE.search(text) and not S_TECH_RE.search(text):
        return "K"
    return fallback if fallback in TYPES else "S"


def should_drop_span(text: str, sentence: str) -> bool:
    t = (text or "").strip()
    if len(t) < 2:
        return True
    if DROP_RE.search(t):
        if "驾照" in t and ("司机" in sentence or "驾驶" in sentence and "辅助驾驶" not in sentence):
            return False
        return True
    if ADMIN_RE.search(t) and not SKILLISH_RE.search(t):
        return True
    return False


def clean_clause_text(text: str) -> str:
    t = NUM_LEAD.sub("", text).strip()
    t = DUTY_LEAD.sub("", t).strip(" ，,、:：")
    return t


def is_admin_clause(text: str) -> bool:
    t = text.strip()
    if len(t) <= 2 and not SKILLISH_RE.search(t):
        return True
    if ADMIN_RE.search(t) and not SKILLISH_RE.search(t):
        return True
    return False


def rule_spans(rec: dict) -> list[tuple[int, int, str]]:
    toks = tokens_of(rec)
    sent = rec.get("sentence") or ""
    silver = bio_spans(rec.get("list_of_selection_bio4") or [])
    n = len(toks)
    if n == 0:
        return []
    if not silver and not SKILLISH_RE.search(sent) and (is_admin_clause(sent) or len(sent.strip()) < 8):
        return []
    out = []
    for a, b in clause_ranges(toks):
        raw = "".join(toks[a:b])
        if is_admin_clause(raw):
            continue
        hit = [(x, y, t) for x, y, t in silver if x < b and y > a]
        if not hit and not SKILLISH_RE.search(raw):
            continue
        core = clean_clause_text(raw)
        if should_drop_span(core, sent) or len(core) < 2:
            continue
        loc = find_span(toks[a:b], core)
        if loc is None:
            if hit:
                for xa, yb, typ in _tight_from_silver(toks, a, b, hit) if TIGHT else [
                    (
                        min(x for x, _, _ in hit),
                        max(y for _, y, _ in hit),
                        Counter(t for _, _, t in hit).most_common(1)[0][0],
                    )
                ]:
                    out.append((xa, yb, assign_type("".join(toks[xa:yb]), typ)))
            continue
        sa, sb = a + loc[0], a + loc[1]
        if TIGHT and (sb - sa) > TIGHT_MAX:
            if hit:
                out.extend(
                    (xa, yb, assign_type("".join(toks[xa:yb]), typ))
                    for xa, yb, typ in _tight_from_silver(toks, a, b, hit)
                )
                continue
            sa, sb = _trim_to_max(toks, sa, sb, TIGHT_MAX)
        fb = Counter(t for _, _, t in hit).most_common(1)[0][0] if hit else "S"
        typ = assign_type(core, fb)
        if should_drop_span("".join(toks[sa:sb]), sent):
            continue
        out.append((sa, sb, typ))
    # drop overlapping by keeping longer
    out.sort(key=lambda x: (x[0], -(x[1] - x[0])))
    kept = []
    for sp in out:
        if any(not (sp[1] <= k[0] or sp[0] >= k[1]) for k in kept):
            continue
        kept.append(sp)
    return kept


def project_final80() -> dict[str, list[tuple[int, int, str]]]:
    items = {r["id"]: r for r in load_json(TRAIN)}
    locked = {}
    n_miss = 0
    for rec in load_json(FINAL80):
        src = items.get(rec["id"])
        if src is None:
            continue
        toks = tokens_of(src)
        spans = []
        for sp in rec.get("spans") or []:
            hit = find_span(toks, sp.get("text") or "")
            if hit is None:
                n_miss += 1
                continue
            typ = str(sp.get("type") or "S").upper()[:1]
            spans.append((hit[0], hit[1], typ if typ in TYPES else "S"))
        locked[rec["id"]] = spans
    return locked, n_miss


def rewrite_split(rows: list[dict], locked: dict[str, list], lock: bool) -> tuple[list[dict], dict]:
    out_rows = []
    src_count = Counter()
    n_empty = n_span = 0
    agree_exact = agree_n = 0
    for rec in rows:
        iid = rec.get("id")
        toks = tokens_of(rec)
        if lock and iid in locked:
            spans = locked[iid]
            source = "human80"
        else:
            spans = rule_spans(rec)
            source = "rule_v2_tight" if TIGHT else "rule_v1"
        if lock and iid in locked:
            pred = rule_spans(rec)
            agree_n += 1
            if set(pred) == set(locked[iid]):
                agree_exact += 1
        src_count[source] += 1
        tags = spans_to_bio(len(toks), spans)
        if any(t != "O" for t in tags):
            n_span += 1
        else:
            n_empty += 1
        out = {
            "id": iid,
            "global_id": rec.get("global_id"),
            "sentence_order": rec.get("sentence_order"),
            "sentence": rec.get("sentence"),
            "tokens": toks,
            "source_domain": rec.get("source_domain"),
            "title": rec.get("title"),
            "list_of_selection_bio4": tags,
            "goldstyle_spans": [[a, b, t] for a, b, t in spans],
            "goldstyle_source": source,
        }
        out_rows.append(out)
    stats = {
        "n": len(out_rows),
        "n_empty": n_empty,
        "n_with_span": n_span,
        "source": dict(src_count),
        "rule_vs_human80_exact": {"n": agree_n, "exact": agree_exact},
    }
    return out_rows, stats


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for rec in rows:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def _tight_from_silver(
    toks: list[str], a: int, b: int, hit: list[tuple[int, int, str]]
) -> list[tuple[int, int, str]]:
    out = []
    for xa, yb, typ in hit:
        xa = max(a, xa)
        yb = min(b, yb)
        while xa > a and toks[xa - 1] not in PUNCT_TOK and (yb - xa) < TIGHT_MAX:
            xa -= 1
        while yb < b and toks[yb] not in PUNCT_TOK and (yb - xa) < TIGHT_MAX:
            yb += 1
        if yb - xa > TIGHT_MAX:
            yb = xa + TIGHT_MAX
        if yb > xa:
            out.append((xa, yb, typ))
    return out


def _trim_to_max(toks: list[str], sa: int, sb: int, cap: int) -> tuple[int, int]:
    if sb - sa <= cap:
        return sa, sb
    # keep the skill-keyword-heavy window
    best = (sa, sa + cap)
    best_n = 0
    for i in range(sa, sb - cap + 1):
        n = 1 if SKILLISH_RE.search("".join(toks[i : i + cap])) else 0
        if n >= best_n:
            best = (i, i + cap)
            best_n = n
    return best


def main() -> None:
    global TIGHT, OUT_TRAIN, OUT_DEV, OUT_META
    ap = argparse.ArgumentParser()
    ap.add_argument("--tight", action="store_true", help="Shorter spans (v2); default is clause-level v1")
    ap.add_argument("--out_train", type=Path, default=OUT_TRAIN)
    ap.add_argument("--out_dev", type=Path, default=OUT_DEV)
    ap.add_argument("--out_meta", type=Path, default=OUT_META)
    args = ap.parse_args()
    TIGHT = bool(args.tight)
    OUT_TRAIN, OUT_DEV, OUT_META = args.out_train, args.out_dev, args.out_meta
    locked, n_miss = project_final80()
    train = load_json(TRAIN)
    dev = load_json(DEV)
    tr_rows, tr_stats = rewrite_split(train, locked, lock=True)
    dv_rows, dv_stats = rewrite_split(dev, {}, lock=False)
    write_jsonl(OUT_TRAIN, tr_rows)
    write_jsonl(OUT_DEV, dv_rows)
    lens = [b - a for r in tr_rows for a, b, _ in r["goldstyle_spans"]]
    sil_lens = []
    for rec in train:
        for a, b, _ in bio_spans(rec.get("list_of_selection_bio4") or []):
            sil_lens.append(b - a)
    meta = {
        "mode": "tight_v2" if TIGHT else "clause_v1",
        "tight_max_tokens": TIGHT_MAX if TIGHT else None,
        "train_out": str(OUT_TRAIN),
        "dev_out": str(OUT_DEV),
        "overwrote_corpus_train": False,
        "touched_gold_v2": False,
        "human80_locked": len(locked),
        "human80_unaligned_spans": n_miss,
        "train": tr_stats,
        "dev": dv_stats,
        "span_token_len_goldstyle_mean": (sum(lens) / len(lens)) if lens else 0,
        "span_token_len_silver_mean": (sum(sil_lens) / len(sil_lens)) if sil_lens else 0,
        "n_goldstyle_spans": len(lens),
        "n_silver_spans": len(sil_lens),
    }
    OUT_META.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(meta, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
