# JobBERT1M：跳过正式训练

编码器与发布 CRF 的 SHA256 均与 Hub README 一致，加载路径存在。

不满足本轮「纯预训练规模消融」可比性：

1. 1M 为 100 万句 × 3 个 MLM epoch（`BertForMaskedLM`）；3M 为 `encoder_ckpt65000`（`BertModel`）。不是同一预训练阶段。
2. 两边发布 CRF 都缺少 `history.json` / 选模清单。本轮 3M 已改为重初始化任务头；即使 1M 同样重初始化，仍不能把差异解释为「只改预训练规模」。
3. 不为凑表重复训练。

不阻塞 Qwen、HEM 与论文写作。不宣称 1M vs 3M 规模消融。
