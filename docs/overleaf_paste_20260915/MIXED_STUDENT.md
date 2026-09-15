# Overleaf — pooled public-API silver (appendix; not Tables A–D)

Do **not** write “10,000 Silver sentences”. Do not change Abstract or Tables A–D. Gold150 remains the 150-sentence human overlay. These runs are **additional benchmark baselines**, not GPT distillation.

Paste `tables_H_public_api_silver.tex` after Tables E–G.

## Methods sentences (English)

An additional silver pool was labelled with protocol `silver_public_api_v1.0` (7,936 sentences; 7,676 keep after holding out `adjudication_required`). Wave1–2 used Codex CLI; Wave3 used Codex CLI for the reported contrast (the earlier website-proxy labels are retained only as a channel check); the 2,500-sentence subset still uses website-proxy labels until the Codex relabel arrives. Isolation is sentence-level. Gold150 was not used for gradients or checkpoint selection.

A further pooled baseline concatenates unique v6a_nocross B2 sentences (2,077 unique NFC) with that keep set ($n_{\mathrm{keep}}=9{,}646$; train/val/test $8{,}943/351/352$). The two silver protocols (handbook v4212 B2 and `silver_public_api_v1.0`) are training annotations for a benchmark baseline; they are not a teacher–student distillation setup. This pool must not replace the v6a_nocross 2,150 / 169 JobBERT cell.

## Results now (seed 42 unless noted; Gold150 typed exact / relaxed)

These are **Gold150** scores, not silver-dev / silver-test.

| Subset | Channel | Exact | Relaxed |
|---|---|---:|---:|
| Wave3 $n_{\mathrm{train}}=1678$ | proxy | 0.5870 | 0.7169 |
| Wave3 $n_{\mathrm{train}}=1579$ | Codex CLI | 0.5853 | 0.6991 |
| Wave1+2 $n_{\mathrm{train}}=3159$ | Codex CLI | 0.5745 | 0.6951 |
| Public-API 7117, full-dev select | mixed | 0.5883 | 0.7099 |
| Public-API 7117, TVT | mixed | 0.5732 | 0.7087 |
| Pooled 9,646 keep, Qwen (train 8,943) | two protocols | **0.5966** | 0.7126 |
| JobBERT-zh 3M CRF on 7117 | mixed | $0.2367\pm0.0015$ | — |
| JobBERT-zh 3M CRF on pooled 8,943 | two protocols | 0.2416 | — |

Qwen pooled checkpoint = epoch 1 (silver-val exact 0.7826; patience 2). Do **not** paste that 0.7826, and do not paste silver-test 0.7585.

Codex vs proxy on Wave3 is within 0.002 exact on Gold150.

## Leave blank until Codex 2500 arrives

- Swap the 2,459 website-proxy keep rows with Codex run2500, then a **second** pooled train. Do not invent that F1.

## What not to paste

- 0.5536, 0.1215, 0.5403, 0.4331, and these rows in one SOTA sentence
- “10,000”, “dual teacher”, “human cover 500”
- Silver-val 0.7826 / silver-test 0.7585
