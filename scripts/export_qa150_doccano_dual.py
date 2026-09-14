#!/usr/bin/env python3
"""QA150 Doccano export: human L/K/S/T + Astra L1 + Grok L2 + red DIFF.

Human annotators tag L/K/S/T while viewing both machine layers.
Not majority vote. Not Gold150 / v6a / paper counts.
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from silver_public_api_lib import validate_records

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
QA = PAPER / "data/silver_plus_10k_prep_20260913/human_qa150"
OUT = QA / "doccano"
PROMPT_ID = "silver_public_api_v1.0"
GROK_ID = "cursor-grok-6.0"
ASTRA_ID = "gpt-6-astra"
LKST = {"L", "K", "S", "T"}
ASTRA_SUFFIX = {"L": "L1", "K": "K1", "S": "S1", "T": "T1"}
GROK_SUFFIX = {"L": "L2", "K": "K2", "S": "S2", "T": "T2"}
# Human = L/K/S/T (empty at import). Astra = L1..T1. Grok = L2..T2. Disagreement = DIFF (red).
LABEL_COLORS = (
    ("L", "l", "#2563eb"),
    ("K", "k", "#059669"),
    ("S", "s", "#d97706"),
    ("T", "t", "#7c3aed"),
    ("L1", "5", "#1d4ed8"),
    ("K1", "6", "#047857"),
    ("S1", "7", "#b45309"),
    ("T1", "8", "#6d28d9"),
    ("L2", "1", "#60a5fa"),
    ("K2", "2", "#34d399"),
    ("S2", "3", "#fbbf24"),
    ("T2", "4", "#c084fc"),
    ("DIFF", "d", "#dc2626"),
)

# Independent Grok mentions: (surface, type). Order = left-to-right first unused hit.
# None / [] + empty=True → confirmed_empty.
GROK: dict[str, dict] = {}


def g(
    sid: str,
    mentions: list[tuple[str, str]],
    *,
    empty: bool = False,
    adj: str | None = None,
    note: str = "",
    issues: list[dict] | None = None,
) -> None:
    GROK[sid] = {"mentions": mentions, "empty": empty, "adj": adj, "note": note, "issues": issues}


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def dump_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def place(text: str, mentions: list[tuple[str, str]]) -> list[list]:
    used: set[tuple[int, int]] = set()
    spans = []
    for needle, lab in mentions:
        lab = lab.upper()
        if lab not in LKST:
            raise ValueError(f"bad type {lab}")
        start = 0
        hit = None
        while True:
            i = text.find(needle, start)
            if i < 0:
                break
            j = i + len(needle)
            if (i, j) not in used and text[i:j] == needle:
                hit = (i, j, lab)
                break
            start = i + 1
        if hit is None:
            raise ValueError(f"missing {needle!r} in {text!r}")
        used.add((hit[0], hit[1]))
        spans.append([hit[0], hit[1], hit[2]])
    spans.sort(key=lambda x: (x[0], x[1], x[2]))
    for i in range(1, len(spans)):
        if spans[i][0] < spans[i - 1][1]:
            raise ValueError(f"overlap {spans[i-1]} {spans[i]} | {text}")
    return spans


def fmt_suggest(spans: list[list], text: str) -> str:
    if not spans:
        return "[]"
    return " | ".join(f"{text[a:b]}/{lab}" for a, b, lab in spans)


def remap(triples: list[list], mapping: dict[str, str], who: str) -> list[list]:
    out = []
    for a, b, lab in triples:
        mapped = mapping.get(str(lab).upper())
        if not mapped:
            raise ValueError(f"bad {who} type {lab}")
        out.append([int(a), int(b), mapped])
    return out


def astra_overlay(triples: list[list]) -> list[list]:
    return remap(triples, ASTRA_SUFFIX, "astra")


def grok_overlay(triples: list[list]) -> list[list]:
    return remap(triples, GROK_SUFFIX, "grok")


def diff_highlight(text: str, astra: list[list], grok: list[list]) -> list[list]:
    """Red spans over characters where Astra type occupancy != Grok type occupancy."""
    n = len(text)
    oa = [None] * n
    og = [None] * n
    for a, b, lab in astra:
        for i in range(int(a), int(b)):
            oa[i] = lab
    for a, b, lab in grok:
        for i in range(int(a), int(b)):
            og[i] = lab
    spans: list[list] = []
    i = 0
    while i < n:
        if oa[i] == og[i]:
            i += 1
            continue
        j = i + 1
        while j < n and oa[j] != og[j]:
            j += 1
        spans.append([i, j, "DIFF"])
        i = j
    return spans


def comments_line(text: str, astra: list[list], grok: list[list], agree: bool) -> str:
    flag = "两套一致" if agree else "两套有差异（红 DIFF）"
    return (
        f"请用 L/K/S/T 打人标，参考 L1=Astra、L2=Grok，不要只改机器层。[{flag}] "
        f"Astra: {fmt_suggest(astra, text)} || Grok: {fmt_suggest(grok, text)}"
    )


def fill_grok() -> None:
    spec_path = Path(__file__).with_name("qa150_cursor_grok_spec.json")
    data = json.loads(spec_path.read_text(encoding="utf-8"))
    GROK.clear()
    GROK.update(data)


def resolve(text: str, spec: dict) -> dict:
    mentions = [tuple(x) for x in (spec.get("mentions") or [])]
    if spec.get("empty") and not spec.get("adj"):
        return {"spans": [], "status": "confirmed_empty", "note": spec.get("note") or "", "issues": []}
    spans = place(text, mentions)
    if spec.get("adj") or spec.get("issues"):
        issues = spec.get("issues")
        if not issues:
            kind = spec.get("adj") or "scope"
            issues = [
                {
                    "kind": kind,
                    "text": text if kind == "scope" else (text[spans[0][0] : spans[0][1]] if spans else text),
                    "alternatives": ["纳入主层", "不抽或改边界/类型"],
                    "reason": spec.get("note") or "待裁决",
                }
            ]
        return {
            "spans": [{"start": a, "end": b, "text": text[a:b], "label": lab} for a, b, lab in spans],
            "status": "adjudication_required",
            "note": spec.get("note") or "",
            "issues": issues,
        }
    status = "candidate_complete" if spans else "confirmed_empty"
    return {
        "spans": [{"start": a, "end": b, "text": text[a:b], "label": lab} for a, b, lab in spans],
        "status": status,
        "note": spec.get("note") or "",
        "issues": [],
    }


def to_triples(spans) -> list[list]:
    if spans and isinstance(spans[0], dict):
        return [[int(s["start"]), int(s["end"]), s.get("label") or s.get("type")] for s in spans]
    return [[int(a), int(b), str(c)] for a, b, c in (spans or [])]


def main() -> int:
    fill_grok()
    tasks = load_jsonl(QA / "qa150_human_task.jsonl")
    if len(GROK) != len(tasks):
        missing = sorted({t["id"] for t in tasks} - set(GROK))
        extra = sorted(set(GROK) - {t["id"] for t in tasks})
        raise SystemExit(f"grok map size {len(GROK)} != 150 missing={missing[:8]} extra={extra[:8]}")
    grok_rows = []
    astra_doc, grok_doc, dual = [], [], []
    n_agree = 0
    for t in tasks:
        spec = GROK[t["id"]]
        grok = resolve(t["text"], spec)
        triples_g = to_triples(grok["spans"])
        triples_a = to_triples(t.get("ai_label") or t.get("spans") or [])
        rec = {
            "id": t["id"],
            "qa_seq": t["qa_seq"],
            "text": t["text"],
            "source_domain": t.get("source_domain"),
            "wave": t.get("wave"),
            "prompt_id": PROMPT_ID,
            "model": GROK_ID,
            "status": grok["status"],
            "note": grok["note"],
            "issues": grok["issues"],
            "spans": grok["spans"],
        }
        grok_rows.append(rec)
        agree = triples_a == triples_g
        n_agree += int(agree)
        meta_base = {
            "id": t["id"],
            "qa_seq": t["qa_seq"],
            "source_domain": t.get("source_domain"),
            "wave": t.get("wave"),
            "do_not_train": True,
            "not_independent_blind_gold": True,
            "possible_future_test": True,
            "quality_check_of": "new_silver_only",
            "prompt_id": PROMPT_ID,
            "prelabel": "human_LKST_empty",
            "aux_labeler": GROK_ID,
            "machine_layer_1": ASTRA_ID,
            "machine_layer_2": GROK_ID,
            "astra_status": t.get("ai_status"),
            "grok_status": grok["status"],
            "suggest_astra": fmt_suggest(triples_a, t["text"]),
            "suggest_cursor_grok": fmt_suggest(triples_g, t["text"]),
            "label_layers_agree": agree,
            "sandbox": "new_silver_qa150",
        }
        astra_doc.append(
            {
                "id": t["id"],
                "text": t["text"],
                "label": triples_a,
                "labels": triples_a,
                "meta": {**meta_base, "prelabel": ASTRA_ID},
            }
        )
        grok_doc.append(
            {
                "id": t["id"],
                "text": t["text"],
                "label": triples_g,
                "labels": triples_g,
                "meta": {**meta_base, "prelabel": GROK_ID},
            }
        )
        canvas = astra_overlay(triples_a) + grok_overlay(triples_g) + diff_highlight(t["text"], triples_a, triples_g)
        comment = comments_line(t["text"], triples_a, triples_g, agree)
        dual.append(
            {
                "id": t["id"],
                "text": t["text"],
                "label": canvas,
                "labels": canvas,
                "Comments": comment,
                "meta": {
                    **meta_base,
                    "label_human": [],
                    "label_astra": triples_a,
                    "label_cursor_grok": triples_g,
                    "label_astra_overlay": astra_overlay(triples_a),
                    "label_grok_overlay": grok_overlay(triples_g),
                    "label_diff": diff_highlight(t["text"], triples_a, triples_g),
                    "astra_note": t.get("ai_note"),
                    "grok_note": grok["note"],
                    "grok_issues": grok["issues"],
                    "human_edit": "draw L/K/S/T; L1/K1/S1/T1=Astra, L2/K2/S2/T2=Grok, DIFF=red; not majority vote",
                    "allow_overlapping": True,
                },
            }
        )

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "batches").mkdir(exist_ok=True)
    dump_jsonl(OUT / "qa150_cursor_grok_labels.jsonl", grok_rows)
    dump_jsonl(OUT / "doccano_qa150_astra_prelabel.jsonl", astra_doc)
    dump_jsonl(OUT / "doccano_qa150_grok_prelabel.jsonl", grok_doc)
    dump_jsonl(OUT / "doccano_qa150_dual.jsonl", dual)
    dump_jsonl(OUT / "qa150.jsonl", dual)
    for i in range(0, len(dual), 50):
        dump_jsonl(OUT / "batches" / f"batch_{i // 50 + 1:02d}.jsonl", dual[i : i + 50])
    labels = [{"text": n, "suffix_key": k, "background_color": c, "text_color": "#ffffff"} for n, k, c in LABEL_COLORS]
    (OUT / "labels.json").write_text(json.dumps(labels, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (OUT / "labels.jsonl").open("w", encoding="utf-8") as f:
        for lab in labels:
            f.write(json.dumps(lab, ensure_ascii=False) + "\n")
    parsed = {
        "records": [
            {"id": r["id"], "spans": r["spans"], "status": r["status"], "note": r["note"], "issues": r["issues"]}
            for r in grok_rows
        ]
    }
    val = validate_records(tasks, parsed)
    if not val["ok"]:
        raise SystemExit("grok validate_records failed: " + json.dumps(val["errors"][:8], ensure_ascii=False))
    prompt_sha = hashlib.sha256((PAPER / "silver_prompt.txt").read_bytes()).hexdigest()
    types_a = Counter(lab for r in astra_doc for _, _, lab in r["label"])
    types_g = Counter(lab for r in grok_doc for _, _, lab in r["label"])
    types_canvas = Counter(lab for r in dual for _, _, lab in r["label"])
    n_human_on_canvas = sum(1 for r in dual for *_, lab in r["label"] if lab in LKST)
    report = {
        "n": 150,
        "prompt_id": PROMPT_ID,
        "prompt_file": "silver_prompt.txt",
        "prompt_sha256": prompt_sha,
        "astra": ASTRA_ID,
        "aux": GROK_ID,
        "human_layer": "L/K/S/T empty at import",
        "canvas": "L/K/S/T=human empty; L1=Astra; L2=Grok; DIFF=red",
        "not_majority_vote": True,
        "validate_records_ok": True,
        "n_span_exact_agree": n_agree,
        "n_span_exact_disagree": 150 - n_agree,
        "astra_empty": sum(1 for r in astra_doc if not r["label"]),
        "grok_empty": sum(1 for r in grok_doc if not r["label"]),
        "n_human_lkst_on_canvas": n_human_on_canvas,
        "grok_status": dict(Counter(r["status"] for r in grok_rows)),
        "span_types_astra": dict(types_a),
        "span_types_grok": dict(types_g),
        "span_types_canvas": dict(types_canvas),
        "n_sentences_with_diff_highlight": sum(1 for r in dual if any(lab == "DIFF" for *_, lab in r["label"])),
        "n_diff_spans": sum(1 for r in dual for *_, lab in r["label"] if lab == "DIFF"),
        "sha256_qa150": sha256_file(OUT / "qa150.jsonl"),
        "sha256_dual": sha256_file(OUT / "doccano_qa150_dual.jsonl"),
        "sha256_astra": sha256_file(OUT / "doccano_qa150_astra_prelabel.jsonl"),
        "sha256_grok_prelabel": sha256_file(OUT / "doccano_qa150_grok_prelabel.jsonl"),
        "sha256_grok_labels": sha256_file(OUT / "qa150_cursor_grok_labels.jsonl"),
        "not_paper_main": True,
        "not_independent_blind_gold": True,
    }
    (OUT / "EXPORT_REPORT.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "IMPORT.md").write_text(
        """# Doccano 导入（新增 Silver 人检 150）

