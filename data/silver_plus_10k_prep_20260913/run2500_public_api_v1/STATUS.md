# Public-API Silver 2500 + JobBERT student

Date: 2026-09-13.

- Prompt: `silver_public_api_v1.0` (`Chinese_skill_benchmark_Paper/silver_prompt.txt`)
- Model: `gpt-6-astra` via `https://claudeed.ysaikeji.cn`
- n = **2500 sentences** (Hamilton 1000/750/750), **250** HTTP batches of 10
- Caller: `scripts/run_silver_public_api.py` (resume, offset repair, per-record fallback)
- After labels: JobBERT-zh 3M CRF, freeze encoder, continue V4 `crf/best.pt`, seeds 42/43/44, score Gold150
- Reference cell (do not overwrite): v6a B2 **0.5536±0.0054**
- This run uses **new** sentences + new teacher. It cannot bit-reproduce 0.5536.
- Do **not** write the new F1 into `confirmed-results.md` until the author confirms.
- Does not rewrite Gold150 / V4 hybrid / v6a files / paper counts.
