# Overleaf — methods sentences (English)

Isolation after v4: **sentence-level isolation (extended)**. Do not write “document isolation” for v4–v6a.

Two students are not one recipe:

- **JobBERT-zh 3M (Gold150 main).** No prompt. Character BIO + CRF. v3–v6a load the released `crf/best.pt`. AdamW $2\times10^{-5}$, weight decay 0.01, batch 16, at most 6 epochs, patience 2, 10% warmup. Checkpoint = argmax frozen-dev typed exact. Independence of that CRF is unproven (original `history.json` missing).
- **Qwen2.5-14B (Gold150 supplement, official P0).** Short JSON-offset instruction in the user message; no demonstrations. LoRA $r=16$, $\alpha=32$, q/k/v/o, lr $1\times10^{-4}$, batch $1\times16$, 6 epochs, `do_sample=false`, `max_new_tokens=256`, assistant-only loss. This is **not** official SOP extract 0.1724. Frozen Instruct + the same JSON prompt without LoRA is Gold150 exact 0.0000.
- **Qwen2.5-14B shared-handbook SFT (laboratory; not Table C).** Same base model and LoRA budget, but the frozen shared guidelines (occurrence schema, `max_new_tokens=2048`) replace the short JSON-offset prompt. Gold150 typed exact **0.5403±0.0354**. This is **not** JSON-offset 0.1215, not SOP extract 0.1724, and must not replace Table C or be ranked with JobBERT v6a 0.5536. Adapters are not in the public release.

B1/B2 = same sentences, different labels (old SOP-style vs Silver-plus teacher), not two prompts.

Allowed wording for the volume contrast: the observed B2-versus-B1 difference on v3 (+0.391 typed exact) is larger than the B2 change from 1,382 to 2,156 training sentences (+0.024). Do **not** write “label quality far exceeds data size”.

**P1 (appendix only).** Same LoRA budget and `v6a_nocross` list; only the instruction changes (system role + JSON-wrapped sentence). Select on frozen-dev $k=0$. Same checkpoint decoded at $k=0$, random $k=3$, and $k$NN $k=3$. Gold150 is not used for gradients, neighbours, or selection.

**Watermark peel (appendix only).** About 1% of Silver-plus train sentences carry `macrodatas.cn` / 马克数据网. Gold150 has none. A new 2,138 / 168 list was stripped and retrained; official v6a and v6a_nocross files were not overwritten.

**Public-API silver (appendix Table H only).** Additional Qwen occurrence LoRA baselines on later silver subsets (Wave3 proxy vs Codex; Wave1+2; 7,117-sentence keep set; pooled keep with unique v6a_nocross). Seed 42. Proxy-run2500 pool (\(n_{\mathrm{keep}}=9{,}646\); train 8,943) is Gold150 exact 0.5966 (relaxed 0.7126). Codex-run2500 pool (\(n_{\mathrm{keep}}=9{,}540\); train 8,842) is Gold150 exact 0.5854 (relaxed 0.7032). These do **not** replace Table C 0.1215 or JobBERT v6a 0.5536. Do not write 10,000. Not GPT distillation.
