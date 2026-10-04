# Membership of the 50-sentence annotation-agreement sample

The three independent annotation exports dated 3 October 2026 were compared with frozen experimental inputs. This audit reports sentence membership, agreement counts and file hashes. It does not change annotations or model results and does not create an adjudicated test set.

## Results

Mean pairwise typed exact F1 is **0.818**, boundary F1 is **0.850**, and all three annotators give identical annotations on **34 of 50 sentences**, including **11 sentences empty for all three**. The individual exports contain 104, 123 and 113 spans; each contains two L spans. The authors identify the labels as independent annotations with individual self-review and consultation of the handbook. They are not adjudicated consensus labels.

| Frozen input | Sample sentences present |
| --- | ---: |
| B2 training | 0 |
| B2 development | 0 |
| Gold150 human reference | 0 |
| Adopted Codex expanded training | 46 |
| Adopted Codex expanded validation | 2 |
| Adopted Codex expanded Silver test | 1 |
| Alternative API expanded training | 46 |
| Alternative API expanded validation | 2 |
| Alternative API expanded Silver test | 1 |

ID, full original text, NFC-normalized text, and NFKC-normalized text with whitespace removed and case folded give identical counts. Each expanded pool contains 49 of the 50 sample sentences. The split hashes match the earlier frozen-data audit. The earlier experiment-identity check also verified that expanded BIO sentence IDs and texts match the occurrence-format inputs recorded for the Qwen experiments.

The study assesses independent human agreement. It is not a held-out model test. Adjudication alone would not make these sentences independent of the expanded models' training and validation. Training exposure does not, by itself, invalidate an agreement study in which annotators did not see model suggestions or one another's labels.

The expansion source mapping confirms one sampled sentence per recorded advertisement. Expanded training shares 47 of those source-document groups, validation two and Silver test one; groups can occur in more than one split, so these counts cannot be added. Document identifiers from separate source namespaces are not treated as a universal crosswalk.

## Prompt checks

Four retained files were examined: historical Silver rev1 and rev2 prompts, the public API prompt reformulation, and the shared inference prompt. None contains a complete sampled sentence under any of the three text-matching rules. This check does not cover unarchived sessions, every historical prompt, or partial examples. The reformulated prompt is not substituted for an executed historical prompt.

## Files and reproduction

- `audit.json` contains aggregate results, file hashes and the scope of the checks. It contains no recruitment sentences or machine-specific paths.
- `recompute.py` uses the Python standard library and writes counts and hashes only.
- `inputs.example.json` shows the required configuration keys with **illustrative relative paths**. It is a template, not an executable manifest or a statement that all input files are public.

Copy the example to a local configuration, replace each placeholder path with the corresponding available file, then run:

```text
python recompute.py --inputs inputs.local.json --output audit.recomputed.json
```

Paths are resolved against the current working directory. The `files` mapping requires the three pseudonymized coder exports (`study_id`, `text`, `label`), sample manifest, B2 training/development files, Gold150, the complete archived expanded-split ZIP, the expansion source mapping, and two earlier audit files. The `author_confirmation` document is hashed as provenance but is not parsed to calculate overlap or agreement. The `prompts` mapping lists the four retained prompt texts.

The complete expanded-pool inputs are not supplied in this public package. Full recomputation therefore requires access to those original files; the aggregate report alone does not reproduce the membership calculation.

The prior audit inputs can be the public files `reproduction/major_revision_20261004/data_audit/audit.json` and `reproduction/major_revision_20261004/data_audit/key_semantics/recheck.json`. The script reads their recorded split hashes and verification flags rather than requiring a particular hash of those report files. Public sanitization changes the report-file hashes without changing the fields used here. Consequently, a rerun using the public reports can reproduce the counts and verification flags while recording different report-input hashes. The original hashes in the published `audit.json` are retained and must not be silently replaced to force a byte-for-byte match.
