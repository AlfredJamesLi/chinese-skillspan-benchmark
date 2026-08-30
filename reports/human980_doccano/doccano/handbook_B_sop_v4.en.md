# Handbook B — LSKT v4 SOP (paper main protocol), one page

**Handbook version:** `B.sop_v4.2` (2026-08-28). 2026-08-30 added literature keys only; rules unchanged. Overlap/adjudication: `handbook_B_overlap_adjudication.md`. Sources: `handbook_B_citations.md`. Changelog: `LSKT_V4_RULE_CHANGELOG.md`. LLM prompt: `prompts/LSKT_V4_ANNOTATION_PROMPT.txt`.  
**Keys:** [ESCO14] [ESCO-L] [Z22] [AP08] [TKS02] [FM09] [Yu20] [UD20] [D18]. `[本协议]` / *this protocol* = Chinese-job operationalization, not a gold standard forced by one paper.

**Use:** the **reported** evaluation operationalization. Train silver: `train_lskt_v4_silver`. Test gold: `test_lskt_v4_cws_simhuman980_hybrid.jsonl` (2601 = 980 SimHuman rule_v4 + 1621 SOP-CWS; **same IDs as Gold v2**; jieba snap on **gold and** predictions).  
**Not** human Doccano Gold. **Do not overwrite** `gold_canonical_v2.jsonl`. The 980 overlay is rule-based, not a full human pass under this handbook.

P2 main LLM rows remain **frozen old dumps** + jieba, not an official `gpt-4o` SOP re-call.

## Labels (still LSKT; optional Zhang projection L+K→KNOWLEDGE, S+T→SKILL)

| Tag | Meaning | Examples | Source |
|---|---|---|---|
| L | Natural language: name, proficiency, or language exam/certificate. Both knowledge and skill, so kept as its own branch | 英语, 商务英语, 英语六级, CET-6, 日语N2 | [ESCO-L] [本协议] |
| K | Degree, major, domain knowledge, technical standard, **non-language** professional certification | 本科及以上学历, ISO 27001, OCJP-Java认证 | [ESCO14] [Z22] |
| S | Tool, method, executable skill (applying knowledge) | Python, Excel, 测试 | [ESCO14] [Z22] |
| T | Trait / soft skill | 沟通能力, 抗压能力 | [ESCO14] [Z22] [本协议] |

L follows ESCO’s separate skills-pillar class **Language skills and knowledge** (hierarchy letter L), listed alongside Knowledge and Skills, not inside either [ESCO-L]. Sources: [ESCO skill_main](https://esco.ec.europa.eu/en/classification/skill_main); [ESCOpedia: Skills pillar](https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/skills-pillar). Conceptual source [ESCO14]. Inside that class, language names are knowledge concepts and CEFR-style use is skill; a language examination still stays in **L**, not ISCED-F domain knowledge [本协议]. The Zhang projection L+K→KNOWLEDGE is evaluation-only [Z22] and is **not** an ESCO identity. Four types (including a separate T) are this resource’s schema, not SkillSpan’s original two-layer table [Z22] [本协议].

## Spans (short, complete, original)

Contiguous original substring; **no mid-word cuts** [Z22] [D18] [本协议]. Prefer **2–8** tokens [本协议] (**do not cite [Z22] for shortness**: SkillSpan spans are often longer and may nest knowledge inside skill; unitization [AP08]). Split **independent** coordinated skills [Z22] [本协议]; one verb licensing several objects: overlap addendum [UD20]. Mark only the **object** of 熟悉/掌握/精通/了解 [Z22] [本协议]. Tools and programming languages in job use → **S** [ESCO14] [本协议]. Language names, levels, and language examinations (CET-6 / 英语六级 / 日语N2) → **L** [ESCO-L] [本协议]. ISO / OCJP and other technical or occupational certifications → **K**. This restores the original silver API; Gold v2 / Handbook A put CET-6 in K — **do not relabel that file**. SQL in executable job use → **S**; explicit theory → **K** [ESCO14] [本协议]. 报名/体检/公示/福利 → empty [Z22] [本协议]. Flat, non-overlapping [TKS02] [本协议]; this round is not nested NER [FM09] [Yu20]. L–K–S–T is mnemonic only; **no** `L > S > K > T` fallback [本协议] [AP08]. Human character offsets are Gold; jieba is a validator/derived view, not an annotator [AP08] [D18]. Log same-boundary / nested / crossing candidates; do not put them in the main Gold layer [FM09] [Z22]. See `handbook_B_overlap_adjudication.md`.

**Headline numbers (P2 only):** JobBERT 3M v4+jieba typed exact **0.4331**; frozen ChatGPT dump+jieba exact **0.2854** / relaxed **0.6249**. Never claim these beat ChatGPT **0.6365** on Gold v2.
