# Chinese-SkillSpan Benchmark

**Chinese-SkillSpan / Chinese Skill Benchmark** — DASFAA 2026 数据集与评测备份（私有仓库）。

评分器：`cnss-lskt-1.2.0` · Gold 评测集：`data/gold_canonical_v2.jsonl` · 更新：2026-08-24 15:40

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
| Claude | 0.6300 | 0.2570 | 0.2952 | 0.3789* | 缺 98 ID |
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
| JobBERT 1M | 0.1287 | **0.1332** | 0.0181 |
| listed mix 1M | 0.1282 | 0.1240 | 0.0153 |
| RoBERTa-wwm v3 | 0.1242 | 0.1191 | 0.0115 |

Encoder 在**事业单位**上接近失败（~0.015），ChatGPT 在该域最强。CSV：[`tables/per_domain_gold_v2.csv`](tables/per_domain_gold_v2.csv)

## Encoder 实验榜（Gold v2，typed exact micro F1）

| Run | test F1 | dev F1 | vs baseline 0.1224 |
|---|---:|---:|---|
| JobBERT 3M ckpt65000 | **0.1233** | 0.3205 | +0.0009 |
| JobBERT 1M + v3 | **0.1224** | 0.3185 | baseline |
| human380 + v3 merge | 0.1207 | 0.3163 | −0.0017 |
| listed mix 1M | 0.1201 | 0.3257 | −0.0023 |
| JobBERT 3M final encoder | 0.1170 | 0.3209 | −0.0054 |
| JobBERT 3M ckpt100k | 0.1167 | 0.3207 | −0.0057 |
| JobBERT demo 80k | 0.1152 | 0.3231 | −0.0072 |
| RoBERTa-wwm smoke v3 | 0.1156 | 0.3210 | −0.0068 |

完整 JSON/CSV → [`paper_results/repo/encoder_gold_v2.csv`](paper_results/repo/encoder_gold_v2.csv)

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
| Encoder 3-seed（ckpt65000 / 1M / vanilla） | **进行中**（GPU3；seed 42 已有，补 123/2026） |
| Claude / Kimi dump 补全 | **受阻**（`api.claude-Plus.top` 返回 HTML；不伪造 Claude/Kimi 标签） |
| BERT-CRF 已有 vanilla 对照 | RoBERTa-wwm v3 seed42 = 0.1156；3-seed 待填 |
| XLM-R / ESCO lexicon / span baseline | 待填（本地无 XLM-R 权重） |
| human IAA-300 | 待填 |
| listed mix **3M** DAPT | 已跳过 |
| domain-mix DAPT 1M（AI 36.8% / 应届生 29.0% / 阿里云 22.0% / 事业单位 12.2%） | **已提交**（语料 100 万句；SLURM 50649 排队 + 本地 GPU waiter；**尚无 F1**） |
| Hybrid / RAG | 待填 |

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
