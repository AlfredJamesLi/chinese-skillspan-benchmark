# Codex / Overleaf — vanilla WWM v4 ablation (consult first)

**Overleaf:** https://www.overleaf.com/project/68fe17a53e53a7f800e4f2b4  
**This chat is consult-only unless the user later says to insert the appendix table.**  
Do **not** change abstract F1. Do **not** replace JobBERT 3M **0.4331**. Do **not** touch IEEE Access / SRICL.

These files ship in `vanilla_wwm_v4_codex_pack_20260830.tgz`. Unpack into the Overleaf repo root (next to `main.tex`) **before** pasting the prompt.

| Pack path | Overleaf path |
|---|---|
| `CODEX_PROMPT_VANILLA_WWM.md` | this file |
| `tex/skillspan_style_vanilla_wwm_v4.tex` | `tex/skillspan_style_vanilla_wwm_v4.tex` |
| `notes/vanilla_wwm_v4_methods.md` | `notes/vanilla_wwm_v4_methods.md` |
| `tables/vanilla_wwm_v4_seed42.csv` | `tables/vanilla_wwm_v4_seed42.csv` |

If `ls notes/vanilla_wwm_v4_methods.md tex/skillspan_style_vanilla_wwm_v4.tex` fails, **stop** and ask the user to unpack the pack. Do not invent F1.

---

## PROMPT (copy from here)

You are advising on the **Chinese-SkillSpan / Chinese Skill Benchmark** paper (**PeerJ Computer Science**). This is **not** IEEE Access / SRICL.

### Start

`git pull --ff-only`. Read `.cursor/skills/cnss-overleaf/confirmed-results.md` and `not-for-paper.md`. **Do not edit tex in this consult pass.** Return: (1) where a factory-encoder ablation should sit (Methods vs appendix); (2) a 4-sentence patch plan; (3) the exact sentences that must remain unchanged.

### Frozen

- Abstract / main SOTA stay JobBERT 3M v4 exact **0.4331** and ChatGPT dump+jieba exact **0.2854** / relaxed **0.6249**.
- Do **not** write factory base **0.4341** as beating JobBERT, and do **not** put 0.4341 and Gold v2 ChatGPT **0.6365** in one SOTA sentence.
- Vanilla rows are **single seed 42**, 待验证, alignment OK, $n{=}2601$, scorer `cnss-lskt-1.2.0`.
- Factory large 0.4289 did **not** help; no 3-seed / no large DAPT.

### Draft paragraph (may quote, do not invent other F1)

See `notes/vanilla_wwm_v4_methods.md` (English paragraph). Table: `tex/skillspan_style_vanilla_wwm_v4.tex`.

### Return

Methods placement + whether the table is appendix-only + a bullet list of files you would `\input` **after** the user confirms. No commit, no push, no abstract edit.
