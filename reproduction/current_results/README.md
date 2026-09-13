# Current manuscript results

- [Six inference configurations, Table 5](inference.csv): readable display names and original system identifiers; numerical fields copied from the existing repository result CSV.
- [Three Qwen LoRA runs, Table 11](qwen_runs.csv): seeds 42/43/44 with selection-only development scores kept separate from test results.

Current Table 6A pairs Qwen no adapter (exact F1 **0.3612**) with B2 LoRA (**0.5403 ± 0.0354**, full-precision mean/sample SD over three seeds). Table 6B reports JobBERT B1 **0.1422 ± 0.0138** and B2 **0.5536 ± 0.0054**. JobBERT compares supervision and checkpoint selection on matched texts; Qwen compares adaptation under a fixed inference protocol. The two panels are not a controlled architecture ranking.

The legacy `tables/gold150_shared_guidelines_qwen_sft.csv` places its combined mean/SD string in the relaxed-F1 column of the summary row, although the note identifies it as exact F1. That historical file is retained unchanged. Use the explicit per-seed exact-F1 column above and mean/sample SD for the current summary. No model was rerun or rescored for these display tables.
