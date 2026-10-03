# Evaluation presentation revision — 3 October 2026

The revision retains the current manuscript and incorporates the useful parts of the metric-comparison proposal without adding another table or changing table numbers.

- Table 7 retains the separate Qwen and historical JobBERT comparisons. Its Qwen panel now includes typed relaxed and newly verified boundary-exact F1; JobBERT retains only the verified typed exact scores.
- Table 8 retains encoder overall and macro-F1 scores and adds a full L/K/S/T panel across Qwen without an adapter, Qwen B2 LoRA, XLM-R-large, and ESCOXLM-R. Reference-span counts and the very small L support are explicit.
- The results paragraph reports Qwen's S/K gains and treats cross-model category differences as descriptive. Figure 5 remains a per-seed diagnostic, while the table provides aggregate category comparisons.
- Appendix C identifies the new offline boundary scoring and links the full-precision metric records and reproduction scripts. Original Qwen exact/relaxed and encoder results are preserved.

The optional S/K-only pooled F1, new category-level significance tests, a new model ranking, and claims that the Chinese task is necessarily harder than SkillSpan were not added. Those would either duplicate the per-category results or require a different experimental comparison. No unverified JobBERT result was filled.

All four Qwen prediction sets were checked using the official scorer and an independent coordinate-based implementation. Parser replay matched all 600 frozen outputs. Qwen and encoder reference files were identical by ID, text, and typed span despite serialization differences. Six encoder receipts and their source prediction/reference hashes were independently checked. All means and sample SDs use complete-precision per-seed values.

The previous tracked sources and PDF are backed up locally in this delivery folder. The edit record specifies every changed passage. The manuscript remains within the 40-page limit, and the existing title, abstract, AI disclosure, formulas, bibliography, figures, and table numbering are retained. Publication status and final validation are recorded separately after compilation and visual inspection.

Final verification passed: 40 pages; Table 7 on page 16, Table 8 on page 17, and the new scoring note on page 27. There are no unresolved references, overfull boxes, missing characters, or new short paragraph-ending lines. New displayed values match the ten official scoring receipts. The original title, abstract and AI disclosure are byte-for-byte unchanged in the main source.
