# Codex consult — Handbook A vs B (no tex edits yet)

**Overleaf:** https://www.overleaf.com/project/68fe17a53e53a7f800e4f2b4  
Paste **this file only**. Do **not** patch `main.tex` in this chat. Return a Methods insertion plan. Wait for `CODEX_PROMPT_ALL.md` before editing.

Copy `overleaf_cursor_bundle/` into the Overleaf repo root if not already there. Read:

- `handbooks/README.md`
- `handbooks/handbook_A_gold_v2.en.md` and `handbooks/handbook_B_sop_v4.en.md`
- `.cursor/skills/cnss-overleaf/confirmed-results.md`
- `.cursor/skills/cnss-overleaf/not-for-paper.md`

Numbers only from `confirmed-results.md`. Ban list: `not-for-paper.md`.

---

## PROMPT (copy from here)

You are advising on **Methods wording** for the Chinese-SkillSpan / Chinese Skill Benchmark paper submitted to **PeerJ Computer Science**. This is **not** the IEEE Access / SRICL method paper. Do not invent F1.

**This chat is consult-only.** `git pull --ff-only`, read `main.tex` (annotation / gold / encoder / evaluation subsections) and the two one-page handbooks. **Do not edit tex, do not commit, do not push.**

### Two handbooks (never merge)

| | Handbook A | Handbook B |
|---|---|---|
| Protocol | **P1** official human Gold v2 | **P2** matched SOP+jieba |
| File | `handbooks/handbook_A_gold_v2.en.md` | `handbooks/handbook_B_sop_v4.en.md` |
| Test gold | `gold_canonical_v2.jsonl` (2601) | hybrid 2601 = 980 SimHuman rule_v4 + 1621 SOP-CWS, jieba both sides |
| Span | Gold-length complete NP (~4–12 tokens; median 4, mean ≈4.9) | short 2–8, no mid-word cuts, mark object of 熟悉 only |
| Headline | ChatGPT typed **0.6365**; JobBERT 1M 3-seed **0.1288** | JobBERT 3M v4 exact **0.4331**; frozen ChatGPT dump+jieba exact **0.2854** / relaxed **0.6249** |

**How Gold was actually made (do not rewrite history):** LLM silver from `prompt_template_rag.py` → `chinese_skillspan` (`@@span##[L|K|S|T]`, *minimal sufficient span*) → light Doccano check → Gold v2. Handbook A describes the **Gold / goldstyle operationalization**, not a word-for-word reprint of that silver API. The original silver API put language **certificates** in **L**; Gold-style / current Gold practice put CET-6 in **K**. Do **not** claim Handbook A = the original silver prompt.

**Handbook B** matches LSKT v4 SOP (`GUIDELINES.md` + SOP extract prompt). The 980 SimHuman overlay is **rule_v4**, not a full human pass under Handbook B. Do **not** overwrite `gold_canonical_v2.jsonl`. Do **not** replace Gold v2 as the official gold.

P2 LLM rows are **frozen old dumps** + jieba (old prompt, new gold). ChatGPT’s drop 0.6365 → 0.2854 is a **span-convention** effect, not a new `gpt-4o` run.

**Forbidden:** one SOTA sentence that compares JobBERT **0.4331** (P2) with ChatGPT **0.6365** (P1). Future Gold v3 would be a **new file** + dual IAA under Handbook B; it does not exist yet.

P0 PDF Table 3 (ChatGPT 0.6700 … Qwen 0.2130) stays frozen.

### Question

Where should Handbook A and Handbook B appear in a PeerJ CS dataset paper, and what must stay out of Methods so reviewers do not treat P2 as a rewrite of official Gold?

Authors currently lean toward: **two short Methods subsections** (A then B) plus **two result tables**, with the English one-pagers also available as Supplemental Information. Critique that, then rank the options.

### Options to rank

**A. Two Methods subsections + two result tables (prior)**  
- Methods: “Official Gold v2 (Handbook A)” then “Matched SOP+jieba protocol (Handbook B)”.  
- Results: Gold v2 table vs matched-protocol table. Abstract: two sentences, one per protocol.  
- English one-pagers: Supplemental Information (or a compact table of contrast examples in Methods).

**B. One merged “annotation guideline” subsection**  
Rewrite A and B as a single evolving SOP. **This erases the Gold history.** Say so if you agree it is misleading.

**C. Handbook B only, Gold v2 as a legacy footnote**  
Treat P2 as the new official gold. **Authors reject this.** Confirm or dissent in one sentence.

**D. Handbooks appendix-only; Methods stays at the old silver-prompt story**  
Reviewers never see why encoder F1 jumps 0.13 → 0.43. Say whether that is acceptable for PeerJ CS.

**E. Paste the Chinese one-pagers into the English PDF**  
Venue is English. Flag this if it is the wrong register.

### Constraints

- Dataset-paper identity: human Gold + IAA remain first-class. Handbook A must not look like a post-hoc rewrite of Doccano.
- Encoder 0.43 is protocol-bound (Handbook B + jieba). Weak baseline ~0.13 stays on Handbook A gold.
- Caption: 980 is SimHuman rule overlay, not full human SOP gold.
- CET-6: Gold-style / both handbooks → **K**; original silver API → **L** (footnote only).
- Do not invent a dual-IAA number for Handbook B; Table 2 IAA (n=100, strict F1 0.532) is Gold-era only.
- Page budget: PeerJ CS can take two short subsections. Prefer contrast examples over dumping both full Chinese pages into the PDF.

### Deliverable (markdown in the chat)

1. **Verdict:** rank A–E. Recommended default for camera-ready Methods.
2. **Insertion map:** current tex section titles → proposed subsection titles. Quote 1–2 existing sentences that must be patched (old silver-prompt-only story).
3. **Mock Methods skeleton:** headings + 4–8 English sentences per handbook (you may tighten the `.en.md` one-pagers; do not add new F1). Include **one contrast-example table** (2–3 rows).
4. **What goes to Supplemental Information** vs main text.
5. **Caption sentences** that stop (i) treating 980 as human SOP gold, (ii) ranking 0.4331 against 0.6365.
6. **What not to write:** Handbook A = original `chinese_skillspan` silver API; Gold v3 already done; mixed SOTA.
7. Stop. Do not edit files.

End prompt.
