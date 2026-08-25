# Fill later — missing LLM IDs on hybrid 2601

Old dumps already scored (`python scripts/eval_hybrid_llm_old_dumps.py`). No API in that pass.

| Model | miss | domain | in SimHuman 980 |
|---|---:|---|---:|
| Claude | 98 | 人工智能招聘 98 | 45 |
| Kimi | 293 | 人工智能 246 + 阿里云 47 | 160 |

ChatGPT / DeepSeek / Qwen: miss = 0.

Files:

- `missing_ids_Claude.txt` / `missing_ids_Kimi.txt` — one ID per line
- `missing_queue_Claude.jsonl` / `missing_queue_Kimi.jsonl` — `id`, `sentence`, `source_domain`, `title`, `hybrid_source`, `in_simhuman980`

Do not overwrite `reports/views/*_unique_first_v2.jsonl`. Merge fills into a new view, then re-score.
