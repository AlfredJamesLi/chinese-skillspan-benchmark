# Chinese-SkillSpan code release, 17 October 2026

Historical scope: the original tag is unchanged. The Qwen row and item 2 below are updated in this working revision after the server-A delivery; other original scope statements retain their historical context. For subsequently recovered sources and current limitations, see [revision 1](../code_release_20261017_1/README.md).

This version adds the retained external common-protocol implementation and a consolidated README covering code, inputs, requirements, usage, methodology, citations and component-specific licensing. It preserves all reported results and model/prediction files. This is a documented code release, not certification of full end-to-end reproducibility.

## Entry points and evidence

| Experiment | Available implementation | Evidence limits |
|---|---|---|
| JobBERT domain pretraining | [`train_jobbert_zh_mlm.py`](../../scripts/train_jobbert_zh_mlm.py), [`jobbert_zh_3m.sbatch`](../../scripts/jobbert_zh_3m.sbatch), [`export_jobbert_mlm_encoder.py`](../../scripts/export_jobbert_mlm_encoder.py) | Some original runtime records are missing. |
| JobBERT CRF and continuation | [`train_cn_roberta_crf.py`](../../scripts/train_cn_roberta_crf.py) is the general CRF implementation; existing checkpoints and predictions remain available. | A laboratory recovery report located the five continuation entry files listed below, but their bytes have not been supplied to this release. The fresh-head extension is not a replacement. |
| Qwen shared-guideline B2 and expanded pools | [Existing Qwen release](https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/releases/tag/qwen-repro-pack-20260919), `CNSS_Qwen_Reproduction.zip`: `shared_guidelines_b2/scripts/` and `expanded_silver/{codex,proxy}_seed42/scripts/` | Actual training/inference/scoring scripts are already published. Some paths require local configuration; full expanded training texts are not public. |
| Qwen no-adapter paired baseline | [Recovered A originals](qwen_no_adapter_shared_guidelines/INTEGRATION.md): `run_qwen_worker.py`, `gold150_qwen.sbatch`, `gold150_qwen_shard1.sbatch`, `merge_qwen_shards.py`, frozen prompt/parser and worker fingerprints | DS209213; Slurm 50966/50967; `adapter: null`; recorded typed exact F1 0.3612. The two fingerprint SHA-256 values and source paths are recorded in the linked audit. `infer_gold150_sft.py` is not this baseline generator. No execution on B or new model run is claimed. |
| Chinese XLM-R / ESCOXLM-R | [Pinned encoder archive](https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/tree/0c73207c0f9b00fa87f385b78bcb7342bd00bfcb/results_snapshots/table11_evidence_20260924): `code/run_chinese_encoder.py`, launch scripts, configurations and environment record | Software and GPU records exist; they are not proof of the environment of other experiments. |
| External common protocol (48 runs) | [Retained runner, helper, dispatcher, model revisions and six input manifests](../external_common_code_20261017/README.md) | Protocol/matrix/revisions match the reported receipts; final server-source byte identity is unverified. |
| Native SkillSpan / Gnehm | [B-side code archive](https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/tree/0c73207c0f9b00fa87f385b78bcb7342bd00bfcb/results_snapshots/table11_evidence_20260924/code), including `scripts/run_remaining_today.py` | [B follow-up](../server_b_machamp_emit_20261017/README.md) supplies the aggregation entry/helper and three complete modified SkillSpan MaChAmp files. The old diff remains truncated and complete upstream/configuration binding remains incomplete. |
| Native Kompetencer / NNOSE | [Pinned A-native records](https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/tree/b84f218b7142c97ab03a60499a9b30e7ec332cab/results_snapshots/a_native_20260924) | Records, environment and predictions are available; project-specific launch/configuration/patch coverage remains incomplete. |

## Specific unresolved items

1. Resolved by the [server-B source delivery](../server_b_code_addendum_20261017/README.md): the five JobBERT continuation entries and project-owned dependencies are supplied. Historical environment and initialization-byte binding are not resolved by source delivery.
2. Resolved by the 17 October server-A delivery: the original no-adapter shared-guideline Qwen generation entry, launch/merge scripts and retained run binding are now supplied; see [the A integration audit](qwen_no_adapter_shared_guidelines/INTEGRATION.md). This closes source recovery, not full environment/input reproducibility.
3. Historical server-byte binding/configurations for the retained external runner; remaining native-task configuration/patch files.
4. Historical OS and some JobBERT/Qwen software/GPU records. A present-day server query cannot fill historical fields.

The release search checked the available local history, the previously inventoried public branches and 114 accessible local archives. The original external runner was also present in two September handoff ZIPs. The five named JobBERT continuation files were not located in that initial search; the later B delivery supplied them. This is a scoped search result, not a claim that the files never existed.

## Validation and reproduction levels

See [VALIDATION.json](VALIDATION.json) for checks actually run for this release. File checksums, syntax, known-answer protocol checks, input-manifest verification and a dry-run job matrix do not establish GPU training reproduction. No model call, training, inference or prediction rescoring was performed for this release.

Use [the evaluation guide](../EVALUATION_ENTRY.md) to rescore already released predictions. Retraining or new inference additionally requires the matching data, model weights, environment and entry point. The 2,156-record JobBERT training set is distinct from the 2,150-record Qwen/encoder set.

## Fixed citation and access

Use the dedicated [code citation metadata](CITATION.cff), separate from the dataset citation at the repository root. Identify this release by tag `code-materials-20261017` and the resolved Git commit. Keep existing dataset/model DOIs for their original contents; this tag does not retroactively change those Zenodo snapshots or create a new DOI. A new code addendum can also be supplied as a journal supplemental Dataset with a legend containing "code". This release does not claim that unresolved items above have been recovered or accepted by the journal.

Source texts remain subject to their providers' terms. No additional full third-party text or model weights were added. See [data access](../../DATA_AVAILABILITY.md), [licence](../../LICENSE), and [contribution guidelines](../../CONTRIBUTING.md).
