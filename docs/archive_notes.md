# Archive citation and release notes

Checked on 20 September 2026. These notes correct citation and release-status text; they do not change labels, model weights, predictions, scores, or the identity of either archived ZIP.

## Correct citation

The current manuscript, both Zenodo records below, and the [project citation file](../CITATION.cff) list nine authors in this order:

Guojing Li; Zichuan Fu; Junyi Li; Wenlin Zhang; Kaifeng Guo; Jinning Yang; **Xinyang Wu**; Jingtong Gao; Xiangyu Zhao.

Xinyang Wu is affiliated with Wuhan University. Use the current citation file or the citation exported from the relevant Zenodo record. The dataset and model package have different DOIs; cite the material actually used.

## Dataset archive v0.1.3

[Dataset record](https://doi.org/10.5281/zenodo.22698504).

The ZIP retains the eight-author list that existed when the snapshot was created. This affects its `CITATION.cff`, README citation and author block, and release metadata/templates under `release/zenodo/`, `release/huggingface-dataset/`, and `release/huggingface-model/`. These embedded lists omit Xinyang Wu and are superseded by the corrected citation above. The live record now lists all nine authors.

The archived dataset ZIP has not been replaced. Its MD5 remains `8bf2b55ae539ed40f5f8add3bf047f86`. Its contents remain the v0.1.3 dataset snapshot; later experiments and the model package are separate resources.

## Qwen model-reproduction archive

[Model record](https://doi.org/10.5281/zenodo.22851581).

The ZIP's final README section says it is awaiting a later Zenodo upload. That sentence is obsolete: the package is published at the model DOI above. No eight-author project citation was found in the checked README, citation, model-card, or release-metadata files. Use the nine-author citation exported by the model record when citing this package.

The model ZIP has not been replaced. Its MD5 remains `8d4651c2623a4e7ef5b4545212de36fc`. It contains the three shared-guideline B2 adapters, selected expanded-Silver adapters, and supplementary checkpoints with their recorded configurations and frozen predictions. See [model access](models.md) and the package's `MODEL_INDEX.csv` for the experiment mapping.

These documentation corrections do not expand any component's licence or supply missing training data. Consult [data access and licensing](../DATA_AVAILABILITY.md) for the remaining access limits.
