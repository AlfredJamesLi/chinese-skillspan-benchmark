# DeepSeek thinking 输出失败核查

核查日期：2026-10-05。仅重放冻结响应与评分程序；没有新增模型调用、修改预测或重做实验。

## 结论

18 例 `format_failed` 全部是**长度预算耗尽时尚未生成最终答案**。原始响应的 `finish_reason` 均为 `length`，最终 `message.content` 均为空，`reasoning_content` 均非空；HTTP 状态均为 200，未记录 HTTP/API 错误。这不是非空 JSON 的语法损坏，也不是片段提取、occurrence 或 offset 校验错误。

冻结解析器将空最终答案交给 JSON 解析，统一产生 `json:Expecting value: line 1 column 1 (char 0)`，因此把它们归为整条响应 `format_failed`。这个名称是解析结果分类，不应被解释为模型写出了 18 份错误 JSON。

## 原始证据与重放

直接读取冻结 pack 中 `01_shared_prompt/raw/deepseek-v4-pro-think8192/raw/*.json` 的 `raw_response`，并与所存 `http` 摘要逐字段核对结束原因、最终答案、reasoning 字段及 usage。每种配置都有 152 个响应文件，其中两个为 `syn-smoke-1` / `syn-smoke-2`；按冻结人工参考集 ID 排除这两个测试请求后，正式评测均为 150 个唯一响应，全部覆盖参考集。

| 核查项 | Thinking | Non-thinking |
| --- | ---: | ---: |
| 正式响应 | 150 | 150 |
| HTTP 200 | 150 | 150 |
| 记录的 HTTP/API 错误 | 0 | 0 |
| `finish_reason=stop` | 132 | 150 |
| `finish_reason=length` | 18 | 0 |
| 正常非空响应 | 124 | 142 |
| 合法空列表 | 8 | 6 |
| 部分片段被拒绝 | 0 | 2 |
| 整条格式失败 | 18 | 0 |

18 个失败响应的配置为 `thinking.type=enabled`、`max_tokens=8192`。它们记录的 completion tokens 分别为：8,192（14 例）、8,191（2 例）、8,189（1 例）、8,193（1 例）；每例的 `reasoning_tokens` 都等于 `completion_tokens`。保留这些供应方原始计数，不将其人为改成全部 8,192。结合 `length` 结束原因和空最终答案，可以确认是生成在长度限制处终止，且最终答案尚未产生；不宜称为“最终 JSON 被截成半条”。

用冻结 `00_freeze/parser_occurrence_v1_1.py` 逐条重放两种配置共 300 个正式响应，accepted spans、outcome、format_failed 均与冻结预测完全一致。Thinking 的 18 例没有任何 accepted span，也没有进入逐片段拒绝阶段；non-thinking 的两例部分拒绝各有一个 overlap conflict，属于不同问题。

关键输入哈希：

- Parser：`a88e8bd740ac560cacdf777ae95119de34e573dee07a15ba2a52b84ac9e65d05`
- Human reference：`ca8db0bc386c24543fec845d42ea8e24883eb67b8ce75129ac1768c5c0310fd0`
- Thinking predictions：`c37436b95c0fe2709431d1b719f7328c2f2cc19472173a9f70516a9af10ce7eb`
- Non-thinking predictions：`29a0bfb0ca9c382d5a3973da00a8f491347e818fdc560083c829149366dc51a7`

## 对评分的影响

所有 150 句继续计分，18 个失败响应以空预测计入。失败句中 17 句共有 180 个参考片段，全部计为 FN；另 1 句参考标注本身为空，对 TP/FP/FN 不贡献计数。不能把这 18 句直接删除后替换主结果。

按发布的 scorer 对冻结 accepted spans 重新聚合，结果与现有记录一致：

| 配置 | Exact TP / FP / FN | Exact P | Exact R | Exact F1 | Relaxed F1 |
| --- | --- | ---: | ---: | ---: | ---: |
| Thinking | 335 / 135 / 328 | 0.712766 | 0.505279 | 0.591350 | 0.670786 |
| Non-thinking | 426 / 228 / 237 | 0.651376 | 0.642534 | 0.646925 | 0.760820 |

这些分数包含输出预算导致的失败。它们不能单独证明 thinking 本身降低抽取质量，也不能把全部性能差异归因于截断，因为成功回答上的预测也可能不同。

## 稿件中保留什么

正文无需详述内部字段、每条失败 ID、解析异常字符串及完整输出状态表；这些工程细节可放在本审计附件或 GitHub。原 Table 10 的分类计数是正确的，但仅写“format failure”容易让读者误解原因。

附录应保留一条可核验的评分说明，例如：

> In the thinking configuration, 18 responses reached the configured output limit before producing a final answer and were scored as empty predictions; all 150 reference sentences remained in the evaluation.

预算、全样本计分和空预测处理会影响结果解释，不能因精简而一并删除。逐项审计支持的是 18/18，不应继续写成“mostly associated with length”。移除正文中对 thinking 与 non-thinking 优劣的泛化解读合理；必要时仅保留各配置的描述性结果和记录的预算。

## 能否不新增调用进行修复

**不能通过重解析修复这 18 个最终答案。** 冻结响应的 final content 是空字符串，缺少可供恢复的最终 JSON。提取 reasoning 中的候选内容、复制另一配置的预测，或用参考答案填补，都会改变输出协议和预测，不能称为修正解析器。

无需新增调用便可开展“在相同 132 个 thinking 已完成响应的句子上，对两种配置重新计分”的事后条件性诊断；它必须注明按某一配置的完成状态选择样本，不能替代全部 150 句的主评分，也不构成对更大预算下 thinking 效果的估计。本次未新增该条件性分析，以保持工作范围集中在失败原因与既有结果核验。

## 交付与复现

- `DEEPSEEK_FAILURE_AUDIT.json`：配置、哈希、聚合状态、重放检查、完整精度评分。
- `DEEPSEEK_RESPONSE_METADATA.csv`：两种配置共 300 个正式响应的非文本元数据。
- `DEEPSEEK_FORMAT_FAILURE_METADATA.csv`：18 个失败响应的非文本元数据及原响应哈希。
- `audit_deepseek_failures.py`：可移植的本地核验脚本。

CSV 不含原句、模型输出正文、reasoning 正文、请求头、请求 ID 或访问密钥。保留的 ID 为冻结数据中的记录标识，路径为 pack 内相对路径。

取得冻结 pack 和发布的 scorer 后运行：

```text
python audit_deepseek_failures.py --pack PATH_TO_FROZEN_PACK --scorer PATH_TO_score_lskt.py --out audit_output
```

脚本以参考集 ID 选择正式响应，读取原始响应体，重放原解析器并核对预测，最后只导出元数据和聚合分数。评分使用现有精确与宽松匹配函数，不改变匹配规则。
