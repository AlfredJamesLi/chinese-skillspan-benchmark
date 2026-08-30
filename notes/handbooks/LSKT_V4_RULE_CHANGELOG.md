# LSKT v4 rule changelog

**Handbook version:** `B.sop_v4.2` (2026-08-28; 2026-08-30 literature keys only)  
Canonical one-pagers: `notes/handbooks/handbook_B_sop_v4.md` (+ `.en.md`).  
Overlap/adjudication: `notes/handbooks/handbook_B_overlap_adjudication.md`.  
Literature keys: `notes/handbooks/handbook_B_citations.md`.  
LLM prompt: `prompts/LSKT_V4_ANNOTATION_PROMPT.txt`.

This log records **rule text** changes. It does **not** freeze a new human Gold and does **not** authorize rewriting paper F1 tables.

## 2026-08-30 — literature keys (no rule change)

Added `handbook_B_citations.md` and inline keys on B / B-en / overlap addendum / C. Version stays `B.sop_v4.2`. Short 2–8 tokens remain **[本协议]** (do not cite Zhang et al. 2022 as the source of shortness). Forbidden claims unchanged: no “long S raises exact F1”; no BERT-CRF nested S+K; no `L > S > K > T` from ESCO.

## 2026-08-28 — v4.2 (language certificates restored to L)

| Rule | v4.1 | v4.2 | Status |
|---|---|---|---|
| Language certificates (CET-6 / 英语六级 / 日语N2) | **K** (v4.1 rejected a Codex draft that used L) | **L**. Restores the original silver API (`prompt_template_rag.py` → `chinese_skillspan`: CET-6→L) and ESCO’s separate class *Language skills and knowledge* (hierarchy letter L): language is both knowledge and skill, so it is not merged into K or S. Technical / occupational certifications (ISO 27001, OCJP) stay **K**. Gold v2 / Handbook A remain **K** as provenance; **do not relabel** `gold_canonical_v2.jsonl`. | **restored L** |

ESCO sources: [skill_main](https://esco.ec.europa.eu/en/classification/skill_main); [Skills pillar](https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/skills-pillar); MAI hierarchy report (languages as knowledge concepts; CEFR competences as skills).

Do **not** re-call frozen P2 dumps or rewrite `train_lskt_v4_silver` solely for this handbook line. New human annotation (980 queue) uses L.

## 2026-08-28 — v4.1 (potential overlap audit; no nested-NER task)

| Rule | Previous (v4.0 / handbook B) | v4.1 | Status |
|---|---|---|---|
| Main layer | Flat, non-overlapping L/K/S/T | Unchanged. One adjudicated span/label in Gold. | **kept** |
| Global fallback `L > S > K > T` | Present in **legacy dump-fill prompts** (`scripts/fill_*_missing_*.py` only). Not in handbook B. | **Forbidden** for new human SOP and new LLM prompts. L–K–S–T is mnemonic only. | **removed for new annotation** |
| Language certificates (CET-6 / 英语六级 / 日语N2) | **K** (handbook A, B, C; SOP extract prompt) | **K** at the time. A Codex draft proposed **L**; v4.1 did not adopt it. | **superseded by v4.2** |
| SQL | Not named | Executable job-use → **S**; explicit principles/theory → **K**. | **added** |
| Jieba | Decode/eval snap on V4 hybrid | Validator and named derived-view transform. **Not** an annotator. **Not** an automatic Gold generator. Human character offsets are Gold. | **clarified** |
| Potential overlap | “Flat, do not nest” | Split if possible; else keep the complete mention; log alternative in adjudication file; crossing spans forbidden. Nested candidates are audit metadata only. | **added** |
| Conflict pairs | Informal K/S notes | Six pairwise tests: L/K, L/S, L/T, K/S, K/T, S/T. Not a priority sequence. | **added** |

Legacy fill-script prompts are **frozen dumps**. Do not rewrite them to invent a new Claude/Kimi Gold row.

## Not done (blockers)

- Dual-blind A/B files for standardized-protocol IAA: **missing**. Historical Table 2 n=100 is Handbook A / Gold-length, not v4.2.
- Adjudicated human Gold on the 980 queue: **missing**. `reports/human980_doccano/` is a **draft** prelabel-correction pack.
- Do not call V4 hybrid or SimHuman 980 final human Gold.
