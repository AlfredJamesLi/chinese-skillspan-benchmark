# Qwen2.5-14B-Instruct SOP-v4 P2 error summary

Run `qwen25_14b_instruct_sopv4_p2_2601`.

| Kind | Count |
|---|---:|
| boundary_only_errors | 930 |
| empty_sentence_false_positives | 47 |
| false_positives_other | 975 |
| invalid_or_truncated_word_fragments | 133 |
| missed_entities | 2408 |
| overlong_spans | 35 |
| parser_failures | 4 |
| type_errors | 353 |

P2-980 is SimHuman SOP overlay, **not** human-validated Gold.
Do not compare P2 F1 with ChatGPT 0.6365 on Gold v2.
confirmed-results.md not updated in this run.
