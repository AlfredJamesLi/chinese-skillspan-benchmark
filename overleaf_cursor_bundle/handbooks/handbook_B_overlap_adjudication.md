# Handbook B addendum — potential overlap and adjudication (v4.1)

**Does not replace** `handbook_B_sop_v4.md`. Labels, CET-6→**K**, short spans, and empty-sentence rules stay there.  
**Does not create** a nested-NER task. The scored Gold layer remains **flat and non-overlapping**.

Version: `B.sop_v4.1`. Log: `LSKT_V4_RULE_CHANGELOG.md`. Empty log: `reports/annotation_v4/adjudication_log.csv`.

## What is not overlap

A sentence may contain several competency mentions that **do not share characters**. Mark each. That is multiple spans, not overlap.

## When candidates share characters

1. **Split first** into independently meaningful shortest-complete spans if meanings and offsets can stay separate.  
2. If one candidate is only an object, modifier, or component of a complete mention licensed by the governing predicate, **keep only the complete mention**.  
3. Do **not** put the same `(start, end)` surface span under two labels in the main Gold.  
4. Record the plausible alternative and the conflict pair in the adjudication log.  
5. Nested candidates stay **audit metadata**. Crossing spans are **prohibited**: re-bound or mark `adjudication_required`.  
6. If context does not resolve the case, **do not guess**. Set `annotator_decision=adjudication_required`.

Human offsets are zero-based, end-exclusive. `sentence[start:end] == span` must hold. Jieba may validate word boundaries; it must not overwrite human Gold.

## Conflict pairs (pairwise tests, not a ranking)

Use all six: **L/K, L/S, L/T, K/S, K/T, S/T**.

| Pair | Typical test | Keep in Gold (default) | Log alternative |
|---|---|---|---|
| L/K | 英语 vs 大学英语六级 | certificate span **K**; bare language word **L** | the other span if both were proposed |
| L/S | 英语教学 vs 英语 | the licensed complete mention | the leftover word |
| L/T | rare; language vs trait | whichever the predicate licenses | the other |
| K/S | SQL / ISO / Python-as-course vs tool use | SQL job-use **S**; SQL principles **K**; ISO 27001 **K**; Python job-use **S** | the other type |
| K/T | 责任心 vs 专业知识 | T vs K by meaning | the other |
| S/T | 沟通 vs 沟通工具 | trait **T**; named tool **S** | the other |

`overlap_type` ∈ {`none`, `same-boundary`, `nested`, `crossing`}. Unadjudicated alternatives **must not** enter the authoritative Gold span list.

## IAA (standardized protocol)

Both annotators see **raw text only** (no model draft, no earlier Gold, no each other). Freeze A/B files and compute pre-adjudication metrics **before** third-person adjudication. Do **not** reuse Table 2 n=100 (Handbook A) as v4.1 IAA.

Those A/B files **do not exist yet**. Do not invent them.
