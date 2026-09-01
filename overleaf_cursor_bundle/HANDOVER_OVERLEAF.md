# Overleaf 窗口交接（Chinese-SkillSpan Benchmark）

本文件是本机 Overleaf 编辑窗口的背景。先读完再改 tex。  
日期：2026-08-27。投稿期刊：**PeerJ Computer Science**（不是 DASFAA）。数字以 `.cursor/skills/cnss-overleaf/confirmed-results.md` 为准（已从服务器同步）。

**本窗口：** 本机 Overleaf Git（项目 https://www.overleaf.com/project/68fe17a53e53a7f800e4f2b4 ；`git.overleaf.com/68fe17a53e53a7f800e4f2b4`）

**服务器论文窗口（本窗口不代替实验）：**  
`/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/`  
GitHub 私有备份：https://github.com/AlfredJamesLi/chinese-skillspan-benchmark

**不要打开：** Access / SRICL 的 `access_paper/overleaf_cursor_bundle`。

状态标记：已确认 / 暂定 / 待验证 / 已废弃 / 未解决。

压缩表：`.cursor/skills/cnss-overleaf/confirmed-results.md`  
禁写：`.cursor/skills/cnss-overleaf/not-for-paper.md`  
手册：**主协议 = B / V4**；A 只作 Gold v2 沿革：`handbooks/`  
Codex 先咨询 V4 主表 Methods：`CODEX_PROMPT_HANDBOOK.md`  
Codex 改稿：`CODEX_PROMPT_ALL.md`  
表 CSV：`tables/`  
SkillSpan 体例图：`figures/`（插入稿 `CODEX_PROMPT_FIGURES.md`）

冲突时以**本文 + 已确认表**为准并报告。

---

## 0. 职责与禁止

**只做：** 检查/修改本文 LaTeX；把「已确认」写入论文；更新图、表、图题；用户确认后才可 commit/push。

**禁止：** 训练、sbatch、conda 实验、猜 F1、把 Access / SRICL / 六语料英文主表写进本文、擅自 commit/push/删文件/force push。

开始前：

```
pwd
git status
git pull --ff-only origin main
git branch --show-current
```

论文数字与「已确认」不一致：先报告（路径 / 论文现值 / 已确认值）。出现第三套数字则停止。

---

## 1. 研究问题

中文招聘文本上的技能相关跨度抽取（flat LSKT：L/K/S/T）。**论文主金标 = V4 hybrid**（与 Gold v2 同一批 2601 ID）。主指标 typed exact micro F1（`cnss-lskt-1.2.0`）。Gold v2 文件冻结，F1 只进附录。

---

## 2. 已确认数字

见 `.cursor/skills/cnss-overleaf/confirmed-results.md`。

要点：

- PDF Table 3 **保留**（Gold 2676 paper S-F1）。
- **主结果表 = V4**（JobBERT 3M exact **0.4331**；ChatGPT dump+jieba exact **0.2854** / relaxed **0.6249**）。
- Gold v2 unique-first（ChatGPT **0.6365**、编码器 ~0.13）改为 **附录**。不要用 0.6365 覆盖 PDF 0.6700，也不要写进摘要 SOTA。
- Methods：手册 B 为报告协议；手册 A 只写「同一批 ID 的源跨度」。不要覆盖 Gold v2，不要把 980 写成全量人标。
- 删除 Concept Accuracy / Time-OOD；分域表只作为 Industry-OOD **代理**。

---

## 3. 下一阶段

**P0：** 对照 Overleaf tex 与 confirmed-results 做冲突表，再补表。  
**P1：** 版式、图题、参考文献（数字不动）。 Methods 写成 **V4 主协议** 前，先贴 `CODEX_PROMPT_HANDBOOK.md`（只咨询，不改 tex）。  
**P2：** 缺 Claude/Kimi 完整 dump 的 P2 主表行 → 交回服务器窗口。 JobBERT 1M goldstyle 5-seed Gold v2 均值 **0.1257±0.0062** 已写入（四模型对比仍用 3-seed **0.1288**）。 RoBERTa-wwm v3 Gold v2 3-seed 均值 **0.1199** 已写入。
