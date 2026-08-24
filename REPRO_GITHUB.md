# Chinese-SkillSpan — GitHub 私有备份复现指南

本目录为 **Chinese Skill Benchmark / Chinese-SkillSpan** 论文工作区备份。
完整父仓库还含 Access/SRICL 与 LLM 实验；**本文档只覆盖本论文 JobBERT + Gold v2 主流程**。

## 1. 环境

```bash
conda activate adasparse   # 或自建 env：torch, transformers, seqeval
export PYTHONPATH="/path/to/SCESC-LLM-skill-extraction/Baseline_Models_Collection/pytorch-crf:${PYTHONPATH}"
```

依赖见父仓库 `requirements.txt`；encoder 默认：
`Baseline_Models_Collection/chinese-roberta-wwm-ext`（需自行下载或从实验室盘拷贝）。

## 2. 数据准备

**最小可跑 CRF（无需 DAPT）：**

- `data/train_goldstyle_v3.jsonl`
- `data/dev_goldstyle_v3.jsonl`
- `data/gold_canonical_v2.jsonl`
- 父仓库 `data/annotated/processed/chinese_skillspan/test.json`（或本仓库 `data/corpus_splits/test.json`）

**JobBERT DAPT：** 见 `data/LARGE_DATA_MANIFEST.md`；需 `chineseskillspan-jobert-pretrain/` 原始 CSV。

## 3. 官方评测

```bash
python3 scorer/score_lskt.py \
  --gold data/gold_canonical_v2.jsonl \
  --pred /path/to/test_pred.jsonl \
  --align-mode official
```

主指标：**typed exact micro F1**（`cnss-lskt-1.2.0`）。

## 4. JobBERT-Zh 1M（已确认内部数字）

```bash
# 语料（若本地无 jsonl）
python3 scripts/prepare_jobbert_1m_corpus.py --n 1000000 --out data/jobbert_1m_sents.jsonl

# MLM + CRF（单卡示例）
bash scripts/run_jobbert_zh_1m.sh
# 或 SLURM: sbatch scripts/jobbert_zh_1m.sbatch
```

参考结果快照：`results_snapshots/jobbert_zh_1m__crf_v3_seed42.json` → test F1 **0.1224**。

## 5. 上市公司混合 DAPT 1M（实验中）

```bash
bash scripts/extract_listed_yearly_csvs.sh
python3 scripts/prepare_jobbert_listed_mix_corpus.py --n 1000000 \
  --out data/jobbert_listed_mix_1m_sents.jsonl
sbatch scripts/jobbert_zh_listed_1m.sbatch   # MaxWall 12h
```

## 6. 论文数字来源

- 只允许写入 `notes/confirmed-results.md` 或用户 PDF 中的数。
- 禁止引用旧 scorer 全局 set bug（~0.46）。
- 协议冻结：`notes/DATA_PROTOCOL_FREEZE.md`。

## 7. 父仓库只读依赖（LLM 银标 / LoRA）

不在本备份仓内，需完整克隆父仓库：

| 组件 | 路径 |
|------|------|
| LLM 推理 | `main.py`, `prompt_template_rag.py` |
| 预处理 | `chinese_skillspan_preprocessing/` |
| Qwen LoRA | `LLaMA-Factory/saves/qwen2_5_14b/lora/sft_CN_skillspan_*` |

## 8. 从 GitHub 恢复后检查清单

- [ ] `data/gold_canonical_v2.jsonl` 行数 = 2601 unique ID
- [ ] `python3 scorer/test_regression.py` 通过
- [ ] `results_snapshots/index.json` 与本地新跑 F1 量级一致（~0.12 typed）
- [ ] 大文件按 `LARGE_DATA_MANIFEST.md` 从网盘/实验室补全
