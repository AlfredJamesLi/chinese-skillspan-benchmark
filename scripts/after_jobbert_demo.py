#!/usr/bin/env python3
"""Compare JobBERT-zh demo CRF vs vanilla v3 and existing LLM dumps.

Internal only. Does not write paper numbers or confirmed-results.md.
"""
from __future__ import annotations

import json
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
JOB = PAPER / "output/jobbert_zh_demo/crf_v3_seed42/run_summary.json"
VAN = PAPER / "output/cn_roberta_wwm_crf/smoke_goldstyle_v3_seed42/run_summary.json"
V2 = PAPER / "output/cn_roberta_wwm_crf/smoke_goldstyle_v2_seed42/run_summary.json"
SILVER = PAPER / "output/cn_roberta_wwm_crf/smoke_seed42_gpu1/run_summary.json"
QWEN = PAPER / "reports/score_v2_unique_Qwen.json"
DS = PAPER / "reports/score_v2_unique_DeepSeek.json"
GPT = PAPER / "reports/score_v2_unique_ChatGPT.json"
JB_SK = PAPER / "reports/score_v2_unique_JobBERT-skill.json"
OUT = PAPER / "reports/gold_style_relabel/jobbert_demo_result.md"


def from_summary(path: Path) -> dict:
    if not path.is_file():
        return {"ok": False, "path": str(path)}
    r = json.loads(path.read_text(encoding="utf-8"))
    te = r.get("typed_exact") or {}
    cr = r.get("collapsed_exact") or {}
    return {
        "ok": True,
        "path": str(path),
        "align": r.get("alignment_ok"),
        "best_dev": r.get("best_dev_typed_f1"),
        "typed_f1": te.get("f1"),
        "p": te.get("precision"),
        "r": te.get("recall"),
        "tp": te.get("tp"),
        "pred": te.get("pred"),
        "gold": te.get("gold"),
        "collapsed_f1": cr.get("f1"),
        "scorer": r.get("scorer_version"),
    }


def from_score(path: Path) -> dict:
    if not path.is_file():
        return {"ok": False, "path": str(path)}
    r = json.loads(path.read_text(encoding="utf-8"))
    te = r.get("typed_exact") or {}
    cr = r.get("collapsed_exact") or {}
    return {
        "ok": True,
        "path": str(path),
        "align": r.get("alignment_ok"),
        "typed_f1": te.get("f1"),
        "p": te.get("precision"),
        "r": te.get("recall"),
        "tp": te.get("tp"),
        "pred": te.get("pred"),
        "gold": te.get("gold"),
        "collapsed_f1": cr.get("f1"),
        "scorer": r.get("scorer_version"),
    }


def cell(d: dict, key: str, nd: int = 4) -> str:
    v = d.get(key)
    if isinstance(v, float):
        return f"{v:.{nd}f}"
    if v is None:
        return "—"
    return str(v)


def main() -> int:
    job = from_summary(JOB)
    van = from_summary(VAN)
    v2 = from_summary(V2)
    sv = from_summary(SILVER)
    qwen = from_score(QWEN)
    ds = from_score(DS)
    gpt = from_score(GPT)
    jb = from_score(JB_SK)

    jf = job.get("typed_f1")
    vf = van.get("typed_f1")
    qf = qwen.get("typed_f1")
    rec = "jobbert_summary_missing"
    vs_van = "n/a"
    vs_qwen = "n/a"
    if job.get("ok") and isinstance(jf, (int, float)):
        if isinstance(vf, (int, float)):
            delta = jf - vf
            vs_van = f"{delta:+.4f}"
            if abs(delta) < 0.005:
                rec = "demo_mlm_no_lift"
            elif delta > 0:
                rec = "demo_mlm_above_vanilla"
            else:
                rec = "demo_mlm_below_vanilla"
        if isinstance(qf, (int, float)):
            vs_qwen = f"{jf - qf:+.4f}"

    rows = [
        ("JobBERT-zh demo CRF (80k×1 MLM + v3)", job),
        ("RoBERTa-wwm + CRF (no DAPT, v3)", van),
        ("RoBERTa-wwm + CRF goldstyle v2", v2),
        ("RoBERTa-wwm + CRF silver", sv),
        ("Qwen dump (Gold v2 unique)", qwen),
        ("DeepSeek dump (Gold v2 unique)", ds),
        ("ChatGPT dump (Gold v2 unique)", gpt),
        ("English JobBERT-skill transfer", jb),
    ]
    lines = [
        "# JobBERT-zh demo vs encoder / LLM dumps",
        "",
        "Internal smoke only. Do **not** copy into the PDF or `confirmed-results.md`.",
        "Primary metric: typed exact micro F1 on Gold v2 (`cnss-lskt`).",
        "",
        f"- recommendation: **{rec}**",
        f"- JobBERT − vanilla v3: `{vs_van}`",
        f"- JobBERT − Qwen dump: `{vs_qwen}`",
        "",
        "| system | align | dev typed | official typed F1 | P | R | collapsed | TP/pred/gold |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for name, d in rows:
        lines.append(
            f"| {name} | {d.get('align', '—')} | {cell(d, 'best_dev')} | {cell(d, 'typed_f1')} | "
            f"{cell(d, 'p')} | {cell(d, 'r')} | {cell(d, 'collapsed_f1')} | "
            f"{d.get('tp', '—')}/{d.get('pred', '—')}/{d.get('gold', '—')} |"
        )
    lines += [
        "",
        "Notes:",
        "- Paper Qwen 0.2130 is unreproducible; not used here.",
        "- Old Qwen typed ~0.34 used raw Gold 2676, not Gold v2.",
        "- Demo is 80k sentences × 1 MLM epoch, not Zhang 3.2M / 3-epoch JobBERT.",
        "",
    ]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(
        json.dumps(
            {
                "rec": rec,
                "vs_vanilla": vs_van,
                "vs_qwen": vs_qwen,
                "jobbert": job,
                "vanilla_v3": van,
                "qwen": qwen,
                "report": str(OUT),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if job.get("ok") else 2


if __name__ == "__main__":
    raise SystemExit(main())
