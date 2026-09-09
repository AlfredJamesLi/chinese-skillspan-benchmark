# Gold150 × frozen V4/SOP — diagnostic only

Same frozen predictions, new Gold150 human gold. Not a new API call.
Not official Table A (that is hybrid 2601) and not official Table B (JobBERT student 0.5536).
Do not rewrite `confirmed-results.md` from these numbers.

Scorer: `cnss-lskt-1.2.0` via `eval_gold150_ext.py`. Gold150 SHA `ca8db0bc…`. All rows below are complete 150/150.

## Prefer this block (unified SOP extract v4, raw, no jieba)

| Pred | exact | relaxed |
|---|---:|---:|
| Claude Sonnet 4.5 SOP | 0.3153 | 0.4287 |
| GPT-5.4 SOP | 0.3103 | 0.4471 |
| Kimi k2.6 SOP | 0.3070 | 0.4244 |
| DeepSeek v4-pro SOP | 0.2951 | 0.4131 |
| Qwen2.5-14B SOP parsed | 0.2498 | 0.3475 |
| Qwen2.5-14B SOP + jieba | 0.2672 | 0.3698 |

## Old dumps (different prompt: `@@span##` ESCO-style, not SOP)

| Pred | exact | relaxed | coverage note |
|---|---:|---:|---|
| ChatGPT unique-first v2 | 0.2614 | 0.3873 | 150/150 |
| Claude filled v2 | 0.2913 | 0.4385 | original unique-first missed 45 IDs |
| Kimi filled v2 | 0.2096 | 0.2605 | original unique-first missed 11 IDs |
| DeepSeek unique-first v2 | 0.1228 | 0.1818 | 150/150 |

Hybrid CWS (Table A jieba snap on old dumps) is a different protocol: ChatGPT 0.2721, Claude 0.2130, Kimi 0.1736, DeepSeek 0.1206, Qwen dump 0.0755.

Frozen JobBERT-zh 3M v4 raw on Gold150: 0.1321. That is the released hybrid checkpoint, not Silver-plus student 0.5536.

Official `gpt-4o` + SOP extract was never called on 2601 or Gold150.
