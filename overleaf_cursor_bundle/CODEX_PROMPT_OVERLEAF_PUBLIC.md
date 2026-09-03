# Codex / Overleaf — ONE paste (public metadata + Data Availability)

**Overleaf:** https://www.overleaf.com/project/68fe17a53e53a7f800e4f2b4  
**Use this file only (2026-09-04).** Do **not** also paste `CODEX_PROMPT_METADATA.md` or `CODEX_PROMPT_DATA_AVAILABILITY.md` in the same chat. Do **not** re-run `CODEX_PROMPT_ALL.md`. Do **not** retouch result tables. **Do not commit or push.**

Copy this file into the Overleaf repo root if missing, then paste **PROMPT** below.

---

## PROMPT (copy from here)

You are editing the **Chinese-SkillSpan / Chinese Skill Benchmark** Overleaf paper for **PeerJ Computer Science**. This is **not** IEEE Access / SRICL / DASFAA.

1. `git pull --ff-only`. Confirm this is the Chinese-SkillSpan Overleaf clone.
2. Read `HANDOVER_OVERLEAF.md` and `.cursor/skills/cnss-overleaf/not-for-paper.md`.
3. Patch **front matter + Data Availability + stale resource URLs only**. Show the full `git diff`. **Do not commit. Do not push.**

### Hard rules

- Venue remains **PeerJ Computer Science**. No DASFAA.
- **Do not change any F1, P, R, n, SHA-256, seed, or table cell.** JobBERT 3M v4 typed exact **0.4331** and ChatGPT (`gpt-4o`) dump+jieba exact **0.2854** / relaxed **0.6249** stay in the **results tables**.
- Do **not** write overlay **0.3884**, n=200 JobBERT **0.1271**, or Gold v2 ChatGPT **0.6365** into the abstract.
- Replace the abstract with the **author-supplied provisional text below**. Do **not** add F1 to that abstract.
- Do **not** invent a Hugging Face **dataset** URL, this paper’s arXiv id, extra emails, extra affiliations, or ORCID.
- Do **not** use sister-paper identifiers `2604.21525` or `2604.23009`.
- **ESCO-informed taxonomy** / **ESCO-derived LSKT inventory** means the four types L / K / S / T. Do **not** add ESCO concept IDs, Concept Accuracy, Time-OOD, or `L > S > K > T`.
- Official public URLs are **GitHub + Hugging Face + Zenodo** only. Do **not** cite https://sites.google.com/view/cn-skillspan-resources, Google Drive, or Baidu Netdisk.
- Do **not** write that the authors chose CC-BY-4.0 (Zenodo applied that label by default).

### 1. Title (exact)

`Chinese-SkillSpan: A Benchmark for Competency Span Extraction from Chinese Job Advertisements`

### 2. Authors and affiliations (exact)

Keep this **order**. Do not add or drop names.

| Author | Marks | Notes |
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

### 3. Keywords (exact, this order)

Chinese JobSkillNER; competency span extraction; skill extraction; Chinese job advertisements; benchmark dataset; span-level annotation; domain-adaptive pretraining; large language models; ESCO-informed taxonomy.

### 4. Abstract (exact English)

> Online job advertisements can reveal changing skill demand only when competency mentions are recoverable as auditable text spans. Chinese lacks a large resource that combines explicit span-boundary rules with coverage of different recruitment genres. We present Chinese-SkillSpan, a corpus of 22,840 sentences from four Chinese recruitment sources. It uses a flat, ESCO-derived inventory of language skills and knowledge, knowledge, skills, and transversal skills and competences (LSKT), with Chinese-specific rules for minimal-complete, non-overlapping spans. Language models propose annotation drafts, but human reviewers retain authority over accepted offsets and types under a shared handbook. The benchmark uses identifier-strict scoring, exact and overlap-tolerant metrics, and source- and length-based analyses. Its evaluation reference is undergoing final human adjudication, so the current results are provisional estimates. The baseline study shows why the resource is challenging: exact extraction changes with Chinese boundary conventions, and accuracy varies across recruitment sources. Taken together, Chinese-SkillSpan contributes a multi-source span resource, a Chinese-specific annotation and evaluation protocol, and a reproducible baseline and diagnostic suite that exposes category, source, and boundary effects. Internal artifact names are confined to the supplementary reproducibility record. Project materials are maintained at https://github.com/AlfredJamesLi/chinese-skillspan-benchmark. The pretrained JobBERT-zh model is available at https://huggingface.co/AlfredJames/jobbert-zh.

Keep `22,840`. Do not append Zenodo to this abstract unless the current tex already has a “data available at” clause there; the DOI belongs in **Data Availability**.

### 5. Data Availability (use this heading or the closest existing one)

Search every `.tex` / `.bib` for Sites / Drive / missing “publicly available” sentences, then write:

> The Chinese-SkillSpan dataset, annotation guidelines, predefined data splits, and documentation are available at https://doi.org/10.5281/zenodo.22288338 (version v0.1.1; concept DOI https://doi.org/10.5281/zenodo.22288337). The source code, preprocessing scripts, and evaluation tools are available at https://github.com/AlfredJamesLi/chinese-skillspan-benchmark. The pretrained JobBERT-zh model, tokenizer, configuration files, and model card are available at https://huggingface.co/AlfredJames/jobbert-zh. Redistribution of original job-advertisement wording remains subject to the source platforms’ terms.

Allowed URLs only:

| Resource | URL |
|---|---|
| Zenodo version DOI | https://doi.org/10.5281/zenodo.22288338 |
| Zenodo concept DOI | https://doi.org/10.5281/zenodo.22288337 |
| GitHub | https://github.com/AlfredJamesLi/chinese-skillspan-benchmark |
| GitHub Release `v0.1.1` | https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/releases/tag/v0.1.1 |
| JobBERT-zh | https://huggingface.co/AlfredJames/jobbert-zh |

If the manuscript already mentions `human_gold_page1_200.jsonl` and the remaining 780 sentences, **keep that sentence** and point it at the same GitHub repository.

Do **not** invent a Hugging Face dataset repo.

### After edits

List: (a) old URLs found; (b) files touched; (c) full `git diff`.  
Confirm no table F1 changed and that the Sites URL is gone. No commit.
