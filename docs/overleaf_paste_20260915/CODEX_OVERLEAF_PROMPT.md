# Codex prompt — edit the PeerJ CS Overleaf project (2026-09-15 night)

Copy everything below the line into **one** Codex message. Codex should edit the Overleaf project only. Do not invent F1. Do not git-push silver jsonl.

---

You are editing the PeerJ Computer Science Overleaf project for Chinese-SkillSpan.

## Goal

Insert **appendix Table H** and a short Methods paragraph for public-API / pooled silver **baselines**. Do **not** change Abstract Results or Tables A–D cells. Do **not** write “10,000”. Do **not** call this GPT distillation, dual-teacher, or teacher–student distillation. These are extra benchmark baselines with two silver **annotation protocols**.

## Frozen (do not rewrite)

| Location | Keep exactly |
|---|---|
| Table A JobBERT 3M hybrid 2601 | 0.4331 |
| Table B JobBERT v6a B2 Gold150 | 0.5536±0.0054 |
| Table C Qwen JSON-offset P0 Gold150 | 0.1215±0.0092 |
| SOP extract (no LoRA) | 0.1724 |
| Shared-handbook LoRA (Methods / Table C footnote only) | 0.5403±0.0354 as a **different protocol**, not a Table C replacement |
| DAS corpus snapshot | Zenodo v0.1.1 `10.5281/zenodo.22288338` |
| Gold150 / v6a_nocross | Zenodo v0.1.3 `10.5281/zenodo.22698504` |
| Gold150 | 150-sentence human overlay; not a 500-sentence test; SHA-256 starts `ca8db0bc` |
| Isolation | sentence-level (extended) |

## Numbers that MAY be added (appendix / Methods only)

All of these are **Gold150** typed F1 (`cnss-lskt-1.2.0`), seed 42 unless a ±SD is shown. They are **not** silver-dev / silver-test.

| Row | n_train | Channel | Exact | Relaxed |
|---|---:|---|---:|---:|
| Wave3 only | 1678 | website proxy | 0.5870 | 0.7169 |
| Wave3 only | 1579 | Codex CLI | 0.5853 | 0.6991 |
| Wave1+2 only | 3159 | Codex CLI | 0.5745 | 0.6951 |
| Public-API keep, full-dev select | 7117 | mixed | 0.5883 | 0.7099 |
| Public-API keep, TVT | 7117 | mixed | 0.5732 | 0.7087 |
| Pooled keep (v6a unique + public-API) | 8943 | two protocols | **0.5966** | **0.7126** |

Footnote only (do not put in Table B):

- JobBERT-zh 3M CRF on 7,117 public-API keep: Gold150 exact **0.2367±0.0015** (seeds 42/43/44).
- JobBERT-zh 3M CRF on pooled train 8,943: Gold150 exact **0.2416** (seed 42).

Pooled inventory (Methods, not the Abstract): \(n_{\mathrm{keep}}=9{,}646\); train/val/test \(8{,}943/351/352\). Public-API labelled 7,936; keep 7,676 after `adjudication_required` (7,117 / 559). Protocol names: `silver_public_api_v1.0` and v6a_nocross B2 (handbook v4212). Qwen pooled checkpoint = epoch 1, patience 2, Gold150 unused for gradients or selection.

## Do NOT paste (forbidden)

- “10,000”, “1万”, “dual teacher”, “双老师”, “GPT distillation”, “human cover 500”
- Silver-val **0.7826** or silver-test **0.7585** (same protocol as training; not Gold150)
- A SOTA sentence that ranks 0.5536 / 0.5403 / 0.4331 / 0.1215 / 0.5966 together
- Any F1 for Codex run2500 (labels have not arrived)
- `notes/confirmed-results.md` edits, new silver jsonl, adapters, WAVE3 dumps

## Concrete Overleaf edits

