# Codex / Overleaf — title, abstract, keywords, corresponding email

**Overleaf:** https://www.overleaf.com/project/68fe17a53e53a7f800e4f2b4  
**This file is a metadata paste (author-supplied 2026-09-04).**  
Do **not** re-run `CODEX_PROMPT_ALL.md`. Do **not** retouch result tables. **Do not commit or push.**

Copy this file into the Overleaf repo root if missing, then paste **PROMPT** below.

If Data Availability URLs are still Sites / Drive / missing, paste `CODEX_PROMPT_DATA_AVAILABILITY.md` in a **separate** pass after this one.

---

## PROMPT (copy from here)

You are editing the **Chinese-SkillSpan / Chinese Skill Benchmark** Overleaf paper for **PeerJ Computer Science**. This is **not** IEEE Access / SRICL / DASFAA.

1. `git pull --ff-only`. Confirm this is the Chinese-SkillSpan Overleaf clone.
2. Read `HANDOVER_OVERLEAF.md` and `.cursor/skills/cnss-overleaf/not-for-paper.md`.
3. Patch **title, author block, affiliations, corresponding-author email, abstract, and keywords only**. Show the full `git diff`. **Do not commit. Do not push.**

### Hard rules

- Venue remains **PeerJ Computer Science**. No DASFAA.
- **Do not change any F1, P, R, n, SHA-256, seed, or table cell.**
- Do **not** write overlay **0.3884**, n=200 JobBERT **0.1271**, or Gold v2 ChatGPT **0.6365** into the new abstract.
- Do **not** add F1 to this abstract. The authors now want a **provisional** abstract (evaluation gold still under human adjudication).
- Do **not** invent a Zenodo DOI, a Hugging Face dataset URL, this paper’s arXiv id, extra emails, or extra affiliations.
- Do **not** use sister-paper identifiers `2604.21525` or `2604.23009`.
- **ESCO-informed taxonomy** / **ESCO-derived LSKT inventory** means the four types L / K / S / T. Do **not** add ESCO concept IDs, Concept Accuracy, Time-OOD, or `L > S > K > T`.
- Official public URLs: GitHub + Hugging Face only. Do **not** add https://sites.google.com/view/cn-skillspan-resources.

### Title (exact)

`Chinese-SkillSpan: A Benchmark for Competency Span Extraction from Chinese Job Advertisements`

### Authors and affiliations (exact)

Keep this **order**. Do not add or drop names.

| Author | Affiliation marks | Notes |
|---|---|---|
| Guojing Li | 1, 2 | equal contribution (†) |
| Zichuan Fu | 2 | equal contribution (†) |
| Junyi Li | 2 | |
| Wenlin Zhang | 2 | |
| Kaifeng Guo | 2 | |
| Jinning Yang | 2 | |
| Jingtong Gao | 2 | |
| Xiangyu Zhao | 2 | corresponding |

1. Renmin University of China  
2. City University of Hong Kong  

Corresponding author: Xiangyu Zhao, `xianzhao@cityu.edu.hk`.  
If the tex already has this block, make it match the table. Do not invent ORCID, extra emails, or a third affiliation.

### Keywords (exact, this order)

1. Chinese JobSkillNER
2. competency span extraction
3. skill extraction
4. Chinese job advertisements
5. benchmark dataset
6. span-level annotation
7. domain-adaptive pretraining
8. large language models
9. ESCO-informed taxonomy

Replace any older keyword list (JobSkillNER-only, SKTL, ESCO concept IDs, etc.) with this list.

### Abstract (exact English; complete the unfinished “maintained at” clause)

> Online job advertisements can reveal changing skill demand only when competency mentions are recoverable as auditable text spans. Chinese lacks a large resource that combines explicit span-boundary rules with coverage of different recruitment genres. We present Chinese-SkillSpan, a corpus of 22,840 sentences from four Chinese recruitment sources. It uses a flat, ESCO-derived inventory of language skills and knowledge, knowledge, skills, and transversal skills and competences (LSKT), with Chinese-specific rules for minimal-complete, non-overlapping spans. Language models propose annotation drafts, but human reviewers retain authority over accepted offsets and types under a shared handbook. The benchmark uses identifier-strict scoring, exact and overlap-tolerant metrics, and source- and length-based analyses. Its evaluation reference is undergoing final human adjudication, so the current results are provisional estimates. The baseline study shows why the resource is challenging: exact extraction changes with Chinese boundary conventions, and accuracy varies across recruitment sources. Taken together, Chinese-SkillSpan contributes a multi-source span resource, a Chinese-specific annotation and evaluation protocol, and a reproducible baseline and diagnostic suite that exposes category, source, and boundary effects. Internal artifact names are confined to the supplementary reproducibility record. Project materials are maintained at https://github.com/AlfredJamesLi/chinese-skillspan-benchmark. The pretrained JobBERT-zh model is available at https://huggingface.co/AlfredJames/jobbert-zh.

Keep `22,840` as written. Do not add 0.4331 / 0.2854 / 0.6249 to this abstract. Those numbers stay in the **results tables** only.

### After edits

List files touched and the full `git diff`. Confirm no table F1 changed. No commit.
