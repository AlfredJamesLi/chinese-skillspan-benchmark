Chinese-SkillSpan — Codex / Overleaf pack (vanilla WWM v4 ablation)
Unpack into the Overleaf Git root (same folder as main.tex).

  tar -xzf vanilla_wwm_v4_codex_pack_20260830.tgz

Then you should have:

  CODEX_PROMPT_VANILLA_WWM.md     <-- paste the PROMPT section into Codex
  notes/vanilla_wwm_v4_methods.md
  notes/vanilla_large_v4.md
  tex/skillspan_style_vanilla_wwm_v4.tex
  tables/vanilla_wwm_v4_seed42.csv
  output/vanilla_wwm_v4/pr_alignment_seed42.json

This chat is consult-only unless the user later asks to insert the table.
Do not change abstract F1 (JobBERT 3M exact 0.4331).
Do not write 0.4341 as beating JobBERT.
Do not put 0.4341 and Gold v2 ChatGPT 0.6365 in one SOTA sentence.
Not IEEE Access / SRICL.
