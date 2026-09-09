# P1 最小对照（不改写正式 P0）

正式 Table C / P0 仍是 **0.1215±0.0092**（`EXTENSION_RESULTS.json` 复用，本轮未重训）。
本文件只报告 P1-SFT 同 checkpoint 的 k=0 / 随机 k=3 / KNN k=3。
不得与 JobBERT 0.4331 或 Qwen SOP 0.1724 混排。样本 SD 不是检验 CI。

## 复用的正式 P0
- Gold150 exact mean = 0.1215
- sample SD = 0.0092

## P1 汇总
- P1_k0|dev: 0.1545±0.0119 (n=3)
- P1_random|dev: 0.0543±0.0154 (n=3)
- P1_knn|dev: 0.0636±0.0108 (n=3)
- P1_k0|gold: 0.1455±0.0196 (n=3)
- P1_random|gold: 0.0452±0.0067 (n=3)
- P1_knn|gold: 0.0315±0.0047 (n=3)
