# Chinese-SkillSpan Benchmark

**Chinese-SkillSpan / Chinese Skill Benchmark** — DASFAA 2026 数据集与评测备份（私有仓库）。

评分器：`cnss-lskt-1.2.0` · Gold 评测集：`data/gold_canonical_v2.jsonl` · 更新：2026-08-25

---

## 论文主表（PDF Table 3，2676 Gold 重打分）

| Model | Paper S-F1 | Repo typed F1 | Repo collapsed F1 | 状态 |
|---|---:|---:|---:|---|
| ChatGPT | 0.6700 | 0.6836 | **0.6703** | 已确认 |
| Claude | 0.6300 | 0.5712 | 0.6062 | dump 不完整 |
| Kimi | 0.5700 | 0.5310 | 0.5618 | dump 不完整 |
| DeepSeek | 0.5130 | **0.5149** | 0.5479 | 已确认 |
| Qwen | 0.2130 | 0.3442 | 0.3949 | 与论文有 gap |
| JobBERT-skill | 0.0045 | — | **0.0045** | 已确认 |
| JobBERT-knowledge | 0.0038 | — | **0.0038** | 已确认 |

## Gold v2 重打分（canonical，unique-first view）

| Model | Paper S-F1 | typed F1 | collapsed F1 | typed relaxed (IoU≥0.5) | align |
|---|---:|---:|---:|---:|---|
| ChatGPT | 0.6700 | 0.6365 | 0.6403 | **0.7221** | OK |
| DeepSeek | 0.5130 | 0.1327 | 0.3569 | 0.1798 | OK |
| Qwen | 0.2130 | 0.0791 | 0.1075 | 0.1272 | OK |
| JobBERT-skill | 0.0045 | 0.0000 | 0.0045 | 0.0000 | OK |
| JobBERT-knowledge | 0.0038 | 0.0000 | 0.0037 | 0.0000 | OK |
| Claude | 0.6300 | **0.2583** | 0.2970 | **0.3861** | OK（补 98 条 sonnet-4-6） |
| Kimi | 0.5700 | 0.1651 | 0.3349 | 0.2130* | 缺 293 ID |

\* Claude/Kimi relaxed 按缺失 ID=空预测计算（`paper_results/repo/relaxed_f1_gold_v2.json`）。unique-first 官方对齐见上表 typed/collapsed。

## 分域 typed F1（Gold v2；Industry-OOD 代理）

Gold v2 域：人工智能招聘 1407 / 事业单位招聘 737 / 阿里云公开数据集 457。无 `year` 字段，Time-OOD **做不了**。

| System | 人工智能 | 阿里云 | 事业单位 |
|---|---:|---:|---:|
| ChatGPT | 0.6489 | 0.5650 | **0.7032** |
| DeepSeek | 0.1392 | 0.1293 | 0.0805 |
| Qwen | 0.0887 | 0.0646 | 0.0207 |
| JobBERT 3M ckpt65000 | **0.1323** | 0.1259 | 0.0150 |
| JobBERT 1M | 0.1287 | 0.1332 | 0.0181 |
| listed mix 1M | 0.1282 | 0.1240 | 0.0153 |
| domain-mix 1M (seed 42) | 0.1276 | **0.1372** | 0.0287 |
| RoBERTa-wwm v3 | 0.1242 | 0.1191 | 0.0115 |

Encoder 在**事业单位**上接近失败（~0.015–0.029；domain-mix seed 42 = 0.0287），ChatGPT 在该域最强。CSV：[`tables/per_domain_gold_v2.csv`](tables/per_domain_gold_v2.csv)

## Encoder 实验榜（Gold v2，typed exact micro F1）

| Run | test F1 | dev F1 | vs baseline 0.1224 |
|---|---:|---:|---|
| domain-mix 1M (seed 42) | **0.1234** | 0.3190 | +0.0010 |
| JobBERT 3M ckpt65000 | 0.1233 | 0.3205 | +0.0009 |
| JobBERT 1M + v3 | **0.1224** | 0.3185 | baseline |
| human380 + v3 merge | 0.1207 | 0.3163 | −0.0017 |
| listed mix 1M | 0.1201 | 0.3257 | −0.0023 |
| JobBERT 3M final encoder | 0.1170 | 0.3209 | −0.0054 |
| JobBERT 3M ckpt100k | 0.1167 | 0.3207 | −0.0057 |
| JobBERT demo 80k | 0.1152 | 0.3231 | −0.0072 |
| RoBERTa-wwm smoke v3 | 0.1156 | 0.3210 | −0.0068 |

完整 JSON/CSV → [`paper_results/repo/encoder_gold_v2.csv`](paper_results/repo/encoder_gold_v2.csv)  
3-seed 均值 → [`tables/encoder_3seed_gold_v2.csv`](tables/encoder_3seed_gold_v2.csv)（1M **0.1288** / domain-mix 0.1269 / 3M ckpt65000 0.1258）

## SOP v4 / jieba 诊断表（附录，不是 Table 3）

官方主指标仍是 Gold v2 typed exact。下表必须自带 **train silver / decode / test gold**，不得写入 PDF Table 3、Gold v2 LLM 主表或摘要 SOTA。CSV：[`tables/sop_v4_cws_diagnostic.csv`](tables/sop_v4_cws_diagnostic.csv)。

