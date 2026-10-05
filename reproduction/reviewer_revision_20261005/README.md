# Supplementary checks and preparation records

These records accompany the October 5 manuscript revision. They separate completion diagnostics and preparation history from the main research results. Frozen model predictions, the 150-sentence evaluation denominator, and previously reported scores are unchanged.

## Completion and parser outcomes

The archived response-outcome table is retained in `archived_output_outcomes.tex`. Its historical `Format failure` category included responses without a final answer, rather than only malformed JSON.

For the 18 such records in the DeepSeek-V4-Pro thinking configuration, retained responses report HTTP 200 and `finish_reason=length`. The final-answer field is empty, while reasoning content is present and consumes the recorded output budget. This is budget exhaustion before a final answer, not an HTTP transport failure or an incorrectly extracted span in a completed answer. The completion audit supplies the counts and retained metadata; it makes no claim about unrecorded transport attempts.

The end-to-end evaluation treats these responses as empty predictions and retains all 150 reference sentences. Removing only failed cases would change the evaluated sample. A new run with a different output budget or decoding protocol would constitute a separate configuration. No inference was repeated for this revision, and reasoning text was not substituted for the required final answer.

The Qwen partial-rejection category retains accepted spans from the same response. It should not be interpreted as a wholly failed request. The main paper now explains this scoring rule without reproducing the full engineering-status table.

## Preparation-count reconciliation

The historical 2,319 Silver training/development records contained 2,079 distinct NFC-normalized complete texts. Removing whitespace and trimming edge punctuation produced 2,075 preparation keys; eleven failed the length or punctuation filter, leaving 2,064. The difference of 255 between records and valid keys combines repeated texts and filtering.

The preparatory target combined 2,064 valid keys with 7,936 new candidates, giving 10,000 records. Final assembly used different admission rules and retained 2,077 earlier-supervision records. Candidate components contained 3,620, 1,816, and 2,500 new records. Exclusions of 213 and 113 from the first two listed components, offset by thirteen additional earlier records, give a net reduction of 313. The channel-comparison batch then excludes 147 candidates in the adopted pool and 41 in the alternative: 10,000 minus 313 minus 147 equals 9,540; 10,000 minus 313 minus 41 equals 9,646. The manuscript's candidate/retained-count table reports this final assembly. Individual exclusions require the retained decision records; arithmetic alone does not establish their reasons.

These are preparation records, not a new deduplicated training experiment. In the evaluated 2,150-record training split, 1,910 distinct complete texts remain, so repeated records retain their training weights. Source-document overlap is reported separately from repeated complete texts.

## Scope of the exploratory results

Expanded JobBERT results remain in the manuscript's supplementary evaluation, including the lower human-reference scores. Their supervision, source composition, and model-selection arrangement changed together. This revision removes repeated discussion from the main results; it does not reclassify those runs as a controlled training-size experiment or discard their results.

Public aggregate checks in this directory contain no recruitment sentence text, API credentials, or private response headers. Restricted expanded-pool inputs remain subject to the access arrangements described in the manuscript and repository data-access guide.

## Blinded annotation comparison

`PUBLIC_BLINDED_SILVER_CHECK.json` and `recompute_blinded_silver_check.py` report the post hoc agreement of the two final Silver pools with three separate final-handbook annotation layers. Both pools retain the same 49 sentences from the 50-sentence study. The absent unresolved candidate is not scored as an empty annotation. Mean typed exact-span micro-F1 is 0.708831 for the adopted pool and 0.719748 for the alternative. These are descriptive within-sample, cross-version agreement scores, not population accuracy estimates or independently tested model performance.

The check validates identical texts across all three human layers and both pools, valid offsets/types, record status, and matching sample membership. It does not rerun models or alter annotation labels. Inputs are identified by their file hashes; complete expanded-pool inputs use the manuscript's restricted review-access route.

Run `python recompute_blinded_silver_check.py --help` for the two input paths. The three human exports are in `reproduction/agreement/finalguide_abc_20261003/data/`.

## Human annotation and review coverage

The [verified census](HUMAN_ANNOTATION_CENSUS.md) reconciles 550 distinct sentence texts: 150 in the human reference, 100 in initial review, 100 in post-generation review, 150 in additional review, and 50 in the final-handbook blinded study. Per-layer span counts, version relationships and overlap checks are provided separately.
