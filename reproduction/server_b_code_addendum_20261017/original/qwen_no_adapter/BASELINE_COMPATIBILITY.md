# Baseline compatibility (Qwen 0.3612)

Group 1 is the existing Gold150 shared-guidelines run. **Reuse; do not re-infer.**

## Location

`Chinese_skill_benchmark_Paper/output/gold150_shared_prompt_rev2_run_20260910/runs/qwen25-14b-instruct/`

| Check | Result |
|---|---|
| n | 150 / 150, intersection of shards 0 |
| adapter | `null` in both worker fingerprints |
| model path | `/home/guojingli3/SCESC-LLM-skill-extraction/Qwen2.5-14B-Instruct` |
| system / user / parser SHA | match frozen patch1 |
| do_sample | false |
| max_new_tokens | 2048 |
| dtype | bfloat16 |
| framework | transformers `generate`, chat template |
| host | DS209213, Slurm 50966/50967 |
| outcomes | ok_nonempty 69, partial_rejected 69, ok_empty 11, all_spans_rejected 1 |
| typed exact F1 | 0.3611650485436893 → written 0.3612 **待验证** |
| scorer | cnss-lskt-1.2.0 |

Scores: `SCORE_PARTIAL.json` row `qwen25-14b-instruct`; `scores/score_qwen25-14b-instruct.json`.

## Pairing

SFT inference scripts use the same system, user template, payload, parser, `do_sample=false`, `max_new_tokens=2048`, Gold150 order, and scorer. The only intended load difference is the new LoRA.

Disk `generation_config.json` has `do_sample: true`. Baseline overrode it; SFT scripts do the same.

## Not a paired row

- Historical SOP extract 0.1724
- Old JSON-offset SFT Gold150 ~0.1215
- JobBERT 0.4331

Do not subtract those from 0.3612.
