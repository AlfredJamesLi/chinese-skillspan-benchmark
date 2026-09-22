# Codex Overleaf 更新提示词（2026-09-22 22:30 HKT，服务器 B 已收尾）

把下面整段交给 **Codex（论文/Overleaf 维护者）**。Cursor 不改 Overleaf。只填已验收数字。禁止脑补、禁止把未跑格子写成完成、禁止把 IEEE 10-epoch 填进本表。

机器可读备份（GitHub 即将推送的快照，以及服务器路径）：

- 服务器：`/home/guojingli3/cnss_external_benchmarks_20260921/receipts/paper_ready_tables_20260922.json`
- `results.jsonl`（逐 seed）、`comparisons.jsonl`（句级配对 bootstrap 2000，seed 20260921）
- 仓库快照目录名：`results_snapshots/external_benchmarks_20260922/`

**B 上本批次 GPU 矩阵已跑完。** 队列空。下面“unavailable”的项从未在 B 上得到原协议结果。

---

## 三条轨道

| 表 | 现在能否填 |
|---|---|
| `tab:external-common` | **填满 8 行**，n=3，mean ± sample SD（ddof=1），尺度 0–1 |
| `tab:external-chinese` | **填满 2 行**，n=3，Gold150 官方 scorer |
| `tab:external-native` | **拆行后填 Rerun**；Published 只从原论文抄。Kompetencer 分类、NNOSE、Gnehm 2022、商业 API 的 Rerun = unavailable，不是 0 |

线性头 ≠ MaChAmp-CRF ≠ NNOSE。三张表数字不可互换。中文字符跨度不可与 token-span 比绝对 F1。

方法段：共同协议、中文桥接、以及已跑的 native 改为过去时。Kompetencer/NNOSE 仍写在 A100 上尝试 / 因 Blackwell 无 CUDA 11 kernel 未在研究机 B 完成。Gnehm 全文 EDU/EXP/LNG 写 data unavailable。

`results.tex` 不要再写 “No neural-model score has been entered”。主论文实验草稿开关仍保持默认关闭，直到编译通过且你核过表。

---

## 表 `tab:external-common`（填这些）

协议：新 linear first-subword BIO 头；XLM-R-large @ `c23d21b0…`；ESCOXLM-R @ `8093cc37…`；AdamW \(2\times10^{-5}\)，batch 8，20 epoch；seed 42/43/44；dev typed exact 选模。**不是** 原 CRF/NNOSE。Gnehm = 公开 ICT，test **2557** 句。

建议格式 `$0.567 \pm 0.012$`。

| Dataset | Stream | Split | XLM-R | ESCOXLM-R |
|---|---|---|---|---|
| Skillspan | Skill | 4,800/3,174/3,569 | 0.567 ± 0.012 | 0.577 ± 0.006 |
| Skillspan | Knowledge | 同上 | 0.698 ± 0.021 | 0.672 ± 0.052 |
| Kompetencer | Skill | 778/346/262 | 0.545 ± 0.028 | 0.527 ± 0.004 |
| Kompetencer | Knowledge | 同上 | 0.618 ± 0.035 | 0.593 ± 0.044 |
| Gnehm public ICT | Skill | 19,889/2,332/2,557 | 0.891 ± 0.005 | 0.867 ± 0.032 |
| Green | Skill | 8,669/964/335 | 0.493 ± 0.009 | 0.491 ± 0.008 |
| Sayfullina | Skill | 3,705/1,855/1,851 | 0.920 ± 0.004 | 0.925 ± 0.005 |
| Fijo | Skill | 399/50/50 | 0.343 ± 0.019 | 0.339 ± 0.007 |

四位小数备查：Skillspan skill 0.5674±0.0121 / 0.5773±0.0056；knowledge 0.6985±0.0214 / 0.6717±0.0517；Kompetencer skill 0.5447±0.0276 / 0.5272±0.0044；knowledge 0.6181±0.0348 / 0.5934±0.0439；Gnehm 0.8907±0.0051 / 0.8674±0.0321；Green 0.4928±0.0094 / 0.4915±0.0075；Sayfullina 0.9197±0.0036 / 0.9253±0.0048；Fijo 0.3429±0.0189 / 0.3387±0.0073。

**禁止写 “domain-adaptive pretraining consistently helps”。** ESCO − XLM-R 三 seed 均值差与句级配对 bootstrap 95% CI：

| 比较 | 差 | CI |
|---|---|---|
| Skillspan skill | +0.010 | [−0.003, +0.023]（含 0） |
| Skillspan knowledge | −0.027 | [−0.041, −0.013] |
| Kompetencer skill | −0.018 | [−0.063, +0.022] |
| Kompetencer knowledge | −0.025 | [−0.102, +0.056] |
| Gnehm | −0.023 | [−0.034, −0.013] |
| Green | −0.001 | [−0.021, +0.017] |
| Sayfullina | +0.006 | [−0.000, +0.011] |
| Fijo | −0.004 | [−0.043, +0.038] |

