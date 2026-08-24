#!/usr/bin/env python3
"""Gold-style v3 labels: complete NP near Gold length. Does not overwrite train.json or Gold v2.

Silver fragments are expanded to a complete noun phrase and stop at ，。；、 or
熟悉/掌握 boundaries. Hard cap 13 tokens. The 80 human lock is kept as-is.
"""
from __future__ import annotations

import json
import re
import statistics
from collections import Counter
from pathlib import Path

ROOT = Path("/home/guojingli3/SCESC-LLM-skill-extraction")
PAPER = ROOT / "Chinese_skill_benchmark_Paper"
TRAIN = ROOT / "data/annotated/processed/chinese_skillspan/train.json"
DEV = ROOT / "data/annotated/processed/chinese_skillspan/dev.json"
GOLD = PAPER / "data/gold_canonical_v2.jsonl"
FINAL80 = PAPER / "reports/gold_style_relabel/sample80_final.json"
OUT_TRAIN = PAPER / "data/train_goldstyle_v3.jsonl"
OUT_DEV = PAPER / "data/dev_goldstyle_v3.jsonl"
OUT_META = PAPER / "reports/gold_style_relabel/goldstyle_v3_meta.json"

TYPES = {"L", "K", "S", "T"}
HARD_CAP = 13
MIN_LEN = 2

ADMIN_RE = re.compile(
    r"五险一金|底薪|提成\d|过节费|生日|带薪年假|法定节假日|工作时间|工作地点|"
    r"股票期权|融资|著名VC|欢迎应届|面试邀约|报名系统|留下姓名|"
    r"水果蛋糕|豪华年度旅游|敬请期待|&nbsp;|晋升空间大|成长迅速|"
    r"年终奖金|定期调薪|底薪加|包吃住|免费住宿"
)
SKILLISH_RE = re.compile(
    r"熟悉|掌握|负责|独立|经验|能力|专业|学历|英语|普通话|编程|开发|设计|"
    r"沟通|团队|责任|证书|资格|框架|算法|销售|管理|分析"
)
L_RE = re.compile(r"英语|英文|普通话|日语|口语|CET|托福|雅思")
K_RE = re.compile(r"学历|专业|本科|硕士|博士|证书|资格考试|理论|思想")
T_RE = re.compile(r"沟通|责任心|团队|抗压|积极|职业道德|服务意识|细心|耐心|开朗|正直|敬业|主动|好学")
S_TECH_RE = re.compile(
    r"框架|Python|JAVA|Java|C\+\+|C#|Office|OFFICE|编程|Spring|MyBatis|Node|"
    r"Web2|MVC|脚本|算法|开发|调试|Hive|Spark|Hadoop|Linux"
)
DROP_RE = re.compile(
    r"身体健康|形象好|气质佳|挑战高薪|留学经验|国外留学|超龄勿扰|"
    r"C1驾照|持有C1|^\d+年以上|^[一二三四五六七八九十]+年以上"
)
NUM_LEAD = re.compile(r"^[\s\d一二三四五六七八九十第（(]+[、.．.）):\：\-—]*")
DUTY_LEAD = re.compile(r"^(负责|任职要求|岗位要求|岗位职责|工作职责|岗位描述|具有|具备|熟悉|掌握|了解|精通)")
PUNCT_TOK = {"。", "；", ";", "！", "？", "，", ",", "、", "：", ":"}
STOP_PUNCT = {"。", "；", ";", "！", "？", "，", ",", "、"}
BOUND_START = ("熟悉", "掌握", "了解", "精通", "具备", "具有")
INCOMPLETE_END = set("的和与或及等、相支开维技好签服经学专工表晋当求")
INCOMPLETE_START = set("务持关发护力验习计理析统案达升")
COMPLETE_END = (
    "能力", "经验", "学历", "专业", "服务", "开发", "设计", "管理", "分析",
    "沟通", "证书", "资格", "框架", "语言", "技能", "意识", "精神", "态度",
    "功底", "基础", "理论", "知识", "系统", "平台", "工具", "方法", "方案",
    "优化", "维护", "支持", "测试", "运营", "实施", "编写", "调试", "算法",
    "编程", "软件", "硬件", "数据", "网络", "安全", "销售", "营销", "培训",
    "指导", "协作", "责任心", "责任", "英语", "普通话", "本科", "硕士", "博士",
    "学习", "教练", "好学", "团队", "抗压", "细心", "耐心", "开朗", "正直",
    "敬业", "主动", "架构", "模型", "处理", "挖掘", "研发", "需求", "问题",
    "工作", "技术", "联调", "集成", "上架", "投放", "监控", "运维", "验收",
)
NAMED_SKILL_RE = re.compile(
    r"^(英语|英文|普通话|日语|口语|沟通|沟通能力|责任心|团队|团队合作|"
    r"Python|JAVA|Java|C\+\+|C#|Office|OFFICE|Spring|MyBatis|NodeJS|Node|"
    r"Ruby|Go|Golang|Hadoop|Hive|Spark|Linux|MySQL|Redis|Docker|K8s|"
    r"MATLAB|Vue|React|Android|iOS|CET-?4|CET-?6)$",
    re.I,
)
ENUM_SPLIT = re.compile(r"[/／、]")


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
    t = (text or "").strip(" ，,、;；。")
    if len(t) < MIN_LEN:
        return True
    if DROP_RE.search(t):
        if "驾照" in t and ("司机" in sentence or ("驾驶" in sentence and "辅助驾驶" not in sentence)):
            return False
        return True
    if ADMIN_RE.search(t) and not SKILLISH_RE.search(t):
        return True
    return False


