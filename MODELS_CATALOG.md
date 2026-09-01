# 模型与下载渠道总表（百度备份备注）

本文件同时放在 GitHub 各项目仓与百度 `/账号交接_20260901/MODELS_CATALOG.md`。  
换机时：**自训权重从百度拉；公有基座优先 Hugging Face。**  
国内可设 `export HF_ENDPOINT=https://hf-mirror.com`。需许可的模型先 `huggingface-cli login`。

网页：百度网盘 → **我的应用数据 → bypy**（不是「我的文件」根目录）→ `/账号交接_20260901/`。

## 百度交接包目录备注（类型 + 渠道）

| 百度路径 `/账号交接_20260901/…` | 内容类型 | 下载渠道备注 |
|---|---|---|
| `MODELS_CATALOG.md`（本文件） | 文档 | 与 GitHub 同步；模型类型与渠道以本表为准 |
| `ACCOUNT_REPRO_FROM_BAIDU.md` | 换机步骤 | GitHub 同名文件 |
| `CNSS_output/` | 自训 JobBERT-zh / CRF checkpoint | **仅百度**，无 HF 公仓 |
| `access_rerun/` | SkillAnchor 实验产物 / dumps | **仅百度**；评测 dumps 另在 GitHub `sricl-skillanchor-access-private-backup` |
| `CNSS_data/`、`SCESC_data/`、`chinese_skillspan_preprocessing/`、`LLaMA-Factory_data/` | 标注与训练 json | **仅百度**（Gold 子集也在 GitHub） |
| `baseline_encoders/` | Encoder **离线包**（RoBERTa / ESCO-XLM-R 基座 / GLiNER / mDeBERTa / DaJobBERT 等） | **百度或 HF**，见下表；不含 ESCO `optimizer.pt` |
| `Job_Reco_BJ_utils/`、`Job_Reco_data_bj/`、`sparksteps_tars/` | Job Reco 处理后数据 | **仅百度** |
| `Pre-DyGAE/` | 代码+小数据 | 代码也在 GitHub `lab-code-misc-backup` |
| （不在交接包）三份招聘 CSV | 原始语料 | 百度根目录 2026-08-23 已传 |
| （故意不上百度）14B / 8B / E5 / CrossEncoder / BGE 权重 | 公有基座 | **仅 Hugging Face**，见下表 |

## 模型类型与下载渠道

| 模型 ID | 类型 | 用于 | 体积量级 | 渠道 | 放到 |
|---|---|---|---|---|---|
| `Qwen/Qwen2.5-14B-Instruct` | 生成器 14B Instruct | SkillAnchor 正式生成器；CNSS SOP/LLM 臂 | ~28 GB | **仅 HF** | `SCESC-LLM-skill-extraction/Qwen2.5-14B-Instruct` |
| `meta-llama/Meta-Llama-3-8B-Instruct` | 生成器 8B Instruct | SkillAnchor 历史 Llama 臂；CNSS SOP | ~16 GB | **仅 HF**（需 Meta 许可） | `LLaMA-Factory/Meta-Llama-3-8B-Instruct` |
| `AlfredJames/skillanchor-qwen25-14b-lora-private` | LoRA 适配器（rank 见 adapter_config） | SkillAnchor 六语料 + CN NER | ~1.4 GB | **HF private** | `lora_finals/` |
| `FacebookAI/xlm-roberta-large` | Encoder XLM-R large | SkillAnchor Table II vanilla | ~2.2 GB | HF；评测 dumps 已在 GitHub | `models/xlm-roberta-large` 或 `access_rerun/.../backbone` |
| `jjzha/esco-xlm-roberta-large` | Encoder XLM-R + ESCO DAPT | SkillAnchor Table II ESCOXLM-R | ~2.1 GB | HF **或** 百度 `baseline_encoders/esco-xlm-roberta-large` | `Baseline_Models_Collection/esco-xlm-roberta-large` |
| `urchade/gliner-multi-v2.1` | 通用 NER（GLiNER） | SkillAnchor Table II | ~2 GB | HF **或** 百度 `baseline_encoders/gliner-multi-v2.1` | 同名目录 |
| `jjzha/jobbert-base-cased` | Encoder BERT JobBERT | SkillAnchor JobBERT 臂 | ~0.4–0.8 GB | HF；本机另有 token-class 头 | `jobbert_skill_extraction` / `jobbert_knowledge_extraction` |
| `jjzha/dajobbert-base-uncased` | Encoder BERT 丹麦 Job | Kompetencer JobBERT | ~4 GB 本机快照 | HF **或** 百度 `baseline_encoders/dajobbert-base-uncased` | 同名 |
| `hfl/chinese-roberta-wwm-ext` | Encoder 中文 RoBERTa base | CNSS JobBERT-zh DAPT 初始化 | ~0.4–1.2 GB | HF **或** 百度 `baseline_encoders/chinese-roberta-wwm-ext` | 同名 |
| `hfl/chinese-roberta-wwm-ext-large` | Encoder 中文 RoBERTa large | CNSS vanilla-large V4 CRF | ~1.3 GB | HF **或** 百度 `baseline_encoders/chinese-roberta-wwm-ext-large` | 同名 |
| `microsoft/mdeberta-v3-base` | Encoder mDeBERTa | SkillAnchor 辅助基线 | ~0.5–3 GB（勿下 tf `.h5`） | HF **或** 百度 `baseline_encoders/mdeberta-v3-base` | 同名 |
| `intfloat/multilingual-e5-large-instruct` | 检索嵌入 E5 | SkillAnchor RAG-1/RAG-2、`demo_retrieval.py` | ~1–2 GB | **HF（复现文档原先未写清，必须下）** | Hugging Face cache 或本地 `models/e5` |
| `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1` | Cross-Encoder 重排 | `utils/rag_local.py` | ~100 MB | **HF** | sentence-transformers 自动缓存 |
| `sentence-transformers/all-MiniLM-L6-v2` | 小型句向量 | 旧 RAG 脚本 `rag_prompt.py` | ~80 MB | **HF**（主实验已改用 E5） | 自动缓存 |
| `BAAI/bge-large-zh-v1.5` | 中文检索嵌入 BGE | Job Reco `local_bge_model` | ~1.3 GB | **HF（实验室目录几乎无权重）** | `Job_Reco_*/job/local_bge_model` |
| `Qwen/Qwen1.5-1.8B-Chat` | 小生成器 | `model_zoo.py` 默认 local，**非论文主表** | ~4 GB | HF，可选 | 仅调试 |

自训、不在 HF 公仓：CNSS `output/*.ckpt`、SkillAnchor `access_rerun/`、Job Reco `sparksteps`/`utils`/`data_bj` → **只走百度** `/账号交接_20260901/`。招聘原始 CSV 在百度根目录三份语料夹。

**不要从 HF 找、也不上传百度：** CUDA `.run`、Spark 发行版、JDK。Spark：https://spark.apache.org/downloads.html （3.4.2 Hadoop3）。IEEE Access 模板 `ieeeaccess.cls`：IEEE 官网模板 zip。

```bash
huggingface-cli download intfloat/multilingual-e5-large-instruct
huggingface-cli download cross-encoder/mmarco-mMiniLMv2-L12-H384-v1
huggingface-cli download Qwen/Qwen2.5-14B-Instruct --local-dir ./Qwen2.5-14B-Instruct
huggingface-cli download BAAI/bge-large-zh-v1.5 --local-dir ./Job_Reco_test/job/local_bge_model
huggingface-cli download AlfredJames/skillanchor-qwen25-14b-lora-private --local-dir ./lora_finals
```
