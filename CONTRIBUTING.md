# Contributing to Chinese-SkillSpan

Thank you for helping improve **Chinese-SkillSpan** and **JobBERT-zh**. Please open an issue at https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/issues. For matters that should not be public, contact the corresponding author, Xiangyu Zhao (`xianzhao@cityu.edu.hk`).

Please do **not** open a pull request that uploads new job-advertisement text.

---

## What to report

Use a short, reproducible description. Include file paths relative to this repository, SHA-256 of gold or prediction files if you have them, the scorer version (`cnss-lskt-1.2.0`), and the exact command you ran.

### Annotation issues

- Disagreement with Handbook B (`B.sop_v4.2.1`): span boundary, type (L / K / S / T), empty-span cases.
- State whether you used Gold v2, the V4 hybrid, or the 200-sentence human overlay. Do not mix protocols in one ticket.
- Quote only the **minimum** span needed to discuss the label. Prefer `id` + token offsets over pasting a full advertisement.

### Data-processing bugs

- Split membership, ID collisions, jieba snap errors, hybrid rewrite changing the frozen SHA-256.
- Attach the command and, if possible, a single-record fixture you created yourself (not scraped ads).

### Code bugs

- Scorer alignment, CRF trainer, evaluation scripts.
- Laboratory absolute paths that break a clean clone are already a known issue; a patch that parameterises `PAPER` / `ROOT` is welcome.

### Reproducibility failures

- You followed `REPRODUCIBILITY.md` and did not obtain the committed CSV cell (for example JobBERT_3M_v4 typed exact **0.433118** after jieba snap).
- Include OS, Python version, `jieba` version, and whether `output/` or `data/frozen_preds/` was used.
- Do not file a bug because direct scoring of `jobbert_3m_v4.jsonl` without jieba snap yields ~0.255 — that behaviour is documented.

### Model-card corrections

- Errors in `release/huggingface-model/README.md` (architecture, licence, intended use).
- Do not change the licence field to a concrete SPDX id until the base-model licence and training-data rights are confirmed.

---

## What not to submit

Contributors **must not** submit:

- Personal data, CVs, or contact details of job seekers or annotators
- Confidential annotation ledgers, API keys, access tokens, or laboratory credentials
- Copyrighted job-advertisement text, bulk CSV / XLSX dumps, or scraped pages **without written permission** from the rights holder
- Weights or data from the sister IEEE Access / SRICL project as if they belonged to Chinese-SkillSpan

If you need to illustrate a sentence, invent a short synthetic example or use a span that is already in a file the maintainers have cleared for discussion.

---

## Development notes

- Public-facing prose is English. Laboratory notes may remain Chinese.
- Do not overwrite `data/gold_canonical_v2.jsonl` or the frozen V4 hybrid with a rebuilt file unless the SHA-256 is unchanged.
- Do not add Concept Accuracy, Time-OOD, or English six-dataset SRICL tables to this project.
- A public code of conduct has not been added yet.

---

## Licence of contributions

No SPDX licence has been chosen for this repository. Do not upload new advertisement text. Patches to scorer, scripts, and documentation are welcome.
