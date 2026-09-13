# Former Table 15

Instruction, demonstration and cleaning sensitivities; archive favorable and unfavorable outcomes together.

Transferred from `tex/appendix_C_experiments_R16.tex`, label `tab:appendix-e-p1`. Exact LaTeX is retained alongside these readable tables. Values are copied from the current manuscript; no computation or new experiment was performed.

## Block 1

| Condition | Exact F1 | Relaxed F1 |
| --- | --- | --- |
| P0, reused | 0.1215±0.0092 | 0.4459±0.0237 |
| P1, no demonstrations (k=0) | 0.1455±0.0196 | 0.4905±0.0109 |
| P1, random demonstrations (k=3) | 0.0452±0.0067 | 0.3507±0.0085 |
| P1, nearest-neighbor demonstrations (k=3) | 0.0315±0.0047 | 0.3491±0.0122 |

## Block 2

| Condition | Designated result | Cleaning rerun |
| --- | --- | --- |
| JobBERT B2 | 0.5536±0.0054 | 0.5509±0.0054 |
| JobBERT B1 | 0.1422±0.0138 | 0.1507±0.0062 |
| Qwen P0 | 0.1215±0.0092 | 0.1071±0.0102 |
| Non-conflict-origin (E) | 0.4345±0.0235 | 0.4355±0.0250 |
