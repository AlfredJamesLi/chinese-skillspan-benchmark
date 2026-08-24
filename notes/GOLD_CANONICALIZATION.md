# Gold canonicalization v2

**18 annotation conflicts adjudicated (Doubao draft + human).** Unique IDs restored to 2601.
Raw Gold was not modified.

This uniqueifies Gold. Do **not** yet write Table 3 into the PDF: most dumps still have duplicate or missing IDs.
Score with `data/gold_canonical_v2.jsonl` and unique-first prediction views.

## Counts

| role | rows | unique IDs | spans | L | K | S | T | SHA256 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| raw | 2676 | 2601 | 6681 | 31 | 2238 | 3401 | 1011 | `103e400c79eb3954d0857e7000b4388773622fda6a333e72be7720bf27f5e172` |
| v1 (conflicts held out) | 2583 | 2583 | 6618 | 31 | 2208 | 3384 | 995 | `458c91478079c7702a82befc15c58f4be7cc77b2cf820b0ed33efb791657e5df` |
| **v2** | 2601 | 2601 | 6627 | 31 | 2211 | 3384 | 1001 | `7a26e32b89d4e501175cb96443e35e171cea08d91501d2a32779b96ee8504ff6` |

Human overrides vs Doubao: `1987-s0045` empty; `1988-s0113` empty; `1991-s0042` only `医学专业`[K].
Log: `data/gold_adjudication_v2.json`.
