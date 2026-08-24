# Train human Gold-style pack: 80 locked + 300 todo

Replace rule v3 on these 380 rows with human Gold-length labels.  
Does **not** overwrite `train.json` or Gold v2.

| set | n | status |
|---|---:|---|
| `sample80_final.json` | 80 | locked (71 accept / 9 edit) |
| `reports/iaa300/` | 300 | train-only worksheet; dual IAA not started |
| `train_human_80_300/` | 380 | combined pack |

Label with `guidelines.md` (Gold-length NP, empty-sentence lock).  
`empty_hint` is a hint, not a label.

When the 300 are human-final, merge into a **new** train file (e.g. `data/train_goldstyle_human380.jsonl`). Keep v3 for the remaining rows until more human labels exist.

阿里云 / 事业单位正文进 DAPT：以后另做，不在本包。
