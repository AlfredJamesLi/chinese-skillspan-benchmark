# Annotation stages and handbook records

Updated 7 October 2026. This document retains supporting details for the paper's concise accounts of reference-set construction and handbook use. It reorganizes documentation; it does not change annotations, sample membership, model predictions, scores, or the scorer.

## Which materials to use

The [handbook index](../../notes/handbooks/README.md) links the Chinese and English reading editions and earlier materials. The [7 October 2026 edition](../../notes/handbooks/reader_20261007/README.md) provides Word and PDF files, checksums, and explicit notes on unresolved examples. Its examples explain the rules; they are not an independent evaluation set.

For new annotation, use the latest reviewed edition appropriate to the task and record the dated file and model settings. To reproduce the reported experiments, use the archived materials for the corresponding study. The latest reading edition must not be substituted retrospectively for a historical execution input. New model calls or reannotation can differ with guideline revisions, model versions, and service settings. Scores from preserved predictions and references should be reproduced with the documented scorer.

## Stage-to-version evidence

| Stage | Recorded handbook evidence | Interpretation |
|---|---|---|
| Human reference, 150 sentences | v4.2.10 in all label records; v4.2.11 in reference-set operating documentation | Label metadata and documented instructions are different kinds of evidence; neither should silently replace the other. |
| Initial silver review, 100 sentences | v4.2.10 rev1 in the initial prompt; v4.2.11 in subsequent coding/adjudication records | The initial prompt and later review describe different stages. |
| Remaining 2,351 original silver records | v4.2.12 rev2 in the archived bulk-generation prompt | This prompt is preserved; no claim is made that these labels were regenerated using a later handbook. |
| Three-annotator study preparation | v4.2.14 training materials | The training source can be identified. |
| Formal coding and individual self-review | v4.2.14 series in study records | The exact dated files consulted by each annotator at each stage have not been established. A nearby file date is not evidence of actual use. |
| Later reading editions | Dated revisions within the v4.2.14 series, including the released bilingual edition of 7 October 2026 | These support reading and subsequent annotation. They do not replace the inputs or labels of completed studies. |

Individual silver training/development records do not carry a handbook-version field. Several different files use the v4.2.14 number; file identity and edition date matter. No unrecorded v4.2.15 or v4.2.16 is inferred.

Sources: [archived generation prompt](../silver_prompt_api_v1/archive/silver_rev2_original.txt), [handbook index](../../notes/handbooks/README.md), [historical label-version documentation](https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/blob/36f009fab01b8433355cb7ef5af8fad02c6cc519/reproduction/process_archive_20260924/source/tex/review20260923/version_matrix.tex), and the existing annotation-stage documentation summarized in the manuscript before this editorial revision (Overleaf source revision `a8676822b9757a52609ad33b55830aff81fbf193`).

## Reference-set construction and preliminary agreement

The model-evaluation reference combines 50 calibration sentences sampled from the 980-record model-disagreement queue and a separate 100-sentence challenge sample. The calibration sentences were separately annotated and adjudicated; the challenge sentences were collaboratively annotated and reviewed. The authors recall machine suggestions being available during calibration, while an earlier protocol specifies raw-text-only coding. The available records do not resolve this discrepancy. This early stage is not treated as the later blinded agreement study.

The available calibration exports contain 211 and 230 spans, including 98 exact boundary-and-type matches, giving typed exact-span F1 of 0.444. Character agreement uses 2,571 source positions and L/K/S/T/O labels, including spaces and punctuation: observed agreement is 0.771, expected agreement is 0.471, and Cohen's kappa is 0.567. These are retrospective calculations from available exports; their exact correspondence to the original frozen files has not been verified. See the [published calculation summary](https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/blob/1d1c24e20ee049fc768034b5baf58fa882e08e2c/reproduction/process_archive_20260924/secondary_review/tables/iaa50.tex).

The adjudicated reference contains 415 challenge-sample spans (290 S, 83 K, 41 T, one L) and 248 calibration-sample spans (158 S, 42 K, 47 T, one L). Seven challenge sentences and one calibration sentence have no span. The 150 sentence identifiers correspond to 61 source-document prefixes. All 50 calibration IDs are absent from the silver training and development sets.

The following secondary comparisons are retained here instead of expanded in the paper:

| Retrospective comparison against the adjudicated 50-sentence reference | Typed exact-span F1 | Boundary-only exact-span F1 |
|---|---:|---:|
| First available individual calibration layer | 0.640 | 0.766 |
| Second available individual calibration layer | 0.606 | 0.684 |

These annotators contributed to the adjudicated reference. The comparisons describe changes introduced by adjudication, not independent human performance. They are carried over unchanged from the manuscript's existing annotation-quality documentation; this editorial revision did not recalculate them. The [annotation-layer archive](../evidence_review_20260925/annotation_layers/README.md) provides the corresponding released materials and provenance qualifications.

The later three-annotator study uses a different 50-sentence sample with machine and peer labels hidden. Its mean pairwise typed exact-span F1 of 0.818 refers to individual labels after self-review. It does not estimate agreement on the 150-sentence reference. Earlier individual labels yielded 0.663, but the timing records do not establish a comparable before-and-after sequence across annotators; these figures do not establish an effect of handbook revision.

## Example of a later rule clarification

The shared-experience example in Appendix A.3 corresponds to silver training record `1838-s0008`. Its preserved two-span annotation includes a shared experience phrase that the later R23 clarification splits into three spans. The record is absent from the human reference and silver development sets. The paper illustrates the later rule without replacing the original training label.

The existing documentation reports rule-family screening across 2,469 reference, training, and development records to identify candidates for contextual review. Screening does not establish that every candidate is an annotation error and did not change the targets or reported scores. Figures showing human-reference examples retain their scoring annotations; the appendix rule examples explain the v4.2.14 series.

## Scope of this documentation update

The paper retains the stage-to-version mapping, relevant agreement estimates, and unresolved procedural limitations. Individual edition history, supporting file records, and the retrospective adjudication comparisons are documented here and in the linked archives. This is a presentation change, not a new annotation study or a new dataset release. Existing Zenodo versions remain unchanged.
