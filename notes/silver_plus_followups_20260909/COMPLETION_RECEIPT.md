# Overleaf E–G update receipt — 2026-09-09

- Project: https://www.overleaf.com/project/68fe17a53e53a7f800e4f2b4
- Base: ea805dce60f8c67aa6f19948d29c8fc18bb24c15
- Pushed and independently checked remote main: 3448f593c888ef16272ba648bc5ff7dbed2bdcc6.
- Scope: five TeX files; appendix E/F/G, methods, results note, limitations, conclusion and release-availability clarification.
- Existing table environments and entire Abstract preserved exactly. Current online A-table/abstract differ from the report's paraphrase; no silent reconciliation was made.
- Local XeLaTeX compilation passed: 41 pages. New tables visually inspected on pages 36–37; no clipped table content. Online compilation was not separately observed.
- Evidence: user-provided frozen Cursor report. Server result JSON files were not directly inspected or independently rescored.
- 36 numeric-bearing locations mapped in NUMERIC_PROVENANCE.md and CSV.
- GitHub preparation only; Cursor remains responsible for pushing notes with original result files and reproduction evidence. No Zenodo release performed.

## Decisions retained for subsequent work

- P0 remains the formal Qwen result; P1, frozen SOP rescoring and tail-cleaning reruns stay in the appendix.
- Seed SD overlap is not a significance test. Aggregate exact/relaxed scores alone do not establish the error mechanism.
- Cleaning reruns change membership and are not a pure watermark ablation.
- No new training, API calls, label edits, or changes to the Gold150 hash.
- This update does not close previously identified annotation-reporting and handbook-synchronization gaps; consult outputs/manuscript_data_gap_audit_20260909/DATA_UPDATE_GAPS.md.
