# Codex / Overleaf — Data Availability links only

**Overleaf:** https://www.overleaf.com/project/68fe17a53e53a7f800e4f2b4  
**This file is a link-only paste (2026-09-04).**  
Do **not** re-run `CODEX_PROMPT_ALL.md`. Do **not** retouch Human-200 tables. **Do not commit or push.**

Copy this file into the Overleaf repo root if missing, then paste **PROMPT** below.

---

## PROMPT (copy from here)

You are editing the **Chinese-SkillSpan / Chinese Skill Benchmark** Overleaf paper for **PeerJ Computer Science**. This is **not** IEEE Access / SRICL / DASFAA.

1. `git pull --ff-only`. Confirm this is the Chinese-SkillSpan Overleaf clone.
2. Read `HANDOVER_OVERLEAF.md` and `.cursor/skills/cnss-overleaf/not-for-paper.md`.
3. Search **every** `.tex` / `.bib` / `.md` in this project (including comments, footnotes, abstract, introduction, conclusion, acknowledgements, Data Availability, supplementary notes) for resource URLs.
4. Patch **links and availability wording only**. Show the full `git diff`. **Do not commit. Do not push.**

### Hard rules

- Venue remains **PeerJ Computer Science**. No DASFAA.
- **Do not change any F1, P, R, n, SHA-256, seed, or table cell.** Abstract SOTA stays JobBERT 3M v4 typed exact **0.4331**; ChatGPT (`gpt-4o`) dump+jieba exact **0.2854** / relaxed **0.6249**.
- Do **not** write overlay **0.3884**, n=200 JobBERT **0.1271**, or Gold v2 ChatGPT **0.6365** into the abstract.
- Do **not** invent a Hugging Face **dataset** URL, this paper’s arXiv id, or a PeerJ article URL. Use the Zenodo DOIs below exactly.
- Do **not** use sister-paper identifiers `2604.21525` or `2604.23009` as this paper’s preprint.
- Delete Concept Accuracy / Time-OOD / ESCO concept-ID claims **only if they appear in the same sentences you are already rewriting for URLs**. Do not start a protocol rewrite.
- Model public name: **JobBERT-zh** (also “Chinese JobBERT”). Hugging Face id: `AlfredJames/jobbert-zh`.
- Corresponding author (if a footnote already exists): Xiangyu Zhao, `xianzhao@cityu.edu.hk`. Do not invent affiliations.
- Official public URLs are **GitHub + Hugging Face + Zenodo**. Do **not** send reviewers through Google Sites, Google Drive, Baidu Netdisk, or any other landing page.

### Allowed URLs (use exactly these)

| Resource | URL | Status |
|---|---|---|
| Code, splits, gold files, handbooks, scorer | https://github.com/AlfredJamesLi/chinese-skillspan-benchmark | **public** (verified 2026-09-04) |
| Versioned GitHub Release | https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/releases/tag/v0.1.1 | exists; commit `0824df0` |
| JobBERT-zh (encoder + `crf/best.pt`) | https://huggingface.co/AlfredJames/jobbert-zh | **public** (verified 2026-09-04) |
| Zenodo version DOI | https://doi.org/10.5281/zenodo.22288338 | **minted** (`v0.1.1`; record https://zenodo.org/records/22288338) |
| Zenodo concept DOI | https://doi.org/10.5281/zenodo.22288337 | all versions |
| Hugging Face dataset | *omit; do not invent* | not created |
| This paper’s arXiv / PeerJ article | *omit or keep existing TBD* | unknown |

### Forbidden URLs (remove or do not add)

- https://sites.google.com/view/cn-skillspan-resources
- any `drive.google.com` / `docs.google.com` file as the archive
- any Baidu / 网盘 link as the public archive
- any claim that the Sites page is the version of record

That Sites page is stale (it still says ESCO-Grounded / SKTL / ESCO concept IDs / `L > S > K > T`). Do **not** cite it, even as a “homepage”.

### Where to patch (search, then edit only hits)

1. **PeerJ Data Availability section** (or the paragraph that PeerJ will copy). This is the main edit.
2. Abstract / introduction / conclusion sentences that say “data and code are publicly available” but give a Sites / Drive URL, or give **no** URL.
3. Footnotes under Table 1 or Methods that point to a project page.
4. A “Resources / Code / Data” URL list if one exists.
5. Bibliography or `@misc` entries whose `url` / `howpublished` is the Sites page.
6. Acknowledgements only if they currently advertise the Sites page.

If a location already has the GitHub or Hugging Face URL and nothing else is wrong, leave it.

### Required English wording (same register as the paper; tighten, do not add claims)

**Data Availability (use this, or the closest existing heading):**

> The Chinese-SkillSpan dataset, annotation guidelines, predefined data splits, and documentation are available at https://doi.org/10.5281/zenodo.22288338 (version v0.1.1; concept DOI https://doi.org/10.5281/zenodo.22288337). The source code, preprocessing scripts, and evaluation tools are available at https://github.com/AlfredJamesLi/chinese-skillspan-benchmark. The pretrained JobBERT-zh model, tokenizer, configuration files, and model card are available at https://huggingface.co/AlfredJames/jobbert-zh. Redistribution of original job-advertisement wording remains subject to the source platforms’ terms.

If the manuscript already has a sentence about `human_gold_page1_200.jsonl` and the remaining 780 sentences, **keep that sentence**. Point the file to the **same GitHub repository**, not to Sites / Drive / Zenodo-as-if-it-existed.

**Do not write:**

- that a Hugging Face **dataset** repo exists;
- that GitHub is still private;
- that the Sites page “documents” the release;
- that the authors chose CC-BY-4.0 (Zenodo’s GitHub hook applied that label by default; do not write it as an author licence decision).

### After edits

List: (a) every old URL you found; (b) files touched; (c) full `git diff`.  
Confirm that no F1 changed and that the Sites URL no longer appears. No commit.
