# Paper-to-file index

This index follows the September 18 manuscript. Topic names and stable LaTeX labels identify the results even when pagination changes. The manuscript source is maintained on Overleaf.

| Paper item | Topic | Supporting material |
|---|---|---|
| Tables 1–2 | Related datasets; annotation layers | [Dataset access](../DATA_AVAILABILITY.md), [resource names](../PAPER_NAMES.md) |
| Table 3; Appendix B, Tables 11–12 | Coding and review agreement | [Agreement guide](agreement/README.md) |
| Table 4; Eqs. 1–3 | Training settings and scoring | [Evaluation guide](EVALUATION_ENTRY.md), [selection records](supplementary_tables/table_19.md) |
| Table 5 | Shared-guideline inference | [Configuration results](current_results/inference.csv) |
| Table 6 | Matched Qwen; JobBERT supervision/selection | [Current results](current_results/README.md) |
| Table 7; Table 14 | Expanded pools and subsets | [Expanded-study guide](expanded_silver/README.md) |
| Tables 8–10 | Annotation rules and examples | [Handbook](../notes/handbooks/handbook_B_sop_v4.md) |
| Table 13 | Qwen per-seed results | [Per-seed CSV](current_results/qwen_runs.csv) |
| Figures 1–2 | Workflow and annotation paths | [Figure assets](../figures/round2/README.md) |
| Figure 3 | Annotation length and type distributions | [Figure and reproduction files](benchmark_profile/README.md): exact length-frequency counts, type counts, source hashes, and plotting script |
| Figure 4 | Boundary and type examples | [Figure assets](../figures/round2/README.md) |
| Figure 5 | Qwen prediction diagnostics | [Diagnostic counts](qwen_diagnostics/README.md) |
| Appendix D | Versions, access, and reproduction | [Reproduction guide](../REPRODUCIBILITY.md) |

The [agreement guide](agreement/README.md) reports which recent human-export summaries are available locally versus publicly. The expanded-study guide links the published adapters and frozen predictions and identifies the remaining access limits for the complete final training partitions.

<details>
<summary>Earlier table numbers and their retained supplementary locations</summary>

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


</details>
