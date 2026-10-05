# Human annotation and review coverage

Checked on 5 October 2026 against recovered annotation exports and source manifests.

The verified materials cover **550 distinct sentence texts with human annotation or review**: 500 in the historical cohorts and 50 in the final-handbook blinded agreement study. The new 50 have **zero overlap** with the historical 500 by source identifier, exact complete text, and NFC-normalized complete text.

## Coverage by study role

| Cohort | Distinct texts | Preserved annotation layers and span counts |
|---|---:|---|
| Human reference set | 150 | Final reference: 663 spans; calibration subset: 50 texts / 248 spans; challenge subset: 100 texts / 415 spans |
| Initial Silver review | 100 | Archived reviewed layer: 419 spans |
| Post-generation Silver review | 100 | Human-reviewed final layer: 148 spans |
| Additional review sample | 150 | Reviewer A: 358 spans; reviewer B: 365 spans; 300 sentence–annotation-layer records |
| Final-handbook blinded agreement sample | 50 | Annotators A/B/C: 104/123/113 spans; 150 sentence–annotation-layer records |
| **Combined coverage** | **550** | Each distinct source text is counted once |

A later recovered collaborative export of the initial review contains **433 spans on the same 100 texts**. Its hash and version relationship are recorded separately; the archived 419-span layer remains the historical record used in this census.

Two further sets of individual layers are nested within the cohorts above:

| Nested sample | Parent cohort | Individual layers |
|---|---|---|
| Historical independent calibration | Human reference set | 50 texts; A: 230 spans, B: 211 spans |
| Assisted double review | Post-generation Silver review | 15 texts; A: 27 spans, B: 27 spans |

These nested layers add annotation evidence while retaining the parent cohort's text count. Repeated exports and multiple annotators likewise contribute layer records rather than additional sentences. The three final-handbook layers contain 340 span instances in total, with each annotator's version preserved separately. Five familiarization and 15 practice sentences are treated as preparation and excluded from the 550-text study/review coverage total. Machine-generated supervision, including the archived H730 component, is counted within Silver supervision rather than as completed human annotation.

## Evidence and matching

The accompanying [JSON census](HUMAN_ANNOTATION_CENSUS.json) provides file SHA-256 hashes, per-layer counts, per-cohort overlap results and repository-relative evidence paths. Key materials are:

- [Human-reference labels](../../data/gold150/gold150_test.jsonl).
- [Historical annotation and review layers](../evidence_review_20260925/annotation_layers/README.md) and [cohort reconciliation](../evidence_review_20260925/COHORT_RECONCILIATION.json).
- [Final-handbook individual exports and sample manifest](../agreement/finalguide_abc_20261003/README.md).
- [Historical 350-text identifier manifest](../../data/silver_plus_10k_prep_20260913/human350/ids.jsonl) and its [preparation script](../../scripts/prep_silver_plus_10k_20260913.py).

The original initial-review and post-generation exports match the SHA-256 identifiers in the published cohort reconciliation. Their full texts were included in the direct overlap check. The later 433-span collaborative export remains an author-held version identified by its own hash.

All 350 hashes in the historical identifier manifest were reproduced from the inspected originals. Its preparation key applies NFC normalization, removes whitespace and trims specified edge punctuation; the census additionally compares exact texts and NFC-only texts directly. SHA-1 serves only as the existing text-matching identifier, while SHA-256 records the inspected file versions.

The resulting **550-text figure describes human annotation and review coverage**. The reference, assisted-review cohorts and blinded agreement sample retain their respective roles, label versions and sampling designs.
