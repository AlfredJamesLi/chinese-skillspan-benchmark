# Benchmark annotation profile

The figure profiles the original B2 Qwen training/development manifests, Gold150,
and the two human-review layers of QA150. It does not describe all 9,540 records
in the expanded Silver experiment. QA150 is one set of 150 sentences, not two
independent samples; the two human layers are not pooled or adjudicated here.
Machine suggestions were visible during QA150 review.

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
offsets and labels, completed QA confirmations, and agreement of histogram totals
with annotation counts. Source files are read only. QA overlapping spans are
retained as span annotations; no character-label projection is performed here.

## Measurement and plotting

- Length: unmodified Unicode code points, including spaces/punctuation.
- ECDF: complete input records, including empty-target records; one curve for QA150.
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
- B2 manifest repeats are retained. Group size is not encoded by violin width.
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
character lengths. The script and aggregates reproduce manuscript Figure 3. Private raw label exports are not included.

## Verified environment

The aggregate reconstruction was checked with Python 3.13, NumPy 2.1.3, SciPy 1.15.3, Matplotlib 3.10.0, and Pillow 11.1.0. Install the pinned dependencies in `requirements.txt`. Arial is the original figure font; another font may change layout. PDF timestamps can change file hashes without changing the rendered figure.
