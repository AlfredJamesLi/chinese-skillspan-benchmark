# Final-handbook agreement: three coders, 50 sentences

**Archived snapshot.** The current manuscript uses the [latest individual exports and results](../finalguide_abc_20261003/README.md), following the authors' clarification that revisions were individual self-review with access to the handbook. The values and files below preserve the earlier snapshot.

This release accompanies Table 3 of Chinese-SkillSpan. Three coders independently annotated the same 50 Chinese recruitment sentences under B.sop_v4.2.14. The preserved pre-discussion exports, not later edited Doccano labels, are the statistical inputs. The study measures inter-coder agreement, not model accuracy against Gold150.

## Verified results

| Pair | Typed exact F1 [95% CI] | Boundary F1 | Equal sentence span sets |
|---|---|---:|---:|
| A–B | 0.657 [0.528, 0.767] | 0.762 | 26/50 |
| A–C | 0.739 [0.612, 0.850] | 0.788 | 33/50 |
| B–C | 0.594 [0.459, 0.717] | 0.721 | 22/50 |
| Mean | 0.663 [0.562, 0.759] | 0.757 | All three: 21/50 |

Three-rater nominal character alpha is 0.817 [0.755, 0.873]. Its point estimate exceeds the plan's conventional 0.80 reference, but the interval extends below it. Mean typed F1 falls below the project's 0.80 target; no labels or participants were discarded to reach that target. The target is a project criterion, not a universal F1 acceptance threshold. Historical results and source labels have not been rewritten.

Ten of the 21 all-identical sentence sets are empty. O occupies 59.5–64.5% of source code points. L has only two spans, both in one sentence; its perfect agreement does not establish category-wide reliability. See [all metrics](recomputed_metrics.json) for per-pair category counts, conditional type disagreements, and character diagnostics.

## Data and computation

- `data/frozen50_A.jsonl`, `frozen50_B.jsonl`, `frozen50_C.jsonl`: aligned, pseudonymized exports with unchanged text, boundaries, types and confirmation status; 97/113/106 spans.
- `data/sample_manifest.json`: 50 distinct recorded advertisement IDs and source counts 8 listed-company / 16 public-institution / 26 Tianchi. A complete sampling frame and inclusion probabilities were not supplied.
- `data/separate15_A.jsonl`, `separate15_C.jsonl`: training exports, explicitly excluded from the formal sample. Their F1 is 0.360 and is not a formal study result or a training-effect estimate. The B export for this library has no confirmed labels and is not treated as 15 empty negatives.
- `recompute.py`: independently implemented scorer. Run `python recompute.py output.json` with Python 3.9+ and NumPy. The exact NumPy version and RNG are recorded in the output.
- `disagreements_29.jsonl`: all 29 sentences without three-way exact span agreement, with each coder's original labels; no adjudicated answer is invented.
- `verification.json`: integrity checks, source/export distinctions, batch overlap screens and later-edit differences.
- `manifest.json`: public-file hashes and original export identities.

F1 pools span counts within each coder pair, then averages A–B, A–C and B–C equally. No coder is gold. Alpha projects each original Unicode code point to O/L/K/S/T, retaining spaces and punctuation. Characters are measurement units, not independent bootstrap observations. No overlaps or projection conflicts were found.

All manuscript intervals were recomputed with 10,000 source-stratified sentence resamples, NumPy default_rng/PCG64 and seed 20260927. Every sampled sentence brings all three coders' labels with it. Each recorded advertisement contributes one sentence. The intervals condition on the observed source proportions and this coder group, without design weights. All resampled reported coefficients were defined.

The supplied AC-only analysis used unstratified sentence resampling, seed 20260928, and reported [0.6094420601, 0.8495575221]. That supplied interval is retained here as a source record; its exact RNG implementation was not included. Our uniform, executable source-stratified analysis yields [0.6124401914, 0.8497474093] for A–C. This is a disclosed analysis-specification difference, not a change to labels or point estimates.

## Training and chronology

On October 2 the authors confirmed that five and fifteen sentences were used for familiarization and training, followed by independently completing fifty sentences; completion times differed across coders. The package calls the 15-sentence library “formal15” or “pilot”, but its role in this study is training. It is not pooled with the 50 formal sentences, and no 5+15+50 training trajectory is inferred from its scores.

The A/C freeze receipt is dated September 28; the three-coder snapshot is dated October 2. Matching hashes verify that A/C labels in the latter snapshot equal the earlier freeze. A later live export has changes in C's labels on ten formal sentences; those edits do not enter the paper. Export timestamps do not establish completion dates. The authors and source report identify the retained layers as independently produced before discussion; individual dated training logs, complete prior-exposure records, and server revision histories are not supplied.

The received archive has SHA-256 `9b50d9d33d985477656e51010467d952bd2fe6445fda8fc1845a4cfa6b4dbd85`. The original archive is retained locally. Public exports remove account names and administrative identifiers; immutable originals remain separately backed up. Normalized text checks find no duplicates between the 5/15/50 batches, no exact matches to the 32 handbook training cases, and no matches to the available old independent50, assisted15 or QA150 releases. These checks are not proof of exhaustive non-exposure or a new independent model test set.

## Relation to the plan and access terms

The [September 27 plan](../../../notes/handbooks/training/archive/protocol_20260927.md) is retained unchanged, including its project F1 target. This release replaces pending statistical fields with observations, retains all three coders, and reports the goal not reached. The [current training guide](../../../notes/handbooks/training/README.md) links the implemented study and historical plan.

Reuse follows the repository's component-specific terms. Publication of the original recruitment text in these analytical files does not create additional third-party redistribution rights.

## References

Hripcsak, G., & Rothschild, A. S. (2005). Agreement, the F-measure, and reliability in information retrieval. Journal of the American Medical Informatics Association, 12(3), 296–298. https://doi.org/10.1197/jamia.M1733

Artstein, R., & Poesio, M. (2008). Inter-coder agreement for computational linguistics. Computational Linguistics, 34(4), 555–596. https://doi.org/10.1162/coli.07-034-R2

Klie, J.-C., Eckart de Castilho, R., & Gurevych, I. (2024). Analyzing dataset annotation quality management in the wild. Computational Linguistics, 50(3), 817–866. https://doi.org/10.1162/coli_a_00516
