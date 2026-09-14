# wave1 候选标注完成报告

**wave1 的1810条已全部生成候选标注并通过本地校验；完成后停止，未启动wave2或wave3。**

| 波次 | 记录 | 25条派生批数 | 末批 | 本次完成 |
|---|---:|---:|---:|---|
| wave1 | 1810 | 73 | 10 | 73批全部完成 |
| wave2 | 1810 | 73 | 10 | 未开始 |
| wave3 | 1816 | 73 | 16 | 未开始 |
| 合计 | 5436 | 219 | — | 1810条，余3626条 |

原始组织方式为544批，每批10条、最后6条。派生批按波次分组，不跨波，原始输入保留不变。

## 执行与版本

仓库下载目录：`C:\Users\James Lee\Documents\Codex\2026-09-13\chinese-skillspan-silver-https-github-com\work\cnss-silver-codex-astra-5436`。

分支main；实际提交`e09f608964f3510d5de4a62e5f6d96472904556c`；公开提示词SHA-256 `b6223e9a2e9b02afa19cba79ba908766d9240acb233723fbe6f53b40e6b04fd6`；schema SHA-256 `b3e7745a4579f7652135b9295bbafeb2f4934df3896e98034ab4f476dba8b8ec`。

首批25条复用此前已校验结果，没有重跑。第2–12批由当前Codex Astra会话进行语义标注；用户随后明确授权串行命令行模式，第13–73批使用现有ChatGPT登录的Codex CLI，指定gpt-6-astra、高推理强度。每次只有一个批次，已核验相邻调用时间无重叠。

Codex CLI版本0.154.0-alpha.6.2。API密钥未读取或导出，未使用独立付费模型API或仓库中的第三方端点。CLI忽略用户配置、指定OpenAI提供方和ChatGPT登录，只读模型沙箱，并禁用shell、web search和子代理工具。没有温度或max_tokens等独立API调用参数。

所有语义跨度、类型、状态及争议理由均来自Codex模型判断。程序只读取原文、提供机械码点位置参考、序列化和校验。第14批起请求附原文每10个Unicode码点的起始位置参考，不含旧标签、Gold或实验答案，不改变原文或公开提示词。各CLI请求全文保存在相应cli_attempt目录中。

第16批原始输出采用成组type issue，最初被本地过严的“一条issue必须等于一个span”检查拦住。核对公开协议后，检查改为允许争议片段包含一个或多个S占位跨度，原始模型语义未改、未重跑。其他本地更正均保留在更正记录中。

## 结果与检查

- 唯一ID：1810；对保留2500条的ID交集为0。
- 跨度总数：3947；类型统计：{"T": 718, "K": 1029, "S": 2175, "L": 25}。
- 状态统计：{"candidate_complete": 1224, "adjudication_required": 103, "confirmed_empty": 483}。
- 待裁决事项：117项，详见ADJUDICATION_QUEUE.json。
- schema、数量/顺序/ID、原文切片、Unicode码点偏移、非重叠及状态一致性检查全部通过。
- 原始181个10条批次均完整覆盖；仅保存来源映射和覆盖清单，没有写入源batches_out。
- 原始源文件及全部219个派生输入哈希均保持不变。源Git工作区无修改。
- CLI输出机械偏移修正：5处，只允许唯一、完全相同的原文匹配；另有2处重复词位置由本会话模型读取完整原文后明确指定，详见POSITION_OVERRIDES.json。两类均未模糊匹配、未默认首次出现、未改跨度文本或标签。

candidate_complete表示本次候选判断完整，不表示人工确认；adjudication_required保留范围、边界或类型争议，类型未决S仅为占位，不能当作最终训练标签。格式校验通过不等于人工准确率通过。本次没有正式人工抽检、Gold评估或模型训练。

## 时间与共享额度

本轮本地执行记录起点（UTC）：2026-09-13T15:50:27.751676+00:00；整波核验完成：2026-09-13T18:56:39.476718+00:00；记录区间用时186.2分钟。包括等待、本地检查及中途检查器修正，首批25条是此前结果复用。

CLI已校验批次共61批，调用耗时合计170.7分钟，按实际CLI处理记录平均6.78秒/条。此为本任务观测，不能据此断言普遍快于其他端点。

CLI返回的真实用量事件汇总：{"input_tokens": 1452736, "cached_input_tokens": 270464, "cache_write_input_tokens": 0, "output_tokens": 318731, "reasoning_output_tokens": 187264}。这些是Codex事件计数，不是独立API账单或本批精确费用。账户额度快照：{"observed_utc": "2026-09-13 18:56:43 UTC", "plan": "pro", "ordinary_usage_allowed": true, "windows": [{"usedPercent": 35, "windowDurationMins": 10080, "resetsAt": 1789806318, "remainingPercent": 65}], "secondary_window": "unavailable", "shared_across_windows": true, "reset_credits_consumed": 0, "additional_credits_purchased": false}。所有窗口共享额度，不把账户前后百分比变化归因于本任务的精确消耗；未重置、购买额度。

## 文件与后续

- batches/batch25_0001至batch25_0073：输入、原始模型输出、validated_output.json、来源映射及校验报告。CLI批次另有运行时间、请求全文和原始事件。
- BATCH_OUTPUT_INDEX.json：73批输出及输入哈希。
- ORIGINAL_BATCH_COVERAGE.json：回到原始181批的ID和位置映射。
- ADJUDICATION_QUEUE.json：全部待裁决事项及其原文，不是另抽的人工检查样本。
- PREVALIDATION_CORRECTIONS.json和OFFSET_CORRECTIONS_ALL.json：显式定位及机械偏移更正。
- PROGRESS.json与outputs/LOCAL_EXECUTION_STATUS.json：独立本地完成记录。

源仓库的波次状态仍保留其下载时状态：{"wave1": "ready", "wave2": "ready", "wave3": "ready"}。未提交、推送或合并Silver，未修改论文、Gold、历史标注、实验清单、解析器或评分器。

下一波入口为prepared_25/wave2/batches/batch25_0001.json。下一波未授权自动执行；本次到此停止。

命令行模式、结构化输出及复用现有登录方式可见[官方Codex文档](https://learn.chatgpt.com/docs/non-interactive-mode)。本任务的实际调用和结果以本地元数据及校验报告为准。
