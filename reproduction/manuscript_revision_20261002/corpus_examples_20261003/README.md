# Corpus examples in Figure 4

Updated 3 October 2026.

Figure 4 uses five records from the frozen 150-sentence human reference. Three panels reproduce complete stored sentences; two reproduce contiguous excerpts. All displayed Chinese characters, highlighted spans and labels are preserved from the archived records. Line wrapping is for presentation only. English explanations are reading aids and were not used as model inputs.

The preceding eight-panel illustration combined handbook teaching examples, shortened corpus fragments and comparisons composed from separate cases. It was useful for explaining rules but did not establish that every panel was a complete original sentence. The replacement includes more context and adds the previously missing L category.

| Panel | Source ID | Extent | Types shown | Main point |
|---|---|---|---|---|
| a | 1802-s0008 | Contiguous excerpt, offsets 52–79 | L, T | English reading/writing differs from communication and teamwork. |
| b | 1806-s0005 | Complete stored sentence | K, S | Conceptual knowledge differs from programming activity. |
| c | 1803-s0002 | Complete stored sentence | S | Separate occupational actions retain their complete boundaries. |
| d | 1973-s0006 | Contiguous excerpt, offsets 4–36 | T | Colloquial and interpersonal capabilities occur in longer requirements. |
| e | 1896-s0005 | Complete stored sentence | S | The occupational activity can be bounded separately from a generic experience qualifier. |

Offsets are zero-based and end-exclusive. The authoritative display ranges are also recorded in [provenance.json](provenance.json). The excerpts do not cut an annotated span. Panel (a) preserves the absence of punctuation between the two numbered requirements. Panel (d) starts at the numbered requirement, after the stored serialization prefix. No source records were cleaned, relabeled or overwritten by this figure revision.

## Source and annotation version

The source is [data/gold150/gold150_test.jsonl at the pinned repository revision](https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/blob/cb1b2e09c0af260c251a57e13add3a23b6e979b9/data/gold150/gold150_test.jsonl). The selected records carry handbook identifier `B.sop_v4.2.10`. They illustrate archived human-reference annotations; they are not new independent annotations under v4.2.14. The manuscript caption states this distinction, and Appendix A describes the current handbook rules.

The source labels are mapped to the manuscript notation without changing their meaning: `Language_Skills&Knowledge` → L, `knowledge` → K, `skills` → S, and `Tranversial SKills` → T (the spelling of the last source label is preserved here). Text and canonical labels were also checked against the BIO reference archived with the Chinese encoder experiments.

## Reusable figure materials

- [Vector PDF](../source/figures/annotation_examples_corpus_20261003.pdf)
- [Figure data, original sentences and span offsets](../source/figures/annotation_examples_corpus_20261003.json)
- [Editable figure generator](../source/figures/generate_corpus_examples_20261003.py)

The figure retains selectable text and embedded fonts. Source IDs appear in each panel. The original eight-panel teaching illustration remains in the repository history and is marked as superseded in its documentation.

## Manuscript checks

The revised manuscript compiles to 40 pages; Figure 4 is on page 10. The source text, all five sets of offsets, type mapping and figure references were checked. The figure page and adjacent pages were inspected for clipping and layout. This revision changes the example figure, its caption and one contextual sentence; it does not change experimental data, scores, formulas or citations.
