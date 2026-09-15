# Overleaf — pooled-silver additional baseline (paste later; not Tables A–D)

Do **not** write “10,000 Silver sentences” in the manuscript. Do not change Abstract or Tables A–D. Gold150 remains the human overlay (150 sentences). This is an **additional benchmark baseline**, not a GPT-distillation experiment.

## Methods sentence (English, appendix)

An additional baseline was trained on a pooled silver set: the existing Silver-plus v6a_nocross B2 unique sentences together with the later public-API silver keep set (Wave1–2 Codex CLI; Wave3 Codex CLI; run2500 still the website-proxy labels until the Codex relabel arrives). Adjudication-required rows were held out. Gold150 was not used for gradients or checkpoint selection. Isolation is sentence-level. The pool joins two silver annotation protocols (handbook v4212 B2 and `silver_public_api_v1.0`); it is not knowledge distillation from GPT, and it must not replace the v6a_nocross 2,150 / 169 JobBERT cell.

## What not to paste

- JobBERT v6a Gold150 0.5536, Qwen JSON-offset 0.1215, shared-handbook 0.5403, hybrid 0.4331, and this pooled-silver baseline’s Gold150 in one SOTA sentence
- “10,000”, “dual teacher”, or “human cover 500”
- Silver-test F1 (fit to silver labels, not human gold)

## Results

Seed-42 JobBERT-zh 3M CRF and Qwen2.5-14B occurrence LoRA were queued on 2026-09-15. Paste Gold150 typed exact here **after both jobs finish**. Until then leave this paragraph out of Overleaf.
