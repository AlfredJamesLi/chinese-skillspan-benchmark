# Handbook B addendum — potential overlap and adjudication (v4.2)

**Does not replace** `handbook_B_sop_v4.md`. Labels, CET-6→**L**, short spans, and empty-sentence rules stay there.  
**Does not create** a nested-NER task. The scored Gold layer remains **flat and non-overlapping** [TKS02] [本协议]. Nested phenomena are audit-only [FM09] [Yu20] [Z22].

Version: `B.sop_v4.2.1`. 2026-08-31: Python/SQL full-NP K examples. Sources: `handbook_B_citations.md`. Log: `LSKT_V4_RULE_CHANGELOG.md`. Empty log: `reports/annotation_v4/adjudication_log.csv`.

## What is not overlap

A sentence may contain several competency mentions that **do not share characters**. Mark each. That is multiple spans, not overlap.

## When candidates share characters

1. **Split first** into independently meaningful shortest-complete spans if meanings and offsets can stay separate. [AP08] [Z22]  
2. If one candidate is only an object, modifier, or component of a complete mention licensed by the governing predicate, **keep only the complete mention**. [Z22] Coordinated objects under one elided verb (gapping, \(v'=v\)) stay one outer S; do not invent skill2 from POS. [UD20]  
3. Do **not** put the same `(start, end)` surface span under two labels in the main Gold. [TKS02] [本协议]  
4. Record the plausible alternative and the conflict pair in the adjudication log. [本协议]  
5. Nested candidates stay **audit metadata** [FM09] [Yu20] [Z22]. Crossing spans are **prohibited**: re-bound or mark `adjudication_required`.  
6. If context does not resolve the case, **do not guess**. Set `annotator_decision=adjudication_required`. [AP08]

Human offsets are zero-based, end-exclusive. `sentence[start:end] == span` must hold. Jieba may validate word boundaries; it must not overwrite human Gold. [AP08] [D18]

## Conflict pairs (pairwise tests, not a ranking)

Use all six: **L/K, L/S, L/T, K/S, K/T, S/T**. Pairwise tests, not a global rank [本协议] [AP08]. `L > S > K > T` is **not** in ESCO or SkillSpan.

| Pair | Typical test | Keep in Gold (default) | Log alternative |
|---|---|---|---|
| L/K | 英语 vs 大学英语六级 vs ISO | language name / level / exam **L** (keep the complete exam span; do not nest 英语 inside 六级); technical or occupational certification **K** [ESCO-L] | the leftover language word, or K if someone tagged CET-6 as domain knowledge |
| L/S | 英语教学 vs 英语 | the licensed complete mention [Z22] | the leftover word |
| L/T | rare; language vs trait | whichever the predicate licenses | the other |
| K/S | SQL / ISO / Python-as-course vs tool use | Job-use bare `Python`/`SQL` **S**; course/principles → full NP **K** (`Python语言原理`, `SQL原理`); ISO 27001 **K** [ESCO14] [本协议] | the other type |
| K/T | 责任心 vs 专业知识 | T vs K by meaning [ESCO14] | the other |
| S/T | 沟通 vs 沟通工具 | trait **T**; named tool **S** [ESCO14] [Z22] | the other |

`overlap_type` ∈ {`none`, `same-boundary`, `nested`, `crossing`}. Unadjudicated alternatives **must not** enter the authoritative Gold span list.

## IAA (standardized protocol)

Both annotators see **raw text only** (no model draft, no earlier Gold, no each other). Freeze A/B files and compute pre-adjudication metrics **before** third-person adjudication [AP08] [Z22]. Report token- and span-level agreement separately (SkillSpan TOKEN κ vs SPAN κ). Do **not** reuse Table 2 n=100 (Handbook A) as v4.2 IAA.

Those A/B files **do not exist yet**. Do not invent them.
