# Overleaf paste sync (2026-09-15)

Public GitHub `main` is already at tag/docs for **Zenodo v0.1.3** and the Qwen protocol split. This folder was still on the 2026-09-09 “Gold150 pending S1” wording. Files below were updated locally so you can paste into Overleaf **now**, without waiting for Codex Wave3 training.

Do **not** paste public-API Silver 7117, Wave3-proxy, Codex wave1/2, or Codex-relabel Wave3 F1 into the manuscript. Those runs are not paper-main.

## Paste order

1. `DATA_AVAILABILITY.md` — short paragraph (Gold150 is in v0.1.3, not S1-pending).
2. `tables_ABCD.tex` — Tables A–D unchanged as cells; Table C footnote now names shared-handbook **0.5403±0.0354** as a **different protocol** that does not replace **0.1215±0.0092**.
3. `tables_EFG_appendix.tex` — already the 09-09 appendix; paste if Overleaf still has the “kNN is running” footnote.
4. `METHODS_SNIPPET.md` — sentence-level isolation; JSON-offset vs shared-handbook.
5. `ABSTRACT.md` — Results **unchanged** (still 0.4331 / 0.2854 / 0.1724 / 0.5536±0.0054 / 0.1215±0.0092).

## Leave frozen

| Cell | Number |
|---|---|
| Table A JobBERT 3M hybrid | 0.4331 |
| Table B v6a B2 | 0.5536±0.0054 |
| Table C JSON-offset P0 | 0.1215±0.0092 |
| SOP extract (hybrid, no LoRA) | 0.1724 |

## GitHub

- Public repo https://github.com/AlfredJamesLi/chinese-skillspan-benchmark. This paste pack lives in `docs/overleaf_paste_20260915/`.
- Do **not** push `WAVE3_VALIDATED.jsonl`, run2500 Codex labels, or the pooled-silver training jsonl to the public repo.

## After Codex Wave3 job 8108/8109

Report Gold150 internally only. Still not Abstract / Tables A–D.

## Pooled-silver additional baseline (queued 2026-09-15 19:30 HKT)

Queued, not finished: v6a B2 unique + public-API keep (Wave3 Codex; run2500 still proxy). This is a **benchmark baseline** on pooled silver, not GPT distillation.  
`MIXED_STUDENT.md` is the paste draft. **Do not paste F1 until JobBERT 42 and Qwen 42 Gold150 exist.** Do not write 10,000 or “dual teacher”. Codex run2500 (~23:30) will replace the proxy 2500 and we will retrain that second mix.

Public GitHub: still do not push this Silver mix.
