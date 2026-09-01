# 636-record audit (processed test 3237 − Gold v2 / V4 hybrid 2601)

Processed test.json: 3237
test_lskt_v4_silver.jsonl: 3237
gold_canonical_v2.jsonl unique IDs: 2601
V4 hybrid 2601: 2601
IDs in test silver not in Gold v2: 636
IDs in that set also in processed test: 636
IDs in that set also in V4 hybrid: 0

Arithmetic: 17460 train + 2143 dev + 2601 eval = 22204; claimed 22840; 22840−22204=636.
22840 = 17460+2143+3237 (full processed corpus). 3237−2601=636.
These 636 are processed-test sentences excluded from unique-first Gold v2 / V4 hybrid.
They still have LSKT v4 silver (rule_v4) labels. They are **not** human Gold.
Do not auto-generate Gold to fill them.

By source: AI=16, Cloud=16, Public=604
Empty (0 spans): 563
Eligible for new stratified pool: 636

980 SimHuman: overlay rule_v4, not dual-blind IAA. File `test_lskt_v4_simhuman980_cws.jsonl` n=980. eval_v3 pilot300 n=300 is a separate Gold-era pilot, not V4 IAA.
