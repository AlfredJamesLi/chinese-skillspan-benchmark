# Overleaf — Data Availability (paste)

Use the **short** paragraph in the PeerJ form and in the manuscript Data Availability section.  
Cite the **version** DOI. Do not write that Gold150 is inside v0.1.1.

## Short (recommended)

The Chinese-SkillSpan corpus (22,840 sentences), V4 hybrid evaluation file (2,601 unique IDs), Gold v2 labels, annotation guidelines, predefined splits, and the official scorer `cnss-lskt-1.2.0` are archived at https://doi.org/10.5281/zenodo.22288338 (version v0.1.1; concept DOI https://doi.org/10.5281/zenodo.22288337). Source code is available at https://github.com/AlfredJamesLi/chinese-skillspan-benchmark. The JobBERT-zh encoder and V4 CRF checkpoint are available at https://huggingface.co/AlfredJames/jobbert-zh. Gold150 and the Silver-plus training lists used for the additional experiments are provided as Supplemental Data S1 pending a later archival version. Redistribution of original job-advertisement wording remains subject to the source platforms’ terms.

## Longer methods footnote (optional)

Chinese-SkillSpan contains 22,840 sentences (train 17,460 / development 2,143 / test 3,237). Evaluation on the paper-main protocol uses 2,601 unique test IDs under the V4 hybrid file (SHA-256 `2ad6342d8b762cf1abb289295315e2521bec0c540f4320113409fceab0818d99`). Gold v2 (SHA-256 `7a26e32b89d4e501175cb96443e35e171cea08d91501d2a32779b96ee8504ff6`) is a construction-history label file on the same IDs and is not the abstract gold. A later draft assignment (`repartition_v1`: 16,350 / 2,268 / 4,222) sums to the same $N$ and is not the main split. The additional Gold150 test file (150 sentences; SHA-256 `ca8db0bc386c24543fec845d42ea8e24883eb67b8ce75129ac1768c5c0310fd0`) is a human overlay (Challenge-100 + Audit-50) and must not replace the V4 hybrid 2,601-ID test. This work was supported by the National Social Science Fund of China, Grant No. 21BGL142.

## Forbidden URLs

- https://sites.google.com/view/cn-skillspan-resources
- Any Google Drive folder
- Sister-paper arXiv `2604.21525` / `2604.23009` as *this* paper’s data link
