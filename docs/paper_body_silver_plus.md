# Manuscript body — Silver-plus methods and results

English draft for the PeerJ Computer Science **main text** (not the laboratory Chinese notes).  
Scorer: `cnss-lskt-1.2.0`. Standard deviations are **n=3 sample SD**, not test-set confidence intervals.  
Human reference set (artifact **Gold150**) SHA-256: `ca8db0bc386c24543fec845d42ea8e24883eb67b8ce75129ac1768c5c0310fd0`. File `gold150_test.jsonl` is not renamed.

**Silver-plus** is the resource release-layer name for teacher-generated silver annotations (automated validation and sampled human review). Plus is not a recognised quality grade; the layer is not item-by-item human verified and is not near-Gold.

A **150-sentence human-annotated reference set** is defined here once. Later short form: **the human reference set**. It is not independent dual-blind coding of all 150 sentences. Independent-coding evidence applies to the corresponding 50-sentence **initial independent-coding study**. Reader names: [`TERMINOLOGY_CROSSWALK.md`](TERMINOLOGY_CROSSWALK.md).

These numbers **must not** be subtracted from, or ranked in the same main table as, V4 hybrid 2601 JobBERT-zh 3M **0.4331** or official zero-shot Qwen SOP extract **0.1724**. Human-reference IDs sit inside hybrid 2601; scoring the same student again on full 2601 is not an independent test.

Isolation wording: **sentence-level isolation (extended)**. Do not call it document isolation after v4.

---

## 1. Two students, two fine-tuning regimes

JobBERT-zh and Qwen2.5-14B-Instruct are **not** the same fine-tuning recipe. They do not share a prompt, a loss, or a decoder.

| | JobBERT-zh 3M (paper Gold150 main) | Qwen2.5-14B-Instruct (Gold150 supplement) |
|---|---|---|
| What is adapted | Full Bert+CRF (encoder + emission + CRF) | LoRA adapters only |
| Supervision | Character BIO tags (`O`, `B/I-L/K/S/T`) | Assistant JSON `[{"start","end","type"}]` |
| Prompt | **None.** The model never sees an instruction. | **Yes.** One fixed extraction instruction; **no** in-context examples |
| Inference | CRF Viterbi, then first-subword → character | Greedy generation (`do_sample=false`), then JSON parse |
| Official SOP extract 0.1724 | Not this protocol | **Not this protocol** (0.1724 is zero-shot SOP, no LoRA) |
| B1 vs B2 | Same characters, different BIO (earlier vs revised supervision) | Same instruction, different target JSON |

B1 and B2 are condition codes for **earlier** versus **revised** supervision on identical sentences. The comparison is the package “handbook + teacher + adjudication”, not two prompts and not a teacher-architecture ablation.

---

## 2. JobBERT-zh — sequence labelling, no prompt

**Initialisation (v3–v6a main runs).** Encoder + CRF from the public `AlfredJames/jobbert-zh` checkpoint, including released `crf/best.pt`. A new independence claim **cannot** inherit that CRF: the original 3M selection `history.json` is missing. HEM (below) re-initialises the CRF and is a different student.

**Input.** Characters (`tokens = list(sentence)`), WordPiece with `is_split_into_words=True`, `max_len=256`. Nine-way joint LSKT BIO. No handbook text, no system message, no few-shot.

**Objective.** Negative log-likelihood of the CRF. Decode with Viterbi; continuation subwords and CLS/SEP are ignored when mapping back to characters.

**Optimiser (all v3–v6a JobBERT runs).** AdamW, learning rate \(2\times10^{-5}\), weight decay 0.01, batch size 16, at most 6 epochs, patience 2, 10% linear warmup, gradient clip 1.0. Seeds 42 / 43 / 44. Checkpoint = argmax **frozen-dev typed exact F1** (tie: keep the earlier epoch if \(\Delta\le10^{-4}\)). Gold150 is not used for training, early stopping, or prompt choice (there is no prompt).

v6a B2 seed 42 ran 810 steps; selected dev typed exact was about 0.65. That is a development figure, not a paper test number.

