# Server B MaChAmp / emit supplement (2026-10-17)

Original-byte copies from DS210039. `cp -a`; not rewritten. No weights,
MacroData, or full upstream MaChAmp tree.

## Answer to Codex

The previous addendum ZIP already contained
`native_patches/patches/machamp_sampler_torch214.patch`. That file is
**truncated at the source on B** (40 lines, 1763 bytes, SHA-256
`cec941c74bc2677b6fdb6190712de5f1b1bb239563eba5a26d3aefeb10d6afec`).
A complete unified-diff `.patch` was **本次未找到**. Do not invent one.

What exists and is packed here:

| File in this pack | Live path on B | SHA-256 |
|---|---|---|
| `scripts/emit_verified_results.py` | `/home/guojingli3/cnss_external_benchmarks_20260921/scripts/emit_verified_results.py` | `f5e1e9f475d9e445c0170762ffe121f3882e97f965e6ceb63a8e52b2f135cbe2` |
| `audit_and_lexicon.py` | `/home/guojingli3/cnss_external_benchmarks_20260921/audit_and_lexicon.py` | `da2cb34f1d81c8b8d8991843b0784f4b4912df447169452f1b4197c18e4c122f` |
| `executed_skillspan_machamp/machamp/data/machamp_sampler.py` | `…/upstream_full/SkillSpan/machamp/machamp/data/machamp_sampler.py` | `2ab043a9d8d28325e0810d15a2bddd27c3b39a2655563d3791b3fdd3482057ae` |
| `executed_skillspan_machamp/machamp/model/trainer.py` | `…/upstream_full/SkillSpan/machamp/machamp/model/trainer.py` | `0af6cacb491765f126be54924edbad43b963029dbef0fbf1441bc063791965a8` |
| `executed_skillspan_machamp/predict.py` | `…/upstream_full/SkillSpan/machamp/predict.py` | `8813af2f308b0f4b5d2e4e359daf5f41c25b3436609ad335cd351b214a2daf8d` |

`emit_verified_results.py` is the native-track summary script called by
`finish_today_2gpu.sbatch` and `gnehm_esco_2gpu.sbatch`. It imports
`audit_and_lexicon` from the tree root (packed as a local dependency).

The executed SkillSpan `machamp_sampler.py` is the complete file the
truncated `.patch` was trying to describe (`super().__init__()` for
torch 2.14). `trainer.py` / `predict.py` contain the
`torch.load(..., weights_only=False)` edits. No separate
`weights_only.patch` was found.

Byte identity with the full upstream MaChAmp checkout is not claimed
beyond these copied files. ESCOXLM-R tree sampler still has
`super().__init__(data_source)` and is not this patch target.
