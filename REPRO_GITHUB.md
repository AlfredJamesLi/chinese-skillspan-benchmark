# Chinese-SkillSpan — GitHub 私有备份复现指南

本目录为 **Chinese Skill Benchmark / Chinese-SkillSpan**（**PeerJ Computer Science** 数据集文）工作区备份。  
完整父仓库还含 Access/SRICL；**不要把 SRICL / 六语料英文主表写进本文**。

两套测试金标不要混成一句 SOTA。**论文主协议 = P2 / V4**（2026-08-27）：

| 协议 | 金标 | 论文位置 | 已确认数字 |
|---|---|---|---|
| **P2 匹配 SOP+jieba（主）** | `data/test_lskt_v4_cws_simhuman980_hybrid.jsonl`（sha `2ad6342d…`） | 摘要 / 主表 | JobBERT 1M/3M v4 **0.4272 / 0.4331** exact；ChatGPT exact **0.2854** / relaxed **0.6249** |
| **P1 Gold v2（沿革）** | `data/gold_canonical_v2.jsonl`（2601 ID，sha `7a26e32b…`） | 附录；文件冻结不覆盖 | ChatGPT **0.6365**；JobBERT-zh 1M 3-seed **0.1288** |

数字只允许来自 `notes/confirmed-results.md` 或用户 PDF。禁止旧 scorer 全局 set bug（~0.46）。协议：`notes/DATA_PROTOCOL_FREEZE.md`。

## 1. 环境

```bash
conda activate adasparse   # 或自建 env：torch, transformers, seqeval, jieba
export PYTHONPATH="/path/to/SCESC-LLM-skill-extraction/Baseline_Models_Collection/pytorch-crf:${PYTHONPATH}"
```

本仓评分与 jieba 对齐：`requirements-repro.txt`。Encoder 训练另需父仓库 `requirements.txt`。

**Hugging Face 公有模型（本仓 Git 不含权重，百度也不传 14B）**：见 [`MODELS_HF.md`](MODELS_HF.md) 与总表 `MODELS_CATALOG.md`。重训 JobBERT-zh 必须先下 `hfl/chinese-roberta-wwm-ext`；vanilla-large 用 `hfl/chinese-roberta-wwm-ext-large`（或百度 `baseline_encoders/` 离线包）。SOP/LLM 臂另需 `Qwen/Qwen2.5-14B-Instruct`（仅 HF）。论文主数字可用 `data/frozen_preds/`，不必先下 14B。

## 2. 数据准备

**官方 Gold v2 CRF（无需 DAPT）：**

- `data/train_goldstyle_v3.jsonl`
- `data/dev_goldstyle_v3.jsonl`
- `data/gold_canonical_v2.jsonl`
- `data/corpus_splits/test.json`（Table 1 test 3237）

**SOP v4 编码器训练银标（非人类 Gold）：** `data/train_lskt_v4_silver.jsonl`、`data/dev_lskt_v4_silver.jsonl`

**P2 测试金标：** `data/test_lskt_v4_cws_simhuman980_hybrid.jsonl`（2601 = 980 SimHuman + 1621 SOP-CWS）

**Human page-1 200（附录/补充，非主金标）：** `data/human_gold_page1_200.jsonl`（980 分歧队列前 200 句；sha256 `fcecb522…617490`）。打分：`python3 scripts/build_and_eval_human200_page1.py`。表：`tables/human200_page1_scores.csv`。不要覆盖 Gold v2，不要替换 V4 hybrid。

JobBERT DAPT 语料与权重见 `data/LARGE_DATA_MANIFEST.md`。表内编码器行可用 `data/frozen_preds/` 的 jsonl，不必下 53GB `output/`。

## 3. 论文主评测（P2 / V4 hybrid）

主指标：**typed exact micro F1**（`cnss-lskt-1.2.0`）。金标：`data/test_lskt_v4_cws_simhuman980_hybrid.jsonl`。预测需 jieba snap。

