# Resource names used in the paper

Current manuscript title: **Chinese-SkillSpan: a benchmark for competency span extraction in Chinese job advertisements**. See the [current manuscript](reproduction/manuscript_revision_20261002/README.md).

Use these names when reading the manuscript. Exact paths stay unchanged for reproducibility. See the [annotation and training terminology](docs/terminology.md) for the current role names and historical aliases.

| Paper name | Resource |
|---|---|
| Human reference set | [150-sentence evaluation set](data/gold150/README.md) |
| Silver training/development sets (Qwen and encoders) | [2,150/169 training/development split](data/silver_plus_v6a_nocross/README.md) |
| Expanded Silver pool / alternative expanded Silver pool | [Adopted Codex and supplementary expansion experiments](reproduction/expanded_silver/README.md) |
| JobBERT-zh initialization / Silver-trained JobBERT-zh + CRF | [Model guide](docs/models.md) |
| Shared-guideline protocol | [Evaluation instructions](reproduction/EVALUATION_ENTRY.md) |
| Historical coding and assisted review | [Agreement guide](reproduction/agreement/README.md) |
| Blinded agreement sample | [Final-handbook three-annotator study](reproduction/agreement/finalguide_abc_20261003/README.md) |

<details>

<summary>Exact model IDs, original file names, and historical aliases</summary>

## Detailed mapping

Short names in the manuscript are display aliases. Original file paths, experiment keys, model identifiers, hashes and archived labels remain authoritative. This guide records the mapping without changing data or model identities.

| Category | Paper name | Recorded identifier | Meaning and handling |
|---|---|---|---|
| model | Qwen | `Qwen2.5-14B-Instruct` | Model full name at first use; Qwen later. Display alias only; do not change model IDs or weight paths. |
| model | Qwen (no adapter) | `no_adapter; Qwen2.5-14B-Instruct without project adapter` | Same baseline prediction across current Qwen comparisons. Keep prediction keys and files. |
| model | Qwen + LoRA | `Qwen2.5-14B-Instruct with B2 LoRA` | Keep seed 42/43/44 distinct. Keep LoRA_42/LoRA_43/LoRA_44 keys and checkpoints. |
| model | Claude Sonnet 4.5 | `Claude Sonnet 4.5` | API gateway; request `claude-sonnet-4-5`, response `claude-sonnet-4-5-20250929`. Preserve recorded access metadata. |
| model | DeepSeek-V4-Pro | `DeepSeek-V4-Pro; deepseek-v4-pro` | Official DeepSeek API (`https://api.deepseek.com`), with request and retained response model `deepseek-v4-pro`. Non-thinking/thinking are separate configurations; preserve mode and output cap. |
| model | Kimi K2.6 | `kimi-k2.6` | Official Moonshot API (`https://api.moonshot.cn`); thinking disabled. Request and retained response model fields match. |
| model | GPT-5.6 Terra | `gpt-5.6-terra` | API gateway; request `gpt-5.4`, response `gpt-5.6-terra`. Display name follows the response identifier; see the access note below. Preserve both fields. |
| model | GPT-6 Astra (via Codex) | `gpt-6-astra` | Official Codex access for adopted Silver labels; distinct from the GPT-5.6 Terra comparison baseline. Codex is the interface. |
| model | Grok 4.6 (high) | `Grok 4.6-high` | Author-confirmed Cursor selection: Grok 4.6 with high reasoning effort. The official model ID is `grok-4.6`; high is a setting. Preserve the historical selection wording and suggestion files. |
| model | JobBERT-zh initialization | `https://huggingface.co/AlfredJames/jobbert-zh` | Released 3M domain-adapted encoder with inherited V4 CRF. Keep published URL and model repository ID. |
| model | Silver-trained JobBERT-zh + CRF | `https://huggingface.co/AlfredJames/jobbert-zh-v6a` | Silver-trained continuation; default released checkpoint is seed 42. Keep published URL and repository ID; do not replace initialization. |
| experiment | Silver training/development sets (JobBERT) | `v6a` | 2156 train / 169 dev; earlier versus revised labels. Documentation alias only; preserve manifest names. |
| experiment | Silver training/development sets (Qwen and encoders) | `v6a_nocross` | 2150 train / 169 dev; train/dev exact NFC text matches removed. Keep exact manifest and membership. |
| dataset | Human reference set | `Gold150; gold150_test.jsonl` | 150 sentences; 663 spans. Keep canonical file, hashes and scripts; add a descriptive README alias. |
| dataset | Initial Silver review sample | `A100` | 100 records with LLM-generated labels reviewed before bulk generation. Keep A100 IDs; distinguish later independent exercise claim and later review versions. |
| dataset | Post-generation Silver review sample | `QA100` | 100 records in the later stratified review. Keep QA100 IDs and sampled membership. |
| dataset | nested review subset | `Dual15` | 15-sentence QA100 assisted-review subset; September 17 export verifies separate coder queues and confirmations. It is distinct from IAA-50 blind calibration. |
| dataset | further conflict-origin records | `H730` | 730 original Silver records from the conflict queue beyond the initial review. Keep H730 IDs and membership. |
| dataset | other original Silver records | `E1621` | 1621 non-conflict-origin historical extraction records. Keep E1621 and historical SOP--CWS provenance. |
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

