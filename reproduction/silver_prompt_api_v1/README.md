# Chinese-SkillSpan Silver 标注：公开 API 提示词包

版本：silver_public_api_v1.0（2026-09-13）。文档与离线格式检查已完成；尚未调用模型、进行标注质量试验或验证代理兼容性。

## 文件与使用顺序
1. silver_prompt.txt：完整中文系统提示词。用于新 API 标注，不是原始冻结提示词。
2. user_template.txt：用户消息模板；以 JSON 序列化后的 example_input.json 同类对象替换 {{INPUT_JSON}}。
3. output_schema.json：结构化输出约束；example_input.json / example_output.json 为人工编写的格式示例，不是模型实验结果，不默认加入正式提示词。
4. run_config.json：拟采用设置，不是已经执行的运行记录。
5. API_GUIDE.md：官方 API 与代理调用的组装和留痕要求。
6. CHANGES.md：表达整理和实际协议变化。
7. archive/：历史提示词原字节副本及当时的来源说明。来源说明中的“公开同步待完成”等内容是历史状态，不是当前 GitHub 状态核验。

## 与旧数据的关系
最初 100 条使用 silver_plus_v4210_rev1；随后 2,351 条使用 silver_plus_v4212_rev2。历史 rev2 文件仍含“草案”“未经批准”文字，但当时来源说明记录其获批后按原字节执行，因此保留原文及 SHA-256。
旧流程是在 Codex 持续会话中分批选择语义跨度并通过程序序列化偏移，不能描述为每批独立 API 调用。历史模型身份主要来自会话配置，不能替代服务端路由证据。
本次新增 API 版更改了消息组织、输出结构和元数据记录方式。继承标注规则并不意味着能逐条重现旧标签。

## 规则与案例
本包以 B.sop_v4.2.12 / 冻结 rev2 为规则基础；学历、经验代理和部分 K/S/T 映射属于项目操作定义，不宣称为 ESCO 逐项官方标签。
系统提示词含历史开发/裁决案例，不能将这些案例描述为未见独立测试。E01–E05 的历史编号对应关系见 CHANGES.md。
运行时不自动打开 URL、额外手册或本地项目文件。使用其他手册或新增示例需要重新冻结版本。

## 正式生成与人工检查
先用拟固定配置开展小批试运行，核验输出格式、偏移、标签及实际 token 用量。配置确定后冻结提示词、schema、程序与输入批次的校验值，再运行正式批次。
现有 Silver 总量以实际去重有效数为准；若保留 2,451 条，补 7,549 条后共 10,000 条。原 Gold150、历史标签、实验 manifest、预测和评分器保持原样，本包不包含新数据划分。
新增数据生成完成后，从新增 Silver 中按预先记录的随机方法抽取 150 条人工检查。先冻结抽样名单，不按已知错误或质量好坏替换；保留 AI 原始结果和人工修改结果。该样本评价新增部分，不能直接代表全池，也不自动成为独立盲标 Gold。用于提示词调试的样本须单独标记；若最终质量样本将其排除，应报告实际抽样框。
adjudication_required 与格式/传输失败分开记录。前者不能自动作为最终训练监督，后者不能伪装成 confirmed_empty。需要复核时保留输入记录并单独追踪状态，不静默丢弃以凑足有效样本量。
有效空标可以保留。最终公开句子数、人审覆盖量及监督准入数量按完成后的清单报告，不提前写成已完成。

## 留痕与公开范围
保存完整业务请求消息、模型响应、请求/响应 ID（如有）、模型字段、执行设置、用量、错误和重试。记录实际可得字段，缺失记 unknown/null，不补造。
公开包不得包含 API 密钥、Authorization 头、代理认证口令或私人会话。原始业务文本及案例的再分发条件由数据发布方确认；无法再分发的内容可提供受控获取说明与校验值。运行原始档案与可公开的脱敏副本分别保存。
提示词、schema 和标签检查程序有助于重复执行与验证；闭源模型更新、平台上下文差异和生成随机性仍可能导致结果变化。

## 参考
- OpenAI GPT-6 Astra：https://developers.openai.com/api/docs/models/gpt-6-astra
- Structured Outputs：https://developers.openai.com/api/docs/guides/structured-outputs
- Model guidance：https://developers.openai.com/api/docs/guides/latest-model
- ESCO skill：https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/skill
- ESCO competence：https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/competence
OpenAI 文档核对日期：2026-09-13；无真实 API 执行。
