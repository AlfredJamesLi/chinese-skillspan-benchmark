# Codex 任务：wave1 — gpt-6-astra 标剩余 Silver

你在仓库 `/home/guojingli3/SCESC-LLM-skill-extraction` 的 **Chinese-SkillSpan** 窗口。
**只做这一波：wave1。** 不要做 wave1/wave2/wave3 中的其它波，不要重标 `ids_held_2500.txt` 的 2500 句。
不要改 `access_paper/`、Gold150、V4 hybrid、`data/silver_plus_v6a_nocross/`、`run2500_public_api_v1/`。不要写论文 F1。

## 本波

目录：`Chinese_skill_benchmark_Paper/data/silver_plus_10k_prep_20260913/codex_remaining_5436/waves/wave1/`

- 句子 **1810**；JSON 批 **181**（`batch_0001.json` … `batch_0181.json`）
- 每批最多 10 条；本波最后一批 10 条
- 系统提示词：本目录 `PROMPT_silver_public_api_v1.0.txt`
- 用户输入：`batches/batch_XXXX.json`（仅 `records[].id` + `text`）
- 输出：同名写入 `batches_out/batch_XXXX.json`

## 调用

模型：**gpt-6-astra**。  
`POST https://claudeed.ysaikeji.cn/v1/chat/completions`，密钥 `~/.config/ysaikeji/api_key`。  
temperature=0，max_tokens=8192，超时 ≥ 180s。不要改成 20 条一批。

系统消息 = 提示词全文。用户消息 = 该批 JSON。各记录独立。

## 输出格式

只返回一个 JSON 对象（不要 Markdown 围栏）：顶层 `records`；条数/顺序/id 与输入一致；每条恰好 `id, spans, status, note, issues`。  
`spans[].start/end` 为 Python Unicode 码点；`text[start:end]` 必须等于 `spans[].text`。  
`status` ∈ candidate_complete | confirmed_empty | adjudication_required。  
失败重试最多 3 次；不要编造跨度。

全部 181 批写完后，把 `PROGRESS.json` 的 `wave1.status` 改成 `done`（若没有该文件，在本波目录写 `STATUS.json`：`{"wave":"wave1","n_out": <已写批次数>}`）。

不要合并 5,436、不要抽 150、不要训练。合并由主窗口在三波都齐后执行：

```bash
cd Chinese_skill_benchmark_Paper/scripts
python3 sync_codex_wave_outputs.py
python3 merge_codex_remaining_silver.py
```
