# LSKT v4 rule changelog

**Handbook version:** `B.sop_v4.1` (2026-08-28)  
Canonical one-pagers: `notes/handbooks/handbook_B_sop_v4.md` (+ `.en.md`).  
Overlap/adjudication: `notes/handbooks/handbook_B_overlap_adjudication.md`.  
LLM prompt: `prompts/LSKT_V4_ANNOTATION_PROMPT.txt`.

This log records **rule text** changes. It does **not** freeze a new human Gold and does **not** authorize rewriting paper F1 tables.

## 2026-08-28 — v4.1 (potential overlap audit; no nested-NER task)

| Rule | Previous (v4.0 / handbook B) | v4.1 | Status |
|---|---|---|---|
| Main layer | Flat, non-overlapping L/K/S/T | Unchanged. One adjudicated span/label in Gold. | **kept** |
| Global fallback `L > S > K > T` | Present in **legacy dump-fill prompts** (`scripts/fill_*_missing_*.py` only). Not in handbook B. | **Forbidden** for new human SOP and new LLM prompts. L–K–S–T is mnemonic only. | **removed for new annotation** |
| Language certificates (CET-6 / 英语六级 / 日语N2) | **K** (handbook A, B, C; SOP extract prompt) | **K** (unchanged). A Codex draft proposed **L**. That draft is **not** adopted. Original silver API had certificates in L; that is history only. | **kept K**; Codex L proposal rejected |
| SQL | Not named | Executable job-use → **S**; explicit principles/theory → **K**. | **added** |
| Jieba | Decode/eval snap on V4 hybrid | Validator and named derived-view transform. **Not** an annotator. **Not** an automatic Gold generator. Human character offsets are Gold. | **clarified** |
| Potential overlap | “Flat, do not nest” | Split if possible; else keep the complete mention; log alternative in adjudication file; crossing spans forbidden. Nested candidates are audit metadata only. | **added** |
| Conflict pairs | Informal K/S notes | Six pairwise tests: L/K, L/S, L/T, K/S, K/T, S/T. Not a priority sequence. | **added** |

Legacy fill-script prompts are **frozen dumps**. Do not rewrite them to invent a new Claude/Kimi Gold row.

## Not done (blockers)

- Dual-blind A/B files for standardized-protocol IAA: **missing**. Historical Table 2 n=100 is Handbook A / Gold-length, not v4.1.
- Adjudicated human Gold on the 980 queue: **missing**. `reports/human980_doccano/` is a **draft** prelabel-correction pack.
- Do not call V4 hybrid or SimHuman 980 final human Gold.
