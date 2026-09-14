# Wave2 Silver 完成报告

已完成 73/73 批、1810/1810 条，原始批号 0182–0362。运行器已正常退出，后台跟进 wave2-silver 已暂停。仅处理 Wave2。

## 结果

| 项目 | 数量 |
|---|---:|
| 记录 | 1810 |
| 跨度 | 3861 |
| S / K / T / L 跨度 | 2108 / 995 / 738 / 20 |
| candidate_complete | 1159 |
| adjudication_required | 110 |
| confirmed_empty | 541 |
| 待裁决事项 | 137（scope 47、type 83、boundary 7） |
| 唯一精确匹配的机械 offset 更正 | 6 |

73 批均通过 schema、ID 顺序与唯一性、Unicode 码点左闭右开偏移、原文切片、非重叠、status/issues 一致性、scope 排除及源映射检查。独立复核确认所有实际请求包含完整公开 prompt、正确本批输入和每 10 码点位置参考；所有输出只进行了留痕的机械 offset 更正，无后处理语义、文本或标签变更，无模型工具调用。

所有结果仍是候选 Silver。110 条记录的 137 个待裁决事项完整保留；类型待决 S 是占位值。格式校验不代表人工准确率，未进行人工准确率评估。

## 调用与耗时

使用指定 gpt-6-astra/high、现有 ChatGPT 登录和一个串行 Codex CLI 运行器。73 次成功语义调用；另有首批 1 次外层沙箱证书错误的失败启动，未返回语义结果或 turn.completed 用量，其现场已保留。经正常权限流程重启，同批实际请求逐字节一致。

成功调用时段（香港时间）：2026-09-14 01:34:55 至 2026-09-14 05:11:34；墙钟 12999.15 秒，约 3 小时 36 分 39 秒。成功批次 CLI 累计耗时 12991.15 秒，约 3 小时 36 分 31 秒。

| 实际 CLI usage 字段 | Token |
|---|---:|
| input_tokens | 1,749,825 |
| cached_input_tokens | 590,336 |
| cache_write_input_tokens | 0 |
| output_tokens | 384,738 |
| reasoning_output_tokens | 225,762 |

这些数值从 73 个真实 turn.completed 事件重新汇总，各字段按 CLI 原样报告；不把缓存或推理字段再相加。不是独立 API 账单，也不能精确归因共享账户额度。未调用独立付费模型 API，未自动重置或购买额度。

## 交付文件

本报告目录为 `C:\Users\James Lee\Documents\Codex\2026-09-14\chinese-skillspan-wave2-astra\outputs\wave2_codex_astra`。

- WAVE2_VALIDATED.jsonl：1810 条校验后候选标注，按派生输入原顺序。
- WAVE2_SOURCE_MAPPING.jsonl：1810 条源批次及 ID 映射。
- WAVE2_ADJUDICATION_ISSUES.jsonl：137 条待裁决事项。
- WAVE2_OFFSET_CORRECTIONS.jsonl：6 条机械偏移更正。
- FINAL_SUMMARY.json：全波计数、耗时和 usage。
- FINAL_PROVENANCE_AUDIT.json：实际请求、原始输出、更正、CLI 事件的独立复核与哈希。
- batches/：每批输入、请求、CLI 事件、stderr、原始 JSON、校验后 JSON、映射、校验报告、更正日志、元数据及耗时。
- REPRODUCTION.md：完整复现和断点续跑说明。全波已完成，无需重新标注；复核命令为在任务根目录执行 `C:/ProgramData/anaconda3/python.exe work/audit_wave2.py --final`。

合并结果 SHA256：`4b5a218af4d5d6d616b856789b2bc0cdb07e3e4fd54dfba76b9ce064fa9b8496`。

准备阶段已核验 Wave2 与 Wave1、Wave3、held2500 均无 ID 交集。未修改 Wave1 工作区、源仓库或 Gold，未推送 GitHub，未训练，未进入其他波次。
