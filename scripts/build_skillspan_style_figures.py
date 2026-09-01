#!/usr/bin/env python3
"""SkillSpan-style tables and figures for Chinese-SkillSpan (PeerJ CS).

Corpus stats and span-length plots are computed from frozen jsonl.
F1 bars / heatmaps use only numbers already in tables/*.csv (no new F1).
Does not train STL/MTL or SpanBERT-from-scratch.
"""
from __future__ import annotations

import csv
import json
import math
import shutil
import statistics
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
TABLES = PAPER / "tables"
FIG = PAPER / "figures"
TEX = PAPER / "tex"
BUNDLE_FIG = PAPER / "overleaf_cursor_bundle" / "figures"
BUNDLE_TEX = PAPER / "overleaf_cursor_bundle" / "tex"
STYLE_CSV = TABLES / "skillspan_style"

DOMAIN_MAP = {
    "人工智能招聘": "AI",
    "阿里云公开数据集": "Cloud",
    "事业单位招聘": "Public",
    "应届生招聘": "Grad",
}
DOMAIN_ORDER = ("AI", "Cloud", "Public", "Grad")
SKILL_TYPES = {"S", "T"}
KNOW_TYPES = {"L", "K"}

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.size": 9,
        "axes.labelsize": 10,
        "axes.titlesize": 10,
        "figure.dpi": 160,
        "savefig.dpi": 300,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "axes.grid": True,
        "grid.linestyle": ":",
        "grid.alpha": 0.5,
        "axes.axisbelow": True,
    }
)


def r4(x: float) -> str:
    return f"{x:.4f}"


def iter_jsonl(path: Path):
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def tags_to_spans(tags: list[str]) -> list[tuple[int, int, str]]:
    spans: list[tuple[int, int, str]] = []
    i = 0
    n = len(tags)
    while i < n:
        t = tags[i] or "O"
        if t.startswith("B-"):
            typ = t[2:]
            j = i + 1
            while j < n and (tags[j] or "O") == f"I-{typ}":
                j += 1
            spans.append((i, j, typ))
            i = j
        else:
            i += 1
    return spans


def rec_spans(rec: dict) -> list[tuple[int, int, str]]:
    if rec.get("cws_spans"):
        out = []
        for item in rec["cws_spans"]:
            out.append((int(item[0]), int(item[1]), str(item[2])))
        return out
    if rec.get("v4_spans"):
        out = []
        for item in rec["v4_spans"]:
            out.append((int(item[0]), int(item[1]), str(item[2])))
        return out
    if rec.get("goldstyle_spans"):
        out = []
        for item in rec["goldstyle_spans"]:
            out.append((int(item[0]), int(item[1]), str(item[2])))
        return out
    for key in ("list_of_selection_bio4", "pred_tags", "tags_skill_clean"):
        tags = rec.get(key)
        if isinstance(tags, list) and tags:
            return tags_to_spans([str(t) for t in tags])
    return []


def rec_domain(rec: dict) -> str:
    raw = str(rec.get("source_domain") or "UNKNOWN")
    return DOMAIN_MAP.get(raw, raw if raw in DOMAIN_ORDER else "Other")


def span_text(rec: dict, start: int, end: int) -> str:
    toks = rec.get("tokens") or []
    if toks:
        return "".join(str(t) for t in toks[start:end])
    sent = str(rec.get("sentence") or "")
    return sent[start:end]


