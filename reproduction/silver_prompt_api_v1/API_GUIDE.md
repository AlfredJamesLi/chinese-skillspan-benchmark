# API 调用与代理说明

本文件是请求组装规范，不包含 API 密钥，也不会自动执行调用。

## 拟采用的 Responses 请求
- 官方 base URL：https://api.openai.com/v1；路径 POST /responses。
- model：gpt-6-astra；reasoning：{"effort":"high"}。
- instructions：silver_prompt.txt 的完整内容。
- input：user_template.txt 替换 {{INPUT_JSON}} 后的完整文本。
- text.format：{"type":"json_schema","name":"silver_annotations","strict":true,"schema": <output_schema.json 的对象>}。
- max_output_tokens：16384（试跑起点，含推理与可见输出预算；不是已证明足够的上限）。
- store：false。不给 previous_response_id，不连接持久会话，不启用工具。
- 不添加 temperature、top_p、seed 等未在本方案中确认支持的参数；若端点拒绝配置，记录失败，不静默删除字段后继续正式运行。
- 计划每批 10 条，末批可少于 10 条；批次大小是新方案参数，不是质量保证。正式运行前根据小批试验冻结。

系统提示词与输入消息必须保留完整文本，schema 必须保存为对象而非描述性文字。使用 UTF-8；JSON 转义不改变解码后的原文。

## “代理”的两种含义
1. 网络传输代理：客户端仍访问 api.openai.com。记录实际 API base URL 和连接方式；能否证明请求由 OpenAI 服务，取决于实际 TLS/网络配置及服务端记录，不凭“用了代理”下结论。
2. 第三方兼容接口/转发商：客户端 base URL 指向第三方。记录服务商、端点域名、请求的模型 ID、响应返回的模型字段以及可获得的路由说明。兼容 OpenAI 请求格式不等于已验证 OpenAI 原厂服务；返回 gpt-6-astra 字符串也不足以独立验证底层模型。
代理地址及身份待选择后填写，当前没有测试任何代理。认证信息从环境或密钥管理中注入，不能写入提示词、公开配置或日志。

## 兼容性与失败处理
先检查代理是否支持 Responses、reasoning.effort 及严格 JSON Schema。若仅支持 Chat Completions，使用独立的配置版本：system/user messages、reasoning_effort 及 response_format.json_schema，并重新做小批验证；不在同一标注运行中静默切换端点或关闭 schema。
保留完整响应对象，检查完成状态、拒绝、截断及错误，再提取业务 JSON。没有合法完整输出时标为 execution_failed/incomplete 等执行状态，不生成空标签代替。
传输类失败最多重试两次，记录每次尝试；未知是否已成功的请求可能产生重复执行/费用，应保留请求标识并检查已有响应。格式错误、偏移错误和语义争议不自动反复重试挑选最满意答案；先隔离，再按预先固定的补救方案另存结果。
若预算导致截断，试跑阶段调整后重新冻结设置；正式阶段按记录的恢复版本处理，保留首个失败输出。

## 调用端必须记录的字段
run_id、batch_id、attempt、开始/结束时间、endpoint_family、base_url（去除凭据与敏感查询）、connection_mode、provider_declared、requested_model、response_model、model_snapshot（仅真实提供时）、request_id、response_id、reasoning_effort、max_output_tokens、store、实际 batch_size、SDK/程序版本、提示词/schema/输入/输出 SHA-256、可获得的输入/缓存/输出/推理 token 数、响应状态、校验状态和人工复核状态。
requested_model 表示请求配置；response_model 表示响应声明；两者都不是独立的底层权重鉴定。不要让模型自己填写这些字段。
API 返回字段随接口而异，未提供时保留 null 并说明缺失。不要记录认证头、API key 或代理口令。

## 本地校验及旧格式导出
逐批检查记录数量、顺序与 ID；逐跨度检查整数索引、Unicode 范围、原文切片完全相等、标签集合、排序和不重叠。检查 status 与 spans/issues 一致。格式合法不等于语义正确。
旧格式导出只在独立派生文件进行：spans 映射为 [[start,end,label],...]，note 和 issues 保留在并行记录，model 从运行记录填写；原协议、来源与旧标签不覆盖。待裁决类型中的 S 必须随状态保留，不能导出后丢失待决标记。
本包仅离线核验人工编写的格式示例与 schema；没有运行模型，没有实测代理，也未实现或验证完整生产调用程序。
