# Overleaf paste sync (2026-09-17; Codex-2500 filled)

Use this folder **now**. Tables A–D and Abstract Results stay frozen. Public-API / pooled-silver numbers go only in **appendix Table H**.

A copy-paste prompt for Codex is `CODEX_OVERLEAF_PROMPT.md` (one message; do not invent F1).

## Paste order

1. `DATA_AVAILABILITY.md` — Zenodo v0.1.3 for Gold150 / v6a_nocross.
2. `tables_ABCD.tex` — cells unchanged; Table C footnote already has shared-handbook 0.5403 as a **different protocol**.
3. `tables_EFG_appendix.tex` — P1 / SOP-on-Gold150 / peel (unchanged).
4. `tables_H_public_api_silver.tex` — seed-42 occurrence LoRA; proxy pool 9,646 and Codex-swap pool 9,540.
5. `METHODS_SNIPPET.md` — plus the pooled-silver sentences in `MIXED_STUDENT.md`.
6. `ABSTRACT.md` — Results **unchanged**.

## Leave frozen

| Cell | Number |
|---|---|
| Table A JobBERT 3M hybrid | 0.4331 |
| Table B v6a B2 | 0.5536±0.0054 |
| Table C JSON-offset P0 | 0.1215±0.0092 |
| SOP extract (hybrid, no LoRA) | 0.1724 |

## In this paste (appendix only; all Gold150 unless noted)

Wave3 proxy 0.5870 vs Codex 0.5853; Wave1+2 0.5745; public-API 7117 0.5883 / 0.5732; pooled 9,646 Qwen **0.5966 / 0.7126**; pooled 9,540 Qwen **0.5854 / 0.7032**; JobBERT 7117 $0.2367\pm0.0015$; JobBERT proxy pool 0.2416; JobBERT Codex-swap 0.2317. Do not write 10,000.

## No later Table H replacements

Codex run2500 labels and the second pooled Qwen student are **done**. Do not invent a third pooled F1.
