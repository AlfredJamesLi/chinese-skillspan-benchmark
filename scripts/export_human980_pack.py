#!/usr/bin/env python3
"""Export the 980 must-human test sentences for SOP-v4 annotation.

Prelabel = rule_v4 (same SOP as CRF train). Codex/Doubao/Kimi are comments only.
Does not overwrite Gold v2, train.json, or confirmed-results.md.
Does not add these test IDs to the CRF train set.
"""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
CSV980 = PAPER / "reports/sandbox_lskt_v4_silver/codex_pack/conflict_v1/human_must_review.csv"
RULE = PAPER / "data/test_lskt_v4_rule_g2ids.jsonl"
CODEX = PAPER / "data/test_lskt_v4_silver_g2ids.jsonl"
DOUBAO = PAPER / "data/test_lskt_v4_doubao_g2ids.jsonl"
KIMI = PAPER / "data/test_lskt_v4_kimi_g2ids.jsonl"
GOLD = PAPER / "data/gold_canonical_v2.jsonl"
OUT = PAPER / "reports/sandbox_lskt_v4_silver/human980_pack"
BATCH = 50

sys_path_note = PAPER / "scripts"
import sys

sys.path.insert(0, str(sys_path_note))
from goldstyle_empty_rules import empty_hint  # noqa: E402
from sandbox_v4_apply import token_char_spans  # noqa: E402


def load_jsonl(path: Path) -> dict[str, dict]:
    out = {}
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rec = json.loads(line)
                out[str(rec["id"])] = rec
    return out


def spans_of(rec: dict | None) -> list[tuple[int, int, str]]:
    if not rec:
        return []
    raw = rec.get("v4_spans") or []
    out = []
    for item in raw:
        if isinstance(item, dict):
            out.append((int(item["start"]), int(item["end"]), str(item.get("type") or "S")))
        else:
            a, b, t = item
            out.append((int(a), int(b), str(t)))
    return out


def fmt_spans(toks: list[str], spans: list[tuple[int, int, str]]) -> str:
    if not spans:
        return "[]"
    return " | ".join(f"{''.join(toks[a:b])}/{t}" for a, b, t in spans)


def char_labels(rec: dict, spans: list[tuple[int, int, str]]) -> list[list]:
    sent = rec.get("sentence") or ""
    toks = rec.get("tokens") or list(sent)
    char_of = token_char_spans(sent, toks)
    labels = []
    n = len(char_of)
    for a, b, t in spans:
        if a < 0 or b > n or a >= b:
            continue
        cs = char_of[a][0]
        ce = char_of[b - 1][1]
        lab = t if t in {"L", "K", "S", "T"} else "S"
        labels.append([cs, ce, lab])
    return labels


