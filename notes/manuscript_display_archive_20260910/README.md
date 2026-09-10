# R13 display archive before R14 slimming

Source: Overleaf commit `2fbaaf9`; 40 tables and 11 figures. This is an archival manuscript snapshot, not a new result release or endorsement of all historical diagnostics.

All scientific values and protocol caveats are preserved. Coder account names are replaced by stable role codes; private comments are omitted. Original identifiable before-images remain private. No author bylines are included in this display-only package.

R14 removes only the approved first group from the active PDF: 23 tables and 7 figures. The second group and main displays remain. Historical handbook panels remain bound to their historical IAA protocol, not V4.2.14.

This backup contains only individual figure/table TeX snippets in `displays/`, their referenced rendered assets, and existing numeric CSV tables. It excludes full manuscript prose, author metadata, private revision logs, raw annotation files, and model weights. `DISPLAY_INVENTORY.json` maps old numbers to stable labels and original source paths. `FILE_HASHES.json` verifies every file. Snippets retain original cross-reference labels and require the manuscript preamble; they are not standalone documents.

## Routing reasons

- Old handbook panels and the workload/coding-stage tables: duplicate current rules or main lineage/quality evidence.
- Earlier human200/IAA100 and Gold-v2 detail: different cohorts and protocols; retain for provenance rather than mix with Gold150.
- Old domain, length, seed-win, and P/R diagnostics: redundant detail under historical references, not current Gold150 error analysis.
- Intermediate SOP/CWS and source-stratified 4,222-record diagnostics: separate exploratory protocols, not the main research questions.
- Retained evidence includes IAA50 details, protocol inventory, factory-encoder counterevidence, cross-protocol bridge, historical benchmark summary, student/HEM tables, and negative prompt/cleaning results.

## Old-number routing

| Display | Page | Stable label | R14 decision |
|---|---:|---|---|
| figure 1 | 3 | `fig:macro-micro` | retain_R14 |
| table 1 | 4 | `tab:related-span` | retain_R14 |
| figure 2 | 6 | `fig:coding-detail` | retain_R14 |
| figure 3 | 6 | `fig:sktl-sample` | retain_R14 |
| table 2 | 7 | `tab:annotation-lineage` | retain_R14 |
| table 3 | 8 | `tab:quality-main` | retain_R14 |
| table 4 | 10 | `tab:appendix-f-sop` | retain_R14 |
| table 5 | 11 | `tab:gold150-main` | retain_R14 |
| table 6 | 14 | `tab:handbook-versions` | retain_R14 |
| table 7 | 14 | `tab:annotation-general-a` | archive_only_R14 |
| table 8 | 15 | `tab:annotation-general-b` | archive_only_R14 |
| table 9 | 15 | `tab:annotation-types` | archive_only_R14 |
| table 10 | 16 | `tab:annotation-conflicts` | archive_only_R14 |
| table 11 | 16 | `tab:annotation-schema` | archive_only_R14 |
| table 12 | 17 | `tab:annotation-qc-output` | archive_only_R14 |
| table 13 | 18 | `tab:annotation-examples` | archive_only_R14 |
| table 14 | 18 | `tab:workload-skillspan` | archive_only_R14 |
| table 15 | 19 | `tab:repro-inventory` | retain_R14 |
| table 16 | 20 | `tab:human-page1-systems` | archive_only_R14 |
| table 17 | 20 | `tab:human-page1-agreement` | archive_only_R14 |
| table 18 | 21 | `tab:iaa50` | retain_R14 |
| table 19 | 22 | `tab:iaa` | archive_only_R14 |
| table 20 | 22 | `tab:gold-v2` | archive_only_R14 |
| table 21 | 22 | `tab:paper-sf1` | archive_only_R14 |
| table 22 | 23 | `tab:pr-gold-v2` | archive_only_R14 |
| table 23 | 23 | `tab:domain-three-seed` | archive_only_R14 |
| figure 4 | 23 | `fig:domain-heatmap` | archive_only_R14 |
| table 24 | 23 | `tab:span-length` | archive_only_R14 |
| figure 5 | 24 | `fig:pred-len` | archive_only_R14 |
| figure 6 | 24 | `fig:span-length-profile` | retain_R14 |
| table 25 | 24 | `tab:seed-win` | archive_only_R14 |
| figure 7 | 25 | `fig:seed-winrate` | archive_only_R14 |
| table 26 | 25 | `tab:pr-p2` | archive_only_R14 |
| table 27 | 26 | `tab:vanilla-wwm-v4` | retain_R14 |
| table 28 | 26 | `tab:sop-diagnostic` | archive_only_R14 |
| table 29 | 27 | `tab:legacy-frozen-outputs` | archive_only_R14 |
| table 30 | 27 | `tab:cross-protocol` | retain_R14 |
| table 31 | 28 | `tab:repartition-joint` | archive_only_R14 |
| table 32 | 28 | `tab:repartition-stl` | archive_only_R14 |
| table 33 | 29 | `tab:dataset-stats` | archive_only_R14 |
| figure 8 | 29 | `fig:violin-spans` | archive_only_R14 |
| table 34 | 30 | `tab:standardized-benchmark` | retain_R14 |
| figure 9 | 30 | `fig:standardized-performance` | archive_only_R14 |
| figure 10 | 31 | `fig:standardized-label-domain` | archive_only_R14 |
| figure 11 | 32 | `fig:standardized-span-length` | archive_only_R14 |
| table 35 | 33 | `tab:qwen-supplement` | retain_R14 |
| table 36 | 33 | `tab:hem-supplement` | retain_R14 |
| table 37 | 35 | `tab:appendix-e-p1` | retain_R14 |
| table 38 | 35 | `tab:appendix-g-peel` | retain_R14 |
| table 39 | 37 | `tab:gold150-shared-r7` | retain_R14 |
| table 40 | 37 | `tab:gold150-shared-subsets-r7` | retain_R14 |

## Interpretation safeguards

Historical IAA tables use their stated manual and comparison layers; available exports reproduce the reported span summary but do not prove original frozen-file byte identity. Gold-v2, hybrid 2601, Gold150, and the 4,222-record silver-draft repartition are separate references. No score is recalculated here. Pending factory/shared-prompt rows remain pending, and negative prompt/retrieval/cleaning findings remain archived and in the retained second group. Do not treat duplicate tables or seed-win matrices as independent evidence or significance tests.
