# Handbook B addendum — potential overlap and adjudication (v4.2)

**Does not replace** `handbook_B_sop_v4.md`. Labels, CET-6→**L**, **shortest-complete** spans, and empty-sentence rules stay there.  
**Does not create** a nested-NER task. The scored Gold layer remains **flat and non-overlapping** [TKS02] [本协议]. Nested Long_S is the **next paper** [FM09] [Yu20] [Z22].

Version: `B.sop_v4.2.9`. 2026-09-05: peel 经验 on jargon (`大项目售前`). Sources: `handbook_B_citations.md`. Log: `LSKT_V4_RULE_CHANGELOG.md`. Empty log: `reports/annotation_v4/adjudication_log.csv`.

## What is not overlap

A sentence may contain several competency mentions that **do not share characters**. Mark each. That is multiple spans, not overlap.

## When candidates share characters

1. **Split first** into independently meaningful shortest-complete spans if meanings and offsets can stay separate. [AP08] [Z22]  
2. If one candidate is only an object, modifier, or fragment of a complete mention, **keep the shortest complete mention**—do not also keep the leftover word. [Z22] Coordinated objects under one verb are **not** automatically one long S. Split independent abilities. Keep one span **only** if splitting would change type (e.g. `优化曝光与转化率` → KPI nouns). Do not invent a second skill from POS alone. [UD20] [本协议]  
3. Do **not** put the same `(start, end)` surface span under two labels in the main Gold. [TKS02] [本协议]  
4. Record the plausible alternative and the conflict pair in the adjudication log. [本协议]  
5. Nested candidates stay **audit metadata** [FM09] [Yu20] [Z22]. Crossing spans are **prohibited**: re-bound or mark `adjudication_required`.  
6. If context does not resolve the case, **do not guess**. Set `annotator_decision=adjudication_required`. [AP08]

Human offsets are zero-based, end-exclusive. `sentence[start:end] == span` must hold. Jieba may validate word boundaries; it must not overwrite human Gold. [AP08] [D18]

## Conflict pairs (pairwise tests, not a ranking)

Use all six: **L/K, L/S, L/T, K/S, K/T, S/T**. Pairwise tests, not a global rank [AP08] [Kr95] [ESCO14]. `L > S > K > T` is **not** in ESCO or SkillSpan. If type is still unresolved after the pair test, mark **S** and log `adjudication_required` (SkillSpan B.3.1) [Z22].

| Pair | Typical test | Keep in Gold (default) | Log alternative |
|---|---|---|---|
| L/K | 英语 vs 大学英语六级 vs ISO / 本科及以上学历 | language name / level / exam **L**; technical or occupational certification **K**; degree/qualification **name** **K** [ESCO-L] [ESCO-Q] [Z22] | leftover language word, or K if someone tagged CET-6 as domain knowledge |
| L/S | 英语教学 vs 英语 | the licensed complete mention [Z22] | the leftover word |
| L/T | rare; language vs trait | whichever the predicate licenses | the other |
| K/S | SQL / ISO / Python-as-course vs tool use | Job-use bare `Python`/`SQL` **S**; course/principles → full NP **K** (`Python语言原理`, `SQL原理`); ISO 27001 **K** [ESCO14] [本协议] | the other type |
| K/T | 责任心 vs 专业知识 | T vs K by meaning [ESCO14] | the other |
| S/T | 沟通管理 / 客户汇报 vs 对接 / 沟通工具 | ESCO transversal communicating / `report facts` **T** even in a duty clause [ESCO-T] [Z22] [Say18]; occupation-specific action or named tool **S** | the other |

`overlap_type` ∈ {`none`, `same-boundary`, `nested`, `crossing`}. Unadjudicated alternatives **must not** enter the authoritative Gold span list.

## IAA (standardized protocol)

Both annotators see **raw text only** (no model draft, no earlier Gold, no each other). Freeze A/B files and compute pre-adjudication metrics **before** third-person adjudication [AP08] [Z22]. Report token- and span-level agreement separately (SkillSpan TOKEN κ vs SPAN κ). Do **not** reuse Table 2 n=100 (Handbook A) as v4.2 IAA.

IAA-50 (project 23) is **frozen**. Pre-adjudication TOKEN κ ≈ 0.57; exact span F1 ≈ 0.44. Do not edit project 23.

## Gold admission (agreement ≠ correctness)

Maple∩James exact match is a **candidate**, not automatic Gold. Agreement ≠ accuracy [AP08] [LK77]. Wendy is a quality gate, not a stamp.

1. **Necessary, not sufficient.** Candidate must still pass handbook type + cut + no missing mention. Joint errors (e.g. cert `安全` tagged S by both) stay out until corrected.  
2. **Disagreement** → third-person official four types (Wendy on 24/25) win.  
3. **Agreement** → default candidate; **sample** agreed sentences (认证名、一词多义、经验、保证/确保优先). Do not leave all agreed sentences unreviewed.  
4. Humans marked + Wendy left empty **on purpose** → Gold empty. 48272 / 48280 stay outside project 25 as previously agreed.  
5. Do **not** rewrite project 22 in bulk until a small batch (IAA-50 / p25) has been checked against these tests.

Unadjudicated alternatives stay in the log. They must not enter the authoritative Gold span list.
