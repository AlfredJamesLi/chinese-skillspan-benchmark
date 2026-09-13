# Round 2 changes and remaining evidence gaps

This index includes the initial second-review revision and the author's subsequent refinements through the final naming pass. It supersedes earlier completion descriptions for figure style and table location.

| Review item | Current outcome | Remaining evidence |
|---|---|---|
| R2-01 Sources and selection | Corpus/reference/supervision roles and known sampling lineage clarified | Platform/date/acquisition rules, segmentation/deduplication, challenge selection and coder training records remain incomplete |
| R2-02 Executable version | Frozen reference, shared protocol, parser/scorer roles mapped; R23 case checked by ID/text | Original scorer executable binding and broader rule compatibility remain unresolved |
| R2-03 JobBERT implementation | Saved configs/selection evidence recovered; shared initialization and 256-token setting documented | Historical training/export code, tokenizer revision, character projection and long-input behavior remain unbound |
| R2-04 Literature | Cao Chinese skill/specialty precedent added; SkillSpan labels and Kompetencer layers corrected | No new literature claim introduced by this sync |
| R2-05 Figures | Author-selected illustrated Figures 1/2 restored; boundary examples updated; final names aligned | Superseded minimalist redraws are not the final figures |
| R2-06 Diagnostics | Existing accepted predictions summarized by type, length and empty-reference errors; final Figure 5 uses mixed chart types | No inference or test-guided prediction repair |
| R2-07 Numbers and referents | Current exact-F1 means use full precision; character kappa 0.5673 added beside span F1 0.4444 | Later coder exports are not proven byte-identical to the initial freeze; historical Coder A recall discrepancy remains documented |
| R2-08 Public handoff | Tables, notes, naming, inventories and reproduction directions now have one repository index | A documentation commit is not release of Qwen adapters, all run predictions, historical implementation, or a new immutable archive |

## Author refinements incorporated

- Structured four-part abstract retained; main inference and student results remain in the body.
- Appendix A–D links repaired; formulas displayed separately; training parameters tabulated.
- DeepSeek model identity separated from non-thinking/thinking mode and output caps.
- Seven supplementary tables and the detailed output-status table moved with complete context; Qwen diagnostic table retained as figure data.
- Experimental reminders condensed into companion notes; material limitations remain summarized in the paper.
- Repeated model names, version keys and example IDs use a 28-entry alias map.

## Decisions still requiring original evidence

1. Complete collection/selection/coder records and redistribution/privacy documentation.
2. Recover the exact JobBERT implementation/checkpoint history, or retain its stated interpretation limits.
3. Reconcile the original coder files and historical rounding discrepancy; keep the current explanation until then.
4. Supply a pinned complete current inference/training package if full rerunning is intended. The original scorer binding, missing predictions/requests and unreleased adapters must not be silently treated as available.
5. Broader rule-version compatibility needs its own evidence; the R23 check is a single-case check.

This synchronization changes presentation and availability of companion documentation. It does not change frozen labels, manifests, predictions, parsers, scorers, model weights, or reported results.
