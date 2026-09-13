# 本地保留的历史结果（不进入当前投稿PDF）

旧表10–12及各自限制保留在同目录HISTORICAL_RESULTS_RETAINED.tex。以下为数据行索引；完整图注、比较条件和输入不一致限制以原TeX为准。未发布到GitHub。

- JobBERT-zh, 3M DAPT & \multirow{2}{*}{\makecell[l]{Protocol-aligned supervised\\encoder}} & \textbf{0.4331} & 0.5873 \\
- JobBERT-zh, 1M DAPT & & 0.4272 & \textbf{0.5952} \\
- \texttt{gpt-5.4} & \multirow{6}{*}{Standardized zero-shot prompt} & 0.2132 & 0.4199 \\
- \texttt{deepseek-v4-pro} & & 0.1980 & 0.3931 \\
- \texttt{kimi-k2.6} & & 0.1979 & 0.4032 \\
- \texttt{claude-sonnet-4-5} & & 0.1972 & 0.3987 \\
- \texttt{Qwen2.5-14B-Instruct} & & 0.1724 & 0.3279 \\
- \texttt{Llama-3-8B-Instruct} & & 0.0582 & 0.1178 \\
- JobBERT-zh, 1M DAPT & Gold v2, 2,601 records; three-seed mean & 0.1288 \\
- JobBERT-zh, 3M V4 & Human-label overlay on 2,601 records; frozen predictions & 0.3884 \\
- Claude Sonnet 4.5 SOP & 0.3153 & 0.4287 \\
- GPT-5.4 SOP & 0.3103 & 0.4471 \\
- Kimi k2.6 SOP & 0.3070 & 0.4244 \\
- DeepSeek v4-pro SOP & 0.2951 & 0.4131 \\
- Qwen2.5-14B SOP, parsed & 0.2498 & 0.3475 \\

历史2601参考、Gold v2、200条人工覆盖派生的2601参考和150句跨参考重评分不是相同实验；后者还有两条输入文本不一致。不得混排为当前匹配测试或将较高分数视为参考更正确。工厂encoder诊断尚待验证，已记入内部版本记录，不称为当前主实验未完成。
