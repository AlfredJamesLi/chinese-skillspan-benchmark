# LSKT v4 rule changelog

**Handbook version:** `B.sop_v4.2.9` (2026-09-05; peel 经验 on jargon like 售前)  
Canonical one-pagers: `notes/handbooks/handbook_B_sop_v4.md` (+ `.en.md`).  
Overlap/adjudication: `notes/handbooks/handbook_B_overlap_adjudication.md`.  
Literature keys: `notes/handbooks/handbook_B_citations.md`.  
LLM prompt: `prompts/LSKT_V4_ANNOTATION_PROMPT.txt`.

This log records **rule text** changes. It does **not** freeze a new human Gold and does **not** authorize rewriting paper F1 tables.

## 2026-09-05 — v4.2.9 (peel 经验 on industry jargon)

`售前` is occupational jargon. `大项目售前` stays readable and stays S without `经验`. Aligns with the only cut: 语义不变则尽量短. Keep `经验` only if peeling would mid-cut or change type.

| Rule | v4.2.8 | v4.2.9 | Status |
|---|---|---|---|
| `大项目售前经验` | keep 经验 | **`大项目售前` S** | **changed** |

## 2026-09-05 — v4.2.8 (remaining five tests)

Writes the last five codebook gaps as if-then tests. Does **not** rewrite project 22 or paper F1. IAA-50 stays frozen.

| Rule | Before | v4.2.8 | Status |
|---|---|---|---|
| 「××能力」 | Examples only; “能做事→S” leaks T | Two-step: domain-bound → S; transferable → T. 科研能力 default T | **frozen** |
| 网络/安全/ICT | Oral Gold only | Cert/major K; ops object S; domain modifier empty | **frozen** |
| 保证/确保 | Only 增长/流量/目标/业绩 | Never mark 保证; result-noun clause empty; tech object marked alone | **frozen** |
| 经验 | Handbook peel-all vs oral keep | Shell empty; peel if leftover complete; keep 售前/开发… | **frozen** |
| Gold admission | Agree-as-default | Agreement = candidate only; sample agreed sentences [AP08] | **frozen** |

## 2026-09-05 — v4.2.7 (points 3–4: same surface, two licenses)

Freezes bare tool/language names for the **flat** layer. Nested Long_S stays the next paper. Does **not** rewrite paper F1.

| Rule | v4.2.6 | v4.2.7 | Status |
|---|---|---|---|
| Bare `Python` / `R` / `SQL` / tools | Job-use default S; CODEBOOK §6 still said K | **Apply / job tool → bare S**; **know-that / course / principles → full NP K**; unclear → S + log | **frozen** |
| ESCO inventory / SkillSpan B.2 | Acknowledged, not followed | Still acknowledged: their default bare Python=K (one type, nestable). Do not claim this rule comes from [Z22] App. B | **clarified** |

## 2026-09-05 — v4.2.6 (only cut: shortest that keeps meaning)

Withdraws the project-22 guideline line「一个动词一条长 S / 能不拆就不拆 / 只有安全拆才拆」so human Gold has **one** unitization, not two. Nested Long_S is explicitly deferred to the next paper.

| Rule | v4.2.5 | v4.2.6 | Status |
|---|---|---|---|
| Coordinated objects under one verb | Easy to keep one long outer S | **Split** unless splitting changes type (半词 / 曝光漂成指标) | **changed** |
| Nested Long_S | “later / 阶段 B” | Next article; this round flat short only | **deferred** |

## 2026-09-05 — v4.2.5 (ESCO wording is the type authority)

No new decision on spans. The label table now **quotes ESCO/EQF** for K, S, T, L. SkillSpan remains span/eval only. Guideline / CODEBOOK carry the same quotes and portal URLs.

| Rule | v4.2.4 | v4.2.5 | Status |
|---|---|---|---|
| What defines S/K/T/L | ESCO cited, mixed with SkillSpan in the same table cells | **ESCO portal wording is the only type authority**; [Z22] must not rewrite the four classes | **clarified** |

## 2026-09-05 — v4.2.4 (literature freeze: 1 / 2 / 5)

Operational freeze only. **Does not** change the four labels, paper F1, or points 3–4 (bare tool names stay job-use **S**).

| Rule | v4.2.3 | v4.2.4 | Status |
|---|---|---|---|
| Uncertain-type fallback | B already forbade `L＞S＞K＞T`; Doccano guideline / CODEBOOK still said use it | **Deleted** from guideline/CODEBOOK. Pairwise tests; if still unresolved → **S** + log (SkillSpan B.3.1) [Z22] [AP08] [ESCO14] | **aligned** |
| Degree / qualification name | B example already K; guideline said「学历壳不进跨度」 | `本科及以上学历` **K** [Z22] [ESCO-Q]. Year counts still empty | **aligned** |
| 沟通管理 / 客户汇报 | IAA memo: duty → S | **T** even in a duty clause [ESCO-T] `report facts` / T4.1. Project to SKILL for Zhang | **changed** |

New citation keys: [EQF] [ESCO-T] [ESCO-Q] [Say18] [Kr95]. Most operational lines in B / citations now carry a source. Do **not** claim `L＞S＞K＞T` or「岗位工具=S」comes from SkillSpan App. B.

## 2026-09-05 — v4.2.3 (会聊天: keep 会)

| Rule | v4.2.2 | v4.2.3 | Status |
|---|---|---|---|
| Oral T phrases `会聊天` / `会说话` / `会来事` / `会做人` | Easy to peel 会 like 熟悉 | **Keep 会** in one **T** span | **added** |
| `会使用Excel` / `会修电脑` | Peel 会 | Unchanged: still peel 会 | **kept** |

## 2026-09-05 — v4.2.2 (action vs result/goal)

Operational clarification only. **Does not** change the four labels or paper F1.

| Rule | v4.2.1 | v4.2.2 | Status |
|---|---|---|---|
| Result / KPI clauses (`保证流量/用户增长`, `确保…目标达成`) | Not named; easy to mark as S | **Do not mark.** 「做什么」(action/method) may be S; 「达成什么」(result/goal) is empty | **added** |
| Action with a metric object (`分析推广效果`, `优化曝光与转化率`) | Short S / one-verb coordinated objects | Unchanged: still **S** | **kept** |

## 2026-08-31 — v4.2.1 (Python/SQL S vs K examples)

Clarifies the existing SQL line. **Does not** adopt nested Long_S or change paper F1.

| Rule | v4.2 | v4.2.1 | Status |
|---|---|---|---|
| Job-use `Python` / `R` / `C` (掌握…如…) | Tools → S; no classic sentence | Bare names **S**; do not flip 如-examples to K; do not mark 掌握 | **examples added** |
| Course / principle / basics / syntax | SQL principles → K only | Mark the **full knowledge NP** (`Python语言原理`, `Python基础知识`, `Python语法`); do **not** mark bare `Python` as K when a longer object is licensed | **examples added** |
| Nested Long_S = S(V+K)+K2+K3 | Forbidden on main layer | Still forbidden | **kept** |

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
