# CNSS_BLIND350_V1 Maple × Yanbin Zheng

Finished independent labels for the 350-sentence Chinese SkillSpan blind set, exported 2026-10-29 from Doccano projects 44 (Maple) and 45 (Yanbin Zheng). Both annotators confirmed every sentence. This is a pre-adjudication reliability pack, not Gold and not a model test set.

James1 is not included: that project had 0 of 350 sentences confirmed at export.

Handbook: B.sop_v4.2.14. Labels are only L / K / S / T. Offsets are zero-based and end-exclusive. A confirmed sentence with an empty `label` list is an intentional empty annotation.

## Files

- `labels/blind350_B_Maple.jsonl` — Maple, Doccano project 44
- `labels/blind350_C_YanbinZheng.jsonl` — Yanbin Zheng, Doccano project 45
- `labels/blind350_paired.jsonl` — same 350 texts, both span lists, `exact` if the span sets match
- `analysis/RELIABILITY.json` — agreement coefficients
- `analysis/DISAGREE.md` — all 223 sentences that are not an exact span-set match
- `analysis/SUMMARY.json` — disagreement counts and examples
- `analysis/ANALYSIS.md` — why the labels diverge

Source-file and row identifiers are not in this pack.

## Agreement on all 350

Primary metric: typed exact-span micro-F1. A hit requires the same sentence, the same offsets, and the same type. Precision uses Maple's span count as the denominator. Recall uses Yanbin Zheng's.

| Setting | P | R | Accuracy | F1 |
|---|---:|---:|---:|---:|
| exact type | 0.531 | 0.489 | 0.841 | 0.509 |
| relax type (same offsets, type ignored) | 0.578 | 0.532 | 0.875 | 0.554 |

Character Cohen's κ = 0.722. Krippendorff's α = 0.722. After dropping characters both marked as outside any span, κ = 0.467. Sentence-resample 95% CI for exact-type F1, 10000 draws, seed 20260928: 0.466–0.551.

Against the Krippendorff bands used elsewhere in this project, α 0.722 is in the tentative 0.67–0.80 range. The project did not set a span-F1 pass line.

127 sentences match exactly, including 69 on which both coders confirmed no span. 223 sentences differ. See `analysis/ANALYSIS.md`.
