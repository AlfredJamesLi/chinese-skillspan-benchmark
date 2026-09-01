# 换机复现：百度云盘 + GitHub + Hugging Face

目标：新服务器上 **GitHub 拉代码 → 百度拉数据/中小权重 → Hugging Face 拉 14B/8B 公有基座**，即可复现三个项目。

百度根目录（网页：**我的应用数据 → bypy**）：

- 语料（2026-08-23）：`/人工智能招聘大数据2014-2025.3`、`/上市公司招聘大数据2014-2026.3`、`/应届生招聘大数据（2014-2025.6）`
- 交接包：`/账号交接_20260901/`

本机对照账号：`DS209213:/home/guojingli3`。`bypy` 远端路径均相对 `/apps/bypy`。

---

## 0. 体积策略

| 决策 | 规则 |
|---|---|
| 上传百度 | 自训权重、实验 `output/`、Job Reco 处理后数据；以及 **≤ ~4 GB** 的 encoder（RoBERTa / JobBERT / GLiNER / mDeBERTa / DaJobBERT / ESCO-XLM-R **基座**） |
| 不上传、改 HF 下载 | **Qwen2.5-14B-Instruct（~28 GB）**、**Llama-3-8B-Instruct（~16–30 GB）**、**BAAI/bge-large-zh-v1.5**（Job Reco 本地目录几乎只有 tokenizer，权重本就应从 HF 拉） |
| 不上传 | `optimizer.pt`、TensorFlow `*.h5` 副本、CUDA/Spark 安装包、三份重复的 `autodl-tmp/data_bj` 只保留一份 |

---

## 1. 先拉代码（GitHub，AlfredJamesLi）

```bash
gh auth login   # 或已有 token
git clone git@github.com:AlfredJamesLi/chinese-skillspan-benchmark.git
git clone git@github.com:AlfredJamesLi/SCESC-LLM-skill-extraction.git
git clone git@github.com:AlfredJamesLi/sricl-skillanchor-access-private-backup.git
git clone git@github.com:AlfredJamesLi/lab-code-misc-backup.git
```

| 仓库 | 对应项目 |
|---|---|
| `chinese-skillspan-benchmark` | Chinese-SkillSpan 论文代码、Gold/银标、协议 |
| `SCESC-LLM-skill-extraction` | SkillAnchor 实验脚本（无 14B 权重） |
| `sricl-skillanchor-access-private-backup` | Table II vanilla XLM-R dumps、论文产物 |
| `lab-code-misc-backup` | Job Reco 三城市脚本、Pre-DyGAE、kvpress |

LoRA（Qwen2.5-14B rank 适配器，无中间 checkpoint）：

https://huggingface.co/AlfredJames/skillanchor-qwen25-14b-lora-private （private）

```bash
huggingface-cli download AlfredJames/skillanchor-qwen25-14b-lora-private \
  --local-dir ./lora_finals
```

---

## 2. 从百度拉数据与中小模型

```bash
# 安装：pip install bypy && bypy info
REMOTE=/账号交接_20260901
ROOT=/workspace   # 改成你的新盘

bypy syncdown $REMOTE/CNSS_output                         $ROOT/Chinese_skill_benchmark_Paper/output
bypy syncdown $REMOTE/CNSS_data                           $ROOT/Chinese_skill_benchmark_Paper/data
bypy syncdown $REMOTE/access_rerun                        $ROOT/SCESC-LLM-skill-extraction/output/access_rerun
bypy syncdown $REMOTE/SCESC_data                          $ROOT/SCESC-LLM-skill-extraction/data
bypy syncdown $REMOTE/chinese_skillspan_preprocessing     $ROOT/SCESC-LLM-skill-extraction/chinese_skillspan_preprocessing
bypy syncdown $REMOTE/LLaMA-Factory_data                  $ROOT/SCESC-LLM-skill-extraction/LLaMA-Factory/data
bypy syncdown $REMOTE/baseline_encoders                   $ROOT/SCESC-LLM-skill-extraction/Baseline_Models_Collection
bypy syncdown $REMOTE/Job_Reco_BJ_utils                   $ROOT/Job_Reco_test/job/utils
bypy syncdown $REMOTE/Job_Reco_data_bj                    $ROOT/Job_Reco_test/autodl-tmp/data_bj
bypy syncdown $REMOTE/Pre-DyGAE                           $ROOT/Pre-DyGAE
bypy syncdown $REMOTE/sparksteps_tars                     $ROOT/tars
```

招聘原始 CSV（Chinese-SkillSpan DAPT 语料源，已在百度根目录）：

```bash
bypy syncdown /人工智能招聘大数据2014-2025.3   $ROOT/chineseskillspan-jobert-pretrain/人工智能招聘大数据2014-2025.3
bypy syncdown /上市公司招聘大数据2014-2026.3   $ROOT/chineseskillspan-jobert-pretrain/上市公司招聘大数据2014-2026.3
bypy syncdown /应届生招聘大数据（2014-2025.6） $ROOT/chineseskillspan-jobert-pretrain/应届生招聘大数据（2014-2025.6）
```

Job Reco spark 分卷还原：

```bash
cd $ROOT/tars
sha256sum -c Job_Reco_BJ_sparksteps.sha256
cat Job_Reco_BJ_sparksteps.tar.* | tar xf - -C $ROOT/Job_Reco_test/job
# 同样处理 SH / SZ
```

---

## 3. 公有大基座：Hugging Face 下载（不要从百度传）

国内可加：`export HF_ENDPOINT=https://hf-mirror.com`

### SkillAnchor / Chinese-SkillSpan 生成器

