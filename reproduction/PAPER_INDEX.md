# Current paper and companion-material index

Aligned to the 22-page manuscript prepared on 2026-09-13. PDF SHA-256: `e047f07b38e60da634d7ccd7cb9262647d2ca42b61f8e3e8dadc4c14fbf25c74`. The source manuscript remains on Overleaf; no draft paper PDF is uploaded by this synchronization. PDF page references below identify this exact local revision, not an older screenshot. Stable topic names and LaTeX labels should be preferred if pagination changes.

## Current paper

| Paper location | Topic | Repository entry |
|---|---|---|
| Abstract, p.1 | Background / Methods / Results / Conclusion; current resource and matched Qwen result | [Current results](current_results/README.md) |
| Tables 1–2, pp.4/6 | Related resources; data layers | [Round 2 change record](ROUND2_CHANGES.md) |
| Table 3, p.9; Eq.(4)/Table 10, pp.16/17 | Independent coding agreement and distinct review designs | [Agreement](agreement/README.md) |
| Eqs.(1)–(3), p.10; Table 4, p.11 | IoU, micro metrics, sample SD; training settings | [Evaluation entry](EVALUATION_ENTRY.md), [selection records](supplementary_tables/table_19.md) |
| Table 5, p.11 | Six shared-guideline inference configurations | [Display CSV](current_results/inference.csv) |
| Table 6, p.12 | Qwen adaptation and JobBERT supervision/selection panels | [Current results](current_results/README.md) |
| Tables 7–9, pp.14–16 | Current handbook rules and examples | [Chinese handbook](../notes/handbooks/handbook_B_sop_v4.md), [version applicability](evaluation/version_applicability.json) |
| Table 11, p.18 | Current Qwen per-seed results | [Per-seed CSV](current_results/qwen_runs.csv) |
| Figure 5, p.19 | Frozen Qwen diagnostics | [Full diagnostic data](qwen_diagnostics/README.md) |
| Appendix D, p.19 | Reproduction and versioned materials | [Evaluation entry](EVALUATION_ENTRY.md), [paper names](../PAPER_NAMES.md) |

## Transferred tables: original numbers belong to different snapshots

| Original location / stable topic | Current destination |
|---|---|
| Output-status table: screenshot Table 16; Table 17 immediately before removal; label `tab:shared-output-quality-r15` | [Nine-row outcome table](output_outcomes/README.md), CSV and original TeX |
| Table 10 before supplementary-table pruning: execution versions | [Version table](supplementary_tables/table_10.md) |
| Table 12 before pruning: historical JobBERT pools | [Pool comparison](supplementary_tables/table_12.md) |
| Table 13 before pruning: earlier Qwen JSON-offset | [Historical Qwen](supplementary_tables/table_13.md) |
| Table 14 before pruning: source composition | [Composition table](supplementary_tables/table_14.md) |
| Table 15 before pruning: instructions/examples and cleaning, both blocks | [Sensitivity tables](supplementary_tables/table_15.md) |
| Table 16 before pruning: cohort breakdown | [Cohort table](supplementary_tables/table_16.md) |
| Table 19 before pruning: seed/epoch/development selection | [Selection records](supplementary_tables/table_19.md) |
| Table 12 after pruning: Qwen diagnostics, now Figure 5 | [Archived table and full counts](qwen_diagnostics/README.md) |
| Stage 2 earlier historical Tables 10–12 | [Original results and context](historical_results/README.md) |

The seven pruned tables retain Markdown, CSV block(s) and exact TeX. All favorable and unfavorable results remain attached to their original conditions. No table number alone identifies an experiment across revisions.

## Detailed prose and names

[Experimental notes](experimental_notes/README.md) collect the reproduction reminders. [Detailed passages](experimental_notes/DETAILED_PASSAGES.md) and [81-entry relocation map](experimental_notes/RELOCATION_MAP.json) preserve the old and shortened wording. Complete manuscript source backups remain local. The public passage and table archives provide the transferred context. [28 name mappings](../PAPER_NAMES.md) connect reader-facing names with original model, file, sample and example identifiers.
