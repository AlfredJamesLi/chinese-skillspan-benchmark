# Codex Overleaf 更新提示词（2026-09-24 11:45 HKT，服务器 A 已收尾）

把下面整段交给 **Codex（论文/Overleaf 维护者）**。Cursor 不改 Overleaf。只填已验收数字。禁止脑补、禁止把未跑格子写成完成、禁止把共同协议线性头填进 native 分类/NNOSE 栏。

机器可读备份（已推 GitHub `results/a-native-20260924`，commit `b8a7ae5`）：

- https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/tree/results/a-native-20260924/results_snapshots/a_native_20260924
- 提示词：https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/blob/results/a-native-20260924/docs/CODEX_OVERLEAF_A_NATIVE_20260924.md
- 服务器 A：`/home/guojingli3/cnss_a_native_20260922/A_NATIVE_RECEIPT.md`
- `paper_ready_a_native_20260924.json`、逐 seed `results.jsonl`

B 上 2026-09-22 批次（`results/external-benchmarks-20260922`，commit `166b882`）**不要改**：`tab:external-common` 8 行、`tab:external-chinese` 2 行、native 里 SkillSpan MaChAmp CRF 与 Gnehm 公开 ICT。本提示词只补 **A100 上才跑成的** Kompetencer **分类** 与 **NNOSE**。

**A 上本批次 GPU 矩阵已跑完。** 队列空。

---

## 三条轨道（与 B 提示词相同，勿混）

| 表 | 现在能否填 |
|---|---|
| `tab:external-common` | **保持 B 的 8 行**。禁止用 A 的数字改它 |
| `tab:external-chinese` | **保持 B 的 2 行** |
| `tab:external-native` | **拆行后填 Rerun**。Published 只从原论文抄。本提示词填 Kompetencer 分类 + NNOSE。BERT/JobBERT/DaBERT 分类、Gnehm 2022、商业 API、NNOSE ∀D 仍 unavailable，不是 0 |

线性头 ≠ MaChAmp-CRF ≠ NNOSE ≠ Kompetencer sklearn-macro 分类。四套数字不可互换。不要把 B 的 Kompetencer span-F1 ~0.53–0.62 填进分类栏。

方法段：Kompetencer 分类与 NNOSE 改为在 **A100 (DS209213, CUDA 11 栈)** 完成；研究机 B Blackwell 无 kernel 的句子改成过去时（B 未完成，A 完成）。Gnehm 全文 EDU/EXP/LNG 仍 data unavailable。

`results.tex` 不要再写 “No neural-model score has been entered” 来指这两块。主论文实验草稿开关仍保持默认关闭，直到编译通过且你核过表。

---

## 表 `tab:external-native` — Kompetencer 细粒度 ESCO **分类**（填这些）

协议：MaChAmp / AllenNLP 2.8 / torch 1.8.1+cu111；20 epoch；种子 3477689/4213916/8749520/6828303/9364029；dev = `3_en_dev.tsv`；**sklearn macro-F1，尺度 0–1，n=5，mean ± sample SD (ddof=1)**。评估主列：**da_test**（784 条 classified span）。

**不是** span-F1。**不是** weighted-F1（plot ylabel 是 Weighted macro-F1，仅作对照，不进 Rerun）。

建议格式 `$0.182 \pm 0.034$`。单 seed 无 ±。

google/rembert pin `65da5133…`。`jjzha/dajobbert-base-cased` Hub 重定向到 **uncased** `b9970acc…` — 脚注写清，不是静默 cased 复现。

| 设定（对应 LREC 图柱） | 训练 | Rerun sklearn-macro da_test | 同设定 weighted（对照，勿填 Rerun） | plot 里 da_test（Published，勿抄进 Rerun） |
|---|---|---|---|---|
| DaJobBERT (DA) | `2_da_train` 138 条 | **0.182 ± 0.034** | 0.385 ± 0.026 | 0.395 ± 0.021 |
| RemBERT (DA) | 同上 | **0.050 ± 0.072** | 0.133 ± 0.139 | 0.166 ± 0.141 |
| RemBERT (EN) 零样本 EN→DA | EN train/dev | **0.261 ± 0.019** | 0.343 ± 0.040 | 0.354 ± 0.021 |
| RemBERT (EN+DA) | enda 多语 | **0.316 ± 0.019** | 0.468 ± 0.011 | 0.472 ± 0.014 |
| DaJobBERT (EN+DA) | enda（原图无此柱） | **0.340 ± 0.017** | 0.518 ± 0.010 | — |