```bash
# Qwen2.5-14B-Instruct  ~28GB  → 放到 SCESC 树里原路径
huggingface-cli download Qwen/Qwen2.5-14B-Instruct \
  --local-dir $ROOT/SCESC-LLM-skill-extraction/Qwen2.5-14B-Instruct

# Llama-3-8B-Instruct  ~16GB（HF 官方 safetensors；实验室另有一份 original/ 更大，不必复原）
huggingface-cli download meta-llama/Meta-Llama-3-8B-Instruct \
  --local-dir $ROOT/SCESC-LLM-skill-extraction/LLaMA-Factory/Meta-Llama-3-8B-Instruct
```

Llama 需在 https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct 接受许可并 `huggingface-cli login`。

### SkillAnchor encoder 基线（也可用百度 `baseline_encoders/` 离线包）

```bash
huggingface-cli download FacebookAI/xlm-roberta-large \
  --local-dir $ROOT/models/xlm-roberta-large
huggingface-cli download jjzha/esco-xlm-roberta-large \
  --local-dir $ROOT/SCESC-LLM-skill-extraction/Baseline_Models_Collection/esco-xlm-roberta-large
huggingface-cli download urchade/gliner-multi-v2.1 \
  --local-dir $ROOT/SCESC-LLM-skill-extraction/Baseline_Models_Collection/gliner-multi-v2.1
huggingface-cli download jjzha/jobbert-base-cased \
  --local-dir $ROOT/models/jobbert-base-cased
huggingface-cli download hfl/chinese-roberta-wwm-ext \
  --local-dir $ROOT/SCESC-LLM-skill-extraction/Baseline_Models_Collection/chinese-roberta-wwm-ext
huggingface-cli download hfl/chinese-roberta-wwm-ext-large \
  --local-dir $ROOT/SCESC-LLM-skill-extraction/Baseline_Models_Collection/chinese-roberta-wwm-ext-large
huggingface-cli download microsoft/mdeberta-v3-base \
  --local-dir $ROOT/SCESC-LLM-skill-extraction/Baseline_Models_Collection/mdeberta-v3-base
```

Table II 的 **vanilla XLM-R 预测** 不必重训：用仓库  
`sricl-skillanchor-access-private-backup/output/xlmr_vanilla_20260827/`。

ESCO-XLM-R **微调过程**（`out_all/`、`out_full/` 含大量 `optimizer.pt`，共 ~90 GB）**不上传**。需要复现训练再跑 `Baseline_Models_Collection/esco-xlm-roberta-large` 里的脚本；评测用 GitHub dumps + 论文数字。

### Job Reco 向量模型

实验室 `job/local_bge_model` 只有配置、**没有** `pytorch_model.bin`。新机器：

```bash
huggingface-cli download BAAI/bge-large-zh-v1.5 \
  --local-dir $ROOT/Job_Reco_test/job/local_bge_model
```

Spark 3.4.2、CUDA、JDK 均从官网装，不要从网盘还原安装包。

---

## 4. 百度目录 ↔ 本地路径

| 百度 `$REMOTE/...` | 原实验室路径 | 约大小 | 说明 |
|---|---|---:|---|
| `CNSS_output/` | `.../Chinese_skill_benchmark_Paper/output` | 104 GB | JobBERT-zh / CRF `last.ckpt` |
| `CNSS_data/` | `.../Chinese_skill_benchmark_Paper/data` | 1.1 GB | Gold + DAPT jsonl |
| `access_rerun/` | `.../SCESC-LLM-skill-extraction/output/access_rerun` | 51 GB | SkillAnchor 实验 |
| `SCESC_data/` | `.../SCESC-LLM-skill-extraction/data` | 1.6 GB | 六语料 processed + RAG |
| `chinese_skillspan_preprocessing/` | 同名 | 0.9 GB | Doccano 流水线 |
| `LLaMA-Factory_data/` | `.../LLaMA-Factory/data` | 0.4 GB | SFT json |
| `baseline_encoders/` | `Baseline_Models_Collection` 中小模型 | ~14 GB | 不含 ESCO 90G 训练缓存 |
| `Job_Reco_BJ_utils/` | `Job_Reco_test/job/utils` | 16 GB | 查询向量 |
| `Job_Reco_data_bj/` | `Job_Reco_test/autodl-tmp/data_bj` | 5.2 GB | 人/岗源数据（三城市共用一份） |
| `sparksteps_tars/` | 打包后的 sparksteps | ~183 GB | 分卷 tar |
| `Pre-DyGAE/` | `/home/guojingli3/Pre-DyGAE` | 0.3 GB | 含 data |

---

## 5. 项目要点

**Chinese-SkillSpan**：conda 环境曾用 `LGJ_LLM_SE_Baseline`。CRF 脚本见 `Chinese_skill_benchmark_Paper/scripts/`。DAPT 句可从 jsonl 直接用，或用 `data/LARGE_DATA_MANIFEST.md` 从 CSV 重建。

**SkillAnchor**：生成器 = `Qwen/Qwen2.5-14B-Instruct` + `lora_finals/sft_*`。评测 `evaluate_src.py`。六语料 processed 在 `SCESC_data/annotated`。

**Job Reco**：代码在 `lab-code-misc-backup` 的 `Job_Reco_BJ/SH/SZ`。数据：`data_bj` + `sparksteps` + `utils`。BGE 必须按第 3 节下载。

---

## 6. 不要拷走的密钥

`api_key.py`、`~/.huggingface/token`、`~/.bypy/bypy.json`、GitHub token。新机器重新 `gh auth login`、`huggingface-cli login`、`bypy info`。
