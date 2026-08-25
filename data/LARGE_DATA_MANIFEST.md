# Large data not in this Git repo

GitHub 单文件上限 100MB；本仓库只备份**代码 + 协议 + 可复现小数据 + 结果快照**。
以下大文件请用实验室盘 / 百度网盘 / 本机另存。

## 已在仓库内（可直接复现 JobBERT CRF）

| 路径 | 约大小 | 说明 |
|------|--------|------|
| `data/gold_canonical_v2.jsonl` | 5 MB | 官方 Gold test（2601 ID） |
| `data/train_goldstyle_v3.jsonl` | 14 MB | CRF 训练银标 v3 |
| `data/dev_goldstyle_v3.jsonl` | 1.8 MB | CRF dev |
| `data/train_lskt_v4_silver.jsonl` | ~14 MB | LSKT v4 训练银标（SOP；非 Gold） |
| `data/dev_lskt_v4_silver.jsonl` | ~2 MB | LSKT v4 dev 银标 |
| `data/train_lskt_v4_cws.jsonl` | ~15 MB | v4 银标 + jieba 禁半词（沙盒；非 Gold） |
| `data/dev_lskt_v4_cws.jsonl` | ~2 MB | 同上，dev |
| `data/test_lskt_v4_cws_g2ids.jsonl` | ~2.6 MB | SOP 测试银标 + jieba（2601 ID；非官方 Gold） |
| `data/test_lskt_v4_rule_g2ids.jsonl` | ~2 MB | **新 SOP 测试金标**（2601 ID；非官方 Gold） |
| `data/test_lskt_v4_simhuman980.jsonl` | <1 MB | 980 句 SOP 模拟人工 |
| `data/test_lskt_v4_cws_simhuman980_hybrid.jsonl` | ~3 MB | P2 测试金标（980 SimHuman + 1621 SOP-CWS） |
| `data/frozen_preds/jobbert_*_v4.jsonl` | ~9 MB | 1M/3M v4 与 CWS 重训的冻结预测（核表用，非权重） |
| `data/test_lskt_v4_silver_g2ids.jsonl` | ~2 MB | Codex 测试银标（对照） |
| `data/corpus_splits/{train,dev,test}.json` | ~87 MB | Table 1 语料切分（若已复制） |
| `data/jobbert_*_sents.meta.json` | KB | DAPT 语料配方与统计 |
| `results_snapshots/` | KB | 各次 `run_summary.json` 快照 |

## 不在仓库内（需本地保留或重新下载）

| 路径（实验室） | 约大小 | 用途 |
|----------------|--------|------|
| `chineseskillspan-jobert-pretrain/` | ~40 GB | 应届生/AI/上市公司原始 CSV + RAR |
| `data/jobbert_1m_sents.jsonl` | 139 MB | 1M DAPT 句 |
| `data/jobbert_3m_sents.jsonl` | 446 MB | 3.2M DAPT 句 |
| `data/jobbert_listed_mix_1m_sents.jsonl` | 166 MB | 上市公司混合 1M 句 |
| `data/jobbert_domain_mix_1m_sents.jsonl` | ~150 MB | 域混合 1M（AI/应届生/阿里云/事业单位） |
| `output/` | ~53 GB | MLM/CRF 权重与预测 |
| `chinese_skillspan_preprocessing/` | ~862 MB | Doccano / 银标流水线（父仓库） |
| `Baseline_Models_Collection/chinese-roberta-wwm-ext/` | ~400 MB | 初始 encoder |
| `Qwen2.5-14B-Instruct/` | 数十 GB | LLM 基线 |

## 重建 DAPT 语料（无需上传 jsonl）

```bash
# 1. 解压上市公司逐年 CSV（一次性）
bash scripts/extract_listed_yearly_csvs.sh

# 2. 原 1M 配方（应届生 59% + AI 41%）
python3 scripts/prepare_jobbert_1m_corpus.py --n 1000000 \
  --out data/jobbert_1m_sents.jsonl

# 3. 上市公司混合 1M（40/35/25）
python3 scripts/prepare_jobbert_listed_mix_corpus.py --n 1000000 \
  --out data/jobbert_listed_mix_1m_sents.jsonl

# 4. 域混合 1M（人工智能 35% / 应届生 25% / 阿里云 22% / 事业单位 14%；无上市公司）
python3 scripts/prepare_jobbert_domain_mix_corpus.py --n 1000000 \
  --out data/jobbert_domain_mix_1m_sents.jsonl
```

原始 CSV 来源：马克数据网（见 `chineseskillspan-jobert-pretrain/` 内参考文献 PDF）。

## SHA256 校验

正式数字以 `manifests/gold_canonical_v2_manifest.csv` 与 `notes/DATA_PROTOCOL_FREEZE.md` 为准。
