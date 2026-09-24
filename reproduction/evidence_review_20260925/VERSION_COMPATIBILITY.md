# Rule-version compatibility: completed checks and remaining work

The primary scores retain their historical targets. All 150 Gold150 rows declare B.sop_v4.2.10. The executed B2 bulk prompt follows v4.2.12; B2 rows lack individual handbook fields, and the initial reviewed layer has its own history. The displayed handbook is v4.2.14. A shared version string is not a semantic compatibility proof.

Verified named difference: B2 training record `1838-s0008` contains S spans [9,25) and [26,37). The later R23 ruling splits the first span into [9,16) and [17,19), retaining [26,37). The record is absent from Gold150 and B2 development. Original labels and all historic results are unchanged. This is one confirmed historical-rule difference, not an estimate of total incompatibility.

`VERSION_SCREEN.json` and `rule_impact_candidates.csv` screen all 2,469 Gold150/B2 train/dev records for experience, coordination, theory/tool, transversal, and scope/empty expressions. Candidate families overlap. Keyword matches are review candidates, not labeling errors; no corpus-wide compatibility success or affected percentage is claimed.

To complete the semantic audit, an adjudicator should compare the applicable historical and final rules for each candidate, retaining original spans, proposed alternatives, rule IDs, rationale, and a separate adjudication status. Preserve no-change decisions as well. Do not overwrite old labels or substitute revised scores into historical tables. First recover existing annotations and decisions before commissioning new coding.
