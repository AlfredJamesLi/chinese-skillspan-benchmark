# Handbook B — LSKT v4 SOP (P2), one page

**Use:** matched-protocol operationalization. Train silver: `train_lskt_v4_silver`. Test gold: `test_lskt_v4_cws_simhuman980_hybrid.jsonl` (2601 = 980 SimHuman rule_v4 + 1621 SOP-CWS; jieba snap on **gold and** predictions).  
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

Contiguous original substring; **no mid-word cuts**. Prefer **2–8** tokens. Split coordinated skills. Mark only the **object** of 熟悉/掌握/精通/了解. Tools and programming languages → **S**. English grade certificates → **K**; bare 英文 → **L**. 报名/体检/公示/福利 → empty. Flat, non-overlapping.

**Headline numbers (P2 only):** JobBERT 3M v4+jieba typed exact **0.4331**; frozen ChatGPT dump+jieba exact **0.2854** / relaxed **0.6249**. Never claim these beat ChatGPT **0.6365** on Gold v2.
