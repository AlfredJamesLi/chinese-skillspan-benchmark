# Blind-350 pre-adjudication disagreement analysis

This **double-coded blind subset** contains 350 sentences independently confirmed by both coders under handbook B.sop_v4.2.14. There are **127 identical span sets and 223 sentences with pre-adjudication disagreement**. These are not errors against a reference answer. Neither coder is treated as correct; no adjudication or final Gold is produced. This subset is separate from the 500-sentence provisional single-coder addition.

## Scope, aliases and provenance

**Coder A and Coder B are analysis-local aliases**, in the same left-to-right order as the legacy paired analysis. They must not be interpreted as the repository's historical person-level A/B aliases. They correspond to **Coder B and Coder C** in the [current pseudonymized package](../data/cnss_blind350_v1_coders_bc_20261029/README.md). These repository coder codes are preserved. The repository already uses cohort-specific aliases, so this scope distinction is essential when comparing studies. No personal name, account, email, project number, or identity lookup table is introduced here.

Sources were read from the frozen 350-sentence package introduced in commit `eb0cd41ed08c5a7131d6469ad61d895f8243087c`, checked against main at `f7eb3ce7bfe82d8d2f692f03876419d868b28291`: both raw JSONL exports, paired JSONL, package README, and analysis `DISAGREE.md`, `SUMMARY.json`, `RELIABILITY.json`, and `ANALYSIS.md`. A subsequent current-version pseudonymization renamed the package, files and identity-bearing keys, removed internal project numbers, and preserved all annotation content and numerical statistics. The aggregate [JSON](annotation_disagreement_analysis_blind350.json) now records the pseudonymized raw file SHA-256 values; all other aggregate values are unchanged. This document is the preferred public summary replacing the role of the legacy detailed analysis; published history is not rewritten.

Earlier Git commits expose identities. Current-version pseudonymization does not undo that exposure or guarantee unlinkability. The identity mapping is kept outside this repository, but the historical exposure remains; this is not a claim of complete anonymity across Git history or other historical cohorts.

## Independently recomputed results

| Quantity | Result |
|---|---:|
| Confirmed sentences per coder; text mismatches | 350; 0 |
| Coder A / Coder B spans | 808 / 878 |
| Identical / differing sentence span sets | 127 / 223 |
| Both confirmed empty | 69 |
| Typed exact span matches | 429 |
| Same-boundary matches, ignoring type | 467 |
| Typed exact micro-F1 | 0.5088967972 |
| Type-ignored, same-boundary micro-F1 | 0.5539739027 |
| Character Cohen's kappa | 0.7218387915 |
| Character nominal Krippendorff's alpha | 0.7217264336 |
| Same-boundary type differences | 38 span pairs in 26 sentences |
| Coder B strictly inside Coder A | 157 sentences |
| Coder A strictly inside Coder B | 44 sentences |
| Coder A empty / Coder B nonempty | 15 sentences |
| Coder B empty / Coder A nonempty | 3 sentences |
| Coder A spans with no Coder B overlap | 39: S=29, K=7, T=3; 27 sentences |
| Coder B spans with no Coder A overlap | 72: S=48, K=23, T=1; 38 sentences |

All rows above independently match the existing summaries. Sentence categories overlap and must not be summed. Span pairs, spans, and sentences are distinct units. Longer/shorter describes offsets only, not quality.

The script validates unique IDs, matching text, confirmed status, valid zero-based end-exclusive offsets, unique spans and boundaries, and absence of within-coder character overlap. Sentence agreement compares sets of `(start, end, type)`. Micro-F1 is `2 * matches / (808 + 878)`; if directional precision/recall are reported, their denominators are Coder A=808 and Coder B=878. This convention does not make either coder a reference answer.

Character coefficients project all 12,378 characters to O/L/K/S/T, including punctuation and both-outside positions. Kappa uses separate coder marginals. Nominal alpha uses pooled marginals with finite-sample expected disagreement: `De = 1 - sum(n_c*(n_c-1))/(N*(N-1))`, where `N=24,756` ratings, and `alpha=1-Do/De`. Neither coefficient substitutes for span-level F1: character agreement credits shared interiors and outside positions, while exact F1 requires both boundaries and type to match.

