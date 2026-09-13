# Shared-guideline output outcomes

This companion reproduction material contains the full output-status breakdown removed from the manuscript at the author's request on 2026-09-13. It preserves the existing frozen-result counts; no inference or rescoring was performed. It is included in the Round 2 companion package; [the paper index](../PAPER_INDEX.md) identifies its previous manuscript location.

- `shared_guideline_output_outcomes.csv`: machine-readable counts; each row covers all 150 reference sentences.
- `archived_table.tex`: the former manuscript table, retained for traceability and excluded from compilation.

## Interpretation and counting rules

The six outcome categories are mutually exclusive. Valid nonempty means an accepted nonempty output without rejected candidates. Empty means a legal empty span list, not necessarily a correct negative. Partial means a response with both accepted and rejected candidates. All-spans-rejected means a nonempty candidate list with none accepted. Format failure means an invalid whole response. Missing means no response record.

Accepted spans from partial responses remain in scoring. Fully rejected and malformed responses count as empty predictions; the full 150-sentence denominator for coverage is retained. Every row sums to 150. These statuses describe output-contract adherence, not semantic correctness.

DeepSeek-V4-Pro is the same API model (`deepseek-v4-pro`) in both rows: thinking is disabled/enabled, and configured output caps are 2,048/8,192 tokens. These are configuration distinctions, not official model-name suffixes. Blank output-cap cells mean this extract does not specify the cap.

The Qwen no-adapter baseline has 69 partially rejected responses; LoRA seeds 42, 43 and 44 have 2, 4 and 1. DeepSeek-V4-Pro in thinking mode has 18 format failures. These counts do not isolate how much score change comes from output-format adherence versus span recovery. The recorded no-adapter Qwen parser diagnostics contain 168 rejected candidates: 167 occurrence-index errors and one overlap conflict. Candidate counts differ from sentence-level outcome counts.

## Provenance

Transferred without numerical changes from `tex/appendix_C_shared_R16.tex`, label `tab:shared-output-quality-r15` (Table 17 in the immediately preceding 29-page PDF; Table 16 in the author's earlier screenshot). Retain the frozen `rev2 patch1` prompt, occurrence parser v1.1 and scorer `cnss-lskt-1.2.0` identities. No frozen labels, manifests, predictions, parser, scorer, or run configurations are modified.

| Model / configuration | Valid nonempty | Empty | Partial | All rejected | Format failure | Missing |
|---|---:|---:|---:|---:|---:|---:|
| DeepSeek-V4-Pro / non-thinking | 142 | 6 | 2 | 0 | 0 | 0 |
| Claude Sonnet 4.5 / recorded configuration | 145 | 4 | 1 | 0 | 0 | 0 |
| DeepSeek-V4-Pro / thinking | 124 | 8 | 0 | 0 | 18 | 0 |
| Kimi k2.6 / recorded configuration | 142 | 6 | 2 | 0 | 0 | 0 |
| Qwen2.5-14B-Instruct / no project adapter | 69 | 11 | 69 | 1 | 0 | 0 |
| gpt-5.6-terra / recorded configuration | 141 | 7 | 2 | 0 | 0 | 0 |
| Qwen2.5-14B-Instruct / LoRA / seed 42 | 139 | 8 | 2 | 1 | 0 | 0 |
| Qwen2.5-14B-Instruct / LoRA / seed 43 | 136 | 9 | 4 | 1 | 0 | 0 |
| Qwen2.5-14B-Instruct / LoRA / seed 44 | 138 | 10 | 1 | 1 | 0 | 0 |
