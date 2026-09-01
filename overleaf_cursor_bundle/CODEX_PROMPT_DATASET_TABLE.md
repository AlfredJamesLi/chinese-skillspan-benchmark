# Codex / Overleaf — replace corpus Table 2 + related figures/text

**Overleaf:** https://www.overleaf.com/project/68fe17a53e53a7f800e4f2b4  
**This is a patch on the current PeerJ CS draft.** Do **not** re-run `CODEX_PROMPT_ALL.md`. Do **not** touch IEEE Access / SRICL.

Copy these files from the server bundle into the Overleaf Git root (same folder as `main.tex`) **before** pasting the prompt:

| Server path | Overleaf path |
|---|---|
| `overleaf_cursor_bundle/tex/skillspan_style_dataset.tex` | `tex/skillspan_style_dataset.tex` |
| `overleaf_cursor_bundle/tex/skillspan_style_dataset_old_split.tex` | `tex/skillspan_style_dataset_old_split.tex` |
| `overleaf_cursor_bundle/tex/skillspan_style_related.tex` | `tex/skillspan_style_related.tex` |
| `overleaf_cursor_bundle/tex/skillspan_style_figures.tex` | `tex/skillspan_style_figures.tex` |
| `overleaf_cursor_bundle/figures/fig_violin_span_length.pdf` | `figures/fig_violin_span_length.pdf` |
| `overleaf_cursor_bundle/tables/skillspan_style/dataset_stats_repartition_v1.csv` | `tables/skillspan_style/dataset_stats_repartition_v1.csv` |
| `overleaf_cursor_bundle/CODEX_PROMPT_DATASET_TABLE.md` | this file |

If `ls tex/skillspan_style_dataset.tex figures/fig_violin_span_length.pdf` fails, **stop** and ask the user to copy the bundle. Do not invent counts.

---

## PROMPT (copy from here)

You are editing the **Chinese-SkillSpan / Chinese Skill Benchmark** Overleaf paper for **PeerJ Computer Science**. This is **not** the IEEE Access / SRICL method paper.

### Start
1. `git status`; `git pull --ff-only`; confirm project `68fe17a53e53a7f800e4f2b4`.
2. Read `.cursor/skills/cnss-overleaf/confirmed-results.md` (section “Dataset table — source-stratified repartition_v1”) and `not-for-paper.md`.
3. Locate the SkillSpan-style corpus table currently titled like “Corpus statistics for Chinese-SkillSpan by split and source” (label `tab:dataset-stats` or equivalent). It still has the **old** source-imbalanced numbers (Train AI 630 + Grad 970 = 1,600 posts; Evaluation 2,601 sentences; Cloud/Public missing from train; Grad missing from evaluation).
4. Produce a short conflict table, then patch **one pass**. Show the full `git diff`. **Do not commit or push.**

### Hard rules
- Replace the **corpus statistics table** with `tex/skillspan_style_dataset.tex` **verbatim**. Do not retype numbers. Every cell is already counted from `data/repartition_v1/{train,dev,test}.jsonl` (seed 7).
- Move the **old** source-imbalanced table into the appendix using `tex/skillspan_style_dataset_old_split.tex` (`tab:dataset-stats-old`). Do not delete those numbers; they remain provenance for the V4 hybrid F1 table.
- **Keep the paper main F1 gold = V4 hybrid 2601.** Abstract / main results stay JobBERT 1M/3M v4 exact **0.4272 / 0.4331** and frozen ChatGPT dump+jieba exact **0.2854** / relaxed **0.6249**.
- Do **not** replace those F1 cells with repartition_v1 RoBERTa-wwm **0.3115** / 3-seed mean **0.3070** / Qwen SOP **0.1473**. Different split, silver-draft gold.
- Do **not** call Evaluation 4,222 “human Gold”, “Doccano Gold”, or “completed SOP”. Caption already says **pre-release silver drafts pending human adjudication**.
- Do **not** change PDF Table 3 paper S-F1 cells (0.6700 … 0.2130). Do **not** change IAA (n=100, strict F1 0.532) — that is Gold-era, not this corpus table. The table you are replacing is the **dataset-statistics** table, not IAA.
- Do **not** invent F1. Do not add ChatGPT/Claude/Kimi/DeepSeek rows on the 4,222 split (old dumps cover only 702/4222).
- Venue remains **PeerJ Computer Science**. No DASFAA. No English six-dataset SRICL tables.
- Dev Public **# L = 0** is a real count. Write 0, not n/a.

### Authoritative counts (must match the tex; comma as thousands separator)

**Train (draft)** — 1,427 posts / 16,350 sentences / 589,618 tokens. Skill (S+T) 17,027; Knowledge (L+K) 6,964; L 287; K 6,677; S 11,719; T 5,308; overlap 0.

| | AI | Cloud | Public | Grad | Total |
|---|---:|---:|---:|---:|---:|
| Posts | 707 | 28 | 12 | 680 | 1,427 |
| Sentences | 7,863 | 318 | 846 | 7,323 | 16,350 |
| Tokens | 289,444 | 11,178 | 38,555 | 250,441 | 589,618 |
| S+T | 10,307 | 285 | 101 | 6,334 | 17,027 |
| L+K | 4,756 | 170 | 232 | 1,806 | 6,964 |
| L | 100 | 2 | 2 | 183 | 287 |
| K | 4,656 | 168 | 230 | 1,623 | 6,677 |
| S | 7,801 | 216 | 63 | 3,639 | 11,719 |
| T | 2,506 | 69 | 38 | 2,695 | 5,308 |

