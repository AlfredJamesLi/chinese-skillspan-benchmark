# Qwen reference correction — 3 October 2026

Only the `qwen2025report` bibliography record is revised. The citation key is unchanged.

- Corporate author: **Qwen Team**, as recommended in the [official Qwen citation](https://qwenlm.github.io/blog/qwen2.5-max/#citation). BibTeX braces preserve the group name rather than parsing it as a personal name.
- The reference explicitly identifies **arXiv:2412.15115v2**, retains **Version 2**, and displays a clickable version-specific URL.
- The year remains **2025** because the [version history](https://arxiv.org/abs/2412.15115v2) dates version 2 to 3 January 2025. The official generic citation's 2024 identifies the initial release.
- The active PeerJ template uses `apalike`, which does not print this misc record's `eprint` and `url` fields. The arXiv identifier is therefore also provided in `howpublished`, and the visible version and URL in `note`.

A long author list is not, by itself, a formatting error. The [PeerJ CSL style](https://github.com/citation-style-language/styles/blob/master/peerj.csl) truncates eligible in-text author lists but does not apply the same rule to bibliography entries. The official author-instructions page could not be retrieved in this check; no new journal-wide truncation rule is inferred. No other author lists were shortened.

Validation: regenerated the bibliography in an isolated build and compared all 51 entries. Only Qwen changed; the other 50 entries were retained. The main-text citation now uses Qwen Team, 2025. The compiled PDF was checked for the visible identifier, version, working link, cross-references and page layout. Experimental results, handbook rules and all other manuscript sources remain unchanged.