## Counting differences from the legacy summary

For transparency the new script enumerates **every cross-coder pair** in each sentence. Strict containment permits one equal endpoint but excludes identical boundaries. Partial overlap means positive intersection with neither span containing the other. Touching endpoints do not overlap. A single long span may therefore contribute several containment pairs.

| Quantity | Legacy summary | Independently recomputed, all pairs |
|---|---:|---:|
| B inside A, same type S | 106 | 148 |
| B inside A, same type T | 65 | 73 |
| B inside A, same type K | 24 | 31 |
| Partial-overlap sentences | 5 | 9 |
| Partial-overlap pairs | Not stated as a total | 10 |

The legacy 106/65/24 and 5 are **retained from the existing summary, not independently reproduced under its original counting procedure**. They are not interchangeable with exhaustive pair counts. The legacy document appears selective in its pair descriptions, but the original selection algorithm has not been established; this is not a claim that the raw annotations changed. The reverse same-type containment counts do match: A inside B has S=41, T=12, K=7 pairs. All directional type combinations are available in the aggregate JSON. Both definitions recover the headline 157/44 containment sentence counts.

Bootstrap intervals, both-outside-excluded kappa and other ancillary legacy statistics are outside this reproduction's scope and are not newly certified here.

## Type differences and interpretation

Direction below is **Coder A type → Coder B type**, never an error or correction direction.

| Type pair | Same-boundary pairs |
|---|---:|
| K → S | 13 |
| S → K | 10 |
| S → T | 10 |
| T → S | 2 |
| K → T | 2 |
| L → T | 1 |

K/S accounts for 23 of 38 pairs, S/T for 12. The 38/467 same-boundary type differences should not be generalized to spans whose boundaries differ. Boundary inconsistency is a major contributor to low exact F1: ignoring type improves F1 by only 0.0451, and containment affects many sentences. These observations do not by themselves demonstrate failure of the type taxonomy, nor do they causally apportion all disagreement to boundaries. Segmentation, coverage and type differences can coexist.

## Priorities for subsequent human adjudication

1. Operationalize the **shortest complete span** rule with inclusion/exclusion criteria and new synthetic examples; shortest alone must not imply correctness.
2. Decide when the **能力** suffix is semantically necessary, and apply that rule consistently across types.
3. Clarify responsibility phrases: whole activity versus core concept, modifiers, and coordinated activities.
4. Clarify education/major phrases: qualification level, subject, degree and trailing requirements.
5. Review the 38 same-boundary type disagreements, prioritizing K/S and S/T; also examine type differences within boundary disagreements.
6. Review one-sided coverage and confirmed-empty disagreements. These are possible omissions or scope differences, not established coder errors.

These priorities are qualitative synthesis of the existing analysis, not newly counted semantic categories. No new recruitment sentence or full disagreement list is distributed. Human adjudicators must record decisions separately from the preserved blind annotations.

## Reproduction and access

Run the standard-library [analysis script](../scripts/analyze_blind350_disagreement.py) with authorized raw exports in the hash-identified order:

```text
python scripts/analyze_blind350_disagreement.py A.jsonl B.jsonl aggregate.json
```

Input filenames above are placeholders. The output contains only aggregate statistics and source hashes, with no sentence IDs, text, metadata identities or source paths. Compare its parsed JSON to the committed aggregate. File hashes reflect the checked-out raw bytes; line-ending transformations can change hashes without changing annotations.

[Data access and licensing](../DATA_AVAILABILITY.md) excludes third-party recruitment text from the repository's general reuse permission. [Contribution rules](../CONTRIBUTING.md) favor synthetic examples and prohibit unauthorized source-text redistribution. The analysis adds aggregates and generic category descriptions only. Package pseudonymization changes identifiers and identity metadata; all sentence text, confirmed states, labels, numerical statistics and the 500-sentence package are preserved. Public availability of legacy text is not a new grant of redistribution rights.