LLM 旧 dump（无 API）：

```bash
python3 scripts/eval_hybrid_llm_old_dumps.py
# CSV: tables/hybrid_cws_llm_old_dumps.csv
# Claude 缺 98、Kimi 缺 293：reports/sandbox_lskt_v4_silver/hybrid_cws_eval/fill_later/
```

编码器 + 全模型（本地有 `output/` 时跑全表；克隆本仓时至少可用 frozen v4 preds）：

```bash
python3 scripts/eval_hybrid_cws_simhuman.py
# CSV: tables/hybrid_cws_simhuman980_all_models.csv
```

冻结预测：

| 文件 | 对应表行 |
|---|---|
| `data/frozen_preds/jobbert_1m_v4.jsonl` | JobBERT 1M v4（jieba 后处理 → 0.4272） |
| `data/frozen_preds/jobbert_3m_v4.jsonl` | JobBERT 3M v4（0.4331） |
| `data/frozen_preds/jobbert_1m_v4_cws_retrain.jsonl` | 1M CWS 重训（0.4049） |

LLM 预测：`reports/views/*_unique_first_v2.jsonl`（Claude/Kimi 原 dump 不完整；filled 视图是混型号，不能写成原 Table 3 模型）。

## 3b. 附录评测（P1 Gold v2；不是摘要 SOTA，不是 PDF Table 3）

```bash
python3 scorer/test_regression.py
python3 scorer/score_lskt.py \
  --gold data/gold_canonical_v2.jsonl \
  --pred reports/views/ChatGPT_unique_first_v2.jsonl \
  --align-mode official
```

## 3c. SOP v4 银标训练（可选重跑）

```bash
bash scripts/run_jobbert_zh_3m_lskt_v4.sh
```

同规则 SOP 测试银标 `data/test_lskt_v4_rule_g2ids.jsonl` 上的 0.3170 等是**诊断一致性**，不得写入 PDF Table 3 或 Gold v2 摘要 SOTA。

## 4. JobBERT-zh 1M goldstyle（P1 弱基线）

```bash
python3 scripts/prepare_jobbert_1m_corpus.py --n 1000000 --out data/jobbert_1m_sents.jsonl
bash scripts/run_jobbert_zh_1m.sh
```

快照：`results_snapshots/jobbert_zh_1m__crf_v3_seed42.json` → Gold v2 typed **0.1224**（3-seed mean **0.1288**）。

## 5. 其它 DAPT 变体

上市公司 mix 1M **已输给** 0.1224（0.1201）。域混合 1M 3-seed mean **0.1269**，低于 1M。不要扩 listed-3M。脚本：`scripts/run_jobbert_zh_listed_1m.sh`、`scripts/run_jobbert_zh_domain_1m.sh`。

## 6. 父仓库只读依赖（LLM 原始 dump / LoRA）

不在本备份仓内：

| 组件 | 路径 |
|------|------|
| LLM 推理 | `main.py`, `prompt_template_rag.py` |
| 预处理 / 原 dump | `chinese_skillspan_preprocessing/` |
| Qwen LoRA | `LLaMA-Factory/saves/qwen2_5_14b/lora/sft_CN_skillspan_*` |

本仓已有 unique-first **views**，核 P1/P2 表一般不必再碰原 dump。

## 7. 从 GitHub 恢复后检查清单

- [ ] `data/gold_canonical_v2.jsonl` 行数 = 2601；sha256 前缀 `7a26e32b`
- [ ] hybrid 金标 2601 行；sha256 前缀 `2ad6342d`
- [ ] `python3 scorer/test_regression.py` 通过
- [ ] `python3 scripts/eval_hybrid_llm_old_dumps.py` → ChatGPT 2601 exact ≈ 0.2854
- [ ] 大文件按 `LARGE_DATA_MANIFEST.md` 从实验室盘补全（权重 / DAPT 语料）
