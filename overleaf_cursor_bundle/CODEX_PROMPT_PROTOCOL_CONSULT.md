# Codex consult — old vs new protocol (no tex edits yet)

**Overleaf:** https://www.overleaf.com/project/68fe17a53e53a7f800e4f2b4  
Paste **this file only**. Do **not** patch `main.tex` in this chat. Return a layout recommendation + a mock caption/table skeleton. Wait for a second prompt before editing.

Copy `overleaf_cursor_bundle/` into the Overleaf repo root if not already there. Numbers: `.cursor/skills/cnss-overleaf/confirmed-results.md`. Ban list: `not-for-paper.md`.

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
| **P1** Gold v2 official | human Doccano `gold_canonical_v2.jsonl`, 2601 unique IDs | human gold spans (long NPs OK) | same frozen dumps | goldstyle v3 CRF | official human benchmark. ChatGPT typed **0.6365** / relaxed **0.7221**. JobBERT-zh 1M 3-seed **0.1288**. Encoder is a **weak baseline**. |
| **P2** matched SOP+jieba | hybrid 2601 = 980 SimHuman rule_v4 + 1621 SOP-CWS, jieba snap on gold **and** pred | LSKT v4 SOP (short, 禁半词, 熟悉只标对象) | **still the old dumps**, jieba-snapped after the fact (not a new GPT-4o SOP-extract call) | SOP v4 silver CRF + jieba | matched train/test convention. JobBERT 1M/3M v4 typed exact **0.4272 / 0.4331**. ChatGPT exact **0.2854**, relaxed **0.6249**. |

Claude/Kimi on P2: old dumps miss 98 / 293 IDs (empty-fill 0.1483 / 0.0964). Filled views exist but mix haiku+sonnet-4-6 and k2-0711+k2.6. Do not present them as the original Table-3 models.

SOP-extract re-calls (gpt-5.4 n=100; DeepSeek V4 Pro n=46) did **not** beat the frozen ChatGPT dump on the same IDs. Do not put them in any 2601 table.

**Forbidden in any design:** one SOTA sentence that compares JobBERT 0.4331 (P2) with ChatGPT 0.6365 (P1). Those golds and span conventions differ. ChatGPT’s drop 0.6365 → 0.2854 is a **span-convention** effect, not a new model.

### Question (this is what we need you to answer)

We have a **new benchmark + new SOP definition + new encoder silver/prompt**, and an **old benchmark + old definition + old LLM prompt**. How should the paper relate them?

Authors currently lean toward either:

1. **Best-numbers-as-main-table:** put the most flattering scores in the main results table (P2 encoder exact + P1 ChatGPT, or P2 relaxed ChatGPT, etc.).
2. **One wide main table:** keep old and new together by adding a **column** (same models, two protocols) or a **row** (new systems inserted into the old ranking).

Please **critique 1 and 2**, then pick among the options below (or a hybrid). Say what a **PeerJ Computer Science** dataset-paper reviewer would attack.

### Options to rank

**A. Two peer main tables (recommended prior — attack or defend it)**  
- Table X = P1 Gold v2 (official human gold; LLM SOTA = ChatGPT 0.6365; encoder ~0.13).  
- Table Y = P2 matched SOP+jieba (encoder exact lead 0.4272/0.4331; ChatGPT relaxed lead 0.6249).  
- Abstract: **two sentences**, one per protocol.  
- P0 PDF Table 3 stays as a “paper-reported / old split” table or footnote, cells frozen.  
- SOP-silver diagnostic 0.3170 / both-sides ~0.43 on silver **appendix only**.

**B. One table, two column-groups**  
Same model rows; columns `Gold v2 typed exact | P2 typed exact | P2 typed relaxed`. Caption must say columns are **not rankable across**. No bold for a cross-protocol max. Risk: readers still compare 0.6365 vs 0.4331 horizontally.

**C. One table, extra rows**  
Insert “JobBERT-zh v4 (SOP+jieba protocol)” into the Gold v2 ranking. **This is the most misleading.** Say so if you agree.

**D. Best-score collage as the only main table**  
Pick max(P1 ChatGPT, P2 JobBERT, P2 ChatGPT relaxed, …). **This is not a scientific main table.** Say so if you agree.

**E. Replace Gold v2 with P2 as the official gold**  
We currently **reject** this: P2 is SOP+SimHuman+jieba, not human Doccano Gold. Human Gold v2 stays official. Confirm or dissent with a one-sentence reason.

### Constraints for your recommendation

- Dataset-paper identity: human gold + IAA (Table 2) must remain a first-class result, not an appendix casualty of the encoder story.
- Encoder story is real but **protocol-bound**: v4 silver + jieba helps when test gold uses the same SOP/CWS; it does **not** beat ChatGPT on Gold v2.
- P2 LLM column is **old prompt + new gold**, so encoder vs LLM on P2 is only partly matched. Caption must say that. A fully matched LLM would need a 2601 SOP-extract re-call; we are not doing that this pass.
- Page budget: PeerJ CS allows more space than a conference track. Still prefer two clear tables over a collage; extra protocol detail can go in Methods or Supplemental Information.
- Claude/Kimi incomplete or mixed-model fills: mark in caption, do not let them look like complete original-model rows.

### Deliverable (markdown in the chat)

1. **Verdict:** rank A–E. One recommended default for the camera-ready structure.
2. **Abstract skeleton:** two sentences max for P1, two for P2. No mixed SOTA.
3. **Table mock:** captions + column headers + which rows, using only confirmed numbers. Mark Claude/Kimi incomplete.
4. **What stays appendix:** P0? diagnostic SOP-silver? 980-only columns?
5. **If we used option B**, the exact caption sentence that stops cross-column ranking.
6. **Current tex:** list existing table numbers/titles so we know what to rename (Table 3 vs 4).
7. Stop. Do not edit files.

End prompt.
