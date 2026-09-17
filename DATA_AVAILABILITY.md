# Data access and licensing

## Available materials

| Resource | Access | Scope |
|---|---|---|
| Core dataset and guidelines | [Zenodo v0.1.3](https://doi.org/10.5281/zenodo.22698504) | Original corpus, human reference, and released B2 files |
| Human reference | [Dataset guide](data/gold150/README.md) | 150 sentences, 663 spans |
| Qwen B2 supervision | [Training/development files](data/silver_plus_v6a_nocross/README.md) | 2,150 / 169 records |
| Evaluation code and saved results | [Reproduction guide](REPRODUCIBILITY.md) | Protocol-specific scoring and supporting analyses |
| JobBERT checkpoints | [Model guide](docs/models.md) | Initialization and B2 continuation; default continuation is seed 42 |
| Expanded Silver | [Study guide](reproduction/expanded_silver/README.md) | Partial annotations, source-selection records, and result snapshots; complete final 9,540/9,646 partitions are not released |
| Qwen LoRA adapters | Not publicly released | Needed for a complete inference rerun |

The 500-sentence human coverage reported in the current manuscript combines distinct coding and review cohorts. It is not a single 500-sentence Gold dataset. [Agreement documentation](reproduction/agreement/README.md) separates the designs and identifies the supplied export evidence.

## Which archive version?

Use **v0.1.3** for the human reference and B2 files. Earlier [v0.1.1](https://doi.org/10.5281/zenodo.22288338) and [v0.1.2](https://doi.org/10.5281/zenodo.22685143) do not include those additions. The [concept DOI](https://doi.org/10.5281/zenodo.22288337) groups the versions. Later expanded-Silver experiments on GitHub are outside the immutable v0.1.3 archive.

## Reuse conditions

The authors report research-use permission for recruitment notices purchased from a commercial compiler of publicly posted advertisements. This permission is distinct from an open-content licence for the original wording. Source text, software, and model weights have different terms:

- **Software and original documentation:** consult [LICENSE](LICENSE) for the repository's proposed Apache-2.0 notice and its scope.
- **Advertisement wording:** no general CC-BY grant is made by the authors. Do not treat public download access as unrestricted redistribution permission.
- **Model weights:** the Hugging Face cards currently use `license: other`.

**Metadata discrepancy:** Zenodo v0.1.3 currently displays `cc-by-4.0`, while the repository's source-text notice does not grant that licence. This discrepancy requires author clarification. This documentation update does not change or grant data rights.

Original vendor CSV/XLSX exports are not part of the public data package. Questions about additional artifacts or permitted reuse should be directed to the corresponding author identified in the project citation metadata. Availability on request is not promised for artifacts that have no documented access arrangement.
