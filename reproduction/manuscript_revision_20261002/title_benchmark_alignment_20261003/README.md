# 题名与正文定位对齐（2026-10-03）

当前题名：**Chinese-SkillSpan: a benchmark for competency span extraction in Chinese job advertisements**。

已先快进同步用户在Overleaf改好的题名，再落实以下对齐：

- 摘要Methods明确Chinese-SkillSpan的benchmark定位，保留原结果和限制。
- 引言说明基准由标注指南、独立用途的数据子集、评分协议和模型基线组成；L/K/S/T与competency spans的术语解释不变。
- 结论首句与基准定位对应，仍明确人类参考集上的结果为诊断性评估。
- Table 1补入独立盲编一致性研究，按预测单位、标注层、材料呈现；具体规模留在现有Table 2和质量表，避免重复堆放。历史人工覆盖仍为500句，正式独立一致性研究仍为50句，不合计为550句。
- 精简参考集构成段落的末句，并让Appendices B and D整体不断行，修正D单独占行；段内所有数字与统计口径不变。
- 同时精简Table1材料列、将Appendix D连排，缩短实验总结段的极短段末行，并禁止JobSkape专名单词跨页断词。
- PDF标题属性自动读取LaTeX标题；仓库首页和论文目录注明最新题名，修正首页“未发布PDF”的过时说明，补独立盲编入口。
- CITATION.cff用于引用已归档的v0.1.3数据集，保留其原题名和DOI；通过message与首页区分数据引用和当前论文题名。历史发布、数据文件名和模型标识未改。

resource、dataset、corpus仍按各自含义保留；图1–图5的标签与图注未发现因新题名产生的冲突，无需重画。图2与Table 2已正确区分历史人工覆盖和独立三编码员研究。

验证：编译为40页，摘要Results、实验数字、公式和引用键均未修改；检查了题名/PDF属性、交叉引用及关键页面。Overleaf与GitHub的实际同步状态在本地发布回执记录。