## Recorded API names and study roles

| Evaluated baseline | Request model | Response model |
|---|---|---|
| GPT-5.6 Terra | `gpt-5.4` | `gpt-5.6-terra` |
| Claude Sonnet 4.5 | `claude-sonnet-4-5` | `claude-sonnet-4-5-20250929` |

The manuscript uses readable display names. These fields identify retained service records. Each configuration has 150 formal prediction records plus two preliminary checks. The shared protocol was frozen for September 10; the GPT run includes a September 11 retry. Retained call metadata accompany raw records; missing dates, decoding settings and checkpoint identities are not inferred.

GPT-5.6 Terra and Claude Sonnet 4.5 provide inference baselines in the Chinese evaluation. The additional-review GPT-6 Astra--Grok 4.6 comparison concerns archived machine suggestions, distinct from the blinded human agreement study. The authors identify the Cursor selection as Grok 4.6 with high reasoning effort (historical selection wording: `Grok 4.6-high`). The archived suggestion file does not independently pin its exact model snapshot or retain complete decoding settings.

The earlier display aliases `GPT (API)`, `Claude (API)`, `DeepSeek`, `Kimi`, and `OpenAI Codex annotation` map to the full display names above. Exact run keys and historical files retain their original wording.

## Official model-name references

Official names were checked on October 5, 2026. These references establish model names and documented settings; the retained run records establish which requests, responses, and access routes were recorded for this study.

| Display name | Official reference | Naming detail |
|---|---|---|
| GPT-5.6 Terra | [OpenAI model page](https://developers.openai.com/api/docs/models/gpt-5.6-terra) | `gpt-5.6-terra`; the separate requested alias `gpt-5.4` is documented on the [GPT-5.4 page](https://developers.openai.com/api/docs/models/gpt-5.4). |
| GPT-6 Astra | [OpenAI model page](https://developers.openai.com/api/docs/models/gpt-6-astra) | `gpt-6-astra`; Codex and API-gateway access routes remain distinct. |
| Claude Sonnet 4.5 | [Anthropic release](https://www.anthropic.com/news/claude-sonnet-4-5) and [model IDs](https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions) | Request alias `claude-sonnet-4-5`; response ID `claude-sonnet-4-5-20250929`. |
| DeepSeek-V4-Pro | [DeepSeek release](https://api-docs.deepseek.com/news/news260813/) and [API documentation](https://api-docs.deepseek.com/quick_start/pricing/) | `deepseek-v4-pro`; retain the separately recorded non-thinking and thinking configurations. |
| Kimi K2.6 | [Kimi API guide](https://platform.kimi.com/docs/guide/kimi-k2-6-quickstart) | `kimi-k2.6`; retain the recorded non-thinking setting. |
| Grok 4.6 (high) | [xAI model documentation](https://docs.x.ai/developers/models/grok-4.6) and [Cursor model documentation](https://prod.cursor.com/docs/models/grok-4-6) | Model ID `grok-4.6`; high reasoning effort. The study used Cursor. |

The human reference combines independently coded and adjudicated calibration sentences with collaboratively coded and reviewed challenge sentences. Humans determined its final labels. Separate model-generated Silver labels provide supervision and Silver-target evaluation; the independently blinded three-coder sample measures handbook agreement and is not a model test set.

## API access

GPT-5.6 Terra and Claude Sonnet 4.5 comparison baselines used third-party API gateways because of access constraints. Their upstream model identities were not independently verified against vendor APIs. The authors report qualitatively similar outputs in informal manual comparisons with the vendors' web interfaces; these checks do not establish model identity or controlled equivalence. Official APIs are recommended for replication where available. Adopted Silver labels were generated through official Codex with the recorded GPT-6 Astra selection. A separate API-gateway route reporting `gpt-6-astra` supplied labels for supplementary Qwen/JobBERT training comparisons and retains the historical name `proxy` in archived files.

## Naming rules

- Introduce full model names once; use the short names consistently in narrative, tables and chart legends.

- Preserve model versions and modes in configuration documentation. A short display name does not authorize changing an API request or checkpoint.

- Keep the primary data, frozen metadata, source IDs, experiment keys and public model URLs unchanged. Prefer readable documentation links and aliases over renaming these files.

- Use the full model display names in comparison tables and chart legends, with inference modes where relevant. Model IDs and access routes are listed separately in the model table and configuration documentation.

- The Dual15 export supports independent submissions within the QA100 review design; it does not establish blind raw-text coding.

- Existing historical notes may use canonical identifiers; preserve those records and link to this guide instead of mass replacement.

The CSV mapping is in `reproduction/paper_names.csv`. The containing Git commit identifies this documentation version.

</details>