冻结 150 句，**不要写入训练集**。抽中不换样。不是独立盲标 Gold，也不是 Gold150。

**协议：对照两套机器标，用人层 L/K/S/T 独立打标。不要只改 Astra，也不要多数决合并。**

导入时人层为空；画布只预填机器对照层。

| 标签 | 谁 | 颜色 | 快捷键 |
|---|---|---|---|
| **L / K / S / T** | **人标工作层（导入时空）** | 蓝 / 绿 / 橙 / 紫 | l k s t |
| L1 / K1 / S1 / T1 | gpt-6-astra 对照（只看不改） | 深蓝同族 | 5 6 7 8 |
| L2 / K2 / S2 / T2 | Cursor-Grok 对照（只看不改） | 浅色同族 | 1 2 3 4 |
| **DIFF** | 两套占用不一致的字 | **红** | d |

一致句：L1 与 L2 叠在同一跨度上。不一致句：另有红 DIFF。Comments 里有两套摘要。

## 建项目

1. Create → **Sequence Labeling**。
2. **打开 overlapping**（人层会叠在机器层上）。可开嵌套。
3. 先导入 `labels.json`（**13** 个标签）。
4. Dataset → Import → **JSONL**。文本=`text`，标签=`label`。
5. 若界面有 Comments 列，会显示 Astra / Grok 对照摘要。

## 导入哪个文件

| 文件 | 用途 |
|---|---|
| **`qa150.jsonl`**（同 `doccano_qa150_dual.jsonl`） | 全量 150：人层空 + Astra L1 + Grok L2 + 红 DIFF |
| `batches/batch_01.jsonl` | 先标 50 句 |
| `doccano_qa150_astra_prelabel.jsonl` | 仅 Astra 的 L/K/S/T（关 overlapping 时用，不是人检主文件） |
| `doccano_qa150_grok_prelabel.jsonl` | 仅 Grok |

已导入旧版的项目：请先重新导入 `labels.json`（13 类），再导入本 `qa150.jsonl`。

`meta.id` 是冻结句子 ID，不要改 `text`。不要改 L1/L2/DIFF。导出后我们只保留你画的 L/K/S/T。

## 导出后怎么还

人标 JSONL 放到本目录 `exports/`。不要覆盖 Gold150 / v6a / `qa150_human_task.jsonl`。
""",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