**HEM (supplement only).** Same 3M DAPT encoder, **freshly initialised** CRF (released `best.pt` refused). Equal-\(n\) **conflict-origin / non-conflict-origin / mixed** source contrast (`H_468` / `E_468` / `M_468`), 564 unique sentences per condition. The **initial teacher-label review cohort** (artifact **A100**) is the shared Silver-plus base; it is not promoted to Gold. HEM does **not** replace the full v6a main cell and must not be mixed with generation pools H730 / E1621.

---

## 3. Qwen2.5-14B — LoRA SFT with a short JSON-offset prompt

**Base.** Read-only `Qwen2.5-14B-Instruct` (14.7B). No IEEE Access adapter and no adapter reused across seeds. Each seed starts a **new** LoRA.

**Prompt (train = infer).** One user message, **zero demonstrations**. The chat template is Qwen’s. Loss is **assistant-only** (all prompt tokens labelled `-100`).

Official extension prompt (v6a_nocross):

```
从中文招聘句子中抽取能力跨度。类型只能是 L（语言）、K（知识）、S（技能）、T（特质/软技能）。只输出一个 JSON 数组，元素为 {"start":整数,"end":整数,"type":"S"}。偏移是原文 Unicode 码点，0 起始、左闭右开。不要改写招聘原文。同一短语多次出现时必须给出该次出现的确定偏移。没有跨度则输出 []。
句子：{sentence}
输出：
```

The target is a JSON array of Unicode code-point offsets, half-open, 0-based. Empty sentences target `[]`. v3 used a slightly shorter instruction (same schema; it did not spell out “0-based / do not rewrite / repeated phrases need a definite offset”).

**This is not official SOP extract v4.** Frozen Instruct + this JSON prompt without LoRA scores Gold150 exact **0.0000**. That cell is **not** 0.1724.

**LoRA / generation.** \(r=16\), \(\alpha=32\), dropout 0.05, modules `q_proj k_proj v_proj o_proj`, BF16. Learning rate \(1\times10^{-4}\), per-device batch 1, gradient accumulation 16 (effective batch 16), 6 epochs. Inference: `do_sample=false`, `max_new_tokens=256`. Unparseable rows are kept, not dropped. No retrieval, no random demos, no ESCO lookup, no retry, no score fusion.

**Two Qwen rounds (must not be collapsed).**

| Round | Data | Checkpoint | Gold150 conditions |
|---|---|---|---|
| v3 | B2 1382 / 169 (B1 also run) | **Last epoch only** | B1 and B2 |
| Extension | `v6a_nocross` B2 2150 / 169 | **Dev typed exact** (all three seeds chose epoch 6) | **B2 only** |

The move from 0.0788 to 0.1215 changed **both** data and selection. Do not attribute the whole delta to volume. The B2-only extension **cannot** independently confirm B2 > B1.

---

## 4. Silver-plus data versions

Silver-plus remains the release-layer name. Counts below are list versions of teacher-generated silver annotations, not a claim that every row was human-verified.

| Version | train / dev | Role |
|---|---|---|
| v3 | 1382 / 169 | Strict document isolation. JobBERT B1/B2 and Qwen JSON-offset. |
| v4 | 1913 / 169 | Sentence-level expansion. JobBERT only. |
| v5 | 2200 / 169 | Plus exact-duplicate extras (includes 44 copies of frozen-dev text). JobBERT only. |
| **v6a (JobBERT main)** | **2156 / 169** | Drop those 44 from train. **Paper Gold150 main config.** |
| v6b | 2200 / 132 | Cleaner dev; B2 weights equal v5. No new B2 evidence. |
| Extension list | 2150 / 169 | `v6a_nocross`: drop 6 train IDs after 3 whole-sentence NFC collisions. Does not edit v6a files. |

