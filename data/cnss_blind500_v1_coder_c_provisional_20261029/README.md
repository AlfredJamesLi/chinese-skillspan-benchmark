# CNSS_BLIND500_V1 — Coder C annotation draft

**Provisional single-coder annotation draft pending independent second annotation and adjudication.** Agreement analysis is also pending. This package is for annotation maintenance and review, not model evaluation or scoring other coders.

These are post-submission repository-maintenance materials. They were not used to train, select, or evaluate models, calculate results, or support claims reported in manuscript 149505. The citable dataset associated with that manuscript remains Chinese-SkillSpan v0.1.3 on Zenodo; these materials do not change the archived dataset, submitted manuscript or reported results.

Exported on 2026-10-29 from Doccano project 50 (CNSS_BLIND500_V1), using handbook B.sop_v4.2.14. Coder C confirmed all 500 sentences. The neutral identifier preserves the source coder code C. At export, Coder A (project 48) and Coder B (project 49) each had 0/500 confirmed sentences and 0 spans; neither was exported or included. These are export-time observations, not live project status.

## Counts

| Measure | Count |
|---|---:|
| Sentences / confirmed | 500 / 500 |
| Sentences with spans | 396 |
| Confirmed empty sentences | 104 |
| L spans | 6 |
| K spans | 324 |
| S spans | 773 |
| T spans | 197 |
| Total spans | 1300 |

## Format and files

- `labels/blind500_C.jsonl`: 500 records, IDs CNSS-B500-001 through CNSS-B500-500, in original order. Annotator name metadata is anonymized. Three confirmed-empty records have authorized equal-length text redactions described below; labels, offsets, confirmation, record order and other fields are preserved.
- `DRAFT_STATUS.json`: export counts, anonymous coder identifiers and pending steps.
- `CODEX_HANDOFF.md`: maintenance requirements.
- `.gitattributes`: preserves LF line endings so checksums also hold in Windows Git checkouts.
- `SHA256SUMS.txt`: SHA-256 for the five files above, excluding this checksum manifest itself.

Labels are L / K / S / T. Offsets are zero-based, end-exclusive Unicode-code-point character offsets: `text[start:end]`. An empty `label` list with `meta.confirmed=true` means the coder confirmed that the sentence has no spans; it is not missing annotation. No source-file identifiers, source-row identifiers or sampling ledger are supplied.

## Scope and next steps

No 500-sentence IAA has been calculated and no adjudication has been performed. Wait for a completed independent second annotation before computing IAA or adjudicating. Keep both independent versions for that analysis. Do not pool this package with CNSS_BLIND350_V1 or report a combined 850-sentence annotation or agreement set. This later 500-sentence cohort is also distinct from the historical 500-sentence annotation/review coverage described in the manuscript and repository overview.

The existing 350-sentence two-coder package is unchanged. Its reported exact F1=0.509, relaxed F1=0.554, character kappa=0.722 and alpha=0.722 belong only to that cohort; its 223 disagreements are pre-adjudication differences, not errors against a standard answer.

This repository addition is outside the immutable v0.1.3 archive. Existing component-specific licensing and third-party text conditions in the root DATA_AVAILABILITY.md and LICENSE still apply.

## Privacy redactions

With maintainer approval on 2026-10-29, three URLs in CNSS-B500-067 and CNSS-B500-163, and two contact names and two phone numbers in CNSS-B500-290, were replaced with one U+2588 FULL BLOCK per original Unicode code point. All three records are confirmed empty annotations. The record text lengths are unchanged; all 500 records retain their original order, labels, offsets and confirmed status. All other source text is unchanged. Redacted originals are not included in this public package. These privacy changes do not constitute label adjudication.

The JSONL contains full sentence-level recruitment text, with documented privacy redactions. Public visibility does not confer author-granted redistribution or relicensing rights over underlying third-party text. Users must observe the original source terms; public redistribution permission remains for the authors to verify. See [reuse conditions](../../DATA_AVAILABILITY.md#reuse-conditions).
