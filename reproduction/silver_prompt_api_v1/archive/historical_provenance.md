# Actual prompts versus subsequent revisions

The initial 100 reviewed Silver-plus records used silver_plus_v4210_rev1 (header base B.sop_v4.2.10; execution/adjudication records identify applied B.sop_v4.2.11). They were not regenerated with the later prompt.

The subsequent 2,351 records (730 conflict-source and 1,621 non-conflict-source) used the same silver_plus_v4212_rev2 frozen prompt, based on B.sop_v4.2.12. SHA256: a4505a51ebfe43e56712444d7b8d4671307ad650f67a37de6764cbde5b85c01e. All 226 post-pilot batch log rows carry this hash.

The frozen file retains draft/approval-gate wording. The first-pilot log records user approval and explicitly retains the unchanged bytes for provenance. Do not edit the historical file to remove this wording.

Execution took place incrementally in the current conversation with semantic span selection and deterministic offset serialization, not independent fresh API sessions for every batch. Model metadata must distinguish recorded gpt-6-astra identity and its evidence source from an API-verified runtime ID; some runtime IDs are unknown.

The GitHub main file notes/handbooks/PROMPT_silver_plus_v4212.txt checked at bc075cf608b766006b6d43b5b550df9c914c0718 is rev1, not this frozen rev2. Public-release reconciliation is pending.

The new Qwen prompt design is a separate proposal. Its presence in this package does not establish which prompt the currently running experiment actually used. Obtain the run's frozen prompt and hash.
