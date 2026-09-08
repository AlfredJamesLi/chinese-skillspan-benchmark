#!/usr/bin/env python3
"""Synthetic + frozen-dev parser diagnostics. No Gold150. No model weights."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path("/home/guojingli3/Chinese-Skillspan-Benchmark")
PAPER = ROOT / "Chinese_skill_benchmark_Paper"
sys.path.insert(0, str(PAPER / "scripts"))
from qwen_ext_protocol import build_user_prompt, format_target, parse_model_output, to_bio  # noqa: E402

EXT = PAPER / "output/silver_plus_extensions"
DEV = EXT / "data/v6a_nocross_20260908/dev_b2.jsonl"


def load(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def check(name: str, raw: str, sent: str, expect_spans=None, expect_status=None) -> dict:
    p = parse_model_output(raw, sent)
    ok = True
    notes = []
    if expect_status and p["status"] != expect_status:
        ok = False
        notes.append(f"status {p['status']} != {expect_status}")
    if expect_spans is not None and p["spans"] != expect_spans:
        ok = False
        notes.append(f"spans {p['spans']} != {expect_spans}")
    return {"name": name, "ok": ok, "got": {"spans": p["spans"], "status": p["status"], "failures": p["failures"]}, "notes": notes}


def main() -> int:
    cases = []
    # leading space in generation
    cases.append(check("leading_space", '  [{"start":0,"end":2,"type":"S"}]', "沟通能力", [[0, 2, "S"]], "ok"))
    # Chinese
    sent = "要求精通机器学习。"
    cases.append(check("chinese", format_target([[2, 4, "S"], [4, 8, "K"]]), sent, [[2, 4, "S"], [4, 8, "K"]], "ok"))
    # English tool name
    sent = "熟悉 Python 与 SQL。"
    # offsets on Unicode code points (Python str)
    i = sent.find("Python")
    j = sent.find("SQL")
    cases.append(check("english_tool", format_target([[i, i + 6, "K"], [j, j + 3, "K"]]), sent, [[i, i + 6, "K"], [j, j + 3, "K"]], "ok"))
    # repeated mention: two 沟通
    sent = "沟通与沟通能力"
    first = sent.find("沟通")
    second = sent.find("沟通", first + 1)
    raw = json.dumps(
        [{"start": first, "end": first + 2, "type": "T"}, {"start": second, "end": second + 2, "type": "T"}],
        ensure_ascii=False,
    )
    cases.append(check("repeat_offsets", raw, sent, [[first, first + 2, "T"], [second, second + 2, "T"]], "ok"))
    # surface-only repeats: left-to-right unused
    raw = json.dumps([{"text": "沟通", "type": "T"}, {"text": "沟通", "type": "T"}], ensure_ascii=False)
    cases.append(check("repeat_surface_ltr", raw, sent, [[first, first + 2, "T"], [second, second + 2, "T"]], "ok"))
    # empty
    cases.append(check("empty_ok", "[]", "无要求。", [], "ok"))
    # multi-span + punctuation
    sent = "具备沟通、协调能力。"
    cases.append(
        check(
            "punct_multi",
            format_target([[2, 4, "T"], [5, 9, "T"]]),
            sent,
            [[2, 4, "T"], [5, 9, "T"]],
            "ok",
        )
    )
    # long span
    sent = "负责" + "技术" * 20 + "工作"
    cases.append(check("long_span", format_target([[2, 2 + 40, "S"]]), sent, [[2, 42, "S"]], "ok"))
    # truncated / no json
    cases.append(check("trunc_no_json", '{"start":0,"end":2,"type":"S"', "沟通能力", [], "no_json"))
    # oob not silently kept
    cases.append(check("oob", '[{"start":0,"end":99,"type":"S"}]', "短", [], "oob"))
    # do not edit sentence: offset kept even if surface mismatches
    sent = "使用PyTorch框架"
    raw = json.dumps([{"start": 2, "end": 9, "type": "K", "text": "WRONG"}], ensure_ascii=False)
    p = parse_model_output(raw, sent)
    cases.append(
        {
            "name": "keep_offset_not_rewrite",
            "ok": p["spans"] == [[2, 9, "K"]] and sent == "使用PyTorch框架",
            "got": p,
            "notes": [] if p["spans"] == [[2, 9, "K"]] else ["rewrote or dropped"],
        }
    )

    dev = load(DEV)
    assert len(dev) == 169
    empty_dev = [r for r in dev if not r.get("spans")]
    multi_dev = [r for r in dev if len(r.get("spans") or []) >= 2]
    # roundtrip gold-format targets from train-style spans on frozen DEV (protocol check only)
    rt_ok = 0
    for r in dev:
        raw = format_target(r.get("spans") or [])
        got = parse_model_output(raw, r["sentence"])
        gold = [list(x) for x in (r.get("spans") or [])]
        if got["spans"] == gold:
            rt_ok += 1
    cases.append(
        {
            "name": "dev_roundtrip_targets",
            "ok": rt_ok == 169,
            "got": {"n": 169, "roundtrip_ok": rt_ok, "n_empty": len(empty_dev), "n_multi": len(multi_dev)},
            "notes": [] if rt_ok == 169 else [f"roundtrip {rt_ok}/169"],
        }
    )
    # prompt does not mutate sentence
    s = "  前导空格与Python"
    user = build_user_prompt(s, [{"sentence": "例", "spans": []}])
    cases.append({"name": "prompt_keeps_sentence", "ok": f"句子：{s}" in user, "got": {"in": f"句子：{s}" in user}, "notes": []})

    report = {
        "n_cases": len(cases),
        "n_pass": sum(1 for c in cases if c["ok"]),
        "n_fail": sum(1 for c in cases if not c["ok"]),
        "cases": cases,
        "gold150_not_used": True,
        "offset_convention": "unicode_codepoint_0_based_half_open",
    }
    out = EXT / "PARSER_TEST_REPORT.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"pass": report["n_pass"], "fail": report["n_fail"], "out": str(out)}, ensure_ascii=False))
    return 0 if report["n_fail"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