def looks_complete(text: str) -> bool:
    t = (text or "").strip(" ，,、;；。：:")
    if len(t) < MIN_LEN:
        return False
    if any(t.endswith(s) for s in COMPLETE_END):
        return True
    if re.search(r"[A-Za-z0-9+#.]{2,}$", t):
        return True
    if 2 <= len(t) <= 6 and t[-1] not in INCOMPLETE_END:
        return True
    return False


def at_bound(toks: list[str], i: int) -> bool:
    if i < 0 or i >= len(toks):
        return True
    if toks[i] in STOP_PUNCT:
        return True
    pair = "".join(toks[i : i + 2])
    return pair in BOUND_START


def left_bound(toks: list[str], i: int) -> bool:
    if i <= 0:
        return True
    if toks[i - 1] in STOP_PUNCT:
        return True
    pair = "".join(toks[max(0, i - 2) : i])
    return pair in BOUND_START


def expand_to_np(toks: list[str], a: int, b: int) -> tuple[int, int]:
    n = len(toks)
    a = max(0, a)
    b = min(n, b)
    if a >= b:
        return a, b
    while b > a and toks[b - 1] in PUNCT_TOK:
        b -= 1
    while a < b and toks[a] in PUNCT_TOK:
        a += 1
    # grow right only while the current phrase is still a fragment
    while b < n and (b - a) < HARD_CAP:
        if at_bound(toks, b):
            break
        cur = "".join(toks[a:b])
        if looks_complete(cur) and (b - a) >= 3 and cur[-1] not in INCOMPLETE_END:
            break
        b += 1
    # grow left only to finish a cut word, not a whole 的-modifier chain
    grew_left = 0
    while a > 0 and (b - a) < HARD_CAP and grew_left < 4:
        if left_bound(toks, a):
            break
        cur = "".join(toks[a:b])
        if looks_complete(cur) and cur[0] not in INCOMPLETE_START and (b - a) >= 3:
            break
        if cur[0] not in INCOMPLETE_START and looks_complete(cur):
            break
        a -= 1
        grew_left += 1
    while b > a and toks[b - 1] in PUNCT_TOK:
        b -= 1
    if (b - a) > HARD_CAP:
        b = a + HARD_CAP
        while b > a and toks[b - 1] in PUNCT_TOK:
            b -= 1
    return a, b


def merge_close_silvers(
    toks: list[str], spans: list[tuple[int, int, str]]
) -> list[tuple[int, int, str]]:
    if not spans:
        return []
    spans = sorted(spans, key=lambda x: (x[0], x[1]))
    out = [spans[0]]
    for a, b, t in spans[1:]:
        pa, pb, pt = out[-1]
        gap = "".join(toks[pb:a])
        if a <= pb:
            out[-1] = (pa, max(pb, b), pt if pt == t else assign_type("".join(toks[pa:max(pb, b)]), pt))
            continue
        if (b - pa) <= HARD_CAP and re.fullmatch(r"[的和与或及\s]*", gap or ""):
            out[-1] = (pa, b, assign_type("".join(toks[pa:b]), pt))
            continue
        out.append((a, b, t))
    return out


