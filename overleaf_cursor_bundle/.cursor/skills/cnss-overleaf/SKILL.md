---
name: cnss-overleaf
description: >-
  Edit the Chinese-SkillSpan benchmark Overleaf paper on the local Git clone.
  Use when the user asks to sync Chinese-SkillSpan tables, figures, captions,
  or claims with confirmed results, or when this workspace is the Chinese
  SkillSpan Overleaf repo. Do not use for the IEEE Access / SRICL paper.
---

# Chinese-SkillSpan Overleaf editor

## Start

1. Read [HANDOVER_OVERLEAF.md](../../../HANDOVER_OVERLEAF.md) in full before editing tex.
2. Confirm this is the Chinese-SkillSpan Overleaf clone, not `access_paper` / SRICL.
3. `git pull --ff-only origin main` (or the branch the user names).
4. Use [confirmed-results.md](confirmed-results.md) as the compact checklist; if it disagrees with the handover, stop and report.
5. Keep [not-for-paper.md](not-for-paper.md) out of the PDF.
6. Span conventions: [handbooks/](../../../handbooks/) — Handbook A (Gold v2) vs Handbook B (SOP v4). Do not merge. Consult `CODEX_PROMPT_HANDBOOK.md` before rewriting Methods.

## P0

Diff abstract, intro, data section, experiments, conclusion, tables, and captions against confirmed-results.md. List mismatches. Patch only confirmed cells. If a third value appears, stop.

## After edits

Show full `git diff` + conflict table (file, old, confirmed, action). No commit/push until the user says so.

## Server vs this window

Missing dumps, rescoring, or a new PDF extract: send back to the server folder `Chinese_skill_benchmark_Paper/`.
