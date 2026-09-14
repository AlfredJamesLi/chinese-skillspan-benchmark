# Chinese-SkillSpan — Codex pack for gpt-6-astra (5,436 remaining Silver sentences)

Private working pack. **Not** a public data release. Job-ad text is licensed for academic research, not CC-BY. Do not fork public.

This is **7,936 − 2,500 = 5,436** new Silver sentences. The local 2,500 IDs are in `ids_held_2500.txt` and must **not** be labeled again.

## Clone

```bash
gh repo clone AlfredJamesLi/cnss-silver-codex-astra-5436
cd cnss-silver-codex-astra-5436
```

## Label (one wave per Codex session)

Model: **gpt-6-astra**. System prompt: `PROMPT_silver_public_api_v1.0.txt`. User message: one `batches/batch_XXXX.json`. Write JSON to `batches_out/batch_XXXX.json`. Max 10 records per call.

| Wave | Sentences | Batches | Codex prompt |
|------|----------:|--------:|----------------|
| 1 | 1,810 | 0001–0181 | `waves/wave1/CODEX_PROMPT.md` |
| 2 | 1,810 | 0182–0362 | `waves/wave2/CODEX_PROMPT.md` |
| 3 | 1,816 | 0363–0544 | `waves/wave3/CODEX_PROMPT.md` |

Start with **wave1**. Do not start wave2 until wave1 `batches_out/` has 181 JSON files.

API: `POST https://claudeed.ysaikeji.cn/v1/chat/completions` with `~/.config/ysaikeji/api_key`. Do not commit the key.

## After a wave

```bash
git add waves/wave1/batches_out
git commit -m "wave1 Astra labels"
git push
```

Server merge (after all three waves):

```bash
python3 scripts/sync_codex_wave_outputs.py
python3 scripts/merge_codex_remaining_silver.py
```

(Those scripts live in the paper repo, not this pack.)

Do not edit Gold150, V4 hybrid, or v6a. Do not write paper F1.
