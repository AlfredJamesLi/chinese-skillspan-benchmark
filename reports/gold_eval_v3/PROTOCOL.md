# Eval Gold v3 pilot (not official)

**Gold v2 stays frozen.** Official typed exact micro F1 still uses  
`data/gold_canonical_v2.jsonl` + `cnss-lskt-1.2.0`.

This folder is a **new** evaluation Gold: 300 stratified Gold-v2 sentences for dual IAA, then expand.  
Do not overwrite v2. Do not write these F1 into the PDF or `confirmed-results.md`.

## Empty-sentence lock

事业单位流程/福利默认空。Rules: `reports/gold_style_relabel/guidelines.md` §5 and `scripts/goldstyle_empty_rules.py`.

## Files

| file | role |
|---|---|
| `pilot300_manifest.json` | 300 IDs, domain × v2-span bucket |
| `pilot300_annotator_A.csv` / `_B.csv` | dual IAA sheets (no v2 spans) |
| `pilot300_v2_reference.json` | adjudicator only |
| `pilot300_meta.json` | quotas, SHA256 of v2 |

## After IAA

1. Adjudicate A vs B; empty-rule conflicts default to empty if the sentence is process/welfare.
2. Write a **new** file such as `data/gold_eval_v3_pilot300.jsonl` — never `gold_canonical_v2.jsonl`.
3. Expand only after IAA is logged.

阿里云 / 事业单位 **unlabeled JD text** for DAPT is a later corpus step, not this pack.
