# Methods / ablation draft (vanilla WWM v4)

**Status: 待验证.** Do not change the abstract (JobBERT 3M exact **0.4331**). Do not write 0.4341 as beating JobBERT. Gold v2 untouched.

JSON on this machine:

- `output/vanilla_wwm_base_v4_silver_seed42/hybrid_eval.json`
- `output/vanilla_wwm_large_v4_silver_seed42/hybrid_eval.json`
- `output/vanilla_wwm_v4/pr_alignment_seed42.json`
- `tables/vanilla_wwm_v4_seed42.csv`
- `tex/skillspan_style_vanilla_wwm_v4.tex`

## English (PeerJ, one paragraph)

To test whether encoder capacity or continued job-domain MLM explains V4 exact-span F1, we fine-tuned factory `hfl/chinese-roberta-wwm-ext` (base; no DAPT) and `chinese-roberta-wwm-ext-large` with the same CRF recipe as JobBERT-zh (seed 42; 6 epochs, patience 2, batch 16, max length 256, $\mathrm{lr}{=}2{\times}10^{-5}$). Predictions were jieba-snapped and scored with `cnss-lskt-1.2.0` on the V4 hybrid gold ($n{=}2601$; alignment OK; no missing IDs). Factory base reached typed exact 0.4341 / relaxed 0.5888, matching the confirmed JobBERT-zh 3M row (0.4331 / 0.5873) in magnitude and precision--recall shape. The 24-layer factory large model did not improve exact F1 (0.4289) or long-span exact F1 (0.4157 vs 0.4135). We therefore do not attribute the V4 encoder score to model size or to 1M/3M job DAPT; the contrast with goldstyle-trained RoBERTa-wwm (~0.29 on the same test gold) is the training-label protocol. The abstract continues to report the confirmed JobBERT 3M figure 0.4331.

## 中文备忘

出厂 base 与 JobBERT 3M 同量级；large 不抬 exact、也不抬长跨度；不要再预训练。摘要仍用 0.4331。