def split_enumerated(
    toks: list[str], a: int, b: int, typ: str
) -> list[tuple[int, int, str]]:
    text = "".join(toks[a:b])
    # "英语，Python，沟通能力" is the same independent-skill list as / or 、
    if "，" in text or "," in text:
        comma_parts = [p.strip() for p in re.split(r"[，,]", text) if p.strip()]
        if len(comma_parts) >= 2 and all(2 <= len(p) <= 8 for p in comma_parts):
            if any(NAMED_SKILL_RE.match(p) or L_RE.search(p) for p in comma_parts):
                found = []
                cursor = a
                for p in comma_parts:
                    hit = find_span(toks[cursor:b], p)
                    if hit is None:
                        found = []
                        break
                    sa, sb = cursor + hit[0], cursor + hit[1]
                    found.append((sa, sb, assign_type(p, typ)))
                    cursor = sb
                if found:
                    return found
    if not ENUM_SPLIT.search(text):
        return [(a, b, typ)]
    parts = [p.strip() for p in ENUM_SPLIT.split(text) if p.strip()]
    if len(parts) < 2:
        return [(a, b, typ)]
    if any(len(p) < 2 or len(p) > 8 for p in parts):
        return [(a, b, typ)]
    named = sum(1 for p in parts if NAMED_SKILL_RE.match(p) or re.search(r"[A-Za-z]{2,}", p))
    if named < 1 and not all(2 <= len(p) <= 6 for p in parts):
        return [(a, b, typ)]
    found = []
    cursor = a
    for p in parts:
        hit = find_span(toks[cursor:b], p)
        if hit is None:
            return [(a, b, typ)]
        sa, sb = cursor + hit[0], cursor + hit[1]
        found.append((sa, sb, assign_type(p, typ)))
        cursor = sb
    return found or [(a, b, typ)]


def keyword_fallback(toks: list[str], sent: str) -> list[tuple[int, int, str]]:
    if not SKILLISH_RE.search(sent):
        return []
    n = len(toks)
    out = []
    i = 0
    while i < n:
        pair = "".join(toks[i : i + 2])
        if pair in BOUND_START:
            a, b = expand_to_np(toks, i + 2, min(n, i + 6))
            text = "".join(toks[a:b])
            if not should_drop_span(text, sent) and looks_complete(text):
                out.append((a, b, assign_type(text, "S")))
            i = max(b, i + 2)
            continue
        i += 1
    return out


def rule_spans(rec: dict) -> list[tuple[int, int, str]]:
    toks = tokens_of(rec)
    sent = rec.get("sentence") or ""
    silver = bio_spans(rec.get("list_of_selection_bio4") or [])
    n = len(toks)
    if n == 0:
        return []
    if not silver and not SKILLISH_RE.search(sent):
        return []
    seeds = merge_close_silvers(toks, silver)
    raw = []
    for a, b, typ in seeds:
        sa, sb = expand_to_np(toks, a, b)
        core = NUM_LEAD.sub("", "".join(toks[sa:sb])).strip()
        core = DUTY_LEAD.sub("", core).strip(" ，,、:：")
        loc = find_span(toks[sa:sb], core) if core else None
        if loc is not None:
            sa, sb = sa + loc[0], sa + loc[1]
        text = "".join(toks[sa:sb])
        if should_drop_span(text, sent) or (sb - sa) < MIN_LEN:
            continue
        if (sb - sa) >= n and n > HARD_CAP:
            continue
        raw.extend(split_enumerated(toks, sa, sb, assign_type(text, typ)))
    if not raw and not silver:
        raw = keyword_fallback(toks, sent)
    raw.sort(key=lambda x: (x[0], -(x[1] - x[0])))
    kept = []
    for sp in raw:
        if (sp[1] - sp[0]) > HARD_CAP:
            sp = (sp[0], sp[0] + HARD_CAP, sp[2])
        if any(not (sp[1] <= k[0] or sp[0] >= k[1]) for k in kept):
            continue
        if should_drop_span("".join(toks[sp[0] : sp[1]]), sent):
            continue
        kept.append(sp)
    return kept


