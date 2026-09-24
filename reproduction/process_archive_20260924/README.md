# Supporting process records and exploratory results

This collection accompanies the September 24, 2026 manuscript consolidation. It preserves material moved out of the PDF to focus the paper on the Chinese annotation framework, quality evidence, and principal evaluations. Table numbers below refer to the **43-page manuscript before this consolidation**, not the current numbering. No new experiments or independent rescoring were performed for this documentation change.

| Previous item | Archived material | Reason for relocation |
|---|---|---|
| Table 20 | [Qwen subset runs](#qwen-subset-runs-previous-table-20) | Exploratory supervision and selection history |
| Table 13 | [Execution-version matrix and hashes](source/tex/review20260923/version_matrix.tex) | Detailed version ledger; scientific compatibility limitations remain in the paper |
| Table 25 | [Pooled SkillSpan BIO scores](#skillspan-pooled-scores-previous-table-25) | A second scoring view of the same native runs; primary native-task comparisons remain in the paper |
| Appendix D detail | [Original reproduction and audit text](source/tex/appendix_D_reproduction_R16.tex) | Archive history and detailed preparation records |
| Appendix E detail | [Original experiment records](source/tex/external_benchmarks/paper_appendix.tex) | Revision identifiers, run-count bookkeeping, and selected-epoch records |

## Qwen subset runs (previous Table 20)

All five runs use seed 42, the shared guidelines and occurrence-based output, evaluated against the same 150-sentence human reference (Gold150). That reference was used in guideline development and is not a new blind test. Full-development and train/validation/test (TVT) denote different checkpoint-selection arrangements.

| Supervision subset | Training sentences | Exact F1 | Relaxed F1 |
|---|---:|---:|---:|
| Wave3, proxy labels | 1,678 | 0.587 | 0.717 |
| Wave3, Codex labels | 1,579 | 0.585 | 0.699 |
| Waves1–2, Codex labels | 3,159 | 0.575 | 0.695 |
| New Silver, full-development selection | 7,117 | 0.588 | 0.710 |
| New Silver, TVT selection | 7,117 | 0.573 | 0.709 |

The Wave3 conditions start with the same candidate identifiers but differ in annotation channel and retained training sets. These runs do not isolate an annotation-channel effect, a data-size effect, or a general selection advantage. No multi-seed uncertainty is available. All rows, including lower scores, are retained. The displayed values are copied from the manuscript, not full-precision raw metrics. [CSV](tables/qwen_subsets.csv); [original LaTeX and context](source/tex/expanded_silver_supplement_20260917.tex).

These five rows and the two pooled Qwen rows retained in the manuscript correspond to Table H of the [September 17 result snapshot](https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/tree/11355ff567d647cb087b0f033e09fd0825dac3c4). The [model archive](https://doi.org/10.5281/zenodo.22851581) supplies supporting adapters and scoring materials, but does not include all expanded-pool training texts and labels.

## SkillSpan pooled scores (previous Table 25)

| Model | Skills | Knowledge |
|---|---:|---:|
| BERT | 0.495 ± 0.011 | 0.639 ± 0.005 |
| SpanBERT | 0.511 ± 0.012 | 0.632 ± 0.009 |
| JobBERT | 0.525 ± 0.008 | 0.654 ± 0.003 |
| JobSpanBERT | 0.522 ± 0.008 | 0.628 ± 0.008 |

Mean ± sample SD over five seeds. These are reported pooled HOUSE+TECH BIO scores for the same native runs whose MaChAmp per-site scores remain in the paper. Pooling predictions and using the BIO scorer differs from averaging per-site F1 and from the per-site MaChAmp scoring procedure. Native runs contain 3,570 test sentences versus 3,569 in the common-protocol release; the one-record mismatch is unresolved at the ID level. These results do not establish a matched replication of the original full SkillSpan evaluation. [CSV](tables/skillspan_pooled.csv); [exact original table](tables/skillspan_pooled.tex).

## Provenance and verification scope

The source excerpts are copied without numeric edits from Overleaf commit `e165c7ef6e9b005b081865aea73b9d8d291b780d`. Internal LaTeX references in these archival excerpts retain their original labels; they are not standalone compilable manuscripts. [Archive manifest](manifest.json) records checksums for these copies. Existing source records remain at the [server-B snapshot](https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/tree/46d1166f8e11dd52d473f645536074bb8dd0a53c/results_snapshots/external_benchmarks_20260922) and [server-A snapshot](https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/tree/b84f218b7142c97ab03a60499a9b30e7ec332cab/results_snapshots/a_native_20260924).

Relocation does not remedy missing artifacts, establish final-guide compatibility, verify provider checkpoints, or independently rescore external/Chinese encoder predictions. The manuscript retains these limitations, the access matrix, the overlap finding and limits of sentence-level leakage checks, and the relevant native-task comparisons. This archive contains documentation and aggregate results, not newly released recruitment text or model weights.
