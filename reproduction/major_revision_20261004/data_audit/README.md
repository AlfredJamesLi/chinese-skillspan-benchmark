# Data counts and document overlap

This audit reads the frozen inputs and recomputes counts. It does not change labels, split membership, checkpoints or reported model scores. No private sentence texts are included in this folder.

**Clarification after checking the earlier prevention reports:** the original corpus had a documented posting-level split with zero shared `global_id` values, and the later B2 experiments explicitly used sentence-level exclusion of Gold150 identifiers and complete texts. Both earlier checks are valid within their stated scope. The group counts below do not mean that no leakage prevention was performed, that 143 reference sentences were copied into training, or that any specific score inflation has been measured. See `RECHECK_zh.md` and `key_semantics/recheck.json` for the exact version checks and the three observed sentence-version differences.

## Count reconciliation

The preparatory target and the final experimental pools used different admission rules. They must not be treated as a single uninterrupted 10,000-record pipeline.

| Stage | Count | Meaning |
|---|---:|---|
| Original Qwen B2 train + development | 2,319 | 2,150 + 169 records |
| Distinct complete NFC texts | 2,079 | 240 repeated training records removed in this counting view |
| Distinct preparation keys | 2,075 | NFC, whitespace removal and edge-punctuation trimming |
| Valid preparation keys | 2,064 | Eleven short or punctuation-only keys excluded |
| New annotation candidates | 7,936 | 2,500 + 3,620 + 1,816 |
| Preparatory target | 10,000 | 2,064 + 7,936 |
| Old B2 contribution actually retained in final pools | 2,077 | Recomputed from final JSONL `mix_source` values |
| Shared retained new batches | 5,110 | 3,407 of 3,620, plus 1,703 of 1,816 |
| Adopted Codex comparison batch | 2,353 | Of 2,500 candidates |
| Supplementary API comparison batch | 2,459 | Of the same 2,500 candidates |
| Adopted final pool | 9,540 | 2,077 + 3,407 + 1,703 + 2,353 |
| Supplementary final pool | 9,646 | 2,077 + 3,407 + 1,703 + 2,459 |

The apparent unexplained 313 is therefore 213 + 113 - 13: exclusions from the two other new batches, offset by the 13-record difference between the preparatory old-data count and the final old-data count. This reconciles the counts; it does not establish a semantic reason for every excluded annotation. Final pools retain eleven old records whose preparation keys fail the earlier minimum-length filter, plus two additional raw-text variants merged by that preparation key. They were not silently removed during this audit.

The post-generation QA sampling frame also reconciles: 2,451 - 100 initially reviewed A100 - 100 records exported for an earlier pilot - 72 pending records = 2,179 eligible records. The pilot exclusion does not itself prove completed human review and adds no records to the manuscript's human-review coverage. The manifest's prose mentions `pending82`, but its actual exclusion count is 72. Its stratum populations sum to 2,179 and allocations sum to 100; two unsampled strata contain eleven records. Consequently, the sample cannot provide an unbiased accuracy estimate for the whole original Silver pool.

## Document overlap

The original corpus contains stored `global_id` values. All 22,840 sentence IDs agree with those document prefixes. The original training/development/test partitions have 1,600/200/200 document IDs, respectively, and no shared document IDs. They nevertheless contain repeated complete texts across different documents. The later supervision and reference partitions are a different construction and do share documents.

| Comparison | Shared document IDs | Sentences on left from shared documents | Sentences on right from shared documents |
|---|---:|---:|---:|
| B2 train / B2 development | 1 | 4 | 27 |
| B2 train / Gold150 | 59 | 531 | 143 |
| B2 development / Gold150 | 0 | 0 | 0 |
| Expanded Codex train / validation | 185 | 1,060 | 208 |
| Expanded Codex train / test | 188 | 1,076 | 210 |
| Expanded Codex validation / test | 42 | 55 | 54 |
| Expanded alternative train / validation | 186 | 1,069 | 210 |
| Expanded alternative train / test | 189 | 1,079 | 211 |

Original records are grouped by `global_id`; new expansion records are grouped by `source_file` and `source_row_id` from the 7,936-candidate manifest. Every analysed record can be mapped within its source namespace. A crosswalk between the old and new namespaces is unavailable, so the counts do not exclude further cross-source duplication.

The B2 training/development files have no common exact or NFC sentence texts, but contain two common keys after NFKC normalization, whitespace removal and case folding. Both expanded variants contain one such train/validation key. Gold150 has no complete-text overlap with these training files under the examined normalizations. This does not negate the document overlap.

## Source categories

The original corpus's four collection categories are not the expansion's source groups. The original training split contains 10,312 graduate-recruitment and 7,148 AI sentences; development contains 2,143 AI sentences; test contains 1,423 AI, 473 Tianchi/cloud and 1,341 public-institution sentences. The three acquisition routes describe providers or collection channels, not a second partition of these counts. The expansion adds listed-company records.

The latest agreement sample contains 50 distinct source-document IDs: eight listed-company, sixteen public-institution and twenty-six Tianchi/cloud records. A sample manifest verifies these counts. It does not by itself reconstruct the entire eligible frame and selection process, so reproducibility of the reported random draw remains incomplete.

## Recomputing

`audit.json` contains the count checks and sentence-key comparisons. `document_groups.json` contains the document-based checks and the source hashes. `recompute_data_audit.py` and `audit_document_groups.py` are standard-library Python scripts. Each script documents its command-line inputs. Supply local paths to the same input versions; the private expanded archive must be obtained through an authorized route. The output contains hashes and identifiers, not raw recruitment text.

Evidence: frozen split JSONL and `SPLIT.json` in `expanded_silver_splits_20260920_docs_20260921.zip`; original B2 inputs; the Gold150 release; `03_QA100_SpotCheck/SAMPLING_MANIFEST.json`; the September 13 preparation composition; the current public corpus and new-candidate manifest; and the latest three-annotator sample manifest. SHA-256 values in the result files distinguish the exact inputs.
