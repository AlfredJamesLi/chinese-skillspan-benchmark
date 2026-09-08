# Qwen 协议冻结（本轮：仅 SFT）

冻结时间：2026-09-08。选模与提示均只用开发集、无检索。**未查看 Gold150 分数来选择本协议。**

本文件替代此前含 KNN / 随机示例 A/B/C 对照的草案。本轮 Qwen **只做 SFT**。不引入 SpanAnchor 适配、检索增强或其他新方法模块。沿用本项目已验证的 JSON-offset LoRA 抽取流程。

## 输出与定位

- 保留 K/S/T/L 类型及连续原文跨度。
- 不修改招聘原文。
- 输出：JSON 数组 `{"start","end","type"}`。
- 定位：Python `str` 下标 = Unicode 码点，0 起始，右开。
- 重复短语：优先使用模型给出的偏移；仅有表面串时按从左到右、尚未占用的出现次解析。不用 Gold 选位置。
- 不可解析：写入 `parse_status` / `parse_failures`，样本保留，不静默删除。

## 训练 / 推理

SFT 与 Gold 推理使用同一用户提示（系统说明 + 查询原句），**不含**训练示例。

三种子共用：同一输出协议、同一解码（`do_sample=false`）、同一输入格式、同一 `max_new_tokens=256`。

每个 run 从同一经核验的 Qwen2.5-14B-Instruct 基础权重 **新建** adapter，不从另一种子续训，不加载其他论文 / IEEE Access adapter。

本轮不加入：随机训练示例、近邻检索、ESCO 定义检索、多轮重试、概率融合、额外规则模块。

## LoRA（复用已验证配方）

r=16，α=32，dropout=0.05，目标 `q_proj k_proj v_proj o_proj`，BF16，assistant-only loss，Qwen chat template，pad=eos。表示未改，无需因目标表示重选超参。协议不依据 Gold 分数调整。

## 选模

每个训练种子：按 **开发集 typed_exact_f1** 选一个 epoch（更高者胜，差值 ≤1e-4 取更早 epoch）。不用 Gold 选 checkpoint、提示词或解析规则。

相对旧 JSON-offset v3：v3 取最后一轮、数据为 v3 1382；本轮数据为 `v6a_nocross` 2150，且按开发集选模。相对旧结果的变化不能全部归因于数据量。

## 解析诊断

合成句 + 开发集目标往返见 `PARSER_TEST_REPORT.json`（13/13 通过；Gold150 未参与）。覆盖：前导空格、中文、英文工具名、重复提及、空标、多跨度、长跨度、标点、输出截断。
