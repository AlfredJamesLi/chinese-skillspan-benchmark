# JobBERTa-zh 3.2M follow-up (internal)

Not paper numbers. Do not copy into the PDF or `confirmed-results.md`.

3.2M is queued as Slurm `jbzh_3m` (CPU wait, no GPU) until the 1M setsid runner exits, then it picks free cards. The old `wait_1m_then_3m.sh` setsid launcher was stopped to avoid a double start.

After the 1M mid-rung CRF finishes, the Slurm job scores Gold v2 and:

- **1M above vanilla v3:** continue DAPT from the 1M encoder on 3.2M sentences × 2 epochs (Zhang sentence scale, less wall time).
- **1M flat:** 3.2M × 3 epochs from `chinese-roberta-wwm-ext` (the 80k demo was also flat; this is the real scale test).
- **1M clearly worse:** keep the 3.2M corpus, do not launch.

Mix stays corpus-train 59:41. Leak filter is train/dev/test/Gold. Standard token MLM (HF WWM cannot batch this tokenizer).
