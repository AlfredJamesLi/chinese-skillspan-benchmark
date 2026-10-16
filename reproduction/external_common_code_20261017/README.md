# External common-protocol encoder code

This directory releases the retained 21 September 2026 implementation for the controlled XLM-R-large / ESCOXLM-R linear-BIO comparison. It is separate from native MaChAmp, Kompetencer, or NNOSE experiments.

## Provenance and scope

The six original code/configuration files are preserved byte-for-byte; [PROVENANCE.json](PROVENANCE.json) records SHA-256 values. The six dataset manifests retain upstream revisions and 24 input-file hashes. Recruitment data, weights and private credentials are not included here.

The [published 48-run receipts](https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/blob/46d1166f8e11dd52d473f645536074bb8dd0a53c/results_snapshots/external_benchmarks_20260922/results.jsonl) name `run_common_encoder.py` and `audit_and_lexicon.entities`. Their experiment matrix and model/dataset revisions match this retained implementation. Those receipts did not record a source-code hash, so identity with the final server-executed bytes remains unverified. This release does not relabel the retained preparation code as recovered original server code. No training was rerun for this release.

## Files and method

- `run_common_encoder.py`: first-subword BIO supervision, source-word chunks (at most 128 words), AdamW, development-set checkpoint selection, and saved predictions.
- `audit_and_lexicon.py`: span conversion, strict span/type micro-F1 and a separate training-only lexical control.
- `run_matrix.py`: dry-run dispatcher; six datasets, eight label streams, two encoders and three seeds make 48 full runs.
- `models.json`: immutable model revisions; only the two models selected by the dispatcher are used in this comparison.
- `requirements-common.txt`: retained installation recipe, not a historical environment lock.
- `test_protocol.py`: seven known-answer scoring/protocol checks without GPU dependencies.
- `data/*/download_manifest.json`: original source URLs, revisions and hashes; not the dataset contents.
- `prepare_data.py`: a new 17 October 2026 retrieval/verification helper; not part of the historical experiment code.

The runner defaults to 20 epochs, batch size 8 and learning rate 2e-5. It chooses the highest development strict span/type micro-F1 (earliest epoch wins ties); test data are not used for checkpoint selection. Do not substitute this protocol for native-task results or for the Chinese character-span evaluation.

## Obtain and verify inputs

Use the six original Hugging Face dataset sources and immutable revisions in the manifests. Their original terms apply. The helper defaults to verification only and never starts a model:

```bash
cd reproduction/external_common_code_20261017
python prepare_data.py --download
python prepare_data.py
python test_protocol.py
python run_common_encoder.py --help
```

`--download` retrieves only the manifest-listed files from their original sources and checks their SHA-256 values before writing. Without it, missing inputs are reported. Existing mismatched files are rejected rather than overwritten. The original runner expects `data/<dataset>/train.json`, `dev.json`, `test.json`, `README.md`, and the retained manifest. Restricted or changed upstream files must be obtained under their source conditions; never replace failed hashes silently.

## Plan or run experiments

```bash
# Write a 48-job plan only; no GPU imports, download or model execution.
python run_matrix.py --phase full --output /path/to/new/run-directory

# On a suitable GPU machine, prepare an isolated environment from the retained
# recipe, inspect the plan, then explicitly opt in to execution.
python -m pip install -r requirements-common.txt
python run_matrix.py --phase smoke --execute --output /path/to/new/smoke-directory
python run_matrix.py --phase full --execute --output /path/to/new/run-directory
```

Use a new output directory. Each run writes its configuration, training history, development-selected model, prediction files and metrics. Smoke mode does not evaluate the test split. Historical software/GPU information is available in the [B-side encoder environment record](https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/tree/0c73207c0f9b00fa87f385b78bcb7342bd00bfcb/results_snapshots/table11_evidence_20260924); the correspondence and limits are described in the [release scope](../code_release_20261017/README.md).

## Citation, licence and contributions

Cite the Chinese-SkillSpan paper and this repository's fixed code revision, and cite the original datasets and model papers when using them. Project-authored software follows the repository [Apache-2.0 licence](../../LICENSE); original data/model terms remain separate. Report issues under the [contribution guidelines](../../CONTRIBUTING.md), including the revision, command, environment and input hashes. Use synthetic examples instead of redistributing restricted source texts.
