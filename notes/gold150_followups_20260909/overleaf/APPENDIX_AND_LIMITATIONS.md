# Overleaf — appendix + limitations (English paste)

## Methods (add after the Qwen P0 paragraph)

A later prompt contrast (P1) kept the same LoRA budget and the same `v6a_nocross` 2,150 / 169 list. The only intended change was the instruction (a system role plus a JSON-wrapped sentence). Checkpoint selection used frozen-dev typed exact at $k=0$. The same checkpoint was then decoded at $k=0$, with three random lessons, and with three $k$NN lessons from a train-only index. Gold150 was not used for gradients, neighbours, or selection.

About 1% of Silver-plus training sentences carry a crawler watermark (`macrodatas.cn` / 马克数据网). Gold150 has none. We stripped those tails into a **new** 2,138 / 168 list and retrained; we did **not** edit the official v6a or v6a_nocross files.

## Limitations (add)

The P1 $k=0$ mean on Gold150 is 0.1455±0.0196 versus official P0 0.1215±0.0092. The sample SDs overlap; seed 42 is not higher than that seed’s P0. Adding three demonstrations collapsed exact F1 to 0.03–0.05 while relaxed stayed near 0.35, so the gap remains boundary / localisation. P1 does not replace Table C.

Frozen SOP-extract outputs already exist for the 150 Gold IDs (they sit inside hybrid 2,601). Rescoring them on Gold150 gold gives teacher exact F1 around 0.30–0.32. That is a new gold, not a new API call, and it is not comparable to the JobBERT student 0.5536.

Stripping the watermark and retraining did not raise the official cells (JobBERT B2 0.5509±0.0054; Qwen P0 0.1071±0.0102). The cleaned list also dropped empty-ad rows and five punctuation NFC collisions, so this is not a pure watermark ablation.

## Abstract Conclusions (optional extra sentence; do not add numbers to Results)

Encoder continuation is insensitive to the rare crawler watermark in this expansion. JSON-offset LoRA remains localisation-limited: a longer prompt does not justify replacing the official P0 row, and in-context demonstrations hurt exact span F1.
