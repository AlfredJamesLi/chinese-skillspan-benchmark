# Codex / local Cursor prompt — SOP v4 / jieba diagnostic table

**Superseded.** Paste [`CODEX_PROMPT_ALL.md`](CODEX_PROMPT_ALL.md) instead. This file is kept for history.

CSV: `tables/sop_v4_cws_diagnostic.csv` (copy from this bundle). Numbers: `.cursor/skills/cnss-overleaf/confirmed-results.md` section “Diagnostic — LSKT v4 SOP / jieba CWS”.

---

## PROMPT (copy from here)

You are editing the **Chinese-SkillSpan** Overleaf paper. Not IEEE Access / SRICL.

### Start
1. `git status`; `git pull --ff-only`; confirm this is the Chinese-SkillSpan Overleaf clone.
2. Read `HANDOVER_OVERLEAF.md`, `.cursor/skills/cnss-overleaf/confirmed-results.md`, `.cursor/skills/cnss-overleaf/not-for-paper.md`.
3. Add **one diagnostic table** (appendix or encoder-ablation subsection). Show full `git diff`. **Do not commit.**

### Hard rules
- Keep PDF Table 3 paper S-F1 cells unchanged.
- Do **not** add any row below to the Gold v2 unique-first LLM table, the encoder 3-seed ranking, or the abstract SOTA sentence.
- Do **not** claim JobBERT-zh beats ChatGPT (0.6365 typed on Gold v2).
- Caption must name **train silver**, **decode**, and **test gold**. Round to 4 decimals. Do not invent cells.

### Table to add

Caption (use this meaning, English as in the rest of the paper):  
Diagnostic JobBERT-zh CRF scores under LSKT v4 SOP silver and jieba CWS snap. Official test gold remains Gold v2 unique-first (2601 IDs). Rows that use SOP rule or SOP-CWS silver as test gold are same-rule consistency checks and are **not** comparable to ChatGPT 0.6365.

| Pred | Train silver | Decode | Test gold | typed exact | IoU≥0.5 |
|---|---|---|---|---:|---:|
| JobBERT 1M | goldstyle v3 | raw | Gold v2 | 0.1224 | — |
| JobBERT 1M | SOP v4 | raw | Gold v2 | 0.1079 | 0.3320 |
| JobBERT 3M | SOP v4 | raw | Gold v2 | 0.1104 | 0.3404 |
| JobBERT 1M | SOP v4 | jieba post-hoc | Gold v2 | 0.1454 | 0.3411 |
| JobBERT 3M | SOP v4 | jieba post-hoc | Gold v2 | 0.1479 | 0.3470 |
| JobBERT 1M | SOP v4 | raw | SOP rule silver | 0.3170 | 0.5663 |
| JobBERT 3M | SOP v4 | raw | SOP rule silver | 0.3229 | 0.5624 |
| JobBERT 1M | SOP v4 | jieba post-hoc | SOP rule silver | 0.2609 | 0.5835 |
| JobBERT 1M | SOP v4 | jieba post-hoc | SOP-CWS silver | 0.4278 | 0.5960 |
| JobBERT 3M | SOP v4 | jieba post-hoc | SOP-CWS silver | 0.4341 | 0.5884 |

Two sentences of discussion (no extra F1):
1. Training on SOP v4 silver **lowers** official Gold v2 typed exact relative to goldstyle v3 (0.1079 / 0.1104 vs 0.1224).
2. 0.3170 and ~0.43 measure agreement with SOP silver (train≈test same rule, or both sides jieba-snapped) and must not be read as official test performance.

Do not mention the still-running CWS retrain as a finished F1.

### After edits
List files touched, confirm Table 3 and Gold v2 LLM cells were not changed.

## End prompt
