# Codex — insert SkillSpan-style figures (edit pass)

**Overleaf:** https://www.overleaf.com/project/68fe17a53e53a7f800e4f2b4

**Before pasting this prompt into Codex:** copy the files below from the server bundle into the **Overleaf Git root** (same folder as `main.tex`). Codex on Overleaf cannot see the lab server paths.

Server bundle root:

`Chinese_skill_benchmark_Paper/overleaf_cursor_bundle/`

Paste **after** `CODEX_PROMPT_HANDBOOK.md` / `CODEX_PROMPT_ALL.md` if those chats already ran.

Numbers only from `.cursor/skills/cnss-overleaf/confirmed-results.md` and `tables/skillspan_style/`. **Do not invent F1. Do not commit.**

---

## Copy map (server → Overleaf root)

| What | Server path (source) | Overleaf path after copy (what Codex must open) |
|---|---|---|
| Related-work table | `overleaf_cursor_bundle/tex/skillspan_style_related.tex` | `tex/skillspan_style_related.tex` |
| Dataset stats | `overleaf_cursor_bundle/tex/skillspan_style_dataset.tex` | `tex/skillspan_style_dataset.tex` |
| Top-5 spans | `overleaf_cursor_bundle/tex/skillspan_style_topspans.tex` | `tex/skillspan_style_topspans.tex` |
| Five figure floats | `overleaf_cursor_bundle/tex/skillspan_style_figures.tex` | `tex/skillspan_style_figures.tex` |
| Violin PDF | `overleaf_cursor_bundle/figures/fig_violin_span_length.pdf` | `figures/fig_violin_span_length.pdf` |
| V4 bars PDF | `overleaf_cursor_bundle/figures/fig_v4_performance.pdf` | `figures/fig_v4_performance.pdf` |
| Win-rate PDF | `overleaf_cursor_bundle/figures/fig_encoder_seed_winrate.pdf` | `figures/fig_encoder_seed_winrate.pdf` |
| Pred-length PDF | `overleaf_cursor_bundle/figures/fig_pred_span_length.pdf` | `figures/fig_pred_span_length.pdf` |
| F1-by-length PDF | `overleaf_cursor_bundle/figures/fig_f1_by_span_length.pdf` | `figures/fig_f1_by_span_length.pdf` |
| Stats CSV | `overleaf_cursor_bundle/tables/skillspan_style/dataset_stats_v4.csv` | `tables/skillspan_style/dataset_stats_v4.csv` |

PNG twins of each figure sit next to the PDFs (optional; Overleaf uses PDF).

If Codex `ls` does not show `tex/skillspan_style_related.tex` and `figures/fig_v4_performance.pdf`, **stop** and tell the user to copy the bundle files first. Do not invent plots.

---

## PROMPT (copy from here)

You are inserting **SkillSpan-layout** figures and tables into the Chinese-SkillSpan PeerJ CS paper. Visual style follows Zhang et al. (NAACL 2022). **Do not copy SkillSpan English span-F1** into any caption or axis.

Workspace = Overleaf Git root (folder with `main.tex`). First run:

```
ls tex/skillspan_style_related.tex tex/skillspan_style_dataset.tex tex/skillspan_style_topspans.tex tex/skillspan_style_figures.tex
ls figures/fig_violin_span_length.pdf figures/fig_v4_performance.pdf figures/fig_encoder_seed_winrate.pdf figures/fig_pred_span_length.pdf figures/fig_f1_by_span_length.pdf
```

If any path is missing, report the missing names and stop.

**Main protocol is V4** (2026-08-27). Figure `figures/fig_v4_performance.pdf` is the main results figure. Gold v2 plots (win-rate, pred length, F1-by-length) are appendix or analysis.

Files to `\input` or paste (paths relative to Overleaf root / `main.tex`):

- `tex/skillspan_style_related.tex` — related-work table (Sayfullina / Gnehm / Zhang / this work)
- `tex/skillspan_style_dataset.tex` — dataset statistics (cyan totals)
- `tex/skillspan_style_topspans.tex` — top-5 on Gold v2 (not V4 SOP noise)
- `tex/skillspan_style_figures.tex` — five figures (`\includegraphics{figures/fig_….pdf}`)

Graphics (must exist before compile):

- `figures/fig_violin_span_length.pdf`
- `figures/fig_v4_performance.pdf`
- `figures/fig_encoder_seed_winrate.pdf`
- `figures/fig_pred_span_length.pdf`
- `figures/fig_f1_by_span_length.pdf`

### Hard rules
- Do not rank JobBERT V4 **0.4331** against ChatGPT Gold v2 **0.6365**.
- Do not call the V4 hybrid human Doccano Gold. 980 = SimHuman rule overlay.
- Win-rate heatmap caption must say **n=3, not ASO+Bonferroni**.
- Do not add STL/MTL or SpanBERT-from-scratch bars. We did not run that grid.
- PDF Table 3 paper S-F1 cells stay frozen (0.6700 … 0.2130).
- If a graphic path 404s, report and stop; do not replace with a made-up plot.

Place related-work + dataset stats in Data/Related work; V4 performance in Results; violin near Data; win-rate / pred-length / F1-by-length in appendix. Show diff. No commit.

End prompt.