def collect_split(path: Path) -> dict:
    posts = defaultdict(set)
    n_sent = Counter()
    n_tok = Counter()
    n_span = {k: Counter() for k in ("L", "K", "S", "T", "skill", "know")}
    lengths = defaultdict(list)  # (split_domain, bucket) -> lengths
    freq_skill = defaultdict(Counter)
    freq_know = defaultdict(Counter)
    n_overlap = Counter()
    n_rows = 0
    for rec in iter_jsonl(path):
        n_rows += 1
        d = rec_domain(rec)
        gid = str(rec.get("global_id") or rec.get("id") or "")
        posts[d].add(gid.split("-")[0] if gid else str(n_rows))
        posts["Total"].add(gid.split("-")[0] if gid else str(n_rows))
        n_sent[d] += 1
        n_sent["Total"] += 1
        toks = rec.get("tokens") or []
        n_tok[d] += len(toks) if toks else len(str(rec.get("sentence") or ""))
        n_tok["Total"] += len(toks) if toks else len(str(rec.get("sentence") or ""))
        spans = rec_spans(rec)
        # flat LSKT: overlaps should be 0
        covered = []
        for s, e, typ in spans:
            typ = typ.upper()
            n_span[typ if typ in "LKST" else "S"][d] += 1
            n_span[typ if typ in "LKST" else "S"]["Total"] += 1
            bucket = "skill" if typ in SKILL_TYPES else "know"
            n_span[bucket][d] += 1
            n_span[bucket]["Total"] += 1
            ln = max(1, int(e) - int(s))
            lengths[(d, bucket)].append(ln)
            lengths[("Total", bucket)].append(ln)
            text = span_text(rec, int(s), int(e)).strip()
            if text:
                (freq_skill if bucket == "skill" else freq_know)[d][text] += 1
            covered.append((int(s), int(e)))
        covered.sort()
        for i in range(1, len(covered)):
            if covered[i][0] < covered[i - 1][1]:
                n_overlap[d] += 1
                n_overlap["Total"] += 1
                break
    return {
        "n_rows": n_rows,
        "posts": {k: len(v) for k, v in posts.items()},
        "n_sent": dict(n_sent),
        "n_tok": dict(n_tok),
        "n_span": {k: dict(v) for k, v in n_span.items()},
        "n_overlap": dict(n_overlap),
        "lengths": lengths,
        "freq_skill": {k: v.most_common(5) for k, v in freq_skill.items()},
        "freq_know": {k: v.most_common(5) for k, v in freq_know.items()},
    }


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def stats_rows(split: str, blob: dict) -> list[dict]:
    rows = []
    cols = [c for c in DOMAIN_ORDER if blob["n_sent"].get(c)] + ["Total"]
    metrics = [
        ("# Posts", lambda c: blob["posts"].get(c, 0)),
        ("# Sentences", lambda c: blob["n_sent"].get(c, 0)),
        ("# Tokens", lambda c: blob["n_tok"].get(c, 0)),
        ("# Skill spans (S+T)", lambda c: blob["n_span"]["skill"].get(c, 0)),
        ("# Knowledge spans (L+K)", lambda c: blob["n_span"]["know"].get(c, 0)),
        ("# L", lambda c: blob["n_span"]["L"].get(c, 0)),
        ("# K", lambda c: blob["n_span"]["K"].get(c, 0)),
        ("# S", lambda c: blob["n_span"]["S"].get(c, 0)),
        ("# T", lambda c: blob["n_span"]["T"].get(c, 0)),
        ("# Sentences with overlap", lambda c: blob["n_overlap"].get(c, 0)),
    ]
    for metric, fn in metrics:
        row = {"split": split, "metric": metric}
        for c in DOMAIN_ORDER + ("Total",):
            row[c] = fn(c) if c in cols or c == "Total" else ""
        rows.append(row)
    return rows


