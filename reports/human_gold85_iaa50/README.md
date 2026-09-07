# Handbook-B human gold85 + IAA-50 model diagnostic (2026-09-07)

**Not paper-main.** Do not replace V4 hybrid JobBERT 3M typed exact **0.4331**, ChatGPT dump+jieba **0.2854 / 0.6249**, or Gold v2 ChatGPT **0.6365**. Do not call n=85 IAA. JSON: `eval_models_gold85_iaa50.json`, `eval_spanlen_gold85_iaa50.json`.

## Golds

| Split | n sent | n gold spans | mean span chars | What it is |
|---|---:|---:|---:|---|
| Gold85 | 85 | 376 | 5.72 | Project 26 seq 1–85 **live official** LSKT (Handbook B). 42/85 have annotator-owned official spans. |
| IAA-50 | 50 | 248 | 4.31 | Frozen `iaa50_gold_locked.jsonl`. Qwen matched 49/50. |

Typed exact = same start, end, and type. No jieba snap on human gold (except the explicit `Qwen2.5-14B SOP+jieba` row, which snaps **predictions only**).

## Scale / protocol (allowed diagnostic claim)

On these **human** golds, typed exact rises with instruction-model scale:

| Family | Example | Gold85 F1 | IAA-50 F1 |
|---|---|---:|---:|
| Encoder CRF (~0.1B) | JobBERT-zh 3M v4, raw BIO | 0.1266 | 0.1522 |
| Mid instruct (14B) + SOP extract | Qwen2.5-14B-Instruct SOP | 0.2424 | 0.2506 |
| Same + jieba snap on pred | Qwen2.5-14B SOP+jieba | 0.2551 | 0.2678 |
| Frontier LLM (suggest / overlay) | Kimi / 豆包 / Codex / GPT-6.0 | 0.40–0.75 | 0.29–0.62 |

**Allowed claim:** Chinese SkillSpan *human* spans (short, typed, Handbook B) are hard for a 100M CRF; a 14B SOP extract already doubles exact F1, and larger instruction models go further.  
**Forbidden:** using this to retire abstract 0.4331; ranking GPT-6.0 **0.7528** against JobBERT 0.4331; calling Gold85 a clean blind test (GPT-6 overlay was visible while humans edited official types). IAA-50 is the cleaner LLM-vs-encoder contrast (Kimi **0.6233** vs Qwen SOP+jieba **0.2678** vs JobBERT **0.1522**).

JobBERT drop vs 0.4331 is protocol, not a crashed checkpoint: same CRF dump is 0.4331 after bilateral jieba on V4 hybrid, 0.2552 without jieba on that hybrid, and ~0.11–0.15 against human gold (see `notes/confirmed-results.md`).

## Overall typed exact

### Gold85

| System | P | R | F1 | n_pred |
|---|---:|---:|---:|---:|
| GPT-6.0 | 0.7878 | 0.7207 | **0.7528** | 344 |
| 建议层 (3-model consensus) | 0.4816 | 0.5931 | 0.5316 | 463 |
| 豆包 | 0.5000 | 0.4282 | 0.4613 | 322 |
| Kimi | 0.4558 | 0.4521 | 0.4539 | 373 |
| Codex | 0.4141 | 0.3910 | 0.4022 | 355 |
| Qwen2.5-14B SOP+jieba | 0.3538 | 0.1995 | 0.2551 | 212 |
| Qwen2.5-14B SOP | 0.3028 | 0.2021 | 0.2424 | 251 |
| JobBERT-Zh | 0.1625 | 0.1037 | 0.1266 | 240 |

### IAA-50

| System | P | R | F1 | n_pred |
|---|---:|---:|---:|---:|
| Kimi | 0.7020 | 0.5605 | **0.6233** | 198 |
| 豆包 | 0.6562 | 0.4234 | 0.5147 | 160 |
| Codex | 0.4320 | 0.2177 | 0.2895 | 125 |
| Qwen2.5-14B SOP+jieba | 0.4153 | 0.1976 | 0.2678 | 118 |
| Qwen2.5-14B SOP | 0.3427 | 0.1976 | 0.2506 | 143 |
| JobBERT-Zh | 0.2180 | 0.1169 | 0.1522 | 133 |

GPT-6 / 建议层 are Doccano overlays (not on IAA-50). Kimi / 豆包 / Codex = fragment strings aligned onto sentence text.

## Span character length (end − start)

Bins follow Handbook B’s short-span preference (about 2–8 characters). Precision uses **predicted** spans in the bin; recall uses **gold** spans in the bin.

Gold85 gold counts: 1–2 = 51, 3–4 = 127, 5–8 = 140, 9–14 = 48, 15+ = 10.  
IAA-50 gold counts: 1–2 = 54, 3–4 = 109, 5–8 = 78, 9–14 = 7, 15+ = 0.

### Gold85 typed exact F1 by span length

| System | 1–2 | 3–4 | 5–8 | 9–14 | 15+ | pred mean chars |
|---|---:|---:|---:|---:|---:|---:|
| GPT-6.0 | 0.7021 | 0.7787 | 0.7663 | 0.7500 | 0.4706 | 5.83 |
| 建议层 | 0.5200 | 0.5373 | 0.5948 | 0.3288 | 0.3333 | 4.43 |
| Kimi | 0.4228 | 0.5374 | 0.4274 | 0.2899 | 0.2667 | 4.69 |
| 豆包 | 0.3860 | 0.5765 | 0.4292 | 0.2373 | 0.1818 | 4.32 |
| Codex | 0.2810 | 0.4533 | 0.4735 | 0.1455 | 0.0000 | 4.21 |
| Qwen2.5-14B SOP+jieba | 0.3488 | 0.3267 | 0.2000 | 0.1429 | 0.0000 | 5.04 |
| Qwen2.5-14B SOP | 0.2560 | 0.3251 | 0.2009 | 0.1429 | 0.0000 | 4.40 |
| JobBERT-Zh | 0.1348 | 0.1194 | 0.1609 | 0.0000 | 0.0000 | 4.91 |

### IAA-50 typed exact F1 by span length

| System | 1–2 | 3–4 | 5–8 | 9–14 | 15+ | pred mean chars |
|---|---:|---:|---:|---:|---:|---:|
| Kimi | 0.6593 | 0.6387 | 0.5960 | 0.4615 | — | 4.52 |
| 豆包 | 0.4500 | 0.5514 | 0.5385 | 0.1538 | — | 4.58 |
| Codex | 0.2727 | 0.3164 | 0.2626 | 0.2222 | — | 3.78 |
| Qwen2.5-14B SOP+jieba | 0.2667 | 0.3506 | 0.1667 | 0.2353 | — | 4.85 |
| Qwen2.5-14B SOP | 0.2000 | 0.3462 | 0.1695 | 0.2353 | — | 4.14 |
| JobBERT-Zh | 0.1818 | 0.1611 | 0.1408 | 0.0000 | — | 4.88 |

**Read:** most human gold is 3–8 characters. Encoder / 14B SOP stay usable on 3–4 chars and fall off after 8; they miss almost all 9+ gold spans (JobBERT recall 0 on Gold85 9–14 / 15+). Frontier LLMs keep more of the longer spans. Jieba on Qwen mainly helps the 1–2 bin (half-word cleanup), not long spans.
