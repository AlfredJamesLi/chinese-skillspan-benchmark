# Vanilla large vs vanilla base (V4 CRF)

Date: 2026-08-30. Seed 42 on **server B**. P/R read-back 待验证. **Not for abstract / confirmed-results until the user copies them in.**

Protocol: V4 hybrid 2601 + jieba + `cnss-lskt-1.2.0`. `alignment_ok=true`, n_gold=2601, n_missing=0, n_filled_empty=0. Gold v2 untouched. n_extra=636 = test.json 3237−2601（不计分）。

## V4 hybrid typed (seed 42)

| System | P | R | exact F1 | relaxed | pred / gold / tp |
|---|---:|---:|---:|---:|---|
| vanilla base（待验证） | 0.4878 | 0.3911 | **0.4341** | 0.5888 | 3360 / 4191 / 1639 |
| vanilla large（待验证） | 0.4589 | 0.4025 | 0.4289 | 0.5766 | 3676 / 4191 / 1687 |
| JobBERT 3M v4（已确认） | 0.4730 | 0.3994 | **0.4331** | 0.5873 | 3539 / 4191 / 1674 |
| JobBERT 1M v4（已确认） | 0.4685 | 0.3925 | 0.4272 | 0.5952 | — |

B−A exact = **−0.0052**. STOP: no 3-seed, no large DAPT. Ignore script “discuss 1M DAPT”.

## Short / long micro exact（同一套 char≤5）

| System | short≤5 | long>5 |
|---|---:|---:|
| vanilla base | 0.4561 | 0.4135 |
| vanilla large | 0.4426 | 0.4157 |
| JobBERT 3M v4（已确认诊断） | 0.4501 | 0.4165 |

Large 对长跨度只 +0.002，短跨度更差。

## Other

- Gold v2 旁路 exact：base **0.1440**，large 0.1398（不是论文主行；附录编码器约 0.12）。
- 两臂都训满 6 epoch。best_dev（v4 silver）base 0.3682 @ep4，large 0.3696 @ep5。dev 0.37 ≠ test 0.43：dev 是银标，test 是 hybrid。
- 机 A **50782 已取消**。

## Applied on server A (2026-08-30)

Installed from `vanilla_wwm_v4_pr_alignment_seed42_for_download.tgz`. Official copies: `output/vanilla_wwm_{base,large}_v4_silver_seed42/hybrid_eval.json`, `output/vanilla_wwm_v4/pr_alignment_seed42.json`, `tables/vanilla_wwm_v4_seed42.csv`, `tex/skillspan_style_vanilla_wwm_v4.tex`, `notes/vanilla_wwm_v4_methods.md`. Overleaf consult: `overleaf_cursor_bundle/CODEX_PROMPT_VANILLA_WWM.md`. **Not** in `confirmed-results.md`.

## Claims allowed / forbidden (until confirmed)

**可写进笔记/消融讨论：** 出厂 base 与 JobBERT 1M/3M 同形状（P>R，F1~0.43）；加大模型不抬 exact、也不抬长跨度；V4 上 DAPT 几乎无加分。

**禁止：** 用 0.4341 换摘要 0.4331；写「vanilla 超过 JobBERT」；0.4341 与 Gold v2 0.6365 同一句 SOTA；为 large 再开 3-seed / DAPT。
