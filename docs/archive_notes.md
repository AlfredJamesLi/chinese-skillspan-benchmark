# Archive citation and release notes

Current citation metadata checked on 5 October 2026. Frozen archive files retain their original contents and checksums; the live record metadata and citation file provide the current author information.

## Current citation

The current manuscript and [project citation file](../CITATION.cff) list seven authors in this order:

Guojing Li; Zichuan Fu; Wenlin Zhang; Kaifeng Guo; Xinyang Wu; Junyi Li; Xiangyu Zhao.

Guojing Li is affiliated with Renmin University of China and City University of Hong Kong; Xinyang Wu is affiliated with Wuhan University. The other authors are affiliated with City University of Hong Kong. Use the current citation file or the citation exported from the relevant Zenodo record. The dataset and model package have different DOIs; cite the material actually used.

## Dataset archive v0.1.3

[Dataset record](https://doi.org/10.5281/zenodo.22698504).

The ZIP retains the historical eight-author list present when that snapshot was created. This affects its `CITATION.cff`, README citation and author block, and release metadata/templates under `release/zenodo/`, `release/huggingface-dataset/`, and `release/huggingface-model/`. The live record metadata and the current seven-author citation above supersede those embedded author lists. Earlier metadata corrections used a nine-author list; current citation guidance follows the author-confirmed manuscript list above.

The archived dataset ZIP has not been replaced. Its MD5 remains `8bf2b55ae539ed40f5f8add3bf047f86`. Its contents remain the v0.1.3 dataset snapshot; later experiments and the model package are separate resources.

## Qwen model-reproduction archive

[Model record](https://doi.org/10.5281/zenodo.22851581).

The ZIP's final README section says it is awaiting a later Zenodo upload. The package is now published at the model DOI above. Use the current seven-author citation exported by that model record when citing the package.

The model ZIP has not been replaced. Its MD5 remains `8d4651c2623a4e7ef5b4545212de36fc`. It contains the three Qwen adapters trained on the released Silver training/development sets, selected expanded-Silver adapters, and supplementary checkpoints with their recorded configurations and frozen predictions. See [model access](models.md) and the package's `MODEL_INDEX.csv` for the experiment mapping. Historical file identifiers such as `B2` remain available through the [terminology guide](terminology.md).

## Chinese encoder audit archive

The current manuscript links the [encoder audit and reproduction record](https://doi.org/10.5281/zenodo.22942441). The [earlier record](https://doi.org/10.5281/zenodo.22937245) remains part of the release history. Use the current record and its linked model index for the six XLM-R/ESCOXLM-R checkpoints.

Component licences and training-data availability are documented in [data access and licensing](../DATA_AVAILABILITY.md).
