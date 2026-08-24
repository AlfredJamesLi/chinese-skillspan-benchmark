# Doubao test 52 merge (sandbox)

Gold v2 untouched. Codex test silver untouched. Doubao written to a **new** file.

- n=2601 unique=2601 expected=2601
- order vs batches_52: True
- missing: 0 extra: 0 dups: 0
- align-error sentences: 928 (bad spans dropped)
- proposed spans 6369, kept 4074, dropped 2295 (almost all `not_in_sentence` paraphrase, 19 overlap)
- empty: 1374; spans>8 kept: 102
- types: {'S': 1887, 'K': 1515, 'T': 652, 'L': 20}
- vs Codex exact span+type match: 1101/2601 (disagree 1500)
- empty sentences: Codex 1187, Doubao 1374, both 1007

Output: `/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/data/test_lskt_v4_doubao_g2ids.jsonl`
Do not copy into confirmed-results.md. Do not train on this test file.