CI 不含 0 **不得**自动写成多重比较后的显著优于。Skillspan knowledge ESCO seed 43 选了 epoch 1（F1 0.612）；Gnehm ESCO seed 42 选了 epoch 2（F1 0.830）。保留，不要删 seed。Fijo test 仅 50 句。禁止按绝对 F1 给数据集排难度。

---

## 表 `tab:external-chinese`（填这些）

B2 2150/169 训练/选模；Gold150 150 条只作最终诊断，官方 `cnss-lskt-1.2.0`。新 LSKT linear 头，不是 JobBERT-zh CRF。尺度 0–1。n=3。

| Encoder | Exact | Relaxed | Boundary | Macro-F1 |
|---|---|---|---|---|
| XLM-R-large | 0.522 ± 0.022 | 0.650 ± 0.021 | 0.571 ± 0.022 | 0.607 ± 0.016 |
| ESCOXLM-R | 0.538 ± 0.021 | 0.662 ± 0.022 | 0.582 ± 0.024 | 0.622 ± 0.010 |

逐 seed exact：XLM-R 0.500 / 0.522 / 0.545（epoch 11/14/14）；ESCO 0.516 / 0.540 / 0.558（epoch 19/15/10）。三 seed 上 ESCO exact 都高约 **+0.016**。不要和 JobBERT-zh CRF ~0.55 塞进同一格。脚注：Gold150 不是新盲测；L 仅 2 个 gold span。Relaxed 高于 exact，差异主要来自边界，但主结论仍用 typed exact。

---

## 表 `tab:external-native`（拆行 + Rerun）

把挤在一行的方法拆开。Published 只从原文表抄（写清 table/subset/metric/scale）。Rerun 用下面数字。**不要**把共同协议线性头 F1 填进 Rerun。

### SkillSpan 公开 HOUSE+TECH（无 BIG），MaChAmp seq_bio CRF，20 epoch，种子 3477689/4213916/8749520/6828303/9364029

主报建议：**MaChAmp 自带 span_f1，分 HOUSE / TECH**（与原评测更接近）。括号内为按任务列重算的 BIO pooled（HOUSE+TECH 合并）。

JobBERT **skills** MaChAmp：HOUSE **0.534 ± 0.014**，TECH **0.538 ± 0.013**（pooled BIO 0.525 ± 0.008）。  
JobBERT **knowledge** pooled BIO **0.654 ± 0.003**（HOUSE 0.575 ± 0.004，TECH 0.689 ± 0.005）。  
JobSpanBERT skills MaChAmp：HOUSE 0.543 ± 0.013，TECH 0.519 ± 0.010（pooled 0.522 ± 0.008）；knowledge pooled 0.628 ± 0.008。  
BERT skills MaChAmp：HOUSE 0.496 ± 0.013，TECH 0.514 ± 0.012（pooled 0.495 ± 0.011）；knowledge pooled 0.639 ± 0.005。  
SpanBERT skills MaChAmp：HOUSE 0.516 ± 0.014，TECH 0.526 ± 0.014（pooled 0.511 ± 0.012）；knowledge pooled 0.632 ± 0.009。

`multi` **未跑** → 该行 Pending 或删并脚注 “multi not rerun”。

### Gnehm 公开 ICT（test 2557），不是 2022 EDU/EXP/LNG

- jobBERT-de，MaChAmp 20 epoch，5 种子 276800/381552/497646/624189/884832：Rerun **0.885 ± 0.010**
- ESCOXLM-R，原 5 epoch 配置（补了新 MaChAmp 所需 `shuffle`/`diverse`/`reset_transformer_model`，lr 与 epoch 未改）：Rerun **0.891 ± 0.005**

Gnehm 2022 全文任务：Rerun **unavailable**（无原始输入）。Published 若引用 2022 全文数字，必须标明 subset 不是本 ICT 公开集。

### 仍 unavailable（Rerun 不要填 0，不要抄 Published）

- Kompetencer 细粒度分类（AllenNLP 2.8 / torch 1.8）：研究机 B 为 Blackwell sm_120，旧 wheel 无 kernel。HF BIO span-F1 **不得**填分类栏。
- NNOSE / JobBERTa 检索增强：同样需要 CUDA 11 栈；计划在 A100 上尝试。仓库 json ≠ 本包 HF json。
- 商业 API LLM：blocked。

---

## 文风

- Pending/unavailable ≠ 0 分。
- 不要改既有 Qwen / JobBERT-zh 主表来“对齐预算”。
- 不要把 train-only lexicon 标成神经 SOTA。
- 跨语言绝对 F1 禁止当难度排名。
- 中文 ESCO 小幅正差（+0.016）**不足以**写成领域预训练在中文上稳定增益；与共同协议英/德/法等混合符号一并讨论。

## 验收

1. common 八行不是 Pending，XLM-R/ESCO 没有填反。  
2. chinese 两行 n=3，不是两 seed。  
3. native 已拆行；分类/NNOSE/Gnehm2022 未用 span-F1 或 0 填。  
4. 方法段写明 linear head ≠ CRF。  
5. 没有 “ESCO consistently outperforms XLM-R”。  
6. 编译通过。
