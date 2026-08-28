# Handbook B — LSKT v4 SOP (paper main protocol), one page

**Handbook version:** `B.sop_v4.1` (2026-08-28). Overlap/adjudication: `handbook_B_overlap_adjudication.md`. Changelog: `LSKT_V4_RULE_CHANGELOG.md`. LLM prompt: `prompts/LSKT_V4_ANNOTATION_PROMPT.txt`.

**Use:** the **reported** evaluation operationalization. Train silver: `train_lskt_v4_silver`. Test gold: `test_lskt_v4_cws_simhuman980_hybrid.jsonl` (2601 = 980 SimHuman rule_v4 + 1621 SOP-CWS; **same IDs as Gold v2**; jieba snap on **gold and** predictions).  
**Not** human Doccano Gold. **Do not overwrite** `gold_canonical_v2.jsonl`. The 980 overlay is rule-based, not a full human pass under this handbook.

P2 main LLM rows remain **frozen old dumps** + jieba, not an official `gpt-4o` SOP re-call.

## Labels (still LSKT; optional Zhang projection L+K→KNOWLEDGE, S+T→SKILL)

| Tag | Meaning | Examples |
|---|---|---|
| L | language **word**, not certificate | 英语, 英文, 普通话 |
| K | degree, major, **certificate**, domain | 本科及以上学历, **大学英语6级** |
| S | tool, method, executable skill | Python, Excel, 测试 |
| T | trait / soft skill | 沟通能力, 抗压能力 |

## Spans (short, complete, original)

Contiguous original substring; **no mid-word cuts**. Prefer **2–8** tokens. Split coordinated skills. Mark only the **object** of 熟悉/掌握/精通/了解. Tools and programming languages → **S**. English grade certificates → **K**; bare 英文 → **L**. SQL in executable job use → **S**; explicit theory → **K**. 报名/体检/公示/福利 → empty. Flat, non-overlapping. L–K–S–T is mnemonic only; **no** `L > S > K > T` fallback. Human character offsets are Gold; jieba is a validator/derived view, not an annotator. Log same-boundary / nested / crossing candidates; do not put them in the main Gold layer. See `handbook_B_overlap_adjudication.md`.

**Headline numbers (P2 only):** JobBERT 3M v4+jieba typed exact **0.4331**; frozen ChatGPT dump+jieba exact **0.2854** / relaxed **0.6249**. Never claim these beat ChatGPT **0.6365** on Gold v2.
