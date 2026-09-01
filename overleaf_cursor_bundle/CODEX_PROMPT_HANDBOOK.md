# Codex consult — V4 as paper main protocol (no tex edits yet)

**Overleaf:** https://www.overleaf.com/project/68fe17a53e53a7f800e4f2b4  
Paste **this file only**. Do **not** patch `main.tex` in this chat. Return a Methods + table-layout plan. Wait for `CODEX_PROMPT_ALL.md` before editing.

Copy `overleaf_cursor_bundle/` into the Overleaf repo root if not already there. Read:

- `handbooks/README.md`
- `handbooks/handbook_A_gold_v2.en.md` and `handbooks/handbook_B_sop_v4.en.md`
- `.cursor/skills/cnss-overleaf/confirmed-results.md`
- `.cursor/skills/cnss-overleaf/not-for-paper.md`

Numbers only from `confirmed-results.md`. Ban list: `not-for-paper.md`.

---

## PROMPT (copy from here)

You are advising on **Methods and table layout** for the Chinese-SkillSpan / Chinese Skill Benchmark paper submitted to **PeerJ Computer Science**. This is **not** the IEEE Access / SRICL method paper. Do not invent F1.

**This chat is consult-only.** `git pull --ff-only`, read `main.tex` and the two one-page handbooks. **Do not edit tex, do not commit, do not push.**

### Decision already taken (2026-08-27) — do not reopen it

Authors will **report only the V4 protocol** as the paper’s main evaluation. Reason: the V4 test gold is **derived from the same 2601 Gold v2 IDs** (not a new sample). Handbook B is the reported span convention. Gold v2 (`gold_canonical_v2.jsonl`) stays on disk as **provenance**; its F1 goes to the **appendix**, not the abstract SOTA.

| | Provenance (Handbook A) | **Paper main (Handbook B)** |
|---|---|---|
| File | `gold_canonical_v2.jsonl` (frozen; do not overwrite) | `test_lskt_v4_cws_simhuman980_hybrid.jsonl` |
| Spans | Doccano Gold-length NPs | SOP v4 short spans + jieba, both sides |
| Makeup | human-checked Gold | 980 SimHuman **rule_v4** + 1621 SOP-CWS |
| Headline | ChatGPT typed **0.6365**; JobBERT 1M 3-seed **0.1288** | JobBERT 3M v4 exact **0.4331**; frozen ChatGPT dump+jieba exact **0.2854** / relaxed **0.6249** |

**Still true — write this honestly or reviewers will attack:**

- V4 hybrid is **not** human Doccano Gold. Do not call 980 a full human SOP pass.
- Table 2 IAA (n=100, strict F1 0.532) measures **Gold-era** spans, not V4 hybrid spans. Do not invent a V4 IAA.
- P2 LLM rows are **frozen old dumps** + jieba (old prompt, new gold). ChatGPT 0.6365 → 0.2854 is a **span-convention** drop, not a new `gpt-4o` run.
- **Forbidden:** one SOTA sentence ranking JobBERT **0.4331** against ChatGPT **0.6365**.
- PDF Table 3 (ChatGPT 0.6700 … Qwen 0.2130) stays frozen (old published protocol, Gold 2676).
- Allowed on V4: JobBERT leads typed exact (0.4331); ChatGPT leads relaxed (0.6249). Caption must say frozen dumps + jieba.

### Question

Given that V4 is the **only** main protocol, how should a PeerJ CS dataset paper present: (i) the Doccano origin of the 2601 IDs, (ii) Handbook B as the reported SOP, (iii) Gold v2 F1 as appendix — without pretending V4 is a second human gold?

### Options to rank (layout only; V4-main is fixed)

**A. Main results = V4 table; Gold v2 unique-first + goldstyle encoder 3/5-seed = appendix; Methods = short provenance paragraph + Handbook B SOP.**

**B. Main results = V4 table; Gold v2 0.6365 stays in the main text as a second results subsection.** (Authors currently **do not** want this. Attack or defend.)

**C. Drop Gold v2 numbers entirely, keep only a citation to Doccano.** Risk: IAA Table 2 becomes unanchored.

**D. One main table with Gold v2 and V4 columns.** Authors reject cross-column ranking. Say if this is still a trap.

### Constraints

- Dataset-paper identity: say the **IDs** are human-adjudicated Gold v2; the **spans used for scoring** are V4 SOP+jieba.
- Encoder 0.43 is protocol-matched (Handbook B train silver + jieba). Encoder ~0.13 on Gold v2 is appendix, a weak baseline on the source convention.
- CET-6 → **L** in Handbook B (v4.2; restores original silver API). Gold v2 / Handbook A kept CET-6 as **K** (provenance only; do not relabel that file). ISO / OCJP stay **K**. Footnote ESCO *Language skills and knowledge*: language is both knowledge and skill, so L is its own branch.
- Page budget: PeerJ CS can take one main table + appendix. Prefer one contrast-example table (2–3 rows) over pasting both Chinese pages.

### Deliverable (markdown in the chat)

1. **Verdict:** rank A–D. Default for camera-ready given V4-only.
2. **Abstract skeleton:** ≤3 sentences. Lead with V4 numbers only. No 0.6365.
3. **Methods skeleton:** headings + 6–10 English sentences (tighten `handbook_B_sop_v4.en.md`; 2–3 sentences of Handbook A as provenance). One contrast-example table.
4. **Table mock:** main V4 caption + appendix Gold v2 caption. Mark Claude/Kimi incomplete on V4 (98 / 293 empty).
5. **IAA caption sentence** that stops readers from treating Table 2 as V4 IAA.
6. **What not to write:** V4 = human gold; 980 fully human; mixed SOTA 0.4331 vs 0.6365; Handbook A = original silver API.
7. Stop. Do not edit files.

End prompt.
