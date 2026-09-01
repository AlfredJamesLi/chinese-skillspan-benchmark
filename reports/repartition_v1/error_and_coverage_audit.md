# Error and coverage audit (repartition_v1)

Written at freeze time, before CRF jobs finish.

- New test n=4222. Manifest SHA256: `fe195254d329ba7b596585a0e73cf3c93b320efda55d063ca72d53269ab1ceb0`.
- Scorer: `cnss-lskt-1.2.0`.
- Train/dev/test sentence-ID overlap: 0 (enforced in split builder).
- Post-ID overlap across splits: 0.
- Near-duplicate groups across splits: 0 (after text-leak repair; no F1 used).
- Qwen2.5-14B-Instruct frozen dump `output/chinese_skillspan_qwen25-14b_test_all.jsonl`: overlap **702 / 4222** new test IDs (missing 3520). **Not rescored as a complete row.** No external API. Local Qwen inference deferred so it does not block encoder CRF.
- Encoder predictions will be scored after each seed into `main_results_by_seed.csv`.
