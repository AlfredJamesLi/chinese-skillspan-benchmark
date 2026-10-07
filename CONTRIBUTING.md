# Contributing to Chinese-SkillSpan

Thank you for helping improve **Chinese-SkillSpan** and **JobBERT-zh**. Please open an issue at https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/issues. For matters that should not be public, contact the corresponding author, Xiangyu Zhao (`xianzhao@cityu.edu.hk`).

Please use synthetic examples when reporting issues. Requirements for sharing source text are listed below.

---

## What to report

Use a short, reproducible description. Include file paths relative to this repository, SHA-256 of gold or prediction files if you have them, the scorer version (`cnss-lskt-1.2.0`), and the exact command you ran.

### Annotation issues

- Questions about span boundaries, types (L / K / S / T), or empty annotations. Cite the handbook version and date you used; the [handbook directory](notes/handbooks/README.md) lists available editions.
- State whether you used Gold v2, the V4 hybrid, the 200-sentence human overlay, or the 150-sentence human reference set. Report issues for different evaluation protocols separately.
- Quote only the **minimum** span needed to discuss the label. Prefer `id` + token offsets over pasting a full advertisement.

### Data-processing bugs

- Split membership, ID collisions, jieba snap errors, hybrid rewrite changing the frozen SHA-256.
- Attach the command and, if possible, a single-record fixture you created yourself (not scraped ads).

### Code bugs

- Scorer alignment, CRF trainer, evaluation scripts.
- Main scoring, CRF training, and human-reference evaluation entry points use paths relative to the cloned repository (`scripts/cnss_paths.py`). Some other scripts still contain laboratory-specific paths. Qwen JSON-offset and shared-guideline SFT are separate evaluation configurations.

### Reproducibility failures

- You followed `REPRODUCIBILITY.md` and did not obtain the committed CSV cell (for example JobBERT_3M_v4 typed exact **0.433118** after jieba snap).
- Include OS, Python version, `jieba` version, and whether `output/` or `data/frozen_preds/` was used.
- Direct scoring of `jobbert_3m_v4.jsonl` without jieba boundary alignment yields approximately 0.255. To reproduce the hybrid-reference result, follow the corresponding preprocessing steps in the evaluation guide.

### Model-card corrections

- Errors in `release/huggingface-model/README.md` (architecture, licence, intended use).
- Hub model cards stay `license: other` (research-use of training text is confirmed; not CC-BY; see `LICENSE`).

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
- Frozen reference files are identified by SHA-256. A rebuilt file must match the archived checksum to serve as the same reference.
- Concept Accuracy, Time-OOD, and English six-dataset SRICL tables belong to a separate project.
- A public code of conduct has not been added yet.

---

## Licence of contributions

Proposed software licence: **Apache-2.0** (`LICENSE`). Patches to the scorer, advertised scripts, and documentation are contributions under that grant once the corresponding author confirms it. Do not upload new advertisement text. Dataset wording is **not** CC-BY.
