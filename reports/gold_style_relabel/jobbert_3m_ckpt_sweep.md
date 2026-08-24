# JobBERT-zh 3.2M checkpoint CRF sweep

Internal only. Gold v2 typed exact micro F1.

Reference JobBERT 1M: typed F1 = 0.12244098344597903

| step | epoch | dev | test typed F1 | P | R | TP/pred |
|---:|---:|---:|---:|---:|---:|---|
| 65000 | 1.30 | 0.3205 | 0.1233 | 0.1790 | 0.0940 | 623/3480 |
| 100000 | 2.00 | 0.3207 | 0.1167 | 0.1719 | 0.0883 | 585/3403 |
| final_encoder | — | 0.3209 | 0.1170 | 0.1724 | 0.0886 | 587/3404 |