1. **Data Availability:** keep v0.1.1 for the 22,840 corpus; state that Gold150 and v6a_nocross are in Zenodo **v0.1.3**. Do not say Gold150 is inside v0.1.1.
2. **Tables A–D:** no cell changes. Table C footnote may already mention 0.5403 as a different protocol — leave that.
3. **After Tables E–G**, insert Table H using this caption and body (LaTeX):

```latex
\begin{table}[t]
\caption{Gold150 typed F1 for additional Qwen2.5-14B occurrence LoRA baselines on public-API silver subsets (seed 42). Official Table~\ref{tab:gold150-qwen} remains JSON-offset $0.1215\pm0.0092$. JobBERT v6a B2 remains $0.5536\pm0.0054$. These rows are not GPT distillation.}
\label{tab:public-api-silver-qwen}
\centering
\begin{tabular}{lcccc}
\hline
Silver subset & $n_{\mathrm{train}}$ & Channel & Exact & Relaxed \\
\hline
Wave3 only & 1678 & website proxy & 0.5870 & 0.7169 \\
Wave3 only & 1579 & Codex CLI & 0.5853 & 0.6991 \\
Wave1+2 only & 3159 & Codex CLI & 0.5745 & 0.6951 \\
Public-API keep, full-dev select & 7117 & mixed channel & 0.5883 & 0.7099 \\
Public-API keep, TVT & 7117 & mixed channel & 0.5732 & 0.7087 \\
Pooled keep (v6a unique + public-API) & 8943 & two protocols & 0.5966 & 0.7126 \\
\hline
\end{tabular}

\vspace{0.4em}
{\small Protocol: frozen shared handbook, occurrence schema, $k{=}0$. Gold150 was not used for gradients or selection.
Wave3 Codex vs proxy is a labelling-channel contrast on the same 1,816 IDs, not a new test set.
Public-API keep $N{=}7{,}676$ after dropping \texttt{adjudication\_required} (7,117 / 559).
The pooled baseline concatenates unique v6a\_nocross B2 with that keep set ($n_{\mathrm{keep}}{=}9{,}646$; train/val/test $8{,}943/351/352$). Do not write ``10,000''. Codex relabel of the 2,500-sentence subset is pending.
JobBERT-zh 3M CRF on 7,117 is Gold150 exact $0.2367\pm0.0015$ (seeds 42/43/44); on the pooled 8,943-sentence train it is $0.2416$ (seed 42). Neither replaces Table~\ref{tab:gold150-jobbert}.}
\end{table}
```

4. **Methods (one paragraph after the shared-handbook sentence):**

> An additional silver pool used protocol `silver_public_api_v1.0` (7,936 sentences; 7,676 keep after holding out `adjudication_required`). Wave1–2 and the reported Wave3 contrast used Codex CLI; a 2,500-sentence subset still uses website-proxy labels until a Codex relabel arrives. Isolation is sentence-level. A further pooled baseline concatenates unique v6a_nocross B2 sentences with that keep set (\(n_{\mathrm{keep}}=9{,}646\); train 8,943). The two silver protocols are training annotations for a benchmark baseline, not a distillation setup. Qwen2.5-14B occurrence LoRA on this pool is Gold150 typed exact 0.5966 (relaxed 0.7126; seed 42). This pool does not replace the v6a_nocross 2,150 / 169 JobBERT cell.

5. **Limitations (one sentence):** Public-API / pooled rows are seed-42 extra baselines; they do not replace Table B or Table C. Codex 2500 is pending.

6. **Abstract:** do not add 0.5966, 0.5883, 0.5870, or 9,646 to Results.

7. Compile. If a label is missing (`tab:gold150-qwen` / `tab:gold150-jobbert`), keep the `\ref` and do not invent a new Table B/C number.

## Done when

- Table H appears after E–G with the six Qwen rows above.
- Abstract Results still end at 0.1215±0.0092.
- PDF does not contain “10,000” or 0.7826.
- DAS mentions v0.1.3 for Gold150.

Stop. Do not start a Codex-2500 F1. Do not upload adapters.
