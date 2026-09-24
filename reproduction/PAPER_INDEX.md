# Paper-to-file index — evidence revision, 25 September 2026

Current main file: `0main.tex`. Table numbers below refer to the compiled evidence revision; stable labels identify the topic across versions. The model repositories named `table11` refer to the older number of the current Chinese encoder Table 9.

| Current item | Page | Topic / evidence | Stable label |
|---|---:|---|---|
| Table 1 | 4 | [Related resources](../DATA_AVAILABILITY.md) | `tab:related-span` |
| Table 2 | 7 | [Data layers](../DATA_AVAILABILITY.md) | `tab:annotation-lineage` |
| Table 3 | 11 | [Coding and review designs](agreement/README.md) | `tab:quality-main` |
| Table 5 | 15 | [Shared-guideline inference](current_results/inference.csv) | `tab:gold150-shared-r7` |
| Table 6 | 15 | [Paired uncertainty](../scorer/score_lskt.py) | `tab:core-paired` |
| Table 7 | 16 | [Qwen and historical JobBERT comparisons](current_results/README.md) | `tab:gold150-main` |
| Table 8 | 17 | [External common protocol](https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/tree/46d1166f8e11dd52d473f645536074bb8dd0a53c/results_snapshots/external_benchmarks_20260922) | `tab:external-common` |
| Table 9 | 17 | [Chinese-supervised encoders](evidence_review_20260925/README.md) | `tab:external-chinese` |
| Table 13 | 25 | [Additional human review](evidence_review_20260925/annotation_layers/README.md) | `tab:qa150-pairs` |
| Table 15 | 30 | [Exploratory expanded supervision](expanded_silver/README.md) | `tab:expanded-silver-main` |
| Table 16 | 32 | [Component access](../DATA_AVAILABILITY.md) | `tab:component-access` |
| Table 17 | 33 | [Source and sampling records](../docs/data_sources.md) | `tab:source-stages` |
| Table 18 | 34 | [External paired intervals](process_archive_20260924/README.md) | `tab:external-common-ci` |
| Table 19 | 35 | [SkillSpan reruns](process_archive_20260924/README.md) | `tab:external-native` |
| Table 20 | 35 | [German ICT reruns](process_archive_20260924/README.md) | `tab:external-gnehm` |
| Table 21 | 36 | [Kompetencer classification](https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/tree/b84f218b7142c97ab03a60499a9b30e7ec332cab/results_snapshots/a_native_20260924) | `tab:external-kompetencer-classification` |
| Table 22 | 36 | [NNOSE](https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/tree/b84f218b7142c97ab03a60499a9b30e7ec332cab/results_snapshots/a_native_20260924) | `tab:external-nnose` |

Tables 10–12 describe the label definitions and boundary/scope rules in Appendix A; they are teaching rules, not a retrospective rewrite of historical labels. Table 4 records original JobBERT/Qwen settings; Table 14 identifies inference configurations. Figures 1–5 retain their workflow, annotation, profile, examples, and Qwen-diagnostic roles.

The [evidence index](evidence_review_20260925/README.md) records executed checks and remaining annotation provenance. The [process archive](process_archive_20260924/README.md) retains moved tables without suppressing negative results.

<details>
<summary>Historical September 18 numbering (superseded)</summary>

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





## Exploratory and process records moved out of the manuscript (2026-09-24)



The [supporting process archive](process_archive_20260924/README.md) preserves former Tables 13, 20 and 25 (numbering from the 43-page draft), including all Qwen subset rows, the execution-version ledger, alternate pooled SkillSpan scores and detailed audit histories. Primary results, scientific limitations and data-access status remain in the paper. The archive index explains scoring and comparability limits.



## Further table and procedure consolidation (2026-09-24)

The [secondary review archive](process_archive_20260924/secondary_review/README.md) preserves former Tables 13, 16 and 17 from the 41-page draft, complete NNOSE settings, and condensed procedural records. Its [25-table audit](process_archive_20260924/secondary_review/TABLE_AUDIT.md) explains every keep/move decision. Main outcomes, statistical definitions and scientific limitations remain in the manuscript.

</details>
