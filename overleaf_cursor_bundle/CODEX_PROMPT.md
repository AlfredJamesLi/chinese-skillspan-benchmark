# Codex / local Cursor prompt — Chinese-SkillSpan Overleaf (2026-08-24)

**Overleaf project (cannot be edited from the GPU server; no Overleaf login here):**  
https://www.overleaf.com/project/68fe17a53e53a7f800e4f2b4  
Git: `https://git.overleaf.com/68fe17a53e53a7f800e4f2b4`

Paste the block below into **Codex** or a **local Cursor** chat whose workspace is the Overleaf Git clone (not IEEE Access / SRICL).

First copy sibling files from `overleaf_cursor_bundle/` into the Overleaf repo **root** (`HANDOVER_OVERLEAF.md`, `AGENTS.md`, `.cursor/`, `tables/`, this prompt).

**Follow-up 1 (methods SOP, no F1 in Table 3):** paste `CODEX_PROMPT_SOP_V4.md`.  
**Follow-up 2 (diagnostic encoder table):** paste `CODEX_PROMPT_DIAGNOSTIC_SOP.md`. Do **not** put 0.3170 / 0.1454 / ~0.43 in Table 3 or next to ChatGPT 0.6365.

---

## PROMPT (copy from here)

You are editing the **Chinese-SkillSpan / Chinese Skill Benchmark** Overleaf paper (DASFAA 2026 dataset paper; LSKT span extraction on Chinese job ads). This is **not** the IEEE Access / SRICL method paper (arXiv 2604.21525). Do not import SkillSpan/Kompetencer/Green/FIJO/Sayfullina/Gnehm tables, SRICL, B8, or A1–A4.

Overleaf project: https://www.overleaf.com/project/68fe17a53e53a7f800e4f2b4

### Start
1. `git status`; `git pull --ff-only`; confirm this is the Chinese-SkillSpan Overleaf clone.
2. Read `HANDOVER_OVERLEAF.md` and `.cursor/skills/cnss-overleaf/confirmed-results.md` in full.
3. Read `.cursor/skills/cnss-overleaf/not-for-paper.md`.
4. Locate the main `.tex` (likely `main.tex` or similar) and current Table 1/2/3.
5. Produce a **conflict table** first: file / current tex value / confirmed value / action (`keep` / `add` / `patch wording` / `delete claim`).
6. Then patch. Show the full `git diff` at the end. **Do not commit or push** until I say so.

### Hard rules
- Write **only** numbers that appear in `confirmed-results.md`. Round to 4 decimals.
- **Do not overwrite PDF Table 3 paper S-F1 cells** (ChatGPT 0.6700, Claude 0.6300, Kimi 0.5700, DeepSeek 0.5130, Qwen 0.2130, JobBERT-skill 0.0045, JobBERT-knowledge 0.0038). Keep them as the published-protocol table (Gold 2676).
- **Add new tables** for Gold v2 unique-first (2601 IDs, scorer `cnss-lskt-1.2.0`). Caption must name Gold v2 + unique-first + typed exact micro F1. Do not pretend Gold v2 typed F1 is the same number as PDF S-F1.
- Claude/Kimi Gold v2 rows are **incomplete** (missing 98 / 293 IDs). Mark them; do not present as complete main-table results.
- Qwen paper 0.2130 is unreproducible under Gold v2 (typed 0.0791). Do not tune text to defend 0.2130 as Gold v2.
- Encoder JobBERT-zh CRF is a **weak baseline** (~0.12 typed F1). Never claim it beats ChatGPT (0.6365 typed).
- listed-mix 1M DAPT **lost** (0.1201 vs baseline 0.1224). Do not add a listed-3M result. Domain-mix 1M seed 42 is 0.1234 (+0.0010 vs 1M); 3-seed mean 0.1269 is **below** JobBERT 1M 0.1288. Do not claim domain-mix wins or fixes 事业单位 (0.0287 vs ChatGPT 0.7032).
- Encoder 3-seed means are confirmed for JobBERT 1M (0.1288), domain-mix 1M (0.1269), and 3M ckpt65000 (0.1258). Do **not** invent a RoBERTa-wwm v3 3-seed mean (seed 123 still running).
- **Delete or rewrite** Concept Accuracy, Time-OOD, and ESCO concept-ID linking claims. Allowed wording: “ESCO-derived LSKT span extraction”. Per-domain table is an **Industry-OOD proxy** (source_domain on Gold v2), not a true held-out industry/time split. No `year` field.
- Do not cite `*.eval_ner.json` or English JobBERT ~0.46.

