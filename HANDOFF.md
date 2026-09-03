# Chinese-SkillSpan 论文 — 服务器窗口交接

日期：2026-08-22。本窗口准备 **Chinese Skill Benchmark / Chinese-SkillSpan** 文，投稿 **PeerJ Computer Science**，不是 DASFAA，也不是 IEEE Access / SRICL。

**本窗口：** 服务器  
`/home/guojingli3/SCESC-LLM-skill-extraction`  
论文材料只写在：`Chinese_skill_benchmark_Paper/`

**GitHub 私有备份（2026-08-26）：** https://github.com/AlfredJamesLi/chinese-skillspan-benchmark — 见 `PUSH_GITHUB.md`、`REPRO_GITHUB.md`。  
**Overleaf（本机改 tex；此服务器无法登录）：** https://www.overleaf.com/project/68fe17a53e53a7f800e4f2b4 — **2026-08-27：论文主评测只用 V4**（手册 B；与 Gold v2 同一批 2601 ID）。Gold v2 文件不覆盖，F1 进附录。手册：`notes/handbooks/`。SkillSpan 体例图：`figures/` + `tex/skillspan_style_*.tex`；本机贴 `CODEX_PROMPT_FIGURES.md` 插入。禁止把 0.4331 与 0.6365 写进同一句 SOTA。禁止把 V4 hybrid 写成人工 Doccano Gold。  
**7 天窗口：** `notes/SEVEN_DAY_WINDOW.md`。每次实验结束后 `bash scripts/backup_push_github.sh`。

**姐妹文（禁止混写）：** IEEE Access 方法文 SRICL，arXiv `2604.21525`，目录 `access_paper/`。

状态标记：

| 标记 | 含义 |
|---|---|
| **已确认** | 有 PDF 或 dump + 约定评测，且应写入论文 |
| **暂定** | 版式/投稿材料，不改变数字 |
| **待验证** | 有作业或内部计数，未按论文协议打分，不得写成结论 |
| **已废弃** | 禁止再写入 |
| **未解决** | 本窗口可做版式，或必须先补实验 |

协议冻结：`notes/DATA_PROTOCOL_FREEZE.md`  
压缩表：`notes/confirmed-results.md`  
决策：`reports/decision_table.md`  
禁写清单：`notes/not-for-paper.md`  
若压缩表与冻结协议冲突，**以冻结协议为准**，不要改 PDF。

---

## 0. 职责

**只做：** 读用户上传的 PDF；整理主张与数字；改本目录下的 tex / 表 / 图 / Overleaf 包；需要时只读父仓库里的中文数据与脚本。

**禁止：** 改 `access_paper/` 或 Access Overleaf 包；把 SRICL / 六语料英文主表写进本文；编造 F1；未确认就 commit/push；覆盖父仓库 `output/` 里 Access 重跑结果。

开始前先看 `pdf/` 是否已有最新稿。没有 PDF 时，只搭结构、列待填项，不要从记忆里填表。

---

## 1. 已知事实（可写进笔记，未对照 PDF 前不要当论文终稿）

- 项目名：Chinese-SkillSpan / Chinese Skill Benchmark。
- Access 交接里记过姐妹文 arXiv `2604.23009`（以用户上传 PDF 与投稿系统为准）。
- 标注体系含 LKST（L / K / S / T 等维度）；Gold 来自 Doccano。
- 数据主体：`chinese_skillspan_preprocessing/`（约 862MB）。
- 银标与推理走父目录 `main.py --dataset_name chinese_skillspan`，prompt 在 `prompt_template_rag.py` 的 `chinese_skillspan` 段。
- 中文 LoRA 在 `LLaMA-Factory/saves/qwen2_5_14b/lora/sft_CN_skillspan_*`。
- **两套 processed 数据可能不一致**，改数前先定权威路径：
  - `chinese_skillspan_preprocessing/data/annotated/processed/chinese_skillspan/`
  - `data/annotated/processed/chinese_skillspan/`

---

## 2. 用户下一步

1. 把最新 PDF 放到 `pdf/`。
2. 告知文件名后，抽出摘要/贡献/数据规模/主表，写入 `notes/confirmed-results.md`。
3. 论文主协议已定为 **V4 only**。本机 Overleaf 先贴 `CODEX_PROMPT_HANDBOOK.md`（咨询如何把 V4 写成主表、Gold v2 写成沿革），再贴 `CODEX_PROMPT_ALL.md`。
4. 若有 Overleaf 工程，把 `overleaf_cursor_bundle/` 拷到本机 Overleaf Git 根目录，另开窗口写作。

---

## 3. 下一阶段

**P0：** 等 PDF → 填 confirmed-results → 冲突表（PDF vs 仓库笔记）。  
**P1：** 在 `tex/` 或 Overleaf 包里改稿，数字不动则只动版式。  
**P2：** 需要新实验时交回本仓库实验脚本，不要在论文目录里重跑训练。  
**Vanilla large vs base（待验证，未入摘要）：** seed 42 已从服务器 B 拷回。`notes/vanilla_large_v4.md`、`notes/vanilla_wwm_v4_methods.md`。表稿 `tex/skillspan_style_vanilla_wwm_v4.tex`。Overleaf 咨询：`overleaf_cursor_bundle/CODEX_PROMPT_VANILLA_WWM.md`。摘要仍用 JobBERT 3M **0.4331**。50782 已取消。

**Human page-1 200（2026-09-03）：** 980 分歧队列前 200 句人标已入库 `data/human_gold_page1_200.jsonl`。附录/补充表数字在 `notes/confirmed-results.md`（ChatGPT exact **0.2772**）。**不覆盖** Gold v2，**不替换** V4 hybrid 2601，摘要仍用 **0.4331**。Overleaf：`overleaf_cursor_bundle/CODEX_PROMPT_HUMAN200.md`。其余 780 句投出后每天 +100，见 `reports/human980_doccano/RELEASE_PLAN_100_PER_DAY.md`。
