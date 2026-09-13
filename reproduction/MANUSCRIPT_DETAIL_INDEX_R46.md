> Historical preparation record. Availability statements and proposed destinations below refer to the time of writing. The current synchronized locations are in [PAPER_INDEX.md](PAPER_INDEX.md). Complete manuscript backups remain local.

# Manuscript reproduction details (R46)

Prepared 12 September 2026. This file is not typeset. It preserves identifiers and execution details removed from reader-facing prose; it does not change any data or result. Intended GitHub destination: `notes/manuscript_reproduction_details.md`, linked from `REPRODUCIBILITY.md`. This new index has not yet been published to GitHub.

## Verified public entries

The following public `main`-branch files returned HTTP 200 on 12 September 2026:

- [Reproduction guide](https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/blob/main/REPRODUCIBILITY.md): file inventory, checksums, scoring, and release boundaries.
- [Terminology map](https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/blob/main/data/gold150/README.md): manuscript names versus stable artifact names.
- [Historical encoder scores](https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/blob/main/tables/encoder_3seed_gold_v2.csv): Table label `tab:archived-reference-checks-r38`, JobBERT-zh 1M three-seed Gold v2 exact F1 0.1288.
- [Human-overlay scores](https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/blob/main/tables/hybrid_human200_overlay_scores.csv): the same table's 3M V4 frozen-prediction row, exact F1 0.3884.
- The reproduction guide inventories `data/human_gold_page1_200.jsonl`. This overlay changes a derived 2,601-record reference, not the frozen original hybrid or Gold v2. The score is not on the 200 sentences alone, and neither historical row is a result on the 150-sentence human reference.

## Stable artifact mappings

Do not rename files to match manuscript display names.

| Reader-facing description | Existing identifier or path |
|---|---|
| Primary JobBERT continuation split, 2,156/169 | `v6a` |
| Qwen supervision split, 2,150/169 | `v6a_nocross` |
| Shared starting CRF checkpoint | `crf/best.pt` |
| Initial teacher-generation prompt | `v4210_rev1` |
| Subsequent 2,351 teacher labels | `v4212_rev2`, based on Handbook B V4.2.12 |
| Frozen teacher prompt in manuscript materials | `PROMPT_silver_plus_v4212_rev2.frozen.txt` |
| Full English handbook in manuscript project | `handbooks/handbook_B_sop_v4.en.md` |
| Handbook execution map in manuscript project | `handbooks/VERSION_MAP_v4214.md` |
| Public handbook copies | `notes/handbooks/handbook_B_sop_v4.md` and `.en.md`, inventoried by the reproduction guide |
| Historical three-model disagreement layer | `SimHuman` |
| Display archive path stated in the pre-R46 manuscript; not currently public | `notes/manuscript_display_archive_20260910` |

Manuscript-project paths and public-repository paths are different namespaces. This table does not imply that every local evidence file has been released. Appendix A retains the handbook-version table and Appendix D retains the core terminology crosswalk.

The GitHub contents API returned HTTP 404 for `notes/manuscript_display_archive_20260910` on `main` on 12 September 2026. The pre-R46 manuscript described 40 tables and 11 figures there. This pass does not claim that directory is publicly accessible: restore or locate and verify the actual public archive before advertising a direct link. Do not delete local display archives or their original conditions.

## Historical input mismatch

In `tab:appendix-f-sop`, archived inputs for `1801-s0004` and `1990-s0022` differ from the frozen human-reference wording. Complete ID coverage is not identical input text. The manuscript retains this limitation without printing IDs. The IDs were documented in the pre-R46 source; their independent public audit file was not located during this pass. Preserve them here when publishing the index; do not describe such an audit file as already public.

## Shared-guideline execution details

- Host identifier: `DS209213`, laboratory server A. Server A ran shared-guideline inference and Qwen adaptation; server B supplied the JobBERT continuation evidence and B2 training/development records. A100 80GB identifies the hardware, not a verified claim that each run used all host GPUs.
- Qwen decoding flag: `do_sample=false`. Baseline and adapter runs share the local base-model path, prompts, parser, and fingerprints. The earlier server-B Qwen copy was not verified byte-identical. The local eight-shard inventory does not supply a recorded Hugging Face revision.
- GPT request alias: `gpt-5.4`. Every successful stored response, including smoke tests, returned `gpt-5.6-terra`. The paper uses that returned name, with the proxy-routing limitation retained. These observations do not establish the identity of historical SOP runs.
- Full 150-sentence shared-guideline aggregation: 11 September 2026. GPT exact F1 remains 0.6667. The already removed 149-sentence retry footnote is not reinstated.
- Outbound message arrays were not captured. They can be reconstructed from frozen templates, ID/text payloads, and configuration fingerprints, but reconstruction is not a captured wire request. Model-weight files were not supplied in the audit package. These limitations remain summarized in the paper.
- The stopped DeepSeek thinking-plus-2,048-token probe is excluded from formal results. The formal nothink and think8192 configurations retain separate rows and budgets, including the latter's 18 format failures.
- A filename containing `DRAFT` does not override the frozen execution fingerprint. Later handbook maintenance does not relabel frozen data or change the prompts actually executed.

## Historical plans and release chronology

The superseded plan for a 200-sentence challenge plus a separate audit is not the completed reference design. The earlier 200-sentence mixed-annotator analysis, diagnostic repartition, and old length plots retain their own populations. Version v0.1.3 includes the human reference and Silver-plus B2 files; v0.1.1 and v0.1.2 do not. Portable scoring and paper-name mappings added on 11 September 2026 belong to GitHub `main`, not the immutable v0.1.3 archive. Existing tags and DOIs must not be replaced or retagged.

## Publication checklist

1. Add this index to the public repository and link it from `REPRODUCIBILITY.md` after author authorization to push.
2. Check that existing paths still resolve. Preserve all filenames, scores, seeds, and protocol distinctions.
3. Do not upload raw private responses, credentials, entire server handoff bundles, or unpublished model weights as part of this documentation change.
4. Keep the complete pre-edit source backup locally: `outputs/prose_cleanup_R46_20260912/pre_R46_sources.zip`. Existing Git history also preserves the original wording.

## Output-status detail transferred from the manuscript (13 September 2026)

The complete nine-row output-status breakdown is preserved in [output_outcomes/README.md](output_outcomes/README.md), with a CSV and archival TeX table. It is excluded from manuscript compilation. These new companion files are prepared locally and await GitHub synchronization.


## Supplementary table transfer (13 September 2026)

Former Tables 10, 12–16 and 19 are preserved in [supplementary_tables/README.md](supplementary_tables/README.md), with exact LaTeX, readable Markdown, CSV blocks and historical context. This local transfer is not a public GitHub upload. The manuscript retains the core results, annotation rules and quality evidence, with updated references.


## Qwen diagnostic chart data (13 September 2026)

Former Table 12 is now Figure 5. Complete counts and chart data are preserved in [qwen_diagnostics/README.md](qwen_diagnostics/README.md). This is a local preparation, not a public upload.
