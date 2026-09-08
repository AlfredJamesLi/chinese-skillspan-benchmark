# 已替代：KNN / 随机示例对照

2026-09-08 用户方案明确：本版本替代此前包含 KNN 和随机示例对照的草案；本轮 Qwen 只做 SFT。

作业 7349 启动时仍按旧脚本建了 `knn_index/`（约 1908 条训练独特文本）。该索引：

- 不进入本轮正式 Gold 评测；
- 不用于选模、提示或参数；
- 保留在磁盘，不覆盖、不删除既有文件。

`infer_qwen_ext_abc.py` 现为兼容包装：只跑 SFT。若旧 bash 循环仍评分 `pred_B` / `pred_C`，那些文件是 SFT 副本，**不是**正式结果。`collect_extension_results.py` 只收 SFT。
