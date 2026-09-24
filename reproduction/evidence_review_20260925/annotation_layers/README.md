# Historical annotation layers, not a new Gold release

These pseudonymized copies preserve the sentence text and annotation offsets in the recovered exports. Annotator A/B replaces account names. They are supplied to permit agreement calculations, not to change the frozen reference, training labels, or annotation-design claims.

- `blind50_A/B.jsonl`: two historical independent raw-text coding exports, 50 sentences each. Live-export provenance does not establish byte identity with the original pre-adjudication freeze. All 50 IDs belong to Gold150; they are not an additional 50 test sentences.
- `dual15.jsonl`: two human layers in 15 auditor-subset sentences. The author corrected the design description on 25 September: both annotators had access to machine coding suggestions. This is machine-assisted double review, not independent blind coding. Perfect agreement is retained as an assisted-review result; it cannot establish blind reliability of the final handbook.
- `QA150.jsonl`: 150 additional dual-reviewer sentences. Existing protocol records describe machine-assisted review; independent submission queues alone do not establish blind raw-text annotation. Do not turn this review sample into Gold without a separate adjudication and isolation protocol.

The identifier comparison currently recovers 500 distinct source texts across Gold150, reviewed100, QA100 and QA150. The blind50 is nested in Gold150 and dual15 in QA100. The author's additional recollection of two later 150-sentence rounds remains to be matched to exports; it is not dismissed or counted twice.

No annotation is modified or newly adjudicated in this release. Kappa calculations must document character projection; the QA150 export includes ambiguous character positions, so use the manuscript's 5,990-position convention rather than silently resolving overlaps.

Author-controlled annotations permit academic research and peer review with attribution; third-party text retains the component-specific source terms described in DATA_AVAILABILITY.md. These review layers are not a blanket CC-BY text release.
