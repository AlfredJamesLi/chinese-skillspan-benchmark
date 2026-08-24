# Dual eval (sandbox, not for paper)

**Do not copy into `confirmed-results.md` or the PDF.** Same JobBERT-zh CRF pred throughout (`crf_lskt_v4_silver_seed42/test_pred.jsonl`), trained on **rule_v4 train**, not Codex.

| Test gold | typed P / R / F1 | collapsed F1 |
|---|---|---:|
| Gold v2 (frozen official) | 0.1543 / 0.0830 / **0.1079** | 0.1187 |
| LSKT v4 **rule** silver (before Codex) | 0.3442 / 0.2938 / **0.3170** | 0.3418 |
| LSKT v4 **Codex** silver (2601 IDs, after 50+51 merge) | 0.1257 / 0.1236 / **0.1246** | 0.1366 |

Codex test: 50 `codex_sample50` + 2551 `codex_batches51`. Alignment OK. 51-batch merge: 1766/2551 changed vs rule, 1176 empty, 0 align errors, 0 id problems.

The 0.3170 was train/test same rule. After Codex rewrote the test labels (more empty, shorter/split spans), the same pred falls to ~0.12, close to Gold v2. Encoder was not retrained.
