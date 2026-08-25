#!/usr/bin/env python3
"""Build Alpaca SFT data: SOP extract prompt + LSKT v4 train/dev silver targets.

Does not use Gold v2 or P2 test IDs. Train/test overlap must stay 0.
"""
from __future__ import annotations

import json
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
LF_DATA = Path("/home/guojingli3/SCESC-LLM-skill-extraction/LLaMA-Factory/data")
PROMPT = (
    PAPER / "reports/sandbox_lskt_v4_silver/gpt4o_sop_extract_pilot100/PROMPT_gpt4o_sop_extract.txt"
).read_text(encoding="utf-8")
USER_PREFIX = (
    "请从下面这一批句子抽出 LSKT 跨度。只输出 JSON 数组，不要 markdown。"
    "id 必须与输入完全一致、顺序一致、不增不删。"
    "text 必须是 sentence 的连续原文子串。不要参考银标或 Gold。\n"
)
P2 = PAPER / "data/test_lskt_v4_cws_simhuman980_hybrid.jsonl"
SPLITS = {
    "train": PAPER / "data/train_lskt_v4_silver.jsonl",
    "dev": PAPER / "data/dev_lskt_v4_silver.jsonl",
}


def rec_id(rec: dict) -> str:
    return str(rec.get("id") or "").strip()


def spans_of(rec: dict) -> list[dict]:
    toks = [str(t) for t in (rec.get("tokens") or list(rec.get("sentence") or ""))]
    out = []
    for sp in rec.get("v4_spans") or []:
        if not isinstance(sp, (list, tuple)) or len(sp) < 3:
            continue
        s, e, typ = int(sp[0]), int(sp[1]), str(sp[2]).strip().upper()[:1]
        if typ not in {"L", "K", "S", "T"} or s < 0 or e > len(toks) or e <= s:
            continue
        text = "".join(toks[s:e]).strip()
        if text:
            out.append({"text": text, "type": typ})
    return out


def load_ids(path: Path) -> set[str]:
    ids = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            ids.add(rec_id(json.loads(line)))
    return ids


def convert(src: Path, dst: Path, banned: set[str]) -> dict:
    rows = []
    skipped = 0
    for line in src.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        cid = rec_id(rec)
        if not cid or cid in banned:
            skipped += 1
            continue
        payload = [{"id": cid, "sentence": rec.get("sentence") or "", "domain": rec.get("source_domain") or ""}]
        target = [{"id": cid, "spans": spans_of(rec), "comment": "sft_v4"}]
        rows.append(
            {
                "instruction": PROMPT,
                "input": USER_PREFIX + json.dumps(payload, ensure_ascii=False),
                "output": json.dumps(target, ensure_ascii=False),
            }
        )
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(rows, ensure_ascii=False) + "\n", encoding="utf-8")
    return {"n": len(rows), "skipped": skipped, "out": str(dst)}


def main() -> None:
    banned = load_ids(P2)
    summary = {"p2_n": len(banned), "prompt_chars": len(PROMPT)}
    for name, src in SPLITS.items():
        dst = LF_DATA / f"{name}_lskt_v4_sop_extract_alpaca.json"
        src_ids = load_ids(src)
        summary[name] = convert(src, dst, banned)
        summary[f"{name}_overlap_p2"] = len(src_ids & banned)
    (PAPER / "reports/sft_lskt_v4_sop_extract_data.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
