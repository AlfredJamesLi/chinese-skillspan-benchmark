# SkillSpan NAACL 2022 vs Chinese-SkillSpan — workload

Source PDF: `Sota-参考文献-2022.naacl-main.366.pdf`  
Zhang, Jensen, Sonniks, Plank. *SkillSpan: Hard and Soft Skill Extraction from English Job Postings.* NAACL 2022. Pages 4962–4984 (23 pp., long appendix).

This note is for **PeerJ Chinese-SkillSpan** only. Do not copy SkillSpan English F1 into our tables. Do not mix Gold v2 with P2.

## What the screenshots actually are

**Table 6 (p. 4981, Appendix E)** is **not** a new model zoo. It is Precision/Recall of the **same** fine-tunes already in Figure 3 / Table 5, sliced by source (BIG / HOUSE / TECH / AVERAGE / TEST), with **five-seed mean ± std**.

**Figure 7 (p. 4982, Appendix F)** is **not** extra training. It is Almost Stochastic Order (ASO, Dror et al. 2019) on the **development** 5-seed scores. Figure 4 is the same test on the **test** set. 8×8 cells = 4 encoders × {STL, MTL}. Dark green = row stochastically dominates column.

Counting every table cell as a training run inflates the workload. Real training is listed below.

## SkillSpan experimental inventory

### Data / annotation (main cost of a dataset paper)

| Item | SkillSpan |
|---|---|
| Annotated JPs | 391 (train 200 / dev 90 / test 101 majority-vote) |
| Sentences / tokens / spans | 14.5K / 232K / ~12.6K skill+knowledge |
| Sources | BIG, HOUSE, TECH (in-domain splits, not time-OOD) |
| Unlabeled DAPT corpus | 126.8K posts, 3.2M sentences, 460M tokens |
| Annotators / IAA | 3 annotators; Fleiss κ 0.70–0.75 on 101 JPs (~57.5K tokens) |
| Guidelines | Released, Appendix B (skill + knowledge rules, nesting) |
| Calendar | ~8 months annotation (Mar 2021 onward) |

### Pre-training (the expensive part we should **not** clone)

| Job | What they did |
|---|---|
| SpanBERT from scratch | BooksCorpus + Wikipedia, 2.4M steps, batch 256, seq 512, TPU v3-8, **14 days** |
| JobBERT | Continue BERT on 3.2M JP sentences, 3 epochs, batch 16 |
| JobSpanBERT | Continue their SpanBERT, 40K steps (~3 passes) |

### Fine-tuning (Table 5/6 density)

4 encoders: `BERTbase`, `SpanBERT`, `JobBERT`, `JobSpanBERT`.  
Each: STL-skill, STL-knowledge, MTL (hard sharing, two CRFs).  
Toolkit: MACHAMP, 20 epochs, **5 seeds** (listed in Appendix D).  
Plus Longformer (document 4096) as a **negative** result (5 seeds, no DAPT).

**Count:** 4 × 3 × 5 = **60** BERT fine-tunes, plus ~5 Longformer runs. Combined F1 is **aggregated STL predictions**, not a fourth training mode.

Hyperparameter table (Table 4) documents MACHAMP **defaults** and a small listed range; they did not publish a full grid search.

### Analysis (appendix look-and-feel)

- Table 5: span-F1 ± std by source × model × STL/MTL × SKILL/KNOWLEDGE/COMBINED, dev + test  
- Table 6: P and R for the same runs  
- Table 7: mean predicted span length vs gold, by source  
- Figure 5–6: length of predictions; F1 **by gold span length** (buckets 1–10)  
- Figure 4 + 7: ASO heatmaps, α=0.05, Bonferroni  
- Tables 8–9: top-10 skill/knowledge strings by split and source  
- Appendix A data statement; B guidelines; C qualitative; D seeds/hardware; E numbers; F ASO

**No LLMs.** Encoder-only paper.

## Chinese-SkillSpan — already done (do not invent F1)

Numbers only from `notes/confirmed-results.md`.

