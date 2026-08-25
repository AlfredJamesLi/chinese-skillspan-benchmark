# CWS engine compare (sandbox)

Same JobBERT-zh 1M+v4 CRF pred. Only word-boundary snap changes. **Not** Table 3.

HanLP 2.x Electra tok: installed, model fetched, **failed** (`BertTokenizer.encode_plus` gone in this env's transformers). Do not downgrade transformers (CRF training uses the same env).

| Engine | Gold v2 exact | Gold v2 IoU≥0.5 | SOP rule exact | mid-word spans | sents changed |
|---|---:|---:|---:|---:|---:|
| jieba | 0.1454 | 0.3411 | 0.2609 | 0.0036 | 0.344 |
| pkuseg_mixed | 0.1441 | 0.3412 | 0.2630 | 0.0041 | 0.338 |
| pkuseg_news | 0.1424 | 0.3418 | 0.2639 | 0.0055 | 0.336 |
| pkuseg_web | 0.1437 | 0.3415 | 0.2620 | 0.0044 | 0.340 |
| pkuseg_news_nodict | 0.1409 | 0.3409 | 0.2646 | 0.0055 | 0.336 |

jieba is the engineering baseline (userdict). pkuseg via `spacy_pkuseg` (original `pkuseg` does not build on Python 3.11).
Do not copy into `confirmed-results.md`.
