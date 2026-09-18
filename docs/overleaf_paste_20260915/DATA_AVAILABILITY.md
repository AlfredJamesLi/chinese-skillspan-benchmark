# Overleaf / PeerJ — Data Availability (paste)

Use the **short** paragraph in the PeerJ form and in the manuscript Data Availability section.  
Cite the **v0.1.3** version DOI. Do not write that the human reference set is inside v0.1.1.  
Do not mint or cite `v0.1.4`. Use only GitHub, Hugging Face model pages, and Zenodo.

## Short (recommended)

The Chinese-SkillSpan dataset, annotation guidelines, predefined data splits, and documentation are available at https://doi.org/10.5281/zenodo.22698504 (version v0.1.3; concept DOI https://doi.org/10.5281/zenodo.22288337). An earlier snapshot is https://doi.org/10.5281/zenodo.22685143 (version v0.1.2). The first archival snapshot remains at https://doi.org/10.5281/zenodo.22288338 (version v0.1.1) on Zenodo; the corresponding GitHub tags v0.1.0 and v0.1.1 have been withdrawn. The source code, preprocessing scripts, and evaluation tools are available at https://github.com/AlfredJamesLi/chinese-skillspan-benchmark. The JobBERT-zh initialization encoder and inherited CRF are available at https://huggingface.co/AlfredJames/jobbert-zh. The JobBERT-zh B2 continuation is available at https://huggingface.co/AlfredJames/jobbert-zh-v6a (default checkpoint is seed 42). The 150-sentence human reference set and Silver-plus B2 training/development files are included in v0.1.3 and are not in Zenodo v0.1.1 or v0.1.2. Qwen LoRA adapters are not published. These materials are released for academic research and peer review. Original job-advertisement wording is not licensed as CC-BY.

## Longer methods footnote (optional)

Chinese-SkillSpan contains 22,840 sentences (train 17,460 / development 2,143 / test 3,237). The current human-reference evaluation uses the 150-sentence overlay (SHA-256 `ca8db0bc386c24543fec845d42ea8e24883eb67b8ce75129ac1768c5c0310fd0`). A historical hybrid evaluation file covers 2,601 unique IDs and is a different protocol. A later draft assignment (`repartition_v1`: 16,350 / 2,268 / 4,222) sums to the same $N$ and is not the main split. This work was supported by the National Social Science Fund of China, Grant No. 21BGL142.