| Pred | Train | Decode | Test gold | typed exact | IoU≥0.5 |
|---|---|---|---|---:|---:|
| JobBERT 1M | goldstyle v3 | raw | Gold v2 | 0.1224 | — |
| JobBERT 1M | SOP v4 | raw | Gold v2 | 0.1079 | 0.3320 |
| JobBERT 3M | SOP v4 | raw | Gold v2 | 0.1104 | 0.3404 |
| JobBERT 1M | SOP v4 | jieba post-hoc | Gold v2 | 0.1454 | 0.3411 |
| JobBERT 3M | SOP v4 | jieba post-hoc | Gold v2 | 0.1479 | 0.3470 |
| JobBERT 1M | SOP v4 | raw | SOP rule silver | 0.3170 | 0.5663 |
| JobBERT 3M | SOP v4 | raw | SOP rule silver | 0.3229 | 0.5624 |
| JobBERT 1M | SOP v4 | jieba post-hoc | SOP-CWS silver | 0.4278 | 0.5960 |
| JobBERT 3M | SOP v4 | jieba post-hoc | SOP-CWS silver | 0.4341 | 0.5884 |

SOP v4 训练在官方 Gold v2 上低于 goldstyle v3（0.1079 vs 0.1224）。0.3170 / ~0.43 是与 SOP 银标的一致性，不是人类 Gold。

## 匹配协议全量测试（SOP-CWS + SimHuman 980，jieba 双边）

测试金标：980 SimHuman rule_v4 + 1621 SOP-CWS，预测与金标都 jieba snap。n=2601。**不是 Gold v2，不是 PDF Table 3。**  
复现：`python scripts/eval_hybrid_cws_simhuman.py` · CSV：[`tables/hybrid_cws_simhuman980_all_models.csv`](tables/hybrid_cws_simhuman980_all_models.csv)

| Model | 2601 exact | 2601 relaxed | 980 exact | 980 relaxed |
|---|---:|---:|---:|---:|
| JobBERT 3M v4 + jieba | **0.4331** | 0.5873 | **0.4401** | 0.6032 |
| JobBERT 1M v4 + jieba | **0.4272** | **0.5952** | **0.4333** | **0.6110** |
| JobBERT 1M CWS retrain | 0.4049 | 0.5904 | 0.4020 | 0.6084 |
| domain-mix 1M (3-seed) | 0.3037 | 0.5278 | — | — |
| JobBERT 1M v3 (3-seed) | 0.3032 | 0.5332 | — | — |
| RoBERTa-wwm v3 (3-seed) | 0.2875 | 0.5206 | — | — |
| ChatGPT | 0.2854 | **0.6249** | 0.2836 | **0.6447** |
| Claude filled (haiku+sonnet) | 0.1519 | 0.3416 | 0.1778 | 0.4101 |
| Kimi filled | 0.1093 | 0.2321 | 0.1116 | 0.2514 |
| DeepSeek | 0.0802 | 0.1577 | 0.0738 | 0.1573 |
| Qwen | 0.0501 | 0.1409 | 0.0483 | 0.1361 |
| JobBERT-skill EN | 0.0096 | 0.0676 | 0.0124 | 0.0919 |

此协议下 JobBERT-zh v4 领先 typed exact；ChatGPT 领先 relaxed。不可与 Gold v2 上 ChatGPT 0.6365 直接比。

## 语料规模（PDF Table 1）

| Split | #Sent | Avg Len | Avg 4D |
|---|---:|---:|---:|
| train | 17460 | 37.41 | 2.354 |
| dev | 2143 | 40.37 | 3.607 |
| test | 3237 | 43.85 | 2.306 |

## 待完成 / 留空

| 实验 | 状态 |
|---|---|
| Relaxed F1 (IoU≥0.5) Gold v2 | **已出表**（ChatGPT 0.7221；Claude/Kimi dump 不完整） |
| 分域 / Industry-OOD 代理 | **已出表**（见上；事业单位是 encoder 短板） |
| Concept Accuracy / ESCO concept-ID | 无 concept ID，不做 |
| Time-OOD | 无 year 字段，不做 |
| Encoder 3-seed（ckpt65000 / 1M / domain-mix） | **已出表**（1M mean 0.1288；RoBERTa seed 123 仍在跑） |
| Claude / Kimi dump 补全 | 原 dump 仍缺 98 / 293；filled 视图为混型号（sonnet-4-6 / k2.6），不覆盖原文件 |
| BERT-CRF 已有 vanilla 对照 | RoBERTa-wwm v3 seed42 = 0.1156；3-seed 均值待填 |
| XLM-R / ESCO lexicon / span baseline | 待填（本地无 XLM-R 权重） |
| human IAA-300 | 待填 |
| listed mix **3M** DAPT | 已跳过 |
| domain-mix DAPT 1M | **已出表**（seed 42 = 0.1234；3-seed mean 0.1269 < 1M 0.1288；事业单位 0.0287） |
| 匹配协议 hybrid（SOP-CWS+SimHuman980） | **已出表**（见上；不是 Gold v2） |
| Hybrid / RAG（Qwen） | 不做（本窗口） |

详情 → [`paper_results/pending/placeholders.json`](paper_results/pending/placeholders.json)

---

## 目录

| 路径 | 用途 |
|---|---|
| **`paper_results/`** | **结果总表**（manifest + paper/ + repo/ + pending/） |
| `tables/` | Overleaf 表源（CSV/JSON） |
| `results_snapshots/` | 各次 run_summary 快照 |
| `reports/` | 完整审计、打分 dump、IAA 工作表 |
| `notes/confirmed-results.md` | 论文已确认数字（勿编造） |
| `pdf/` | 最新稿 PDF |
| `HANDOFF.md` | 服务器窗口交接 |
| `REPRO_GITHUB.md` | 复现说明 |
| `data/` | Gold v2、train/dev goldstyle、corpus_splits |

## 备份说明

- GitHub 私有仓库：https://github.com/AlfredJamesLi/chinese-skillspan-benchmark
- 大文件未纳入（见 `data/LARGE_DATA_MANIFEST.md`）：`output/` 权重、预训练 RAR、DAPT jsonl
- 父仓库实验脚本只读备查；**不要改** `access_paper/`
