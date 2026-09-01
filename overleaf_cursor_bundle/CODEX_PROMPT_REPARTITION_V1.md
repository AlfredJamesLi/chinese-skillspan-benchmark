# Codex / Overleaf — repartition_v1 appendix (after Slurm 50733)

**Overleaf:** https://www.overleaf.com/project/68fe17a53e53a7f800e4f2b4  
**This is a patch on the current PeerJ CS draft.** Do **not** re-run `CODEX_PROMPT_ALL.md`. Do **not** touch IEEE Access / SRICL.

Copy into the Overleaf repo root (if not already there): this file, `tables/repartition_v1_night.csv`, `tables/repartition_v1_stl.csv`, and the updated `.cursor/skills/cnss-overleaf/confirmed-results.md` / `not-for-paper.md`.

---

## PROMPT (copy from here)

You are editing the **Chinese-SkillSpan / Chinese Skill Benchmark** Overleaf paper for **PeerJ Computer Science**. This is **not** the IEEE Access / SRICL method paper.

### Start
1. `git status`; `git pull --ff-only`; confirm this is project `68fe17a53e53a7f800e4f2b4`.
2. Read `HANDOVER_OVERLEAF.md` if present, plus `.cursor/skills/cnss-overleaf/confirmed-results.md` (section “source-stratified repartition_v1”) and `not-for-paper.md`.
3. Locate `main.tex`, the current **main results** table (V4 hybrid 2601; JobBERT 3M exact **0.4331**), Table 1 (train 17460 / dev 2143 / test 3237), and existing appendices.
4. Produce a short conflict table, then patch **one pass**. Show the full `git diff`. **Do not commit or push.**

### Hard rules
- **Keep the paper main gold = V4 hybrid 2601.** Abstract / main table stay JobBERT 1M/3M v4 exact **0.4272 / 0.4331** and frozen ChatGPT dump+jieba exact **0.2854** / relaxed **0.6249**.
- Do **not** replace those cells with repartition_v1 numbers. Do **not** put RoBERTa-wwm **0.3115** or 3-seed mean **0.3070** in the abstract.
- Do **not** rank 0.3115 against 0.4331 or Gold v2 ChatGPT **0.6365**. Different split, different gold provenance.
- Do **not** call repartition_v1 test “human Gold”, “Doccano Gold”, or “completed SOP on 980”. The 980 human labels are **in progress** and must not be described as done.
- Do **not** change PDF Table 3 paper S-F1 cells. Do **not** change Table 2 IAA. Do **not** change Table 1 headline counts unless you add a footnote that those counts are the **old** source-disjoint split.
- `score_official.json` may say `eligible_for_main_table: true`; that only means ID alignment. It does **not** authorize a main-table swap.
- Round to 4 decimals. Use only the tables below. Do not invent F1. No commercial-API rows on the new test (old dumps cover only 702/4222).
- Venue remains **PeerJ Computer Science**. No DASFAA. No English six-dataset SRICL tables.

### What to add (appendix + one Methods sentence)

**Methods (2–4 sentences, English, same register).** After the V4 hybrid paragraph, add that a **source-stratified re-split** (seed 7; frozen before any model F1) was built to mix 人工智能招聘 / 应届生招聘 / 阿里云 / 事业单位 into train, dev, and test, because the old split kept 应届生招聘 in train only and made test source-disjoint. Counts: train **16350** sentences (1427 posts), dev **2268** (194), test **4222** (379). Test labels on this split are **LSKT v4 character silver drafts**, not human adjudication. Encoder checkpoints trained on the old split leak **3163** old-train IDs into the new test, so those checkpoints were **not** reused. Human SOP on the original 980 LLM-disagreement sentences is underway and is **not** used in the numbers below.

**Appendix table A — joint CRF on repartition_v1** (caption must say: silver-draft gold, `cnss-lskt-1.2.0`, n=4222, not human Gold, not comparable to V4 hybrid 0.4331). CSV: `tables/repartition_v1_night.csv`.

| System | seed 42 exact | 123 | 2026 | 3-seed mean exact | 3-seed mean relaxed |
|---|---:|---:|---:|---:|---:|
| JobBERT-zh 1M + CRF | 0.2985 | 0.2989 | 0.2996 | 0.2990 | 0.5324 |
| JobBERT-zh 3M + CRF | 0.2921 | 0.2868 | 0.2886 | 0.2892 | 0.5280 |
| RoBERTa-wwm-ext + CRF | 0.3060 | 0.3035 | 0.3115 | 0.3070 | 0.5309 |
| Qwen2.5-14B-Instruct SOP extract | — | — | — | 0.1473 | 0.3308 |

One sentence: on this silver-draft split RoBERTa-wwm leads typed exact; Qwen Instruct SOP extract is weaker (0.1473). Do not call this a new SOTA versus the V4 hybrid table.

Optional per-source footnote (typed exact, RoBERTa-wwm seed 2026): AI 0.3043 / Grad 0.3183 / Cloud 0.4930 / Public 0.0412. Public is sparse; do **not** write Time-OOD.

**Appendix table B — STL vs joint** (JobBERT 1M seed 42; same gold). CSV: `tables/repartition_v1_stl.csv`. Caption: combined = greedy non-overlap union (119 overlaps dropped). Combined exact **0.2905** does **not** beat joint **0.2985**. Stay in appendix.

| System | L | K | S | T | typed exact | typed relaxed |
|---|---:|---:|---:|---:|---:|---:|
| Joint CRF 1M seed 42 | 0.4628 | 0.3032 | 0.2655 | 0.3536 | 0.2985 | 0.5331 |
| STL combined | 0.5043 | 0.2668 | 0.2604 | 0.3660 | 0.2905 | 0.5155 |

Do not put single-head micro (STL-S 0.1651 etc.) in the same grid as type F1 without saying those micros are versus **all** gold types.

### Do not do
- Rewrite Table 1 to 16350/2268/4222 as the paper’s primary split.
- Claim the 980 SimHuman overlay or this night run is completed human SOP.
- Add ChatGPT/Claude/Kimi/DeepSeek rows on the new test.
- Claim JobBERT 3M is best on this split (it is not; RoBERTa-wwm is).
- Mix 0.3070 with 0.4331 or 0.6365 in one ranking sentence.

### After edits
List files touched and the diff. Confirm abstract still has 0.4331 / 0.6249, Table 3 S-F1 unchanged, and the new numbers are appendix-only. No commit.

## End prompt