def main() -> int:
    ids = []
    csv_rows = {}
    with CSV980.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or "id" not in reader.fieldnames:
            raise SystemExit(f"bad csv header: {reader.fieldnames}")
        for row in reader:
            i = str(row.get("id") or "").strip()
            if not i:
                continue
            ids.append(i)
            csv_rows[i] = row
    rule, codex, doubao, kimi, gold = map(load_jsonl, (RULE, CODEX, DOUBAO, KIMI, GOLD))
    missing = [i for i in ids if i not in rule]
    if missing:
        raise SystemExit(f"missing rule_v4 ids: {missing[:5]} n={len(missing)}")

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "batches").mkdir(exist_ok=True)

    worksheet_fields = [
        "id",
        "batch",
        "status",
        "source_domain",
        "conflict_kind",
        "empty_hint",
        "sentence",
        "prelabel_rule_v4",
        "suggest_codex",
        "suggest_doubao",
        "suggest_kimi",
        "human_spans",
        "comment",
    ]
    doccano_all = []
    ws_rows = []
    kinds = Counter()
    domains = Counter()
    n_empty_pre = 0

    for n, i in enumerate(ids):
        rec = rule[i]
        sent = rec.get("sentence") or csv_rows[i].get("sentence") or ""
        toks = rec.get("tokens") or list(sent)
        domain = rec.get("source_domain") or csv_rows[i].get("domain") or ""
        kind = csv_rows[i].get("status") or ""
        spans = spans_of(rec)
        if not spans:
            n_empty_pre += 1
        kinds[kind] += 1
        domains[domain] += 1
        batch_no = n // BATCH + 1
        labels = char_labels(rec, spans)
        doccano_all.append(
            {
                "text": sent,
                "labels": labels,
                "meta": {
                    "id": i,
                    "global_id": rec.get("global_id"),
                    "source_domain": domain,
                    "conflict_kind": kind,
                    "empty_hint": empty_hint(sent, domain),
                    "prelabel": "rule_v4",
                    "sandbox": "human980_sop_v4",
                    "suggest_codex": csv_rows[i].get("codex") or "",
                    "suggest_doubao": csv_rows[i].get("doubao") or "",
                    "suggest_kimi": csv_rows[i].get("kimi") or "",
                    "do_not_train": True,
                },
            }
        )
        ws_rows.append(
            {
                "id": i,
                "batch": f"{batch_no:02d}",
                "status": "todo",
                "source_domain": domain,
                "conflict_kind": kind,
                "empty_hint": empty_hint(sent, domain),
                "sentence": sent,
                "prelabel_rule_v4": fmt_spans(toks, spans),
                "suggest_codex": csv_rows[i].get("codex") or "",
                "suggest_doubao": csv_rows[i].get("doubao") or "",
                "suggest_kimi": csv_rows[i].get("kimi") or "",
                "human_spans": "",
                "comment": "",
            }
        )

    with (OUT / "doccano_rule_v4_prelabel.jsonl").open("w", encoding="utf-8") as f:
        for row in doccano_all:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    with (OUT / "worksheet.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=worksheet_fields)
        w.writeheader()
        w.writerows(ws_rows)

    n_batch = 0
    for b in range(0, len(doccano_all), BATCH):
        n_batch += 1
        chunk = doccano_all[b : b + BATCH]
        p = OUT / "batches" / f"batch_{n_batch:02d}.jsonl"
        with p.open("w", encoding="utf-8") as f:
            for row in chunk:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")

    manifest = {
        "n": len(ids),
        "n_batches": n_batch,
        "batch_size": BATCH,
        "prelabel": "rule_v4",
        "n_empty_rule_v4": n_empty_pre,
        "conflict_kind": dict(kinds),
        "domain": dict(domains),
        "gold_v2_untouched": True,
        "do_not_train": True,
        "not_for_confirmed_results": True,
        "ids_in_gold_v2": sum(1 for i in ids if i in gold),
        "ids_in_codex": sum(1 for i in ids if i in codex),
        "ids_in_doubao": sum(1 for i in ids if i in doubao),
        "ids_in_kimi": sum(1 for i in ids if i in kimi),
        "start_with": "batches/batch_01.jsonl",
        "guidelines": "reports/sandbox_lskt_v4_silver/GUIDELINES.md",
    }
    (OUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    start = f"""# 980 句人工标 — 开始这里

测试句，**不要写入训练集**。不要覆盖 `gold_canonical_v2.jsonl`。标完重打分后才能考虑进论文主表。

## 怎么标

1. 读 `../GUIDELINES.md`（L/K/S/T；短而完整；熟悉/掌握只标对象；流程/福利空句；禁半词）。
2. 预标是 **rule_v4**，不是 Codex。三家 LLM 只在 `meta` / CSV 里当对照，不要多数决。
3. 先做 `batches/batch_01.jsonl`（50 句）。Doccano 导入后改跨度即可。
4. 没有 Doccano 时填 `worksheet.csv` 的 `human_spans`（格式同预标：`Python/S | 沟通能力/T`），空句留空。
5. `status` 从 `todo` 改成 `done`。

## 文件

| 文件 | 用途 |
|---|---|
| `doccano_rule_v4_prelabel.jsonl` | 全量 980，Doccano 导入 |
| `batches/batch_01.jsonl` … `batch_{n_batch:02d}.jsonl` | 每批 {BATCH} 句 |
| `worksheet.csv` | 表格备选 |
| `manifest.json` | 句数与冲突类型 |

当前队列：{len(ids)} 句。rule_v4 空预标 {n_empty_pre} 句。冲突类型：{dict(kinds)}。
"""
    (OUT / "START_HERE.md").write_text(start, encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
