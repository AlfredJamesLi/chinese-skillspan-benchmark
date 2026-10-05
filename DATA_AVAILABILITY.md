# Data access and licensing

Current annotation versions and experimental access limits are summarized in the [current manuscript](reproduction/manuscript_revision_20261002/README.md). The authors confirm permission for academic research use. This statement does not extend the repository license to third-party recruitment text. Automated contact-pattern screening found candidates requiring human review; it does not certify a fully anonymized release.

## Available materials

| Resource | Access | Scope |
|---|---|---|
| Dataset archive and guidelines | [Zenodo v0.1.3](https://doi.org/10.5281/zenodo.22698504) | Source corpus, human reference set, and released Silver training/development files |
| Human reference set | [Dataset guide](data/gold150/README.md) | 150 sentences, 663 spans |
| Silver training/development sets (Qwen and encoders) | [Training/development files](data/silver_plus_v6a_nocross/README.md) | 2,150 / 169 records |
| Historical human annotation layers | [Pseudonymized exports](reproduction/evidence_review_20260925/annotation_layers/README.md) | Early blinded-coding, assisted-review, and additional-review annotation layers; historical cohort aliases and procedures documented in the linked guide |
| Chinese encoder checkpoints | [Evidence and model index](reproduction/evidence_review_20260925/README.md) | Six public Silver-fine-tuned XLM-R/ESCOXLM-R models; rescored predictions and [audit DOI](https://doi.org/10.5281/zenodo.22942441) |
| Evaluation code and saved results | [Reproduction guide](REPRODUCIBILITY.md) | Protocol-specific scoring and supporting analyses |
| JobBERT checkpoints | [Model guide](docs/models.md) | Initialization and Silver-trained continuation; default continuation is seed 42 |
| Expanded Silver pools | [Study guide](reproduction/expanded_silver/README.md) | Partial annotations, source-selection records, and result snapshots; complete final 9,540/9,646 partitions are available through the corresponding author for confidential peer review |
| Qwen LoRA adapters | [Qwen model-reproduction archive](https://doi.org/10.5281/zenodo.22851581) | Three Qwen LoRA seeds trained on the 2,150/169 Silver sets, two expanded-pool checkpoints, four supplementary adapters, frozen predictions and scoring tools |

The 500-sentence human coverage reported in the current manuscript combines distinct coding and review cohorts, each with its own annotation procedure and purpose. [Agreement documentation](reproduction/agreement/README.md) separates the designs and identifies the supplied export evidence.

## Which archive version?

Use **v0.1.3** for the human reference set and released Silver training/development files. The PeerJ Data Availability statement should cite this version DOI. Earlier [v0.1.2](https://doi.org/10.5281/zenodo.22685143) and the first Zenodo snapshot [v0.1.1](https://doi.org/10.5281/zenodo.22288338) do not include those additions. The [repository archive series concept DOI](https://doi.org/10.5281/zenodo.22288337) groups repository snapshots and currently resolves to record 22846011, version `qwen-repro-pack-20260919`. Use the specific [dataset v0.1.3 DOI](https://doi.org/10.5281/zenodo.22698504) to obtain the human reference and released Silver training/development files. Later expanded-Silver experiments on GitHub are outside the immutable v0.1.3 archive.

GitHub tags `v0.1.0` and `v0.1.1` have been withdrawn because those snapshots contained a rejected conference draft PDF. The Zenodo `v0.1.1` record remains as an immutable first snapshot; reviewers should still use **v0.1.3**. No `v0.1.4` has been minted.

The Qwen model archive provides adapters, the human reference set for scoring, and split identifiers. Base-model weights are obtained from their original releases; the 2,150/169 Silver texts are available through dataset v0.1.3. Complete expanded-pool texts and labels are available through the corresponding author for confidential peer review; public download is currently restricted. Its `README.md` and `MODEL_INDEX.csv` provide loading instructions and checkpoint-to-experiment mappings.

For the current seven-author citation and notes on wording retained inside the ZIP files, see [archive notes](docs/archive_notes.md). The published record metadata and current [CITATION.cff](CITATION.cff) supersede older embedded author lists.

## Reuse conditions

Reuse terms vary by component; see [LICENSE](LICENSE) for the applicable scope.

- **Software and documentation explicitly covered by the repository's Apache-2.0 notice:** retain that licence.
- **Original annotations and research materials:** the authors permit academic research and peer review, with appropriate attribution, to the extent that they hold the necessary rights.
- **Third-party recruitment text:** excluded from this author-granted permission. Its reuse remains subject to applicable source terms, permissions, and statutory exceptions. Inclusion in an archive does not transfer ownership or grant additional redistribution rights.
- **Model weights and adapters:** follow the notices accompanying their respective releases and the applicable base-model licences. For Qwen, consult the reproduction package's `LICENSE_NOTICE.md` and component notices.
- **Zenodo record metadata:** the [v0.1.3 dataset record](https://doi.org/10.5281/zenodo.22698504) uses component-specific reuse terms. The [repository snapshot tagged qwen-repro-pack-20260919](https://doi.org/10.5281/zenodo.22846011) belongs to the repository archive series; it is distinct from the [complete Qwen model-reproduction archive](https://doi.org/10.5281/zenodo.22851581).

The authors confirm that recruitment texts were obtained through lawful channels and that academic research use has been confirmed. The acquisition routes comprise purchased MacroData collections, public recruitment pages collected by the research team, and Alibaba Cloud Tianchi dataset 163746. See [data sources and collection](docs/data_sources.md).

Existing valid licences are unaffected by this clarification.

Original vendor CSV/XLSX exports are not part of the public data package. Questions about additional artifacts or permitted reuse should be directed to the corresponding author identified in the project citation metadata. Availability on request is not promised for artifacts that have no documented access arrangement.