def fig_violin(split_blobs: dict[str, dict], out: Path, title: str | None = None) -> None:
    facets = list(split_blobs.keys())
    fig, axes = plt.subplots(1, len(facets), figsize=(3.1 * len(facets), 3.6), sharey=True)
    if len(facets) == 1:
        axes = [axes]
    colors = {"skill": "#4C78A8", "know": "#F58518"}
    for ax, name in zip(axes, facets):
        blob = split_blobs[name]
        xs_skill, xs_know, labels = [], [], []
        pos_s, pos_k = [], []
        i = 0
        for d in DOMAIN_ORDER:
            sl = blob["lengths"].get((d, "skill")) or []
            kl = blob["lengths"].get((d, "know")) or []
            if not sl and not kl:
                continue
            i += 1
            labels.append(d)
            if sl:
                xs_skill.append(sl)
                pos_s.append(i - 0.18)
            if kl:
                xs_know.append(kl)
                pos_k.append(i + 0.18)
        parts_s = ax.violinplot(xs_skill, positions=pos_s, widths=0.32, showmeans=False, showextrema=True, showmedians=True)
        parts_k = ax.violinplot(xs_know, positions=pos_k, widths=0.32, showmeans=False, showextrema=True, showmedians=True)
        for pc in parts_s["bodies"]:
            pc.set_facecolor(colors["skill"])
            pc.set_alpha(0.7)
        for pc in parts_k["bodies"]:
            pc.set_facecolor(colors["know"])
            pc.set_alpha(0.7)
        ax.set_xticks(range(1, len(labels) + 1))
        ax.set_xticklabels(labels, rotation=20)
        ax.set_title(name)
        ax.set_ylim(0, 25)
        if ax is axes[0]:
            ax.set_ylabel("Length in tokens")
    handles = [
        plt.matplotlib.patches.Patch(facecolor=colors["skill"], alpha=0.7, label="Skill (S+T)"),
        plt.matplotlib.patches.Patch(facecolor=colors["know"], alpha=0.7, label="Knowledge (L+K)"),
    ]
    axes[-1].legend(handles=handles, frameon=True, fontsize=8)
    fig.suptitle(
        title
        or "Span-length distributions (V4 silver train/dev; V4 hybrid test gold)",
        y=1.02,
        fontsize=10,
    )
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(out.with_suffix(".png"), bbox_inches="tight")
    plt.close(fig)


