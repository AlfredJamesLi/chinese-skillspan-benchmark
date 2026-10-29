# CNSS_BLIND350_V1 Coder B × Coder C

Finished independent labels for the 350-sentence Chinese SkillSpan blind set, exported 2026-10-29 from separate annotation projects. Both annotators confirmed every sentence. This is a pre-adjudication reliability pack, not a model test set; neither coder is a reference standard.

Excluded coder is not included: that project had 0 of 350 sentences confirmed at export.

Handbook: B.sop_v4.2.14. Labels are only L / K / S / T. Offsets are zero-based and end-exclusive. A confirmed sentence with an empty `label` list is an intentional empty annotation.

## Files

- `labels/blind350_B.jsonl` — Coder B
- `labels/blind350_C.jsonl` — Coder C
- `labels/blind350_paired.jsonl` — same 350 texts, both span lists, `exact` if the span sets match
- `analysis/RELIABILITY.json` — agreement coefficients
- `analysis/DISAGREE.md` — all 223 sentences that are not an exact span-set match
- `analysis/SUMMARY.json` — disagreement counts and examples
- `analysis/ANALYSIS.md` — why the labels diverge

Source-file and row identifiers are not in this pack.

## Agreement on all 350

Primary metric: typed exact-span micro-F1. A hit requires the same sentence, the same offsets, and the same type. Precision uses Coder B's span count as the denominator. Recall uses Coder C's.

| Setting | P | R | Accuracy | F1 |
|---|---:|---:|---:|---:|
| exact type | 0.531 | 0.489 | 0.841 | 0.509 |
| relax type (same offsets, type ignored) | 0.578 | 0.532 | 0.875 | 0.554 |

Character Cohen's κ = 0.722. Krippendorff's α = 0.722. After dropping characters both marked as outside any span, κ = 0.467. Sentence-resample 95% CI for exact-type F1, 10000 draws, seed 20260928: 0.466–0.551.

Against the Krippendorff bands used elsewhere in this project, α 0.722 is in the tentative 0.67–0.80 range. The project did not set a span-F1 pass line.

127 sentences match exactly, including 69 on which both coders confirmed no span. 223 sentences differ. See `analysis/ANALYSIS.md`.

## Pseudonymization and interpretation

Coder B and Coder C retain their established repository codes. Current filenames,
metadata keys and documentation use neutral codes; internal project numbers are
omitted. The identity lookup is kept outside this repository. Sentence text,
record order, offsets, label types, confirmed status and numerical statistics
are unchanged. This is pseudonymization of the current package, not erasure of
previously published Git history; old commits can still expose identities.

Use the [aggregate disagreement analysis](../../docs/annotation_disagreement_analysis_blind350.md)
as the public analysis entry point. Its local Coder A/B aliases denote this
package's Coder B/C respectively. Legacy pair-selection counts are preserved in
this package and differ from the exhaustive-pair method documented there.

Checksums cover the renamed, pseudonymized files with LF line endings. They
replace the pre-pseudonymization byte hashes, not the underlying annotations.
Third-party text remains subject to [data access conditions](../../DATA_AVAILABILITY.md).

These are post-submission repository-maintenance materials. They were not used to train, select, or evaluate models, calculate results, or support claims reported in manuscript 149505. The citable dataset associated with that manuscript remains Chinese-SkillSpan v0.1.3 on Zenodo; these materials do not change the archived dataset, submitted manuscript or reported results.
