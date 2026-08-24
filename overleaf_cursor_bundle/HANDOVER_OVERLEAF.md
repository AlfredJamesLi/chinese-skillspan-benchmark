# Overleaf 窗口交接（Chinese-SkillSpan Benchmark）

本文件是本机 Overleaf 编辑窗口的背景。先读完再改 tex。  
日期：2026-08-22。数字以服务器 `Chinese_skill_benchmark_Paper/notes/confirmed-results.md` 和用户上传 PDF 为准；**当前表仍为空**。

**本窗口：** 本机 Overleaf Git（路径由用户填入后锁定）

**服务器论文窗口（本窗口不代替实验）：**  
`/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/`

**不要打开：** Access / SRICL 的 `access_paper/overleaf_cursor_bundle`。

状态标记与服务器 `HANDOFF.md` 相同：已确认 / 暂定 / 待验证 / 已废弃 / 未解决。

压缩表：`.cursor/skills/cnss-overleaf/confirmed-results.md`  
禁写：`.cursor/skills/cnss-overleaf/not-for-paper.md`  
冲突时以**本文 + 已确认表**为准并报告。

---

## 0. 职责与禁止

**只做：** 检查/修改本文 LaTeX；把「已确认」写入论文；更新图、表、图题；用户确认后才可 commit/push。

**禁止：** 训练、sbatch、conda 实验、猜 F1、把 Access / SRICL / 六语料英文主表写进本文、擅自 commit/push/删文件/force push。

主编译文件名：上传 PDF 或 Overleaf 工程就位后再填（现为 **未解决**）。

开始前：

```powershell
pwd
git status
git pull --ff-only origin main
git branch --show-current
```

论文数字与「已确认」不一致：先报告（路径 / 论文现值 / 已确认值）。出现第三套数字则停止。

---

## 1. 研究问题（待 PDF 确认）

中文招聘文本上的技能相关跨度抽取与 LKST 维度。细节等 `pdf/` 最新稿。

---

## 2. 已确认数字

见 `.cursor/skills/cnss-overleaf/confirmed-results.md`。在服务器窗口从 PDF 抽出并同步到本包之前，**不要填主表**。

---

## 3. 下一阶段

**P0：** 等服务器窗口根据上传 PDF 更新 confirmed-results，再对照 Overleaf tex 做冲突表。  
**P1：** 版式、图题、参考文献（数字不动）。  
**P2：** 缺 dump / 要重打分 → 交回服务器窗口。
