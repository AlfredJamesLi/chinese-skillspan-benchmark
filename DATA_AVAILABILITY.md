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

Use **v0.1.3** for the human reference and B2 files. The PeerJ Data Availability statement should cite this version DOI. Earlier [v0.1.2](https://doi.org/10.5281/zenodo.22685143) and the first Zenodo snapshot [v0.1.1](https://doi.org/10.5281/zenodo.22288338) do not include those additions. The [concept DOI](https://doi.org/10.5281/zenodo.22288337) groups the versions. Later expanded-Silver experiments on GitHub are outside the immutable v0.1.3 archive.

Do not use GitHub tags `v0.1.0` or `v0.1.1`: those snapshots contain a rejected conference draft PDF and are scheduled for deletion. The Zenodo `v0.1.1` record remains as an immutable first snapshot; reviewers should still use **v0.1.3**. No `v0.1.4` has been minted.

## Reuse conditions

Author decision (2026-09-18): the archived corpus, labels, guidelines, and released checkpoints may be used for **academic research and peer review**. Recruitment notices were purchased from a commercial compiler of publicly posted advertisements. That permission is **not** a general open-content or commercial-redistribution licence on the original wording.

- **Software and original documentation:** consult [LICENSE](LICENSE) for the repository's proposed Apache-2.0 notice and its scope.
- **Advertisement wording:** academic research use is permitted. The authors do not grant CC-BY on the original wording. Do not treat public download access as permission to republish the advertisements commercially.
- **Model weights:** the Hugging Face cards currently use `license: other` and follow the same academic-research scope.
- **Zenodo page label:** the GitHub–Zenodo hook still displays `cc-by-4.0` on the record. That platform default is **not** the author grant. The author grant is academic research use, as stated here.

Original vendor CSV/XLSX exports are not part of the public data package. Questions about additional artifacts or permitted reuse should be directed to the corresponding author identified in the project citation metadata. Availability on request is not promised for artifacts that have no documented access arrangement.
