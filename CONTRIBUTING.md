# Contributing to Chinese-SkillSpan

Thank you for helping improve **Chinese-SkillSpan** and **JobBERT-zh**. Please open an issue at https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/issues. For matters that should not be public, contact the corresponding author, Xiangyu Zhao (`xianzhao@cityu.edu.hk`).

Please do **not** open a pull request that uploads new job-advertisement text.

---

## What to report

Use a short, reproducible description. Include file paths relative to this repository, SHA-256 of gold or prediction files if you have them, the scorer version (`cnss-lskt-1.2.0`), and the exact command you ran.

### Annotation issues

- Disagreement with Handbook B (`B.sop_v4.2.14`): span boundary, type (L / K / S / T), empty-span cases.
- State whether you used Gold v2, the V4 hybrid, the 200-sentence human overlay, or the 150-sentence human reference set. Do not mix protocols in one ticket.
- Quote only the **minimum** span needed to discuss the label. Prefer `id` + token offsets over pasting a full advertisement.

### Data-processing bugs

- Split membership, ID collisions, jieba snap errors, hybrid rewrite changing the frozen SHA-256.
- Attach the command and, if possible, a single-record fixture you created yourself (not scraped ads).

### Code bugs

- Scorer alignment, CRF trainer, evaluation scripts.
- Paper-main scoring, CRF train, and human-reference eval entry points are clone-relative (`scripts/cnss_paths.py`). Other files under `scripts/` may still contain a laboratory absolute root. Human-reference JSON-offset Qwen is not the shared-handbook SFT protocol.

### Reproducibility failures

- You followed `REPRODUCIBILITY.md` and did not obtain the committed CSV cell (for example JobBERT_3M_v4 typed exact **0.433118** after jieba snap).
- Include OS, Python version, `jieba` version, and whether `output/` or `data/frozen_preds/` was used.
- Do not file a bug because direct scoring of `jobbert_3m_v4.jsonl` without jieba snap yields ~0.255 — that behaviour is documented.

### Model-card corrections

- Errors in `release/huggingface-model/README.md` (architecture, licence, intended use).
- Hub model cards stay `license: other` until job-advertisement text rights are confirmed (see `LICENSE`).

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

Proposed software licence: **Apache-2.0** (`LICENSE`). Patches to the scorer, advertised scripts, and documentation are contributions under that grant once the corresponding author confirms it. Do not upload new advertisement text. Dataset wording is **not** CC-BY.
