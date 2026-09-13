# Frozen Qwen diagnostic counts and chart data

The manuscript's former Table 12 is displayed as a four-panel statistical figure. These companion files retain the full counts: type_metrics.csv, length_recall.csv, empty_reference.csv, chart_data.json and the exact archived_table.tex. The chart uses full-precision values from the existing Round2 diagnostic summary; no inference, rescoring, or model API calls are performed. No confidence intervals or significance tests are inferred from three seeds on a shared test set.

K, S and T gold support is 125, 448 and 88; L has only two spans and remains count-based. Length groups contain 346, 243 and 74 spans and may share sentences. Empty-reference sentence errors and span errors are distinct quantities. The four plotted runs are no adapter, LoRA seed 42, seed 43, seed 44. The [paper index](../PAPER_INDEX.md) identifies the final figure and its current page.

 ## Figure presentation update (2026-09-13, restored)

At the author's request, Figure 5 returns to the previous four-panel bar-chart design: grouped bars for type F1 and length-bin recall, horizontal bars for affected empty-reference sentences and false-positive spans. Grey/blue/green/orange colours and patterns identify the same four runs. The temporary dot/line/unit-dot/lollipop design is superseded. All underlying counts, full-precision values and the archived table are unchanged.