def project_final80() -> tuple[dict[str, list[tuple[int, int, str]]], int]:
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
            source = "rule_v3"
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
        out_rows.append(
            {
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
        )
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


def lens_of(rows: list[dict], field: str = "goldstyle_spans") -> list[int]:
    out = []
    for rec in rows:
        if field == "bio":
            for a, b, _ in bio_spans(rec.get("list_of_selection_bio4") or []):
                out.append(b - a)
        else:
            for a, b, _ in rec.get(field) or []:
                out.append(b - a)
    return out


def pcts(xs: list[int]) -> dict:
    if not xs:
        return {"n": 0}
    xs = sorted(xs)
    n = len(xs)

    def p(q: float) -> float:
        if n == 1:
            return float(xs[0])
        k = (n - 1) * q
        f = int(k)
        c = min(f + 1, n - 1)
        w = k - f
        return xs[f] * (1 - w) + xs[c] * w

    return {
        "n": n,
        "mean": sum(xs) / n,
        "median": statistics.median(xs),
        "p10": p(0.10),
        "p25": p(0.25),
        "p50": p(0.50),
        "p75": p(0.75),
        "p90": p(0.90),
        "p95": p(0.95),
        "min": xs[0],
        "max": xs[-1],
        "share_4_12": sum(1 for x in xs if 4 <= x <= 12) / n,
        "share_gt14": sum(1 for x in xs if x > 14) / n,
    }


def example_spans(rows: list[dict], k: int = 10) -> list[dict]:
    out = []
    for rec in rows:
        toks = tokens_of(rec)
        for a, b, t in rec.get("goldstyle_spans") or []:
            out.append(
                {
                    "id": rec.get("id"),
                    "type": t,
                    "len": b - a,
                    "text": "".join(toks[a:b]),
                    "src": rec.get("goldstyle_source"),
                }
            )
            if len(out) >= k:
                return out
    return out


def main() -> None:
    locked, n_miss = project_final80()
    train = load_json(TRAIN)
    dev = load_json(DEV)
    tr_rows, tr_stats = rewrite_split(train, locked, lock=True)
    dv_rows, dv_stats = rewrite_split(dev, {}, lock=False)
    write_jsonl(OUT_TRAIN, tr_rows)
    write_jsonl(OUT_DEV, dv_rows)

    gold = load_json(GOLD)
    gold_lens = []
    gold_ex = []
    for rec in gold:
        toks = tokens_of(rec)
        for a, b, t in bio_spans(rec.get("list_of_selection_bio4") or []):
            gold_lens.append(b - a)
            if len(gold_ex) < 10 and 2 <= (b - a) <= 12:
                text = "".join(toks[a:b])
                if text.strip() == text and "[" not in text:
                    gold_ex.append({"id": rec.get("id"), "type": t, "len": b - a, "text": text})

    h80 = load_json(FINAL80)
    items = {r["id"]: r for r in train}
    h_lens = []
    h_ex = []
    for rec in h80:
        src = items.get(rec["id"])
        toks = tokens_of(src) if src else []
        for sp in rec.get("spans") or []:
            hit = find_span(toks, sp.get("text") or "") if toks else None
            ln = (hit[1] - hit[0]) if hit else len((sp.get("text") or "").strip())
            h_lens.append(ln)
            if len(h_ex) < 10:
                h_ex.append({"id": rec["id"], "type": sp.get("type"), "len": ln, "text": sp.get("text")})

    v3_lens = lens_of(tr_rows)
    sil_lens = []
    for rec in train:
        for a, b, _ in bio_spans(rec.get("list_of_selection_bio4") or []):
            sil_lens.append(b - a)

    mean_v3 = (sum(v3_lens) / len(v3_lens)) if v3_lens else 0
    mean_gold = (sum(gold_lens) / len(gold_lens)) if gold_lens else 0
    closer = abs(mean_v3 - mean_gold) < abs(11.37 - mean_gold) and 5.0 <= mean_v3 <= 8.5
    meta = {
        "mode": "gold_length_v3",
        "hard_cap_tokens": HARD_CAP,
        "train_out": str(OUT_TRAIN),
        "dev_out": str(OUT_DEV),
        "overwrote_corpus_train": False,
        "touched_gold_v2": False,
        "rewrote_sample80_final": False,
        "human80_locked": len(locked),
        "human80_unaligned_spans": n_miss,
        "train": tr_stats,
        "dev": dv_stats,
        "span_token_len": {
            "gold_v2": pcts(gold_lens),
            "human80": pcts(h_lens),
            "silver_train": pcts(sil_lens),
            "v3": pcts(v3_lens),
        },
        "human80_systematically_longer_than_gold": bool(h_lens and (sum(h_lens) / len(h_lens)) > mean_gold + 4),
        "mean_closer_to_gold_than_v2": closer,
        "gpu_smoke_ready": bool(closer),
        "examples": {
            "gold_v2": gold_ex[:8],
            "human80": h_ex[:8],
            "v3": example_spans(tr_rows, 10),
        },
        "n_goldstyle_spans": len(v3_lens),
        "n_silver_spans": len(sil_lens),
    }
    OUT_META.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(meta, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
