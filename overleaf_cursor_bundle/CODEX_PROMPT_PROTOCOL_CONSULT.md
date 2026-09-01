# Codex consult — old vs new protocol (no tex edits yet)

**Overleaf:** https://www.overleaf.com/project/68fe17a53e53a7f800e4f2b4  
Paste **this file only**. Do **not** patch `main.tex` in this chat. Return a layout recommendation + a mock caption/table skeleton. Wait for a second prompt before editing.

Copy `overleaf_cursor_bundle/` into the Overleaf repo root if not already there. Numbers: `.cursor/skills/cnss-overleaf/confirmed-results.md`. Ban list: `not-for-paper.md`. Handbooks: `handbooks/` (B = paper main V4; A = Gold v2 provenance). **Authors chose V4-only as the reported protocol (2026-08-27).** Paste `CODEX_PROMPT_HANDBOOK.md` before this file if Methods layout is still open.

---

## PROMPT (copy from here)

You are advising on **table architecture** for the Chinese-SkillSpan / Chinese Skill Benchmark paper submitted to **PeerJ Computer Science**. This is **not** the IEEE Access / SRICL method paper. Do not invent F1. Use only numbers in `confirmed-results.md`.

**Venue:** PeerJ CS, not DASFAA. Do not recommend DASFAA page-limit tactics as if we were still a conference dataset track.

**This chat is consult-only.** `git pull --ff-only`, read `main.tex` and current Tables 1–3, then recommend. **Do not edit tex, do not commit, do not push.**

### What we actually have (three layers, not two)

Call them **P0 / P1 / P2**. Do not collapse them.

| Layer | Gold | Span definition | LLM prompt | Encoder train | What it measures |
|---|---|---|---|---|---|
| **P0** PDF Table 3 | old paper Gold 2676 | old paper S-F1 | old `@@span##[L\|K\|S\|T]` dumps | EN JobBERT heads | frozen published cells (ChatGPT 0.6700, …). **Keep numbers unchanged.** |
| **P1** Gold v2 provenance | human Doccano `gold_canonical_v2.jsonl`, 2601 unique IDs | human gold spans (long NPs OK) | same frozen dumps | goldstyle v3 CRF | **appendix** (same IDs as V4). ChatGPT typed **0.6365** / relaxed **0.7221**. JobBERT-zh 1M 3-seed **0.1288**. Encoder is a **weak baseline** on this convention. |
| **P2** matched SOP+jieba | hybrid 2601 = 980 SimHuman rule_v4 + 1621 SOP-CWS, jieba snap on gold **and** pred | LSKT v4 SOP (short, 禁半词, 熟悉只标对象) | **still the old dumps**, jieba-snapped after the fact (not a new GPT-4o SOP-extract call) | SOP v4 silver CRF + jieba | **paper main**. JobBERT 1M/3M v4 typed exact **0.4272 / 0.4331**. ChatGPT exact **0.2854**, relaxed **0.6249**. |

Claude/Kimi on P2: old dumps miss 98 / 293 IDs (empty-fill 0.1483 / 0.0964). Filled views exist but mix haiku+sonnet-4-6 and k2-0711+k2.6. Do not present them as the original Table-3 models.

SOP-extract re-calls (gpt-5.4 n=100; DeepSeek V4 Pro n=46) did **not** beat the frozen ChatGPT dump on the same IDs. Do not put them in any 2601 table.

**Forbidden in any design:** one SOTA sentence that compares JobBERT 0.4331 (P2) with ChatGPT 0.6365 (P1). Those golds and span conventions differ. ChatGPT’s drop 0.6365 → 0.2854 is a **span-convention** effect, not a new model.

### Question (this is what we need you to answer)

We have a **new benchmark + new SOP definition + new encoder silver/prompt**, and an **old benchmark + old definition + old LLM prompt**. How should the paper relate them?

Authors **already chose V4-only as the paper main protocol** (same 2601 IDs as Gold v2; Handbook B spans). Do not recommend putting Gold v2 ChatGPT 0.6365 back into the abstract. Critique collage/cross-protocol ranking, then rank A–E **for table layout given that decision**.

### Options to rank

**A. Two peer main tables**  
- Table X = P1 Gold v2 (appendix-worthy provenance; ChatGPT 0.6365; encoder ~0.13).  
- Table Y = P2 V4 (paper main; encoder exact 0.4272/0.4331; ChatGPT relaxed 0.6249).  
Authors now want **Y as the only main results table** and X as appendix. Confirm that is the PeerJ-safe reading of “V4 comes from V2”.

**B. One table, two column-groups**  
Same model rows; columns `Gold v2 typed exact | P2 typed exact | P2 typed relaxed`. Caption must say columns are **not rankable across**. No bold for a cross-protocol max. Risk: readers still compare 0.6365 vs 0.4331 horizontally.

**C. One table, extra rows**  
Insert “JobBERT-zh v4 (SOP+jieba protocol)” into the Gold v2 ranking. **This is the most misleading.** Say so if you agree.

**D. Best-score collage as the only main table**  
Pick max(P1 ChatGPT, P2 JobBERT, P2 ChatGPT relaxed, …). **This is not a scientific main table.** Say so if you agree.

**E. Report P2/V4 as the paper main gold; keep Gold v2 as provenance appendix**  
**Authors chose this (2026-08-27).** P2 is SOP+SimHuman+jieba, not human Doccano Gold — captions must say so. Do not overwrite `gold_canonical_v2.jsonl`. Recommend how to keep IAA Table 2 honest (Gold-era, not V4 IAA).

### Constraints for your recommendation

- Dataset-paper identity: the **2601 IDs** are Gold v2; the **scored spans** are V4. IAA (Table 2) is Gold-era only.
- Encoder story is real but **protocol-bound**: v4 silver + jieba helps when test gold uses the same SOP/CWS; it does **not** beat ChatGPT on Gold v2 (appendix).
- P2 LLM column is **old prompt + new gold**, so encoder vs LLM on P2 is only partly matched. Caption must say that. A fully matched LLM would need a 2601 SOP-extract re-call; we are not doing that this pass.
- Page budget: PeerJ CS allows more space than a conference track. **Main table = V4.** Gold v2 unique-first and goldstyle encoder ranking go to appendix.
- Claude/Kimi incomplete or mixed-model fills: mark in caption, do not let them look like complete original-model rows.

### Deliverable (markdown in the chat)

1. **Verdict:** rank A–E. One recommended default for the camera-ready structure.
2. **Abstract skeleton:** V4 numbers only (JobBERT exact 0.4331; ChatGPT relaxed 0.6249). No mixed SOTA with 0.6365.
3. **Table mock:** captions + column headers + which rows, using only confirmed numbers. Mark Claude/Kimi incomplete.
4. **What stays appendix:** P0? diagnostic SOP-silver? 980-only columns?
5. **If we used option B**, the exact caption sentence that stops cross-column ranking.
6. **Current tex:** list existing table numbers/titles so we know what to rename (Table 3 vs 4).
7. Stop. Do not edit files.

End prompt.