| Axis | Us | vs SkillSpan |
|---|---|---|
| Train sentences | 17460 | Larger than their 5866 |
| Gold types | LSKT (4) | Skill + Knowledge (2, nested) |
| DAPT | JobBERT-zh 1M and 3M on Chinese JDs | JobBERT 3.2M **sentences** (English) |
| Encoder fine-tune | RoBERTa-wwm CRF; JobBERT 1M/3M; domain-mix; listed-mix; CWS retrain; SOP vs goldstyle silver | 4 BERT variants × STL/MTL |
| Seeds | **3** on main encoders (JobBERT 1M mean 0.1288); RoBERTa 3-seed mean **not yet in Gold v2 encoder table** | **5** everywhere |
| Domain slice | 人工智能 / 阿里云 / 事业单位 (Industry-OOD **proxy**) | BIG / HOUSE / TECH |
| LLM | Frozen dumps + SOP extract 2601 (gpt-5.4, kimi-k2.6, DeepSeek v4-pro, Sonnet 4.5, Qwen Instruct, Llama-3-8B) | None |
| Extra protocol | Two golds (Gold v2 vs P2 SOP+jieba); jieba CWS diagnostics | One gold |
| Significance | Sample std over 3 seeds | ASO + Bonferroni |
| P/R appendix | Typed exact F1 primary; no SkillSpan-style P/R ± std table | Table 6 |
| Span-length F1 | Not yet an appendix figure | Figure 6 |

Encoder on Gold v2 remains a **weak baseline** (~0.13 typed) vs ChatGPT 0.6365. That is a result, not a missing SkillSpan clone.

## Verdict: can we be ≥ their workload?

**Breadth (dataset + LLM + two protocols + DAPT size variants): already ≥ SkillSpan.** A reviewer counting *systems evaluated* will see more rows on our side.

**Appendix visual density (Table 5/6 + ASO heatmaps): not yet equal.** Their appendix looks “many models” because 4×2×3 sources×5 seeds are printed as P, R, and F1. We have the runs to *approximate* that look without training SpanBERT from scratch.

**Compute we should not chase:** 14-day TPU SpanBERT-from-scratch. That is a methods contribution, not required for a Chinese dataset paper, and would duplicate Access/JobBERT narrative poorly.

## Minimum appendix pack to match the *kind* of rigor (no new architecture family)

Do these from **existing preds** first; only then extra GPU.

1. **P/R table** (SkillSpan Table 6 analogue) for Gold v2 and/or P2: JobBERT 1M/3M 3-seed, RoBERTa 3-seed, ChatGPT dump. Mean ± std where seeds exist. Caption must name gold and scorer `cnss-lskt-1.2.0`.
2. **Copy RoBERTa-wwm v3 3-seed mean into the Gold v2 encoder table** (seeds already used on P2: 0.2875 P2 exact mean; Gold v2 cells still `—` in confirmed-results).
3. **Source/domain × model F1 ± std** (Table 5 analogue): 3 domains × 3-seed encoders. We already have per-domain **point** F1; add seed std.
4. **Span-length F1 buckets** (Figure 6 analogue) on JobBERT 1M + ChatGPT dump. Analysis only.
5. **ASO  heatmap** on 3-seed encoder scores (Figure 7 analogue). `deep-significance`; α=0.05. Optional Bonferroni. Cheap.
6. **Optional GPU:** 5-seed on **JobBERT 1M goldstyle only** (their main baseline seed count). Do **not** 5-seed every ablation. Do **not** start SpanBERT-from-scratch. Do **not** STL/MTL 4×2 grid unless we want a methods appendix (LSKT joint CRF already is the MTL analogue).

## Done 2026-08-26 (appendix pack from existing preds)

Script: `scripts/build_skillspan_style_appendix.py`. Numbers in `notes/confirmed-results.md`.  
JobBERT 1M goldstyle extra seeds **7 and 13** launched on GPU 0; 5-seed mean **not** yet a paper number.

Do **not** start SpanBERT-from-scratch. Do **not** STL/MTL 4×2 grid.

## Still not for paper

- Qwen LoRA: no test F1 (died ~step 980).  
- Mixing P2 0.4331 with ChatGPT Gold v2 0.6365.  
- Concept Accuracy / Time-OOD.