Gold150 ∩ train/dev IDs = 0. Hold-82 stayed out of training ([PR #1](https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/pull/1)). The human reference set = 100-sentence challenge cohort (`gold100_page1`) + 50-sentence calibration cohort (`iaa50`). Artifact aliases Challenge-100 / Audit-50 / IAA-50 remain valid identifiers; do not mix the calibration split with later audits, and do not treat the full 150 as an independent dual-blind study.

---

## 5. Results for the paper body

### Table A — already published / reproduced (other test, other protocol)

Keep in the **existing** V4 hybrid 2601 table. Do not add Gold150 rows here.

- JobBERT-zh 3M v4 + jieba typed exact **0.4331** (local 0.433118)
- JobBERT-zh 1M v4 + jieba **0.4272**
- ChatGPT dump + jieba exact **0.2854** / relaxed **0.6249**
- Qwen2.5-14B official SOP extract (no LoRA) **0.1724**

### Table B — Gold150 JobBERT-zh 3M (this work, main)

| Version | B1 exact | B2 exact |
|---|---|---|
| v3 1382/169 | 0.1390±0.0112 | 0.5299±0.0105 |
| v4 1913/169 | 0.1398±0.0033 | 0.5436±0.0031 |
| v5 2200/169 | 0.1365±0.0077 | 0.5540±0.0041 |
| **v6a 2156/169** | 0.1422±0.0138 | **0.5536±0.0054** |
| v6b 2200/132 | 0.1332±0.0052 | 0.5540±0.0041 (= v5 B2) |

v6a B2 Gold150 relaxed **0.6890±0.0085**. Challenge cohort (`gold100_page1`) **0.5803±0.0036**. Calibration cohort (`iaa50`) **0.5071±0.0092**. Type exact ≈ L/K/S/T = 0.867 / 0.491 / 0.555 / 0.616.

On v3, B2−B1 ≈ **+0.391**. From v3 to v6a, B2 volume ≈ **+0.024**. Allowed wording: the observed B2-vs-B1 gap is larger than the volume gap in this expansion. Do **not** write “label quality far exceeds data size”.

Released CRF without Silver-plus continuation (B0) is Gold150 exact **0.1745** and is **not** an independent test.

### Table C — Gold150 Qwen JSON-offset LoRA (supplement)

| Data / selection | Condition | exact | relaxed |
|---|---|---|---|
| v3 1382, last epoch | B1 | 0.0162±0.0056 | 0.2513±0.0120 |
| v3 1382, last epoch | B2 | 0.0788±0.0108 | 0.4166±0.0056 |
| v6a_nocross 2150, dev select | B2 only | **0.1215±0.0092** | **0.4459±0.0237** |

Extension seeds 42/43/44 exact: 0.1313 / 0.1203 / 0.1129. Challenge cohort 0.1224±0.0105; calibration cohort 0.1199±0.0073. Parse failures 4–5/150. Empty-label false positives 1–2. exact ≪ relaxed is a **boundary / localisation** gap, not parse collapse. Type exact means ≈ T 0.22, K 0.11, S 0.10; L has only two gold spans.

Do not write that Qwen caught up with JobBERT, that this round independently proves B2>B1, or that 0.12 is comparable to SOP **0.1724**.

### Table D — HEM equal-\(n\) JobBERT (supplement)

DAPT encoder + reinit CRF; 564 sentences; sample seed 20260908.

| Condition | exact | relaxed |
|---|---|---|
| H_468 | 0.4541±0.0103 | 0.6041±0.0096 |
| E_468 | 0.4345±0.0235 | 0.5776±0.0237 |
| M_468 | 0.4562±0.0236 | 0.6089±0.0281 |

H−E ≈ 0.020, smaller than E’s sample SD 0.024. Conclusion: equal-\(n\) **conflict-origin vs non-conflict-origin** contrast only. Not difficulty truth, not a replacement for 0.5536, not continued training of the released CRF, and not a restatement of pools H730 / E1621.

JobBERT-zh 1M × Silver-plus was **not** run (different DAPT recipe; no CRF selection history).

---

## 6. Appendix-only follow-ups (do not rewrite Tables A–D)

Official Table C remains P0 JSON-offset SFT, Gold150 exact **0.1215±0.0092**. Scores live in [`notes/gold150_followups_20260909/`](../notes/gold150_followups_20260909/README.md). Overleaf-synced TeX: [`notes/silver_plus_followups_20260909/tables_EFG_appendix.tex`](../notes/silver_plus_followups_20260909/tables_EFG_appendix.tex).

### Table E — P1 prompt contrast (does not replace P0)

Same `v6a_nocross` 2150/169, same LoRA budget, seeds 42/43/44. Only the instruction changes (system role + JSON-wrapped sentence; design in [`docs/qwen_lskt_sft_v1_proposal_20260909.md`](qwen_lskt_sft_v1_proposal_20260909.md)). Select on frozen-dev $k=0$. Same checkpoint decoded at $k=0$, random $k=3$, and $k$NN $k=3$. Gold150 was not used for gradients, neighbours, or selection.

| Condition | Gold150 exact | Gold150 relaxed |
|---|---:|---:|
| Official P0 (reused, not retrained) | **0.1215±0.0092** | 0.4459±0.0237 |
| P1 $k=0$ | 0.1455±0.0196 | 0.4905±0.0109 |
| P1 random $k=3$ | 0.0452±0.0067 | 0.3507±0.0085 |
| P1 $k$NN $k=3$ | 0.0315±0.0047 | 0.3491±0.0122 |

P1 $k=0$ seeds: 0.1293 / 0.1399 / 0.1673. Mean +0.024 versus P0, but the n=3 sample SDs overlap (seed 42 is slightly below that seed’s P0 0.1313). Adding three demonstrations collapses exact F1; exact ≪ relaxed remains a boundary / localisation gap. Do **not** put 0.1455 into Table C.

### Table F — frozen V4/SOP predictions on Gold150 (not a new API)

The 150 Gold IDs sit inside hybrid 2601. Same frozen SOP-extract v4 predictions, new human gold, raw spans, no jieba. Official `gpt-4o`+SOP was never run. Do not rank against JobBERT student 0.5536 or mix with the older ChatGPT `@@span##` dump.

| System (SOP extract v4) | exact | relaxed |
|---|---:|---:|
| Claude Sonnet 4.5 | 0.3153 | 0.4287 |
| GPT-5.4 | 0.3103 | 0.4471 |
| Kimi k2.6 | 0.3070 | 0.4244 |
| DeepSeek v4-pro | 0.2951 | 0.4131 |
| Qwen2.5-14B (local, parsed) | 0.2498 | 0.3475 |

Older ChatGPT `@@span##` dump on the same gold: 0.2614 raw / 0.2721 jieba. That is a different prompt, not Table A’s 0.2854 (hybrid 2601 + jieba).

### Table G — watermark peel + retrain (no lift)

About 1% of Silver-plus train sentences carry `macrodatas.cn` / 马克数据网. Gold150 has **0**. A **new** 2138/168 list was stripped and retrained; official v6a 2156/169 and `v6a_nocross` 2150/169 were not overwritten. The cleaned list also dropped empty-ad rows and five punctuation NFC collisions, so this is not a pure watermark ablation.

| Condition | Official | After peel |
|---|---:|---:|
| JobBERT B2 | 0.5536±0.0054 | 0.5509±0.0054 |
| JobBERT B1 | 0.1422±0.0138 | 0.1507±0.0062 |
| Qwen P0 | 0.1215±0.0092 | 0.1071±0.0102 |
| HEM-E | 0.4345±0.0235 | 0.4355±0.0250 |

Do **not** write that peel-cleaning improved the main cells, and do not rewrite Tables B–D from this row.

---
## 7. Limitations that stay in the main text

- The human reference set is not a freshly blinded test after several laboratory rounds, and the full 150 sentences are not an independent dual-blind coding.  
- JSON-offset LoRA ≠ official SOP extract 0.1724.  
- v3–v6a JobBERT inherit the released CRF; independence is unproven.  
- HEM is one sample of conflict-origin / non-conflict-origin / mixed conditions; it does not estimate sampling uncertainty.  
- Extension Qwen is B2-only.  
- JobBERT-zh 1M Silver-plus was skipped.  
- P1 $k=0$ is a mean lift of +0.024 with overlapping sample SDs; demonstrations hurt exact F1. It does not replace Table C.  
- A crawler watermark is present in about 1% of Silver-plus train sentences; stripping it and retraining did not raise the official cells.

Score archives (no weights): [`notes/silver_plus_extensions_20260908/`](../notes/silver_plus_extensions_20260908/README.md), [`notes/gold150_followups_20260909/`](../notes/gold150_followups_20260909/README.md).  
Scripts: `scripts/train_jobbert_phase1.py`, `scripts/train_qwen_ext_sft.py`, `scripts/qwen_ext_protocol.py`.
