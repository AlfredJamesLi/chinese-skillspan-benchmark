# 980 人标发布节奏（投出后再按天更新）

**当前已冻结公开：** page-1 **200** 句（`data/human_gold_page1_200.jsonl`）。  
**未标 / 未发布：** 780 句（`human980.jsonl` 第 201–980 行）。

投出 **PeerJ Computer Science** 初稿之后，每天把下一批 100 句人标推进 GitHub `main`（私有仓，评阅期按编辑要求再公开/Zenodo）。

| 日 | 980 行号 | 建议文件名 |
|---|---|---|
| 已完成 | 1–200 | `data/human_gold_page1_200.jsonl` |
| D+1 | 201–300 | `data/human_gold_page2_100.jsonl` → 合并 `human_gold_980_partial.jsonl` |
| D+2 | 301–400 | page3 |
| D+3 | 401–500 | page4 |
| D+4 | 501–600 | page5 |
| D+5 | 601–700 | page6 |
| D+6 | 701–800 | page7 |
| D+7 | 801–900 | page8 |
| D+8 | 901–980 | page9（80 句） |

规则（每天相同）：

1. 原文必须能对上 `human980.jsonl` 的 `id`；对不上先停。  
2. 不覆盖 `gold_canonical_v2.jsonl`，不自动覆盖 V4 hybrid 2601。  
3. 用 `scripts/build_and_eval_human200_page1.py` 的同类流程写评分金标 + QA + `cnss-lskt-1.2.0`。  
4. 新 F1 只进 `notes/confirmed-results.md` 的 **n=200/300/… 分析表**，不得改摘要 JobBERT 3M **0.4331**。  
5. `bash scripts/backup_push_github.sh "human gold pageN +100"`。

980 全部标完并裁决之前，**禁止**把人标写成论文主 Gold。