### Tables to add or refresh (numbers already in confirmed-results.md)

**A. Keep Table 1** (train 17460 / dev 2143 / test 3237). Optionally footnote: raw Gold 2676 rows vs canonical unique Gold 2601.

**B. Keep Table 2 IAA** (n=100): strict F1 0.532; relaxed 0.624; κ 0.554.

**C. Keep PDF Table 3 paper S-F1** as-is (protocol Gold 2676).

**D. Add Gold v2 unique-first table**

| Model | typed exact | collapsed exact | typed relaxed (IoU≥0.5) | note |
|---|---:|---:|---:|---|
| ChatGPT | 0.6365 | 0.6403 | 0.7221 | complete |
| DeepSeek | 0.1327 | 0.3569 | 0.1798 | complete |
| Qwen | 0.0791 | 0.1075 | 0.1272 | complete; gap vs paper 0.2130 |
| JobBERT-skill | 0.0000 | 0.0045 | 0.0000 | complete |
| JobBERT-knowledge | 0.0000 | 0.0037 | 0.0000 | complete |
| Claude | 0.2570 | 0.2952 | 0.3789 | incomplete, −98 IDs |
| Kimi | 0.1651 | 0.3349 | 0.2130 | incomplete, −293 IDs |

**E. Add per-domain typed exact F1** (Gold v2; n=1407 / 457 / 737)

| System | 人工智能招聘 | 阿里云公开数据集 | 事业单位招聘 |
|---|---:|---:|---:|
| ChatGPT | 0.6489 | 0.5650 | 0.7032 |
| DeepSeek | 0.1392 | 0.1293 | 0.0805 |
| Qwen | 0.0887 | 0.0646 | 0.0207 |
| JobBERT 3M ckpt65000 | 0.1323 | 0.1259 | 0.0150 |
| JobBERT 1M | 0.1287 | 0.1332 | 0.0181 |
| listed mix 1M | 0.1282 | 0.1240 | 0.0153 |
| domain-mix 1M (seed 42) | 0.1276 | 0.1372 | 0.0287 |
| RoBERTa-wwm v3 | 0.1242 | 0.1191 | 0.0115 |

One sentence in the discussion: encoder collapse on 事业单位 (~0.015–0.029; domain-mix seed 42 is 0.0287) vs ChatGPT 0.7032 on that domain.

**F. Add encoder ranking table** (Gold v2 typed exact, seed 42)

Best seed 42: domain-mix 1M **0.1234**; JobBERT 3M ckpt65000 **0.1233**; JobBERT 1M baseline **0.1224**; listed mix 1M **0.1201** (Δ −0.0023, do not scale listed to 3M); RoBERTa-wwm v3 **0.1156**.

**G. Add encoder 3-seed table** (typed exact; sample std)

| Run | seed 42 | seed 123 | seed 2026 | mean | std |
|---|---:|---:|---:|---:|---:|
| JobBERT 1M | 0.1224 | 0.1292 | 0.1348 | **0.1288** | 0.0062 |
| domain-mix 1M | 0.1234 | 0.1280 | 0.1294 | 0.1269 | 0.0031 |
| JobBERT 3M ckpt65000 | 0.1233 | 0.1295 | 0.1246 | 0.1258 | 0.0033 |
| RoBERTa-wwm v3 | 0.1156 | — | — | — | — |

Leave RoBERTa mean as `---`. Do not claim domain-mix beats 1M on the 3-seed mean.

CSV copies for `\input` / booktabs conversion are in `tables/` of this repo.

### Abstract / intro / conclusion
Patch only if they currently claim Concept Accuracy, Time-OOD, encoder SOTA, or ESCO ID linking. Keep ChatGPT as the strongest complete LLM under Gold v2. Keep encoder as a Chinese DAPT+CRF baseline.

### If a third number appears
Stop and report tex vs confirmed-results vs PDF. Do not average them.

### After edits
List: files touched, conflict table, full diff, remaining TODOs (RoBERTa 3-seed mean, Claude/Kimi fill). No commit.

## End prompt
