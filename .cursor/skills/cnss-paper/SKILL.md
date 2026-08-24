---
name: cnss-paper
description: >-
  Prepare the Chinese-SkillSpan benchmark paper on the GPU server: extract the
  uploaded PDF, fill confirmed-results, draft tex/tables/figs, and keep the
  Overleaf bundle in sync. Use when the user mentions Chinese-SkillSpan paper,
  Chinese_skill_benchmark_Paper, the benchmark PDF, or Overleaf help in this
  window. Do not use for IEEE Access / SRICL.
---

# Chinese-SkillSpan paper (server window)

## Start

1. Read [HANDOFF.md](../../../HANDOFF.md).
2. List files in `pdf/`. If a new PDF is there, extract title, venue, data sizes, main table, and claims into [confirmed-results.md](../../../notes/confirmed-results.md). Copy the compact table into `overleaf_cursor_bundle/.cursor/skills/cnss-overleaf/confirmed-results.md`.
3. Keep [not-for-paper.md](../../../notes/not-for-paper.md) out of drafts.
4. Code locations: [CODE_MAP.md](../../../notes/CODE_MAP.md) (read-only unless the user asks to change experiments).

## Writing

- Prefer files under `tex/`, `tables/`, `figs/`, `notes/`.
- Unconfirmed numbers stay in notes as **待验证**, not in the PDF abstract.

## After PDF upload

Tell the user: filename, page count if available, which tables were extracted, and any conflict with the repo.
