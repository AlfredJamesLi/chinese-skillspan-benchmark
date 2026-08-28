# human980_doccano

Frozen **980** must-human queue from `codex_pack/conflict_v1/human_must_review.csv`.

- Text = Gold v2 full `sentence` (not truncated SimHuman / CSV text).  
- Prelabel = SimHuman rule_v4 BIO, projected only when the sentence is the same (or a truncatable prefix).  
- 24 IDs had a different SimHuman sentence than Gold v2; those rows have empty prelabel.  
- Protocol: one-pass correction. Split / hybrid rewrite **after** labeling.  
- Does not overwrite `gold_canonical_v2.jsonl`, V4 hybrid, or `human980_pack/`.

Rebuild: `python3 scripts/build_human980_doccano.py` from `Chinese_skill_benchmark_Paper/`.
