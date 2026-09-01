# Pre-split leakage and quality (current source-disjoint split)

Pool sentences: 22840 (train 17460 + dev 2143 + test silver 3237)
Eligible: 22840
Unique posts: 2000
Near-dup groups after union: 1654
Duplicate sentence IDs: 0
Posts spanning multiple current splits: 0
Normalized-text hashes spanning multiple current splits: 59
Offset mismatches: 0
Substring failures: 0
Empty-sentence rate: 0.3900

## Human vs draft (not assumed from chat)
- SimHuman 980 file n=980; hybrid_source counts: {"sop_cws": 1621, "simhuman980_cws": 980}
- Gold v2 n=2601 (Doccano; not V4 IAA)
- eval_v3 pilot300 n=300 (Gold-era; not V4 dual-blind)
- 980 is **not** a completed dual-blind V4 human audit.

## Current source × split (sentences)
- AI: train=7148 dev=2143 test=1423
- Grad: train=10312 dev=0 test=0
- Cloud: train=0 dev=0 test=473
- Public: train=0 dev=0 test=1341
