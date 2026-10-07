> Superseded by [verified corpus examples](../corpus_examples_20261003/README.md). The eight panels described below were handbook illustrations, not eight complete original sentences.

# Highlighted Chinese annotation examples

The previous Table 3 has been replaced by Figure 4, a vector illustration with eight bilingual panels. The figure appears on PDF page 10. The manuscript remains 40 pages.

## Design choice

| Format | Strength | Limitation |
|---|---|---|
| Previous three-column table | Easy to locate a rule and its explanation | Brackets and subscripts make span extent harder to scan; narrow columns break examples and explanations |
| Earlier highlighted illustration | Span boundaries are immediately visible | Restoring its old four examples would omit several current-handbook decisions; coloring the English glosses as well creates unnecessary visual competition |
| Revised highlighted vector figure | Preserves all eight current examples, with Chinese-only highlighting and short English explanations | Occupies more vertical space than the table, accommodated without adding pages |

The original [SkillSpan paper, Figure 1](https://aclanthology.org/2022.naacl-main.366/) also introduces the extraction task with span examples. That figure provides a presentation reference. The Chinese examples and annotations here come from the authors' handbook.

## Exact content retained

- All eight source strings and selected span/type pairs match the replaced table.
- The shared-action example is a single span. The omitted-reference example does not copy Linux into the second span.
- The first experience qualifier remains outside its span; the second remains inside.
- Only Chinese source spans are highlighted. Context and English explanations remain unhighlighted.
- K/S/T labels accompany the colors and identify the categories illustrated in these examples.
- English explanations are display aids, not model inputs or translated gold annotations. Historical study labels, results and uncertainty estimates are unchanged.

## Files and verification

The manuscript uses `figures/annotation_examples_highlighted_20261002.pdf`. Its text and highlight shapes are vector objects with embedded fonts. The accompanying Python source regenerates the figure; the JSON records the exact illustrative strings, offsets and types.

Figure and table references were updated throughout active manuscript sources, including Appendix A. Later figure/table numbers changed automatically. The current manuscript position index uses stable source labels. Local checks compared all eight cases against the pre-edit table and confirmed that other scientific prose, equations, citations and result tables were unchanged apart from references and figure placement. The compiled PDF has 40 pages and no overfull boxes, missing characters or unresolved references. The new figure and adjacent pages were visually inspected.

The pre-edit source and PDF are retained locally. Synchronization records are maintained separately from the rendering checks.
