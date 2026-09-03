# Hugging Face 模型（Chinese-SkillSpan）

本仓库 Git 不含 encoder 权重。换机除百度 `CNSS_output/` 外，须从 **Hugging Face** 准备下列公有模型。国内：`export HF_ENDPOINT=https://hf-mirror.com`。

总表（含 SkillAnchor / Job Reco）：实验室 `ACCOUNT_REPRO_FROM_BAIDU.md` 与百度 `/账号交接_20260901/MODELS_CATALOG.md`。

| 用途 | 类型 | HF ID | 命令 |
|---|---|---|---|
| JobBERT-zh DAPT **初始化** | 中文 RoBERTa base | `hfl/chinese-roberta-wwm-ext` | `huggingface-cli download hfl/chinese-roberta-wwm-ext --local-dir ../Baseline_Models_Collection/chinese-roberta-wwm-ext` |
| Vanilla-large V4 CRF | 中文 RoBERTa large | `hfl/chinese-roberta-wwm-ext-large` | 已有脚本 `scripts/download_cn_roberta_wwm_ext_large.py` |
| SOP/LLM 抽取臂（非主表 encoder） | 14B Instruct | `Qwen/Qwen2.5-14B-Instruct` | 放到父目录 `../Qwen2.5-14B-Instruct` |
| 同上 Llama 臂 | 8B Instruct | `meta-llama/Meta-Llama-3-8B-Instruct` | 需 Meta 许可；`huggingface-cli login` |
| 自训 JobBERT-zh / CRF | checkpoint | [`AlfredJames/jobbert-zh`](https://huggingface.co/AlfredJames/jobbert-zh)（已公开；encoder + `crf/best.pt`） | 百度 `$REMOTE/CNSS_output` 仍为实验室备份 |

论文主数字可用仓内 `data/frozen_preds/`，不必先下 14B。重训 JobBERT 必须有 `hfl/chinese-roberta-wwm-ext`（或百度 `baseline_encoders/` 离线包）。