四位小数备查：DaJobBERT-DA 0.1824±0.0339；RemBERT-DA 0.0503±0.0721；RemBERT-EN→DA 0.2612±0.0187；RemBERT-enda 0.3163±0.0190；DaJobBERT-enda 0.3404±0.0174。

额外（不必进主表）：en_test sklearn-macro DaJobBERT-EN **0.539 ± 0.010**，RemBERT-EN **0.552 ± 0.017**，RemBERT-enda **0.554 ± 0.014**。

**禁止**把上述 Rerun 写成“复现了 LREC 图”。sklearn-macro 与 plot 的 Weighted macro-F1 不是同一指标。数值接近（尤其 RemBERT EN+DA weighted 0.468 vs 0.472）**不足以**写成 match。脚注：**current cannot judge** full official-matrix alignment。

未跑：BERT (EN)、JobBERT (EN)、DaBERT (DA) 分类 → Rerun **unavailable**，不要填 0，不要抄 Published。

---

## 表 `tab:external-native` — NNOSE / JobBERTa（填这些）

协议：官方 NNOSE 栈 torch 1.10.1+cu113 + adapter-transformers 3.2.0 + faiss 1.7.2；seed **113412**（单 seed，**禁止假 SD**）；20 epoch patience；**in-dataset** train-only datastore（不是 ∀D / `DATASTORE=AD`）；dev 扫 k/λ/T，冻结后 **test.json 一次**；指标 **seqeval span F1，0–1**。

`jjzha/jobbert-base-cased` @ `eee1c8da…`。`jjzha/jobberta-base` @ `6b2dd251…`（确已下载，不是 JobBERT 改名）。

建议：主报 **kNN（dev 冻结）**，括号或邻列给 linear head。不要把 B 的 Green/Sayfullina 共同协议线性头（~0.49 / ~0.92，n=3）填进 NNOSE 行。

| Dataset | test n | encoder | ckpt | frozen (k, λ, T) | linear F1 | knn F1 |
|---|---:|---|---|---|---:|---:|
| SkillSpan 公开 HOUSE+TECH | 3569 | JobBERT | epoch_17 | 16, 0.25, 3.0 | 0.613 | **0.612** |
| SkillSpan | 3569 | JobBERTa | epoch_6 | 8, 0.4, 0.5 | 0.631 | **0.625** |
| Green | 335 | JobBERT | epoch_1 | 128, 0.2, 2.0 | 0.491 | **0.500** |
| Green | 335 | JobBERTa | epoch_3 | 128, 0.5, 0.5 | 0.466 | **0.485** |
| Sayfullina | 1851 | JobBERT | epoch_7 | 16, 0.85, 0.5 | 0.897 | **0.896** |
| Sayfullina | 1851 | JobBERTa | epoch_6 | 128, 0.6, 0.1 | 0.915 | **0.912** |

全精度：SkillSpan JobBERT 0.6129447 / 0.6122536；JobBERTa 0.6306194 / 0.6248711；Green JobBERT 0.4910591 / 0.5003446；JobBERTa 0.4658691 / 0.4847626；Sayfullina JobBERT 0.8969697 / 0.8959538；JobBERTa 0.9152815 / 0.9120469。

**禁止**写 “kNN consistently helps”。SkillSpan / Sayfullina 上 knn 未超过 linear；Green 上 knn 略高。这是观察，不是结论。NNOSE ∀D 未跑 → 不要写成完成。EACL Published **不要**抄进 Rerun；与原文哪一格对齐 **current cannot judge**（需 table/subset/scale）。

---

## 文风

- Pending/unavailable ≠ 0 分。
- 不要改既有 Qwen / JobBERT-zh 主表，也不要改 B 的 common / chinese 数字。
- 不要把 train-only lexicon 标成神经 SOTA。
- 跨语言绝对 F1 禁止当难度排名。
- 不要写 “domain-adaptive pretraining consistently helps”。
- 不要把 DaJobBERT 写成 cased 精确复现。

## 验收

1. common 八行、chinese 两行与 B 提示词一致，未被 A 覆盖。  
2. native 已拆行：SkillSpan MaChAmp CRF 仍用 B 的数字；分类栏是 sklearn-macro，不是 span-F1。  
3. NNOSE 行是单 seed span F1，不是 B Green/Sayfullina n=3 线性头。  
4. BERT/JobBERT/DaBERT 分类、Gnehm2022、商业 API、NNOSE ∀D 未用 0 或 Published 填。  
5. 没有 “ESCO consistently outperforms XLM-R”，没有 “kNN consistently helps”，没有 “we reproduced the LREC plot”。  
6. 编译通过。
