# Codex / local Cursor prompt — add LSKT v4 SOP (methods only)

**Overleaf:** https://www.overleaf.com/project/68fe17a53e53a7f800e4f2b4  
Paste the block below **after** the Gold v2 table prompt in `CODEX_PROMPT.md` has been applied, or in a follow-up Overleaf chat. Server cannot log into Overleaf.

GitHub copy of the SOP test files: https://github.com/AlfredJamesLi/chinese-skillspan-benchmark  
Canonical SOP test gold: `data/test_lskt_v4_rule_g2ids.jsonl` (2601 Gold-v2 IDs). Official Gold remains `gold_canonical_v2.jsonl`.

---

## PROMPT (copy from here)

You are editing the **Chinese-SkillSpan** Overleaf paper. Not IEEE Access / SRICL.

### Start
1. `git status`; `git pull --ff-only`; confirm Chinese-SkillSpan Overleaf clone.
2. Read `HANDOVER_OVERLEAF.md`, `.cursor/skills/cnss-overleaf/confirmed-results.md`, `.cursor/skills/cnss-overleaf/not-for-paper.md`.
3. Patch **methods / annotation** only for LSKT v4 operational SOP. Show full `git diff`. **Do not commit.**

### Hard rules
- SOP / jieba encoder F1 (0.1079, 0.1454, 0.3170, ~0.43, …) now live in `confirmed-results.md` as a **diagnostic** table. Do **not** put them in Table 3, the abstract, or the Gold v2 unique-first LLM table. After this methods patch, paste `CODEX_PROMPT_DIAGNOSTIC_SOP.md` to add that table.
- **Do not** replace Gold v2 (2601) with SOP silver. Wording: official test gold is still human/Doccano Gold v2; SOP v4 is a **training-label and diagnostic test-silver** protocol.
- **Do not** claim JobBERT-zh beats ChatGPT. **Do not** invent F1. **Do not** write majority-vote (Codex/Doubao/Kimi) as Gold.
- Keep PDF Table 3 paper S-F1 cells unchanged.

### Methods text to add (no F1)

Add a short operationalization subsection (or tighten the existing LSKT span paragraph):

- Labels remain **L / K / S / T** (not collapsed at annotation time). Optional eval projection: L+K→KNOWLEDGE, S+T→SKILL.
- Span = contiguous original substring; complete mention (no mid-word cuts such as 支持服); prefer **2–8 tokens**; do not tag a whole 岗位职责 clause as one S.
- 熟悉 / 掌握 / 精通 / 了解 mark **the object only**.
- 报名 / 体检 / 公示 / 福利 / 鸡汤 → empty sentence.
- Flat, non-overlapping spans.

One sentence: encoder CRF experiments may train on SOP-rewritten silver (`train_lskt_v4_silver`) and, as a **consistency check only**, score against SOP-rewritten test silver on the same 2601 Gold v2 IDs; the reported main-table metric remains typed exact F1 on Gold v2.

If the draft currently says encoder F1 is only ~0.12, keep that as the **Gold v2 goldstyle** number. SOP/CWS F1 go only in the diagnostic table (`CODEX_PROMPT_DIAGNOSTIC_SOP.md`).

### After edits
List files touched, diff, and confirm Table 3 / Gold v2 F1 tables were not changed.

## End prompt
