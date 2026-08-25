#!/usr/bin/env python3
"""Convert human980 pack to Doccano sequence-labeling JSONL.

Matches this project's earlier import convention (text + label + labels + meta).
Does not overwrite Gold v2, train.json, or the existing prelabel source file.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
SRC = PAPER / "reports/sandbox_lskt_v4_silver/human980_pack/doccano_rule_v4_prelabel.jsonl"
OUT = PAPER / "reports/sandbox_lskt_v4_silver/human980_pack/doccano"
BATCH = 50
LKST = {"L", "K", "S", "T"}
LABEL_COLORS = (
    ("L", "l", "#2563eb"),
    ("K", "k", "#059669"),
    ("S", "s", "#d97706"),
    ("T", "t", "#7c3aed"),
)


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            if line.strip():
                rec = json.loads(line)
                rec["_line"] = i
                rows.append(rec)
    return rows


def clean_spans(text: str, raw: list) -> tuple[list[list], list[str]]:
    issues: list[str] = []
    spans: list[list] = []
    for item in raw or []:
        if not isinstance(item, (list, tuple)) or len(item) < 3:
            issues.append("bad_span_shape")
            continue
        try:
            a, b = int(item[0]), int(item[1])
        except (TypeError, ValueError):
            issues.append("bad_span_int")
            continue
        lab = str(item[2]).strip().upper()[:1]
        if lab not in LKST:
            lab = "S"
        if not (0 <= a < b <= len(text)):
            issues.append(f"oob:{a}:{b}")
            continue
        spans.append([a, b, lab])
    spans.sort(key=lambda x: (x[0], x[1], x[2]))
    flat: list[list] = []
    for a, b, lab in spans:
        if flat and a < flat[-1][1]:
            issues.append(f"overlap:{flat[-1]}|{[a, b, lab]}")
            continue
        flat.append([a, b, lab])
    return flat, issues


def to_doccano(rec: dict) -> tuple[dict, list[str]]:
    text = rec.get("text") or rec.get("sentence") or ""
    spans, issues = clean_spans(text, rec.get("labels") or rec.get("label") or [])
    meta = dict(rec.get("meta") or {})
    cid = str(meta.get("id") or rec.get("id") or "").strip()
    if not cid:
        issues.append("missing_id")
    meta["id"] = cid
    meta["do_not_train"] = True
    meta["sandbox"] = "human980_sop_v4"
    row = {
        "id": cid,
        "text": text,
        "label": spans,
        "labels": spans,
        "meta": meta,
    }
    return row, issues


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> int:
    src = load_jsonl(SRC)
    converted = []
    issue_rows = []
    n_oob = n_overlap = n_empty = 0
    types = Counter()
    for rec in src:
        row, issues = to_doccano(rec)
        converted.append(row)
        if not row["labels"]:
            n_empty += 1
        for a, b, lab in row["labels"]:
            types[lab] += 1
        if issues:
            issue_rows.append({"id": row["id"], "issues": issues})
            if any(x.startswith("oob:") for x in issues):
                n_oob += 1
            if any(x.startswith("overlap:") for x in issues):
                n_overlap += 1

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "batches").mkdir(exist_ok=True)
    write_jsonl(OUT / "human980.jsonl", converted)
    n_batch = 0
    for i in range(0, len(converted), BATCH):
        n_batch += 1
        write_jsonl(OUT / "batches" / f"batch_{n_batch:02d}.jsonl", converted[i : i + BATCH])

    labels = [
        {
            "text": name,
            "suffix_key": key,
            "background_color": color,
            "text_color": "#ffffff",
        }
        for name, key, color in LABEL_COLORS
    ]
    (OUT / "labels.json").write_text(json.dumps(labels, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with (OUT / "labels.jsonl").open("w", encoding="utf-8") as f:
        for lab in labels:
            f.write(json.dumps(lab, ensure_ascii=False) + "\n")
    (OUT / "convert_issues.json").write_text(
        json.dumps(
            {
                "n": len(converted),
                "n_empty_prelabel": n_empty,
                "n_oob_dropped": n_oob,
                "n_overlap_dropped": n_overlap,
                "span_types": dict(types),
                "rows": issue_rows,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    guide = f"""# Doccano 导入（SOP 980）

测试句，**不要写入训练集**。不要覆盖 `gold_canonical_v2.jsonl`。

格式与本仓库以前用的 `doccano_imports/doccano_window.jsonl` 一致：`text` + `label` + `labels` + `meta`。

## 建项目

1. Create → **Sequence Labeling**（序列标注 / NER）。
2. 关闭 overlapping / 嵌套（本任务平面标注）。
3. 先导入标签：`labels.json`（L / K / S / T）。快捷键 l / k / s / t。
4. Dataset → Import → **JSONL** → 选下面其中一个文件。
5. 列映射：文本=`text`，标签=`label`（若界面要 `labels` 也行，两份都写了）。

## 导入哪个文件

| 文件 | 用途 |
|---|---|
| `batches/batch_01.jsonl` | **先标这 50 句** |
| `batches/batch_02.jsonl` … `batch_{n_batch:02d}.jsonl` | 每批 50 |
| `human980.jsonl` | 全量 980，一次导入 |

预标是 **rule_v4**。`meta.suggest_codex/doubao/kimi` 只是对照，不要多数决。  
`meta.id` 是 Gold v2 句子 ID，导出后靠它对齐，不要改 `text`。

## 导出后怎么还

导出 JSONL 放到本目录 `exports/`（自己建）。不要覆盖 Gold。打分前告诉我文件路径。
"""
    (OUT / "IMPORT.md").write_text(guide, encoding="utf-8")
    print(
        json.dumps(
            {
                "n": len(converted),
                "n_batches": n_batch,
                "n_empty_prelabel": n_empty,
                "n_oob_dropped": n_oob,
                "n_overlap_dropped": n_overlap,
                "span_types": dict(types),
                "out": str(OUT),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
