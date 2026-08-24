#!/usr/bin/env python3
"""Score 1M JobBERTa-zh CRF vs vanilla v3. Decide whether to launch 3.2M.

Internal only. Does not write paper numbers or confirmed-results.md.
"""
from __future__ import annotations

import json
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
ROOT = PAPER.parent
JOB = PAPER / "output/jobbert_zh_1m/crf_v3_seed42/run_summary.json"
VAN = PAPER / "output/cn_roberta_wwm_crf/smoke_goldstyle_v3_seed42/run_summary.json"
DEMO = PAPER / "output/jobbert_zh_demo/crf_v3_seed42/run_summary.json"
V2 = PAPER / "output/cn_roberta_wwm_crf/smoke_goldstyle_v2_seed42/run_summary.json"
SILVER = PAPER / "output/cn_roberta_wwm_crf/smoke_seed42_gpu1/run_summary.json"
QWEN = PAPER / "reports/score_v2_unique_Qwen.json"
JB_SK = PAPER / "reports/score_v2_unique_JobBERT-skill.json"
OUT_MD = PAPER / "reports/gold_style_relabel/jobbert_1m_result.md"
OUT_DEC = PAPER / "output/jobbert_zh_1m/decision.json"
BASE = ROOT / "Baseline_Models_Collection/chinese-roberta-wwm-ext"
ENC_1M = PAPER / "output/jobbert_zh_1m/mlm/encoder"


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


def decide(jf, vf, df) -> dict:
    """Recipe for the next rung. Internal smoke only."""
    vs_van = None
    if isinstance(jf, (int, float)) and isinstance(vf, (int, float)):
        vs_van = jf - vf
    lift = isinstance(vs_van, float) and vs_van > 0
    flat = isinstance(vs_van, float) and abs(vs_van) < 0.005
    worse = isinstance(vs_van, float) and vs_van <= -0.005
    if lift:
        return {
            "rec": "lift_continue_1m_encoder_3p2m_2ep",
            "launch_3m": True,
            "init_model": str(ENC_1M),
            "epochs": 2,
            "why": "1M typed F1 above vanilla; continue DAPT on Zhang-scale 3.2M for 2 epochs.",
        }
    if worse:
        return {
            "rec": "drop_hold_3m_corpus",
            "launch_3m": False,
            "init_model": str(BASE),
            "epochs": 3,
            "why": "1M clearly below vanilla; keep 3.2M corpus ready, do not spend two more GPU hours on the same recipe.",
        }
    return {
        "rec": "flat_zhang_scale_3p2m_from_base_3ep",
        "launch_3m": True,
        "init_model": str(BASE),
        "epochs": 3,
        "why": "1M flat vs vanilla (80k demo also flat). Launch Zhang-scale 3.2M x 3 from base while GPUs are free.",
    }


def main() -> int:
    job = from_summary(JOB)
    van = from_summary(VAN)
    demo = from_summary(DEMO)
    v2 = from_summary(V2)
    sv = from_summary(SILVER)
    qwen = from_score(QWEN)
    jb = from_score(JB_SK)
    jf = job.get("typed_f1")
    vf = van.get("typed_f1")
    df = demo.get("typed_f1")
    plan = decide(jf, vf, df)
    vs_van = "n/a"
    vs_demo = "n/a"
    if isinstance(jf, (int, float)) and isinstance(vf, (int, float)):
        vs_van = f"{jf - vf:+.4f}"
    if isinstance(jf, (int, float)) and isinstance(df, (int, float)):
        vs_demo = f"{jf - df:+.4f}"

    rows = [
        ("JobBERTa-zh 1M CRF (1M×3 MLM + v3)", job),
        ("JobBERT-zh demo CRF (80k×1 MLM + v3)", demo),
        ("RoBERTa-wwm + CRF (no DAPT, v3)", van),
        ("RoBERTa-wwm + CRF goldstyle v2", v2),
        ("RoBERTa-wwm + CRF silver", sv),
        ("Qwen dump (Gold v2 unique)", qwen),
        ("English JobBERT-skill transfer", jb),
    ]
    lines = [
        "# JobBERTa-zh 1M vs encoder / dumps",
        "",
        "Internal smoke only. Do **not** copy into the PDF or `confirmed-results.md`.",
        "Primary metric: typed exact micro F1 on Gold v2 (`cnss-lskt`).",
        "",
        f"- recommendation: **{plan['rec']}**",
        f"- launch_3m: `{plan['launch_3m']}`",
        f"- 1M − vanilla v3: `{vs_van}`",
        f"- 1M − 80k demo: `{vs_demo}`",
        f"- next init: `{plan['init_model']}`",
        f"- next epochs: `{plan['epochs']}`",
        f"- why: {plan['why']}",
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
        "- 3.2M target follows Zhang JobBERT / JobBERTa sentence scale, not paper numbers.",
        "- Mix stays corpus-train 59:41 (应届生/人工智能). Gold has 阿里云/事业单位; those CSVs are still missing.",
        "",
    ]
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    dec = {
        "ok": bool(job.get("ok")),
        "rec": plan["rec"],
        "launch_3m": bool(plan["launch_3m"] and job.get("ok")),
        "init_model": plan["init_model"],
        "epochs": plan["epochs"],
        "why": plan["why"],
        "vs_vanilla": vs_van,
        "vs_demo": vs_demo,
        "jobbert_1m": job,
        "vanilla_v3": van,
        "demo_80k": demo,
        "report": str(OUT_MD),
        "paper_numbers": False,
    }
    OUT_DEC.parent.mkdir(parents=True, exist_ok=True)
    OUT_DEC.write_text(json.dumps(dec, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(dec, ensure_ascii=False, indent=2))
    return 0 if job.get("ok") else 2


if __name__ == "__main__":
    raise SystemExit(main())