**Dev (draft)** — 194 posts / 2,268 sentences / 81,752 tokens. S+T 2,406; L+K 926; L 58; K 868; S 1,643; T 763.

| | AI | Cloud | Public | Grad | Total |
|---|---:|---:|---:|---:|---:|
| Posts | 91 | 4 | 4 | 95 | 194 |
| Sentences | 943 | 32 | 230 | 1,063 | 2,268 |
| Tokens | 34,872 | 1,308 | 9,940 | 35,632 | 81,752 |
| S+T | 1,461 | 21 | 23 | 901 | 2,406 |
| L+K | 555 | 15 | 57 | 299 | 926 |
| L | 13 | 1 | 0 | 44 | 58 |
| K | 542 | 14 | 57 | 255 | 868 |
| S | 1,103 | 19 | 22 | 499 | 1,643 |
| T | 358 | 2 | 1 | 402 | 763 |

**Evaluation (pre-release)** — 379 posts / 4,222 sentences / 155,257 tokens. S+T 4,385; L+K 1,697; L 58; K 1,639; S 2,977; T 1,408.

| | AI | Cloud | Public | Grad | Total |
|---|---:|---:|---:|---:|---:|
| Posts | 172 | 8 | 4 | 195 | 379 |
| Sentences | 1,908 | 123 | 265 | 1,926 | 4,222 |
| Tokens | 74,113 | 4,284 | 11,770 | 65,090 | 155,257 |
| S+T | 2,643 | 81 | 32 | 1,629 | 4,385 |
| L+K | 1,135 | 65 | 40 | 457 | 1,697 |
| L | 17 | 5 | 1 | 35 | 58 |
| K | 1,118 | 60 | 39 | 422 | 1,639 |
| S | 1,978 | 54 | 25 | 920 | 2,977 |
| T | 665 | 27 | 7 | 709 | 1,408 |

**Unlabeled DAPT** unchanged: 1,000,000 (AI 409,400 + Grad 590,600); 3.2M mix (AI 1,310,080 + Grad 1,889,920). Cloud/Public = n/a.

SHA256: train `90a70147…ca6f8e1e`; dev `a83915eb…93088f09`; test `fdbcf681…19969fa92`.

### What to change in the body (English, same register; 1–2 sentences each)

Search `main.tex` and any included files for these **old claims** and rewrite them. Do not leave contradictions.

1. **Split design.** Old: graduate recruitment only in train; Cloud and public-sector only in evaluation; source-disjoint test. New: source-stratified post-level split (seed 7, frozen before any model F1) puts AI / Cloud / Public / Grad into train, dev, **and** evaluation (quotas: Public 12/4/4 posts, Cloud 28/4/8, AI and Grad 70/10/20).
2. **Sentence headlines.** Replace 17,460 / 2,143 / 3,237 or 2,601 as the **corpus table** totals with **16,350 / 2,268 / 4,222**. Keep 2,601 wherever you describe the **V4 hybrid F1 gold** (same Gold v2 IDs; SOP-CWS + 980 SimHuman; jieba). One paper may name both numbers if you say which protocol each belongs to.
3. **Related-work size cell.** Input or paste `tex/skillspan_style_related.tex`. This work = 16,350 train sent.; 4,222 eval sent. (silver draft footnote); Gold v2 remains 2,601 IDs.
4. **Violin figure.** Replace `figures/fig_violin_span_length.pdf` and use the caption in `tex/skillspan_style_figures.tex` (all four sources in every labelled split; silver drafts). Delete captions that say “Dev is AI-only” or “Grad appears in train only”.
5. **Keep** `fig_v4_performance.pdf` as the main **results** figure (0.4331 / 0.6249). Keep Gold v2 win-rate / pred-length / F1-by-length in the appendix. Do not retitle the V4 F1 figure as 4,222-split results.
6. **If a footnote already says** “Appendix Table 31 reports a source-stratified split”: invert it. The **main** corpus table is now the stratified split; Table 31 / `tab:dataset-stats-old` is the original source-imbalanced split.
7. **Methods (2–4 sentences).** After the V4 hybrid paragraph, add: the source-stratified re-split was built to mix the four sources because the old split kept 应届生招聘 in train only. Evaluation labels on 4,222 are LSKT v4 character silver drafts, not human adjudication. Human SOP on the original 980 LLM-disagreement sentences is underway and is **not** used in this table. Encoder checkpoints trained on the old split leak 3,163 old-train IDs into the new test, so those checkpoints were not reused for the appendix F1 on 4,222.
8. **Abstract.** You may mention the corpus size 16,350 / 4,222 **if** you also say evaluation labels are silver drafts. Do **not** put RoBERTa-wwm 0.3070 in the abstract. Abstract F1 remains 0.4331 / 0.6249.

### Do not do
- Rewrite the main **results** table onto 4,222 silver-draft F1.
- Claim 980 SimHuman or this night run is completed human SOP.
- Mix 0.3070 with 0.4331 or 0.6365 in one ranking sentence.
- Change IAA Table numbers.
- Leave “Dev is AI-only” / “Grad in train only” / “test is source-disjoint” as if they still describe the corpus table.

### After edits
List files touched and the diff. Confirm: corpus table totals 16,350 / 2,268 / 4,222; abstract still has 0.4331 / 0.6249; IAA unchanged; old 17,460/2,601 table is appendix-only. No commit.

## End prompt
