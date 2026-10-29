# UCP-1.0.0 — internal metadata and continuous spans

Status: **prospective / future-version rule clarification candidate**, 2026-10-29. Not an activated handbook revision and not R24. It is a proposed explanation of existing original-span rules 1–3, R13 and R14. Authors should approve wording and examples before integrating it into a separately versioned future reader. No evidence here establishes author consensus. L/K/S/T definitions remain unchanged.

## Proposed explanation

选择实体时，只有在原要求的含义完整、所选文字仍是原句中单一连续区间的情况下，才可将无关限定留在边界之外。若无关说明夹在表达必要成分之间，不得删除中间字符后拼成一个实体；当前格式应保留能够表达该要求的最短连续原文，并在独立复核记录中注明 `discontinuous_span_candidate`。该标记不是第五类标签，也不是已确认的分段实体。拆成多条须另行满足各条独立表达原要求、类型有依据及互不重叠的现行条件，不能仅为绕过插入说明而拆分。

Positive teaching example (synthetic): `负责每日设备维护工作` may yield `设备维护` S if the frequency is irrelevant to the skill requirement. Both the result and its offset are contiguous. Qualification thresholds, named methods and scope-changing modifiers cannot be removed merely because they look like modifiers.

Counterexample (synthetic): `仪器甲（资产说明）的开放服务` cannot yield the concatenation `仪器甲的开放服务` as one interval. Retaining the enclosing continuous phrase is structurally valid. The sample's original text must not be rewritten to make a desired span pass offset validation.

## U394 / CNSS-B500-066

The source has a specific instrument name, then parenthesized asset-number and price metadata, then the service activity. For privacy and source minimization, the number, price and complete sentence are not repeated here. The semantic target omitting that middle metadata is **discontinuous in the original**, even if the resulting phrase reads naturally. The existing Coder C label already retains the internal metadata within one S interval. This is a structural compatibility finding, not final endorsement of its semantic boundary.

|Option|Current compatibility|Decision and consequences|
|---|---|---|
|Keep the shortest continuous complete service expression, including internal metadata|Compatible with original-span rules 1–3 and R13|Preferred current candidate. Preserve the instrument/service relation; do not include an unrelated outer duty marker or service-hour target solely to make the span longer. Metadata length is part of the interval and may affect overlap scoring.|
|Split before and after metadata into two independent continuous entities|Only if each part independently expresses a supported skill under R14|Not justified merely by wishing to omit metadata. An instrument serving as the object of an open-sharing service is not necessarily a separately required instrument-operation skill. This sentence does not clearly supply two independent skill requirements; retain as a rejected workaround unless authors establish that evidence.|
|Use a grouped/discontinuous entity with two component intervals|Unsupported by the current label schema and scorers|Future research only. It requires a new data schema, annotation training, human review protocol and validated metrics; cannot be counted as one ordinary current span.|

A short `开放共享服务` candidate is structurally continuous, but its semantic sufficiency requires checking whether dropping the instrument object changes the occupational requirement. R14 requires this comparison; the present preferred candidate retains the object. It must not be described as the only imaginable valid boundary.

## Future representation and evaluation design (not implemented)

A future entity could have an entity/group identifier, one L/K/S/T type and an ordered list of nonempty component `[start,end)` intervals over the unchanged original text. Validate bounds, order, segment non-overlap and the policy on overlap between different entities. Store displayed concatenations only as derived views, never as source text or current `span` strings.

Candidate exact group matching would require the type and every ordered component interval to agree. A candidate relaxed group score could compare unions of character positions, with a predeclared IoU threshold and one-to-one maximum-weight matching between entities. Define type-aware and type-ignored variants separately, and test whether this unfairly rewards fragmented entities. Group-level scoring must distinguish one grouped skill from two unrelated skills with the same character union. Report segment-boundary agreement and grouping disagreements as complementary diagnostics.

Before adoption: independently annotate a designated development sample under that representation; retain independent versions; adjudicate whether each segment is necessary, whether groups express one skill and whether omitted material changes scope. Report independent agreement separately from adjudicated reference results, the number/proportion of cases requiring human decisions, unresolved cases, and reasons. Use held-out data to validate thresholds and compare with the continuous baseline. Human assessment does not retroactively become a metric used by today's benchmark. No such score is computed or claimed here.

## Scope, impact ledger and adoption questions

- **U394 / CNSS-B500-066:** definite internal-metadata representation candidate; present export already uses an enclosing continuous span. No relabelling required solely to enforce continuity.
- **U257 / CNSS-B500-007:** parentheses include manufacturing costs, potentially essential scope. Review control case; not automatically a discontinuity candidate and not automatically removable metadata.
- **U459 / CNSS-B500-013:** parentheses contain an independently identifiable degree requirement. Review control case for valid splitting, not metadata deletion.
- **Other 43 reviewed cases:** affected by ordinary interpretation questions in the table, not proven affected by this proposed clarification. No full 350/500 migration-impact audit is claimed; an author-approved future change would require such an audit before adoption.

Small author decision set: (1) accept the proposed explanatory wording and instrument-object retention, (2) resolve shared-core/application questions in B cases, particularly U017/U025/U361/U426, and (3) decide whether a future grouped-span study is worth pursuing. None of these choices blocks preserving the current data and publishing this clearly provisional analysis.

Compatibility: existing 350/500 labels and archived paper metrics remain frozen. Apply an approved clarification prospectively in a named later adjudication/data version after independent second annotation, with a change ledger and before/after offsets. Keep ordinary exact/relaxed metrics on continuous offsets for current releases. Do not silently migrate old data, add grouped labels to old JSONL, or call an investigator's hand calculation an existing benchmark method.

Change log: UCP-1.0.0 introduces a non-normative wording proposal and research design only. No effective date for normative use has been assigned.
