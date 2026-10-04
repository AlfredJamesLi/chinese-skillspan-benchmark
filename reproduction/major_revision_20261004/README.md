# Chinese-SkillSpan: revised analyses and documentation

This package accompanies the 4 October 2026 manuscript revision. It preserves the frozen labels, split membership, predictions and model point scores. New analyses address data accounting, source-document grouping and uncertainty; they do not create a new human test set.

- [Current manuscript](../manuscript_revision_20261002/README.md)
- [Data counts and source-document checks](data_audit/README.md)
- [Recheck of earlier prevention measures](data_audit/RECHECK_zh.md)
- [Paired group bootstrap and K/S/T macro-F1](metrics_audit/README.md)
- [External-task experiments](external_experiments/README.md)
- [Aggregate contact-pattern screening](rules_sources_audit/pii_screen.json)

The original corpus already has disjoint source-document partitions. Later B2 checks exclude Gold150 sentence IDs and complete normalized texts from training and development. Additional grouping finds different sentences with shared source-document identifiers; it does not show that 143 reference texts were included in training or quantify score inflation. The frozen model-input hashes match the audited files.

The latest independent agreement study remains [the 3 October individual exports](../agreement/finalguide_abc_20261003/README.md): mean typed exact F1 0.818, boundary F1 0.850 and character alpha 0.907. Individual self-review and rule consultation were allowed. Historical annotation versions remain unchanged.

The K category includes project-specific qualification and industry-background proxies. K/S/T macro-F1 removes the influence of the sparsely supported L category from that summary; it is not a knowledge-only reannotation. Pattern screening identifies candidates for human privacy review and does not certify anonymization. Complete expanded-pool inputs remain unavailable for public retraining.
