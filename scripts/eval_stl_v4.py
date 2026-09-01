#!/usr/bin/env python3
"""Score JobBERT-zh 1M STL L/K/S/T heads on V4 hybrid gold.

Does not overwrite Gold v2, v4 silver, or the joint CRF dir
`output/jobbert_zh_1m/crf_lskt_v4_silver_seed42`.
Paper role: appendix backup until the user moves a row to the main text.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
sys.path.insert(0, str(PAPER / "scripts"))
sys.path.insert(0, str(PAPER / "scorer"))
import cws_snap as cws  # noqa: E402
import rewrite_train_goldstyle_v3 as g  # noqa: E402
from score_lskt import extract_spans, rec_id, score  # noqa: E402

TYPES = ("L", "K", "S", "T")
TYPE_RANK = {"S": 0, "K": 1, "T": 2, "L": 3}
GOLD = PAPER / "data/test_lskt_v4_cws_simhuman980_hybrid.jsonl"
JOINT_PRED = PAPER / "output/jobbert_zh_1m/crf_lskt_v4_silver_seed42/test_pred.jsonl"
JOINT_PRED_CWS = (
    PAPER / "reports/sandbox_lskt_v4_silver/hybrid_cws_eval/preds_cws/JobBERT_1M_v4.jsonl"
)
ROOT = PAPER / "output/stl_v4/jobbert_zh_1m/seed42"
OUT = PAPER / "reports/sandbox_lskt_v4_silver/stl_v4"
CSV_OUT = PAPER / "tables/appendix_stl_v4.csv"
TEX_OUT = PAPER / "tex/skillspan_style_stl_v4.tex"


def empty_pred(gold: dict) -> dict:
    toks = [str(t) for t in (gold.get("tokens") or list(gold.get("sentence") or ""))]
    tags = ["O"] * len(toks)
    return {
        "id": rec_id(gold),
        "sentence": gold.get("sentence") or "",
        "tokens": toks,
        "pred_tags": tags,
        "list_of_selection_bio4": tags,
    }


def snap_fill(src: Path, dst: Path, gold_map: dict[str, dict]) -> Path:
    raw = cws.load_jsonl(src)
    rows = [cws.rewrite_record(r, tag_field=None) for r in raw]
    by_id = {}
    for r in rows:
        try:
            by_id[rec_id(r)] = r
        except Exception:
            continue
    filled = []
    for gid, gold in gold_map.items():
        filled.append(by_id[gid] if gid in by_id else empty_pred(gold))
    extra = [r for i, r in by_id.items() if i not in gold_map]
    cws.write_jsonl(dst, filled + extra)
    return dst


def per_type_pack(report: dict) -> dict:
    te = report["typed_exact"]
    tr = report["typed_relaxed"]
    pt = report.get("per_type_exact") or {}
    out = {
        "alignment_ok": bool(report.get("alignment_ok")),
        "typed_exact_p": te["precision"],
        "typed_exact_r": te["recall"],
        "typed_exact_f1": te["f1"],
        "typed_relaxed_f1": tr["f1"],
        "per_type_exact": {
            k: {
                "precision": v["precision"],
                "recall": v["recall"],
                "f1": v["f1"],
                "gold": v["gold"],
                "pred": v["pred"],
                "tp": v.get("tp"),
            }
            for k, v in pt.items()
        },
    }
    return out


def merge_spans(span_lists: list[list[tuple[int, int, str]]]) -> list[tuple[int, int, str]]:
    all_s: list[tuple[int, int, str]] = []
    for spans in span_lists:
        for a, b, t in spans:
            if t in TYPES and b > a:
                all_s.append((int(a), int(b), t))
    all_s.sort(key=lambda x: (-(x[1] - x[0]), TYPE_RANK.get(x[2], 9), x[0]))
    kept: list[tuple[int, int, str]] = []
    occupied: set[int] = set()
    n_drop = 0
    for a, b, t in all_s:
        ids = set(range(a, b))
        if ids & occupied:
            n_drop += 1
            continue
        occupied |= ids
        kept.append((a, b, t))
    kept.sort(key=lambda x: x[0])
    return kept


def merge_four(pred_cws: dict[str, Path], gold_map: dict[str, dict], dst: Path) -> dict:
    by_type: dict[str, dict[str, dict]] = {}
    for typ, path in pred_cws.items():
        mp = {}
        for r in cws.load_jsonl(path):
            try:
                mp[rec_id(r)] = r
            except Exception:
                continue
        by_type[typ] = mp
    merged = []
    n_conflict = 0
    for gid, gold in gold_map.items():
        toks = [str(t) for t in (gold.get("tokens") or [])]
        n = len(toks)
        span_lists = []
        for typ in TYPES:
            rec = by_type.get(typ, {}).get(gid)
            if rec is None:
                span_lists.append([])
                continue
            rec_n = {"tokens": rec.get("tokens") or toks, "pred_tags": rec.get("pred_tags")}
            spans = [
                (a, b, t)
                for a, b, t in extract_spans(rec_n, ("pred_tags", "list_of_selection_bio4"))
                if t == typ
            ]
            span_lists.append(spans)
        before = sum(len(s) for s in span_lists)
        kept = merge_spans(span_lists)
        n_conflict += before - len(kept)
        tags = g.spans_to_bio(n, kept)
        merged.append(
            {
                "id": gid,
                "sentence": gold.get("sentence") or "",
                "tokens": toks,
                "pred_tags": tags,
                "list_of_selection_bio4": tags,
            }
        )
    cws.write_jsonl(dst, merged)
    return {"n_ids": len(merged), "n_overlap_dropped": n_conflict, "path": str(dst)}


def fmt(x: float | None) -> str:
    return "—" if x is None else f"{x:.4f}"


def write_tex(joint: dict, stl: dict[str, dict], merged: dict, path: Path) -> None:
    jpt = joint["per_type_exact"]
    lines = [
        "% STL vs joint CRF on V4 hybrid. Appendix backup. Do not put in abstract unless user moves it.",
        "\\begin{table}[t]",
        "\\centering",
        "\\small",
        "\\caption{Single-type CRF heads (STL) vs the joint 9-tag CRF. Encoder: JobBERT-zh 1M. Train: LSKT v4 silver. Test: V4 SOP+jieba hybrid, $n{=}2601$, scorer \\texttt{cnss-lskt-1.2.0}. STL-$X$ is trained with other types mapped to O. Combined = greedy non-overlap union of the four heads (longer span first, then S$\\succ$K$\\succ$T$\\succ$L). Not SkillSpan nested SKILL/KNOWLEDGE STL/MTL.}",
        "\\label{tab:stl-v4}",
        "\\begin{tabular}{lccccc}",
        "\\toprule",
        "System & L & K & S & T & typed exact \\\\",
        "\\midrule",
        f"Joint CRF (1M v4) & {jpt['L']['f1']:.3f} & {jpt['K']['f1']:.3f} & {jpt['S']['f1']:.3f} & {jpt['T']['f1']:.3f} & {joint['typed_exact_f1']:.4f} \\\\",
    ]
    for typ in TYPES:
        pt = stl[typ]["per_type_exact"]
        lines.append(
            f"STL-{typ} only & {pt['L']['f1']:.3f} & {pt['K']['f1']:.3f} & {pt['S']['f1']:.3f} & {pt['T']['f1']:.3f} & {stl[typ]['typed_exact_f1']:.4f} \\\\"
        )
    mpt = merged["per_type_exact"]
    lines += [
        f"STL combined & {mpt['L']['f1']:.3f} & {mpt['K']['f1']:.3f} & {mpt['S']['f1']:.3f} & {mpt['T']['f1']:.3f} & {merged['typed_exact_f1']:.4f} \\\\",
        "\\bottomrule",
        "\\end{tabular}",
        "\\end{table}",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    pred_dir = OUT / "preds_cws"
    pred_dir.mkdir(parents=True, exist_ok=True)
    gold_rows = cws.load_jsonl(GOLD)
    gold_map = {rec_id(r): r for r in gold_rows}

    missing = [t for t in TYPES if not (ROOT / t / "test_pred.jsonl").is_file()]
    if missing:
        print(json.dumps({"status": "pending", "missing_types": missing}, ensure_ascii=False))
        return 2

    joint_src = JOINT_PRED_CWS if JOINT_PRED_CWS.is_file() else JOINT_PRED
    joint_cws = pred_dir / "joint_1m_v4.jsonl"
    if JOINT_PRED_CWS.is_file():
        # already jieba-snapped in the hybrid eval
        cws.write_jsonl(joint_cws, cws.load_jsonl(JOINT_PRED_CWS))
    else:
        snap_fill(joint_src, joint_cws, gold_map)
    joint_rep = per_type_pack(score(str(GOLD), str(joint_cws), align_mode="official", n_boot=0))

    stl_cws: dict[str, Path] = {}
    stl_rep: dict[str, dict] = {}
    for typ in TYPES:
        src = ROOT / typ / "test_pred.jsonl"
        dst = pred_dir / f"stl_{typ}.jsonl"
        snap_fill(src, dst, gold_map)
        stl_cws[typ] = dst
        stl_rep[typ] = per_type_pack(score(str(GOLD), str(dst), align_mode="official", n_boot=0))

    merged_path = pred_dir / "stl_combined.jsonl"
    merge_meta = merge_four(stl_cws, gold_map, merged_path)
    merged_rep = per_type_pack(score(str(GOLD), str(merged_path), align_mode="official", n_boot=0))

    summary = {
        "protocol": "JobBERT-zh 1M STL L/K/S/T vs joint CRF; V4 hybrid jieba bilateral",
        "gold": str(GOLD),
        "scorer": "cnss-lskt-1.2.0",
        "seed": 42,
        "paper_role": "appendix_backup",
        "do_not_overwrite": [
            "data/gold_canonical_v2.jsonl",
            "output/jobbert_zh_1m/crf_lskt_v4_silver_seed42",
        ],
        "joint_1m_v4": joint_rep,
        "stl": stl_rep,
        "combined": merged_rep,
        "merge": merge_meta,
        "move_to_main_if": "combined typed exact > joint 0.4272, or a type F1 clearly beats joint on that type without collapsing micro",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
    with CSV_OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "system",
                "typed_exact_f1",
                "typed_relaxed_f1",
                "L_f1",
                "K_f1",
                "S_f1",
                "T_f1",
                "note",
            ]
        )
        w.writerow(
            [
                "Joint CRF JobBERT 1M v4",
                f"{joint_rep['typed_exact_f1']:.6f}",
                f"{joint_rep['typed_relaxed_f1']:.6f}",
                f"{joint_rep['per_type_exact']['L']['f1']:.6f}",
                f"{joint_rep['per_type_exact']['K']['f1']:.6f}",
                f"{joint_rep['per_type_exact']['S']['f1']:.6f}",
                f"{joint_rep['per_type_exact']['T']['f1']:.6f}",
                "existing main-protocol row 0.4272",
            ]
        )
        for typ in TYPES:
            r = stl_rep[typ]
            w.writerow(
                [
                    f"STL-{typ}",
                    f"{r['typed_exact_f1']:.6f}",
                    f"{r['typed_relaxed_f1']:.6f}",
                    f"{r['per_type_exact']['L']['f1']:.6f}",
                    f"{r['per_type_exact']['K']['f1']:.6f}",
                    f"{r['per_type_exact']['S']['f1']:.6f}",
                    f"{r['per_type_exact']['T']['f1']:.6f}",
                    f"head trained on {typ} only; other-type F1 near 0 is expected",
                ]
            )
        w.writerow(
            [
                "STL combined",
                f"{merged_rep['typed_exact_f1']:.6f}",
                f"{merged_rep['typed_relaxed_f1']:.6f}",
                f"{merged_rep['per_type_exact']['L']['f1']:.6f}",
                f"{merged_rep['per_type_exact']['K']['f1']:.6f}",
                f"{merged_rep['per_type_exact']['S']['f1']:.6f}",
                f"{merged_rep['per_type_exact']['T']['f1']:.6f}",
                f"greedy non-overlap; dropped {merge_meta['n_overlap_dropped']} overlapping spans",
            ]
        )

    write_tex(joint_rep, stl_rep, merged_rep, TEX_OUT)
    bundle = PAPER / "overleaf_cursor_bundle/tex/skillspan_style_stl_v4.tex"
    bundle.parent.mkdir(parents=True, exist_ok=True)
    bundle.write_text(TEX_OUT.read_text(encoding="utf-8"), encoding="utf-8")

    print(
        json.dumps(
            {
                "joint_exact": joint_rep["typed_exact_f1"],
                "combined_exact": merged_rep["typed_exact_f1"],
                "stl_type_f1": {t: stl_rep[t]["per_type_exact"][t]["f1"] for t in TYPES},
                "joint_type_f1": {t: joint_rep["per_type_exact"][t]["f1"] for t in TYPES},
                "csv": str(CSV_OUT),
                "tex": str(TEX_OUT),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
