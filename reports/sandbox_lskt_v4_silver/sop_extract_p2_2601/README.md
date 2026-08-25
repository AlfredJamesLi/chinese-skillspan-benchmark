# SOP extract v4 — P2 2601 API runs

Prompt = `PROMPT_gpt4o_sop_extract.txt` (id + sentence, **no silver**, no Gold).
Scorer after coverage: jieba snap vs `test_lskt_v4_cws_simhuman980_hybrid.jsonl`.
Do not write `confirmed-results.md` until the coverage gate passes.

| Model | Prior work | This run |
|---|---|---|
| `gpt-5.4` | 100 SOP extract (same prompt) | resume remaining **2501** |
| `claude-sonnet-4-6` | 980 **silver-correct** (`human980_pack/sonnet46_round1`, silver in prompt) | **not reused**. SOP extract on all **2601** from scratch |
| `claude-sonnet-4-5` | none on this prompt | SOP extract all **2601**; proxy upstream `claude-sonnet-4-5-20250929` |
| `kimi-k2.6` | Codex 52-batch / dump-fill used k2.6 with **silver in payload** | **not reused**. SOP extract all **2601** on official Moonshot, thinking disabled |
| `deepseek-v4-pro` | 46 SOP extract (same prompt) but `reasoning_effort=high` + thinking | **not seeded**. Full 2601 uses a uniform decode; n=46 stays a pilot |

The 980 sonnet job is a Doccano prelabel pack, not a P2 LLM baseline.
