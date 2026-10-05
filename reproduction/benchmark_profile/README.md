# Benchmark annotation profile

The figure profiles the Silver training/development sets used by Qwen and the
encoder comparison: 2,150 training records and 169 development records,
displayed as "Silver train" and "Silver dev". It also profiles the human
reference set (150 sentences) and two annotation layers of the additional
review sample (150 sentences). The figure does not describe all 9,540 records
in the expanded Silver experiment. The additional review sample is one set
of 150 sentences, not two independent samples; its two human layers are not
pooled or adjudicated here. Machine suggestions were visible during this review.

For reproducibility, the input aggregates retain the archived identifiers
`B2 train`, `B2 dev`, `Gold150`, `QA150 A`, and `QA150 B`, along with the
original source paths and hashes. These identifiers are mapped only to
display names; counts, distributions, and annotations are unchanged.

## Reproduce from the included aggregates

Python with NumPy, SciPy, Matplotlib, and Pillow:

```sh
python reproduction/benchmark_profile/benchmark_profile.py --aggregate reproduction/benchmark_profile/benchmark_profile_data.json --output output/benchmark_profile
```

The JSON contains exact integer-length frequency counts and type counts, with
input SHA-256 hashes. It includes no sentence wording, identifiers, offsets,
annotator names, credentials, or model predictions. Expanding a frequency count
recovers the complete measured length distribution; no random values are generated.

## Rebuild aggregates from the private frozen files

```sh
python reproduction/benchmark_profile/benchmark_profile.py --evidence /path/to/Gold150_shared_prompt_eval_for_Overleaf_20260910 --qa /path/to/QA150_all_layers.jsonl --output output/benchmark_profile
```

All four input file hashes are checked, as are expected record/span totals, valid
offsets and labels, completed review confirmations, and agreement of histogram totals
with annotation counts. Source files are read only. Additional-review overlapping spans are
retained as span annotations; no character-label projection is performed here.

## Measurement and plotting

- Length: unmodified Unicode code points, including spaces/punctuation.
- ECDF: complete input records, including empty-target records; one curve for the additional review sample.
  A log horizontal axis displays the entire observed tail without discarding data.
- Violins: all annotated spans; Gaussian KDE with Scott bandwidth evaluated only
  between observed minimum and maximum; maximum width normalized separately.
  The main viewport is 0--20 characters (96.4--100% of each layer's spans); the
  upper overview displays all observed lengths and labels maxima 47/39/20/41/42.
  Both views use identical full-data KDEs. No long spans are removed and no KDE
  is fitted to a length-truncated subset. Both axes use linear length scales.
  White dot = median; thick line = 25th--75th percentiles. Density smoothing is a
  visual aid for discrete lengths, not additional data or a confidence interval.
- Heatmap: percentages of spans within each layer, annotated with exact counts;
  common 0--70% color scale. Displayed percentages may not sum to 100 after rounding.
- Repeated records in the Silver manifests are retained. Group size is not encoded by violin width.
- Full PDF/SVG vector figures, 300 dpi PNG, and grayscale preview are produced.
- The components have different sampling and annotation designs; the figure is
  descriptive, without claims about annotation accuracy, significance, or SOTA.

## Design references

SkillSpan Figure 2 uses annotated-span-length violins with medians and quartiles:
https://arxiv.org/pdf/2204.12811

CLUENER2020 reports category composition across data splits:
https://arxiv.org/pdf/2001.04351

These inform which dataset properties to display. The present figure is newly
drawn from Chinese-SkillSpan data; no published image or cross-dataset numerical
comparison is reproduced. English token lengths are not equated to Chinese
character lengths. The script and aggregates are ready for repository inclusion;
private raw label exports are not included.
