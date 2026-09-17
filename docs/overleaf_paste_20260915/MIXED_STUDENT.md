# Overleaf — pooled public-API silver (appendix; not Tables A–D)

Do **not** write “10,000 Silver sentences”. Do not change Abstract or Tables A–D. Gold150 remains the 150-sentence human overlay. These runs are **additional benchmark baselines**, not GPT distillation.

Paste `tables_H_public_api_silver.tex` after Tables E–G.

## Methods sentences (English)

An additional silver pool was labelled with protocol `silver_public_api_v1.0` (7,936 sentences; 7,676 keep after holding out `adjudication_required`). The 2,500-sentence subset has Codex CLI labels (`RUN2500_VALIDATED.jsonl`; 2,353 keep after `adjudication_required`). Isolation is sentence-level. Gold150 was not used for gradients or checkpoint selection.

A further pooled baseline concatenates unique v6a_nocross B2 sentences (2,077 unique NFC) with public-API keep. The **proxy** pool ($n_{\mathrm{keep}}=9{,}646$; train 8,943) is Gold150 exact 0.5966 / relaxed 0.7126. The Codex-swap pool ($n_{\mathrm{keep}}=9{,}540$; train 8,842) reuses that split for IDs that remain in keep and is Gold150 exact 0.5854 / relaxed 0.7032. The two silver protocols are training annotations for a benchmark baseline; they are not a teacher–student distillation setup. This pool must not replace the v6a_nocross 2,150 / 169 JobBERT cell.

## Results now (seed 42 unless noted; Gold150 typed exact / relaxed)

These are **Gold150** scores, not silver-dev / silver-test.

| Subset | Channel | Exact | Relaxed |
|---|---|---:|---:|
| Wave3 $n_{\mathrm{train}}=1678$ | proxy | 0.5870 | 0.7169 |
| Wave3 $n_{\mathrm{train}}=1579$ | Codex CLI | 0.5853 | 0.6991 |
| Wave1+2 $n_{\mathrm{train}}=3159$ | Codex CLI | 0.5745 | 0.6951 |
| Public-API 7117, full-dev select | mixed | 0.5883 | 0.7099 |
| Public-API 7117, TVT | mixed | 0.5732 | 0.7087 |
| Pooled 9,646 keep, Qwen (train 8,943, **proxy** run2500) | two protocols | **0.5966** | 0.7126 |
| Pooled 9,540 keep, Qwen (train 8,842, **Codex** run2500) | two protocols | **0.5854** | 0.7032 |
| JobBERT-zh 3M CRF on 7117 | mixed | $0.2367\pm0.0015$ | — |
| JobBERT-zh 3M CRF on pooled 8,943 (**proxy**) | two protocols | 0.2416 | — |
| JobBERT-zh 3M CRF on pooled 8,842 (**Codex**) | two protocols | 0.2317 | — |

Both Qwen pooled checkpoints = epoch 1 (patience 2). Do **not** paste silver-val or silver-test (proxy silver-val 0.7826 / silver-test 0.7585; Codex-swap silver-val 0.8325 / silver-test 0.8092).

Codex vs proxy on Wave3 is within 0.002 exact on Gold150. The pooled Codex swap is 0.0112 exact below the proxy pool; more run2500 rows were held for adjudication (147 vs 41).

## What not to paste

- 0.5536, 0.1215, 0.5403, 0.4331, and these rows in one SOTA sentence
- “10,000”, “dual teacher”, “human cover 500”
- Silver-val 0.7826 / 0.8325 or silver-test 0.7585 / 0.8092
