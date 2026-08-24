# Sandbox v4 — LSKT 预标（方法对齐 Zhang，非正式 Gold）

**Gold v2 冻结。** 官方 typed F1 仍只用 `gold_canonical_v2.jsonl` + `cnss-lskt-1.2.0`。

**主标签仍是 LSKT（L/K/S/T）。**  
对齐 Zhang 的是标注 **方法**（原文 span、完整提及、空句规则、银标→Doccano 人工），不是改成二分类。  
`L+K→KNOWLEDGE`、`S+T→SKILL` 只作为 **评测投影**（见 `output/lskt_projection_audit/`），预标和 Doccano 必须打四类。

禁止覆盖 `gold_canonical_v2.jsonl`、`train.json`、论文主表、`confirmed-results.md`。

## 文件

| 路径 | 角色 |
|---|---|
| `GUIDELINES.md` | **以这个为准** 的操作性定义 |
| `PROMPT_gpt56.md` | 贴给 GPT-5.6（四类） |
| `unlabeled_pilot300.jsonl` / `gpt56_chunks/` | 300 句无答案 |
| `doccano_seed_v3_lskt.jsonl` | v3 四类种子，可导入 Doccano |
| `doccano_seed_v3_2way.jsonl` | 仅投影对照，**不要当主标导入** |

GPT-5.6 合并 JSON 后：

```bash
python scripts/sandbox_v4_apply.py \
  --llm_json reports/sandbox_v4_prelabel/gpt56_raw/all.json
```
