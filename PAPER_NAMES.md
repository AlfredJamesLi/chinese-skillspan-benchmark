# Paper naming guide

Short names in the manuscript are display aliases. Original file paths, experiment keys, model identifiers, hashes and archived labels remain authoritative. This guide records the mapping without changing data or model identities.

| Category | Paper name | Recorded identifier | Meaning and handling |
|---|---|---|---|
| model | Qwen | `Qwen2.5-14B-Instruct` | Model full name at first use; Qwen later. Display alias only; do not change model IDs or weight paths. |
| model | Qwen (no adapter) | `no_adapter; Qwen2.5-14B-Instruct without project adapter` | Same baseline prediction across current Qwen comparisons. Keep prediction keys and files. |
| model | Qwen LoRA | `Qwen2.5-14B-Instruct with B2 LoRA` | Keep seed 42/43/44 distinct. Keep LoRA_42/LoRA_43/LoRA_44 keys and checkpoints. |
| model | Claude | `Claude Sonnet 4.5` | Version retained at first use. Display alias; preserve recorded access metadata. |
| model | DeepSeek | `DeepSeek-V4-Pro; deepseek-v4-pro` | Non-thinking/thinking are configurations of the same model. Preserve API model ID, mode, and output cap; never merge the two rows. |
| model | Kimi | `Kimi k2.6` | Version retained at first use. Display alias; preserve recorded configuration. |
| model | GPT proxy | `gpt-5.6-terra` | Proxy-returned identifier; provider routing/checkpoint not independently verified. Never rename this to an asserted official GPT model; preserve raw metadata. |
| model | teacher configuration | `gpt-6-astra` | Recorded teacher identifier, distinct from the GPT proxy evaluated configuration. Keep original teacher metadata; do not infer model equivalence. |
| model | JobBERT-zh initialization | `https://huggingface.co/AlfredJames/jobbert-zh` | Released 3M domain-adapted encoder with inherited V4 CRF. Keep published URL and model repository ID. |
| model | JobBERT-zh continuation | `https://huggingface.co/AlfredJames/jobbert-zh-v6a` | Current B2 continuation; default released checkpoint is seed 42. Keep published URL and repository ID; do not replace initialization. |
| experiment | primary JobBERT configuration | `v6a` | 2156 train / 169 dev; earlier versus revised labels. Documentation alias only; preserve manifest names. |
| experiment | Qwen training split | `v6a_nocross` | 2150 train / 169 dev; train/dev exact NFC text matches removed. Keep exact manifest and membership. |
| dataset | human reference | `Gold150; gold150_test.jsonl` | 150 sentences; 663 spans. Keep canonical file, hashes and scripts; add a descriptive README alias. |
| dataset | initial review | `A100` | 100 teacher-label records reviewed before bulk generation. Keep A100 IDs; distinguish later independent exercise claim and later review versions. |
| dataset | post-generation review | `QA100` | 100 records in the later stratified review. Keep QA100 IDs and sampled membership. |
| dataset | nested review subset | `Dual15` | 15 machine-prefilled records nested in QA100. Never conflate with the author-reported earlier independent 15-sentence exercise. |
| dataset | further conflict-origin records | `H730` | 730 Silver-plus records from the conflict queue beyond the initial review. Keep H730 IDs and membership. |
| dataset | other Silver-plus records | `E1621` | 1621 non-conflict-origin historical extraction records. Keep E1621 and historical SOP--CWS provenance. |
| protocol | shared protocol | `rev2 patch1` | Frozen system instruction and user template. Keep original prompt filenames, bytes and hashes. |
| protocol | span parser | `parser v1.1` | Occurrence-based output to original character offsets. Keep parser version, implementation and hash. |
| protocol | span scorer | `cnss-lskt-1.2.0` | Typed exact and relaxed span scoring. Keep scorer identity; do not recalculate or modify scoring. |
| handbook | Handbook v4.2.14 | `B.sop_v4.2.14` | Current guide, distinct from frozen execution protocols. Keep version identity; no relabeling. |
| handbook | Handbook v4.2.9 | `B.sop_v4.2.9` | Historical calibration guide. Keep historical agreement binding. |
| handbook | frozen reference version | `B.sop_v4.2.10` | Reference metadata; not a later handbook revision. Preserve metadata exactly. |
| example | shared-experience example | `1838-s0008; R23` | Appendix A.3 example. Keep source_id, offsets and original Chinese text. |
| documentation | reproduction guide | `REPRODUCIBILITY.md` | Existing GitHub reproduction index. Keep file name and add links to new naming/experimental notes. |
| documentation | experimental notes | `reproduction/experimental_notes/README.md` | Detailed experiments and reproduction reminders. Retain directory; use short link text in documentation. |
| documentation | paper naming guide | `PAPER_NAMES.md; reproduction/paper_names.csv` | New human-readable guide and machine-readable map. Add these documentation files; no canonical data renaming. |

## Naming rules

- Introduce full model names once; use the short names consistently in narrative, tables and chart legends.
- Preserve model versions and modes in configuration documentation. A short display name does not authorize changing an API request or checkpoint.
- Keep the primary data, frozen metadata, source IDs, experiment keys and public model URLs unchanged. Prefer readable documentation links and aliases over renaming these files.
- The illustrated workflow retains the full Qwen label as a self-contained model identification. Its name maps to the same Qwen alias.
- The nested review subset is machine-prefilled QA100 material, not the unverified earlier independent exercise.
- GPT proxy and the teacher configuration are recorded identifiers, not independently verified official model identities.
- Existing historical notes may use canonical identifiers; preserve those records and link to this guide instead of mass replacement.

The CSV mapping is in `reproduction/paper_names.csv`. This documentation snapshot accompanies the Round 2 paper alignment; the containing Git commit identifies its version.
