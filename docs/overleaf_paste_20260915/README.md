# Overleaf paste pack (2026-09-17)

Companion paste files for the PeerJ Computer Science manuscript. They do **not** change Tables A–D cells or Abstract Results.

Paste order is in `OVERLEAF_SYNC_20260915.md`. One-shot Codex instructions: `CODEX_OVERLEAF_PROMPT.md`.

- Data Availability cites Zenodo **v0.1.3** for Gold150 / v6a_nocross (not S1-pending).
- Table C footnote names shared-handbook LoRA **0.5403±0.0354** as a **different protocol** from JSON-offset **0.1215±0.0092**.
- Appendix Table H: public-API subsets plus two pooled rows — proxy keep \(n_{\mathrm{keep}}=9{,}646\) (train 8,943) Qwen Gold150 **0.5966 / 0.7126**, and Codex-swap keep \(n_{\mathrm{keep}}=9{,}540\) (train 8,842) Qwen Gold150 **0.5854 / 0.7032**. Not GPT distillation. Do not write “10,000”.
- Codex run2500 relabel is **done**; do not leave a pending row.

Do not add public-API silver jsonl, WAVE3/run2500 labels, or mixed-training checkpoints to this repository.
