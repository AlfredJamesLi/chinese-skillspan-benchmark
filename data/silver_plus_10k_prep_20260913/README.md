# Silver 补齐至 10,000 句 — 本轮准备包

日期：2026-09-13。  
状态：**待完成 AI 标注**；**待完成新增 150 条人工质量检查**。  
**不要**把论文数据量改成 10,000，也**不要**把人工覆盖量改成 500。Gold150、V4 划分、manifest、预测、解析器、评分器本轮未改。

脚本：

- `scripts/prep_silver_plus_10k_20260913.py`（可复现补抽）
- `scripts/sample_silver_plus_new150_qa.py`（AI 标签齐后才抽 150）

---

## 数量关系（句子）

| 口径 | 句子数 | 说明 |
|------|------:|------|
| 文档中的旧 Silver 台账 | 2,451 | A100+QA100+REST；本机无全量 REST jsonl |
| 本机可保留的已标注记录 | 2,319 | 冻结 `data/silver_plus_v6a_nocross/`（2150+169），**未改写** |
| 其中去重后有效句 | **2,064** | 唯一 NFC；去掉空句/过短/纯标点。重复记录不另计句 |
| 若 2,451 条全部当作唯一有效句 | 需补 7,549 | 用户给定对照口径；本轮**未**采用（台账含重复与 hold82） |
| 本轮按核验缺口实际补充 | **7,936** | 10,000 − 2,064 |
| 补后去重有效句（仍无新 AI 标签） | 10,000 | 仅句子清单；标签待标注 |
| 既有人工编码/检查 | **350** | Gold150 150 + A100 100 + QA100 100 |
| 新增人工质量检查 | **150，待完成** | 只从新增 Silver 抽；含在 10,000 内 |
| 人工覆盖量 500 | **待完成** | 350+150 去重且检查完成后才可记；届时句数与跨度数分开统计 |

实体跨度数量：旧 Silver 仍以 v6a 文件为准；新增跨度 **待 AI 标注后统计**。

hold82（82 条未放行）保留为过程证明，**不计入**有效已标注 Silver。

---

## 文件用途

| 路径 | 用途 |
|------|------|
| `COUNTS.json` / `AUDIT_OLD_SILVER.json` | 旧量核验 |
| `DEDUP_AND_SOURCE_VERIFICATION.json` | 去重与 3M 核验范围 |
| `old_silver/` | 指向未改写的 v6a；有效句清单 |
| `human350/` | Gold150+A100+QA100 的 ID，供新 150 避让 |
| `new_unlabeled/new_sentences.jsonl` | 7,936 条新增原文（无标签） |
| `new_unlabeled/sampling_manifest.json` | 种子 `20260913`、盐 `CNSS_SP_10K_TOPUP`、来源分层 |
| `annotation_input/work.jsonl` 与 `batches/` | 待调用模型；每批 20 句，共 397 批 |
| `annotation_input/PROMPT_silver_plus_v4212_rev2.txt` | 与已执行 2351 条同一 rev2 提示词 |
| `COST_AND_AUTH_HOLD.md` | 拟用模型与费用；全量 7,936 **仍待授权** |
| `pilot10_public_api_v1/` | 公开提示词 `silver_public_api_v1.0` + `gpt-6-astra` 的 10 条试标 |
| `run2500_public_api_v1/` | 本机正在标的 2500 句（勿让 Codex 重标） |
| `codex_remaining_5436/` | 其余 5,436 句；已拆 `waves/wave1|wave2|wave3` 供 Codex 分波调 gpt-6-astra |
| `human_qa150/STATUS.json` | 现为 `pending_ai_labels` |

新增来源（真实招聘文本，非编造）：阿里云 3,174 / 事业单位 2,381 / 上市公司 2,381。优先相对论文主 3M（应届生+人工智能 `jobbert_3m_sents.jsonl`）的来源。

3M 核验：已对可获得的 3.2M 句做 **NFC 精确匹配** 硬排除。不宣称排除近重复或未入库文本。选中句与 **domain-mix 1M** 另有 4,919 条精确重叠（该 1M 含阿里云/事业单位，**不是**论文主 3M）；与 listed-mix 1M 重叠 143；与 1M（应届生+人工智能）重叠 0。详见 `DEDUP_AND_SOURCE_VERIFICATION.json`。

---

## 下一步

1. 阅读 `COST_AND_AUTH_HOLD.md`，授权模型与预算。  
2. 用系统消息粘贴 `PROMPT_silver_plus_v4212_rev2.txt`，用户消息逐批 `batches/batch_*.jsonl`。只填 `gpt6_label` / `gpt6_why` / `model` / `gpt6_remark`。  
3. 合并为 `annotation_input/work.labeled.jsonl`。  
4. `python3 scripts/sample_silver_plus_new150_qa.py` → 「新增 Silver 的人工质量检查样本」。抽中不换样。  
5. 人工检查完成后，分别保存 AI 原标与人标；句数与跨度数分开统计。该 150 **不是**独立盲标 Gold，也**不**代表全部 10,000 条质量。
