# Llama-3-8B-Instruct SOP-v4 P2 error summary

Run `llama3_8b_instruct_sopv4_p2_2601`.

| Kind | Count |
|---|---:|
| boundary_only_errors | 285 |
| empty_sentence_false_positives | 249 |
| false_positives_other | 725 |
| invalid_or_truncated_word_fragments | 60 |
| missed_entities | 3248 |
| overlong_spans | 15 |
| parser_failures | 324 |
| type_errors | 512 |

P2-980 is SimHuman SOP overlay, **not** human-validated Gold.
Do not compare P2 F1 with ChatGPT 0.6365 on Gold v2.
confirmed-results.md not updated in this run.
