#!/usr/bin/env python3
"""Aggregate checkpoint CRF sweep results into JSON + markdown."""
from __future__ import annotations

import json
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
SWEEP = PAPER / "output/jobbert_zh_3m_ckpt_sweep"
LEGACY = [
    ("ckpt65000_manual", PAPER / "output/jobbert_zh_3m/crf_ckpt65000_ep1/run_summary.json"),
    ("final_encoder", PAPER / "output/jobbert_zh_3m/crf_v3_seed42/run_summary.json"),
]
REF_1M = PAPER / "output/jobbert_zh_1m/crf_v3_seed42/run_summary.json"


def load_summary(path: Path) -> dict | None:
    if not path.is_file():
        return None
    s = json.loads(path.read_text(encoding="utf-8"))
    te = s.get("typed_exact") or {}
    return {
        "path": str(path),
        "step": None,
        "epoch": None,
        "best_dev": s.get("best_dev_typed_f1"),
        "typed_f1": te.get("f1"),
        "p": te.get("precision"),
        "r": te.get("recall"),
        "tp": te.get("tp"),
        "pred": te.get("pred"),
        "gold": te.get("gold"),
        "model_dir": s.get("model_dir"),
    }


def main() -> None:
    rows = []
    if SWEEP.is_dir():
        for d in sorted(SWEEP.glob("crf_ckpt*"), key=lambda p: int(p.name.replace("crf_ckpt", ""))):
            step = int(d.name.replace("crf_ckpt", ""))
            rec = load_summary(d / "run_summary.json")
            if rec:
                rec["step"] = step
                meta = PAPER / f"output/jobbert_zh_3m/mlm/encoder_ckpt{step}/export_meta.json"
                if not meta.is_file():
                    meta = PAPER / "output/jobbert_zh_3m_ckpt_archive/mlm/encoder_ckpt{step}/export_meta.json"
                if meta.is_file():
                    m = json.loads(meta.read_text())
                    rec["epoch"] = m.get("epoch")
                rows.append(rec)
    for label, path in LEGACY:
        rec = load_summary(path)
        if rec:
            rec["label"] = label
            # skip duplicate if sweep already has same path content
            if any(r.get("typed_f1") == rec.get("typed_f1") and r.get("tp") == rec.get("tp") for r in rows):
                continue
            rows.append(rec)
    ref = load_summary(REF_1M)
    rows.sort(key=lambda r: r.get("step") if r.get("step") is not None else 10**9)
    out = {
        "n": len(rows),
        "paper_numbers": False,
        "ref_1m_typed_f1": ref.get("typed_f1") if ref else None,
        "rows": rows,
        "note": "Gold v2 typed exact micro F1. Internal sweep only.",
    }
    jpath = PAPER / "reports/gold_style_relabel/jobbert_3m_ckpt_sweep.json"
    jpath.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# JobBERT-zh 3.2M checkpoint CRF sweep",
        "",
        "Internal only. Gold v2 typed exact micro F1.",
        "",
        f"Reference JobBERT 1M: typed F1 = {ref.get('typed_f1') if ref else '—'}",
        "",
        "| step | epoch | dev | test typed F1 | P | R | TP/pred |",
        "|---:|---:|---:|---:|---:|---:|---|",
    ]
    for r in rows:
        step = r.get("step") if r.get("step") is not None else r.get("label", "—")
        ep = f"{r.get('epoch'):.2f}" if isinstance(r.get("epoch"), (int, float)) else "—"
        lines.append(
            f"| {step} | {ep} | {r.get('best_dev') or 0:.4f} | {r.get('typed_f1') or 0:.4f} | "
            f"{r.get('p') or 0:.4f} | {r.get('r') or 0:.4f} | {r.get('tp')}/{r.get('pred')} |"
        )
    mpath = PAPER / "reports/gold_style_relabel/jobbert_3m_ckpt_sweep.md"
    mpath.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