def fig_v4_bars(out: Path) -> None:
    # Confirmed P2 numbers (hybrid CSV / confirmed-results). Single-run unless noted.
    rows = [
        ("JobBERT-zh 3M v4", 0.4331, 0.5873, None, None),
        ("JobBERT-zh 1M v4", 0.4272, 0.5952, None, None),
        ("1M CWS retrain", 0.4049, 0.5904, None, None),
        ("goldstyle 1M (3-seed)", 0.3032, 0.5332, None, None),
        ("RoBERTa-wwm (3-seed)", 0.2875, 0.5206, None, None),
        ("ChatGPT gpt-4o dump", 0.2854, 0.6249, None, None),
        ("DeepSeek-r1 dump", 0.0802, 0.1577, None, None),
        ("Qwen2.5-14B dump", 0.0501, 0.1409, None, None),
    ]
    # 3-seed std on P2 from hybrid_cws_simhuman980_all_models.csv
    p2 = {r["model"]: r for r in csv.DictReader((TABLES / "hybrid_cws_simhuman980_all_models.csv").open())}

    def seed_std(keys: list[str], field: str) -> float:
        xs = [float(p2[k][field]) for k in keys if k in p2]
        return statistics.stdev(xs) if len(xs) > 1 else 0.0

    std_map = {
        "goldstyle 1M (3-seed)": (
            seed_std(["JobBERT_1M_v3_s42", "JobBERT_1M_v3_s123", "JobBERT_1M_v3_s2026"], "full2601_typed_exact_f1"),
            seed_std(["JobBERT_1M_v3_s42", "JobBERT_1M_v3_s123", "JobBERT_1M_v3_s2026"], "full2601_typed_relaxed_f1"),
        ),
        "RoBERTa-wwm (3-seed)": (
            seed_std(["RoBERTa_wwm_v3_s42", "RoBERTa_wwm_v3_s123", "RoBERTa_wwm_v3_s2026"], "full2601_typed_exact_f1"),
            seed_std(["RoBERTa_wwm_v3_s42", "RoBERTa_wwm_v3_s123", "RoBERTa_wwm_v3_s2026"], "full2601_typed_relaxed_f1"),
        ),
    }
    labels = [r[0] for r in rows]
    exact = np.array([r[1] for r in rows])
    relax = np.array([r[2] for r in rows])
    e_std = np.array([std_map.get(r[0], (0.0, 0.0))[0] for r in rows])
    r_std = np.array([std_map.get(r[0], (0.0, 0.0))[1] for r in rows])
    x = np.arange(len(labels))
    w = 0.38
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    ax.bar(
        x - w / 2,
        exact,
        w,
        yerr=e_std,
        capsize=2,
        label="Typed exact",
        color="#4C78A8",
        hatch="oo",
        edgecolor="black",
        linewidth=0.4,
        error_kw={"ecolor": "black", "elinewidth": 0.8},
    )
    ax.bar(
        x + w / 2,
        relax,
        w,
        yerr=r_std,
        capsize=2,
        label="Typed relaxed (IoU≥0.5)",
        color="#F58518",
        hatch="//",
        edgecolor="black",
        linewidth=0.4,
        error_kw={"ecolor": "black", "elinewidth": 0.8},
    )
    ax.set_ylabel("Span-F1")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=28, ha="right")
    ax.set_ylim(0, 0.72)
    ax.legend(frameon=True, fontsize=8)
    ax.set_title("V4 matched protocol (2601 IDs; jieba on gold and pred)")
    fig.tight_layout()
    fig.savefig(out.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(out.with_suffix(".png"), bbox_inches="tight")
    plt.close(fig)
    write_csv(
        STYLE_CSV / "fig_v4_performance.csv",
        [
            {
                "model": a,
                "typed_exact": r4(b),
                "typed_relaxed": r4(c),
                "exact_std": r4(d) if d else "",
                "relaxed_std": r4(e) if e else "",
            }
            for (a, b, c, _, _), d, e in zip(rows, e_std, r_std)
        ],
        ["model", "typed_exact", "typed_relaxed", "exact_std", "relaxed_std"],
    )


def fig_winrate(out: Path) -> None:
    rows = list(csv.DictReader((TABLES / "appendix_aso_encoder_3seed_gold_v2.csv").open()))
    names = []
    for r in rows:
        if r["row"] not in names:
            names.append(r["row"])
    short = {
        "JobBERT 1M goldstyle v3": "JobBERT 1M",
        "domain-mix 1M": "domain-mix",
        "JobBERT 3M ckpt65000": "JobBERT 3M",
        "RoBERTa-wwm v3": "RoBERTa-wwm",
    }
    labels = [short.get(n, n) for n in names]
    mat = np.full((len(names), len(names)), np.nan)
    lookup = {(r["row"], r["col"]): float(r["p_row_gt_col"]) for r in rows}
    for i, a in enumerate(names):
        for j, b in enumerate(names):
            mat[i, j] = lookup.get((a, b), np.nan)
            if i == j:
                mat[i, j] = np.nan
    fig, ax = plt.subplots(figsize=(4.6, 3.8))
    im = ax.imshow(mat, cmap="Greens", vmin=0, vmax=1)
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=30, ha="right")
    ax.set_yticklabels(labels)
    for i in range(len(names)):
        for j in range(len(names)):
            if math.isnan(mat[i, j]):
                ax.text(j, i, "—", ha="center", va="center", fontsize=8)
            else:
                ax.text(j, i, f"{mat[i, j]:.2f}", ha="center", va="center", fontsize=8, color="black")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label=r"$P$(row seed F1 $>$ col seed F1)")
    ax.set_title("Gold v2 encoder seed win-rate (n=3; not ASO)")
    fig.tight_layout()
    fig.savefig(out.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(out.with_suffix(".png"), bbox_inches="tight")
    plt.close(fig)


def fig_pred_len(out: Path) -> None:
    rows = list(csv.DictReader((TABLES / "appendix_span_length_mean_gold_v2.csv").open()))
    models = [
        ("Gold v2", None, "mean_gold_len"),
        ("ChatGPT dump", "ChatGPT (gpt-4o)", "mean_pred_len"),
        ("JobBERT 1M", "JobBERT 1M seed42", "mean_pred_len"),
        ("RoBERTa-wwm", "RoBERTa-wwm v3 seed42", "mean_pred_len"),
    ]
    domains = ["人工智能招聘", "阿里云公开数据集", "事业单位招聘"]
    dlab = ["AI", "Cloud", "Public"]
    hatches = ["", "//", ".."]
    colors = ["#E45756", "#B279A2", "#54A24B"]
    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    x = np.arange(len(models))
    w = 0.25
    for i, (dom, lab, h, c) in enumerate(zip(domains, dlab, hatches, colors)):
        ys = []
        for _, sys, key in models:
            if sys is None:
                hit = next((r for r in rows if r["system"] == "ChatGPT (gpt-4o)" and r["domain"] == dom), None)
            else:
                hit = next((r for r in rows if r["system"] == sys and r["domain"] == dom), None)
            ys.append(float(hit[key]) if hit else 0.0)
        ax.bar(x + (i - 1) * w, ys, w, label=lab, color=c, hatch=h, edgecolor="black", linewidth=0.4)
    ax.set_ylabel("Avg. length in tokens")
    ax.set_xticks(x)
    ax.set_xticklabels([m[0] for m in models], rotation=15, ha="right")
    ax.set_ylim(0, 7)
    ax.legend(ncol=3, fontsize=8, frameon=True)
    ax.set_title("Gold v2: gold vs predicted mean span length by domain")
    fig.tight_layout()
    fig.savefig(out.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(out.with_suffix(".png"), bbox_inches="tight")
    plt.close(fig)


def fig_f1_by_len(out: Path) -> None:
    rows = list(csv.DictReader((TABLES / "appendix_span_length_f1_gold_v2.csv").open()))
    systems = [
        ("ChatGPT (gpt-4o)", "#4C78A8", "oo"),
        ("JobBERT 1M seed42", "#F58518", "//"),
        ("RoBERTa-wwm v3 seed42", "#54A24B", ".."),
    ]
    buckets = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10+"]
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    x = np.arange(len(buckets))
    w = 0.26
    for i, (sys, c, h) in enumerate(systems):
        ys, ns = [], []
        for b in buckets:
            hit = next((r for r in rows if r["system"] == sys and r["bucket"] == b), None)
            ys.append(float(hit["f1"]) if hit else 0.0)
            ns.append(int(float(hit["gold"])) if hit else 0)
        ax.bar(x + (i - 1) * w, ys, w, label=sys.replace(" (gpt-4o)", ""), color=c, hatch=h, edgecolor="black", linewidth=0.35)
        if i == 0:
            for xi, n in zip(x, ns):
                ax.text(xi, 0.01, str(n), ha="center", va="bottom", fontsize=6, rotation=90, color="#333333")
    ax.set_xticks(x)
    ax.set_xticklabels(buckets)
    ax.set_xlabel("Gold span length (tokens)")
    ax.set_ylabel("Span-F1")
    ax.set_ylim(0, 0.85)
    ax.legend(fontsize=8)
    ax.set_title("Gold v2 typed exact F1 by gold span length (support = ChatGPT gold n)")
    fig.tight_layout()
    fig.savefig(out.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(out.with_suffix(".png"), bbox_inches="tight")
    plt.close(fig)


def latex_related_work() -> str:
    return r"""% Related-work comparison (SkillSpan Table 1 analogue). Cite sources; do not copy SkillSpan English F1.
% Requires: booktabs, graphicx, pifont (or replace \cmark/\xmark)
\begin{table}[t]
\centering
\caption{Span-level skill extraction resources. Size is annotated data (not DAPT).
$\checkmark$ = publicly released with the paper.
Corpus counts in this paper's Table~\ref{tab:dataset-stats} use the source-stratified split (16{,}350 / 2{,}268 / 4{,}222 sentences).
Reported span-F1 in the main results table remains the V4 SOP+jieba hybrid on the same 2{,}601 Gold v2 IDs.}
\label{tab:related-span}
\scriptsize
\setlength{\tabcolsep}{3pt}
\begin{tabular}{l l l r l l c c}
\toprule
\textbf{Work} & \textbf{Ann.} & \textbf{Approach} & \textbf{Size} & \textbf{Types} & \textbf{Models} & \textbf{Data} & \textbf{Guide.} \\
\midrule
Sayfullina et al.\ (2018) & Span & Crowdsourcing & 4{,}863 sent. & Soft & CNN/LSTM & $\checkmark$ & $\times$ \\
Gnehm et al.\ (2021) & Span & Manual & $\sim$3{,}000 sent. & Hard & BERT & $\checkmark$ & $\times$ \\
Zhang et al.\ (2022) & Span & Domain experts & 391 JPs / 14.5K sent. & Both (nested) & JobBERT & $\checkmark$ & $\checkmark$ \\
\textbf{This work} & Span & LLM silver + Doccano & 16{,}350 train sent.; 4{,}222 eval sent.\textsuperscript{*} & LSKT (flat) & JobBERT-zh, LLMs & $\times^\dagger$ & $\checkmark$ \\
\bottomrule
\end{tabular}
\end{table}
\vspace{-0.4em}
{\scriptsize $^\dagger$Private backup at submission; guidelines in the paper / SI (Handbook B).
$^*$Evaluation 4{,}222 are LSKT v4 silver drafts (pre-release). Provenance Gold v2 remains 2{,}601 IDs.}
"""


def latex_dataset_stats(rows: list[dict]) -> str:
    splits = []
    for r in rows:
        if r["split"] not in splits:
            splits.append(r["split"])
    lines = [
        r"% Dataset statistics (SkillSpan Table 2 analogue). Cyan = totals.",
        r"% Requires: booktabs, xcolor, colortbl, rotating, multirow",
        r"\definecolor{totcyan}{RGB}{210,235,242}",
        r"\begin{table}[t]",
        r"\centering",
        r"\caption{Statistics of Chinese-SkillSpan. Train/dev spans follow LSKT v4 silver; Test-V4 is the paper main gold (SOP-CWS + 980 SimHuman, jieba). AI/Cloud/Public are \texttt{source\_domain} values; Grad = 应届生招聘 (train/dev only). Overlap is 0 because labels are flat.}",
        r"\label{tab:dataset-stats}",
        r"\scriptsize",
        r"\setlength{\tabcolsep}{3.5pt}",
        r"\begin{tabular}{ll rrrr | r}",
        r"\toprule",
        r"\multicolumn{2}{l}{\textbf{Statistics} $\downarrow$ / src. $\rightarrow$} & \textbf{AI} & \textbf{Cloud} & \textbf{Public} & \textbf{Grad} & \cellcolor{totcyan}{\textbf{Total}} \\",
        r"\midrule",
    ]
    def cell(v):
        if v in ("", None):
            return "---"
        return f"{int(v):,}"

    for split in splits:
        sub = [r for r in rows if r["split"] == split]
        n = len(sub)
        for i, r in enumerate(sub):
            left = r"\multirow{" + str(n) + r"}{*}{\rotatebox{90}{\textbf{" + split + "}}}" if i == 0 else ""
            tot = r"\cellcolor{totcyan}{" + cell(r["Total"]) + "}"
            lines.append(
                f"{left} & {r['metric']} & {cell(r['AI'])} & {cell(r['Cloud'])} & {cell(r['Public'])} & {cell(r['Grad'])} & {tot} \\\\"
            )
        lines.append(r"\midrule" if split != splits[-1] else r"\bottomrule")
    lines += [r"\end{tabular}", r"\end{table}", ""]
    return "\n".join(lines)


def latex_top(freq_skill: dict, freq_know: dict) -> str:
    def five(counter_list, d):
        items = freq_skill.get(d) if counter_list == "s" else freq_know.get(d)
        if not items:
            return "---"
        return "; ".join(t for t, _ in items)

    # rebuild from passed dicts of domain -> [(text, n)]
    def join(d, which):
        src = freq_skill if which == "s" else freq_know
        items = src.get(d) or []
        if not items:
            return "---"
        return "; ".join(t for t, _ in items)

    return r"""\begin{table}[t]
\centering
\caption{Top-5 Skill (S+T) and Knowledge (L+K) surface strings on \textbf{Gold v2} (Doccano provenance; same 2{,}601 IDs as V4). V4 hybrid frequencies (noisier SOP strings on Public) are in \texttt{tables/skillspan\_style/top5\_spans\_v4.csv}.}
\label{tab:top-spans}
\scriptsize
\begin{tabular}{l p{0.28\linewidth} p{0.28\linewidth} p{0.28\linewidth}}
\toprule
 & \textbf{AI} & \textbf{Cloud} & \textbf{Public} \\
\midrule
\rotatebox{90}{\textbf{SKILL}} & %s & %s & %s \\
\midrule
\rotatebox{90}{\textbf{KNOW.}} & %s & %s & %s \\
\bottomrule
\end{tabular}
\end{table}
""" % (
        join("AI", "s"),
        join("Cloud", "s"),
        join("Public", "s"),
        join("AI", "k"),
        join("Cloud", "k"),
        join("Public", "k"),
    )


def copy_outputs() -> None:
    for dst in (BUNDLE_FIG, BUNDLE_TEX, STYLE_CSV):
        dst.mkdir(parents=True, exist_ok=True)
    for p in FIG.glob("*"):
        if p.suffix in {".pdf", ".png"}:
            shutil.copy2(p, BUNDLE_FIG / p.name)
    for p in TEX.glob("skillspan_style*.tex"):
        shutil.copy2(p, BUNDLE_TEX / p.name)


def main() -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    TEX.mkdir(parents=True, exist_ok=True)
    STYLE_CSV.mkdir(parents=True, exist_ok=True)

    train = collect_split(PAPER / "data/train_lskt_v4_silver.jsonl")
    dev = collect_split(PAPER / "data/dev_lskt_v4_silver.jsonl")
    test = collect_split(PAPER / "data/test_lskt_v4_cws_simhuman980_hybrid.jsonl")
    print("counts", train["n_rows"], dev["n_rows"], test["n_rows"])

    rows = (
        stats_rows("Train (v4 silver)", train)
        + stats_rows("Dev (v4 silver)", dev)
        + stats_rows("Test-V4 (paper gold)", test)
    )
    u_rows = [
        {
            "split": "Unlabeled DAPT",
            "metric": "# Sentences",
            "AI": 409400,
            "Cloud": "",
            "Public": "",
            "Grad": 590600,
            "Total": 1000000,
        },
        {
            "split": "Unlabeled DAPT",
            "metric": "# Sentences (3.2M mix)",
            "AI": 1310080,
            "Cloud": "",
            "Public": "",
            "Grad": 1889920,
            "Total": 3200000,
        },
    ]
    write_csv(
        STYLE_CSV / "dataset_stats_v4.csv",
        rows + u_rows,
        ["split", "metric", "AI", "Cloud", "Public", "Grad", "Total"],
    )

    top_rows = []
    gold = collect_split(PAPER / "data/gold_canonical_v2.jsonl")
    for split, blob in (("dev_v4", dev), ("test_v4", test), ("gold_v2", gold)):
        for kind, store in (("skill", blob["freq_skill"]), ("knowledge", blob["freq_know"])):
            for d, items in store.items():
                for rank, (text, n) in enumerate(items, 1):
                    top_rows.append({"split": split, "kind": kind, "domain": d, "rank": rank, "text": text, "n": n})
    write_csv(STYLE_CSV / "top5_spans_v4.csv", top_rows, ["split", "kind", "domain", "rank", "text", "n"])

    fig_violin({"Train": train, "Dev": dev, "Test-V4": test}, FIG / "fig_violin_span_length")
    fig_v4_bars(FIG / "fig_v4_performance")
    fig_winrate(FIG / "fig_encoder_seed_winrate")
    fig_pred_len(FIG / "fig_pred_span_length")
    fig_f1_by_len(FIG / "fig_f1_by_span_length")

    TEX.mkdir(exist_ok=True)
    (TEX / "skillspan_style_related.tex").write_text(latex_related_work(), encoding="utf-8")
    # Dataset table tex is hand-maintained from repartition_v1
    # (tex/skillspan_style_dataset.tex). Do not overwrite it here.
    (TEX / "skillspan_style_topspans.tex").write_text(
        latex_top(gold["freq_skill"], gold["freq_know"]), encoding="utf-8"
    )
    copy_outputs()
    print("wrote", FIG, TEX / "skillspan_style_related.tex")


if __name__ == "__main__":
    main()
