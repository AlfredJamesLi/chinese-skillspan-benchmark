# Blind-500 uncertainty review, v1.0.0

These are post-submission repository-maintenance materials. They were not used to train, select, or evaluate models, calculate results, or support claims reported in manuscript 149505. The citable dataset associated with that manuscript remains Chinese-SkillSpan v0.1.3 on Zenodo; these materials do not change the archived dataset, submitted manuscript or reported results.

2026-10-29. **AI-assisted analytical working draft, pending author review.** This reviews Coder C's provisional single-coder annotation draft pending independent second annotation and adjudication. It is not a second annotation, an IAA study, or evidence that all authors accepted these interpretations. No original labels, types, offsets, confirmation fields, order, data files or existing results were changed.

## Evidence and inventory

All **46 PNG files** in the supplied uncertainty directory were visually read; there were no text, spreadsheet or other case files. Each screenshot represents one sentence-level case, possibly with several uncertain spans. No written question accompanied the screenshots: the doubts and recommendations here are analyst interpretations, not quotations from the coder. The selection is not a representative error-rate sample of 500 sentences.

Baseline: repository main `4c035dbb63d252f3cf0eeb1e6e72f62d2a682b2f`, including the completed anonymous 500 package and 350 disagreement summary. The supplied source directory was not a Git checkout and contained no AGENTS.md. An independent clone was clean before work; no tracked AGENTS.md was found in that clone. No parallel checkout was edited.

The sole current rule baseline is the [current handbook reader](../../notes/handbooks/reader_20261007/README.md): **B.sop_v4.2.14 series, document revision 2026-10-09**, despite the directory's 20261007 date. Chinese DOCX SHA-256: `285f9d30906eec1946e93f2cd52f70da193176c934249abd18921ebc94e7a078`. The historical v4 Markdown and model prompts are not substituted for this reader. The reader itself says its revision is for review before subsequent annotation; the batch metadata's series name does not establish the exact file Coder C used.

The 46 screenshots were matched by unique sentence content to [the public single-coder package](../../data/cnss_blind500_v1_coder_c_provisional_20261029/README.md), not by screenshot filename, UI queue number or JSONL row number. U007's screenshot file number differs from its UI number (57); neither is its public record suffix (344). All 46 map to distinct public IDs. The source image bytes and identifying local directory names are not published.

Four screenshots differ from the released export: **U387, U426, U462, U480**. The JSON preserves both observed screenshot labels and current export labels as offsets and types. Other screenshot spans were visually checked against the matched export. These are different observation points, not evidence of an unauthorized modification. Some screenshots show incomplete progress, whereas the published export records all 500 as confirmed; screenshot progress is not a substitute for export status.

## Findings and use

|Primary classification|Cases|Meaning|
|---|---:|---|
|A|23|Existing provisions sufficient for the stated interpretation|
|B|22|Existing provisions, but semantic application or example needs clarification/review|
|C|1|Desired discontiguous selection cannot be represented by one continuous span|
|D|0|No genuinely new normative rule shown necessary by this evidence|

See the [46-case decision table](decision_table.md) and [separate adjudication-candidate JSON](adjudication_candidates.json). JSON offsets are zero-based, end-exclusive Unicode code points in the identified **existing public record**. They record observed labels, not proposed replacements. Proposals are prose because assigning authoritative corrected offsets before human adjudication would overstate certainty. An A classification means the stated issue can be addressed using existing provisions; it does not resolve the sentence's entire annotation.

The main recurring issues are preserving shared objects/actions, generic experience versus specific activity, knowledge versus practical tool use, general communication versus occupational function, and activities versus desired results. R11 already provides an unresolved-candidate process. R14 and R23 do not authorize mechanical splitting at every conjunction. They allow a short activity such as maintenance when its object is unambiguous in the same sentence; a bare state, attribute or unrelated brand does not automatically become a skill.

**No handbook rule is activated or revised by this release.** [Proposal UCP-1.0.0](future_rule_proposal.md) adds a prospective explanatory candidate and future research design. It changes neither L/K/S/T definitions nor current scoring. Examples in this diagnostic set must be disclosed as exposed to rule discussion, not subsequently presented as an untouched independent test of rules developed from them.

After the independent second coder finishes, preserve both original independent versions, compute agreement under the declared frozen protocol, then adjudicate with the authors. Do not expose these candidate answers to a coder whose work is meant to remain blind; if exposure occurs, document it. Version any adjudicated release separately. No retrospective silent relabelling, 500-sentence IAA, or combination into an 850-sentence annotation set is performed here.

## Metric boundary

All current labels use continuous character intervals. A changed boundary can alter exact matches; a type change affects typed scoring; splitting alters span counts and match denominators. No direction or magnitude of score change is inferred here, and no existing paper result is recalculated.

“Relaxed” is protocol-specific in this repository: the [350 analysis](../annotation_disagreement_analysis_blind350.md) documents the legacy value as **same-boundary, type-ignored** F1, whereas the [scorer](../../scorer/README.md) includes token-IoU relaxed scoring after continuous-span projection. Neither definition accepts a concatenated, discontinuous entity as one ordinary interval. Do not describe all relaxed scores as character-overlap F1 or transfer thresholds between protocols.

## Privacy, permissions and verification

Only anonymous Coder C, public record IDs, observed offsets/types, short necessary locating fragments and original analysis are included. No screenshots, full recruitment sentences, local paths, coder names/accounts, identity maps, source ledgers, instrument number or price are newly published. Existing public history may permit linking aliases to identities; this addition does not claim to erase that exposure or establish unlinkability.

[DATA_AVAILABILITY](../../DATA_AVAILABILITY.md) excludes third-party recruitment texts from the author-granted reuse permission. Academic research access is not a blanket redistribution licence. These diagnostic excerpts do not extend source licences. No full source texts, vendor files or protected directories are added.

Checks: 46 images / 46 unique content matches; A/B/C/D = 23/22/1/0; current and screenshot interval bounds/non-overlap validated; source package and handbook hashes verified; all new public files scanned for identifying names, local paths, credentials, contacts and source URLs; links checked locally. Scanning is a bounded check, not a general legal or anonymity certification. Only this directory is committed; no original data changes are staged.

## Change log

- **1.0.0 (2026-10-29):** first uncertainty inventory, rule decision table, observation/candidate ledger and UCP-1.0.0 proposal. Analytical documentation only; no adoption, adjudication, data migration or score changes.
