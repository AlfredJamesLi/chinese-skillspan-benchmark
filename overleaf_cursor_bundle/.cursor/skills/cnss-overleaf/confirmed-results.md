# Confirmed results (Overleaf compact copy)

Synced from server `Chinese_skill_benchmark_Paper/` on **2026-08-25**.
Scorer: `cnss-lskt-1.2.0`. Do not invent cells. Round to **4 decimals** in tex.

**Two protocols — do not mix them in one table without a caption:**

| Protocol | Gold | n | Use in Overleaf |
|---|---|---:|---|
| **PDF Table 3** (keep) | `admin_Baseline_test.jsonl` | 2676 | Existing main table paper S-F1; do **not** overwrite these cells |
| **Gold v2 unique-first** (add) | `gold_canonical_v2.jsonl` | 2601 unique IDs | New tables: typed exact / collapsed / relaxed / per-domain / encoder |

CSV copies live in `tables/` of this bundle (and server `Chinese_skill_benchmark_Paper/tables/`).

---

## Identity

- Paper: Chinese-SkillSpan / Chinese Skill Benchmark
- Filename venue: DASFAA 2026; protocol note also targets PeerJ CS
- Task: Chinese JobSkillNER, ESCO-1.20 **LSKT** (L/K/S/T) **span** extraction
- Wording: “ESCO-derived LSKT span extraction”, **not** ESCO concept-ID linking

## Table 1 — corpus (PDF; keep)

| Split | #Sent | Avg Len | Avg 4D | Avg L | Avg K | Avg S | Avg T |
|---|---:|---:|---:|---:|---:|---:|---:|
| train | 17460 | 37.41 | 2.354 | 0.019 | 0.639 | 1.183 | 0.513 |
| dev | 2143 | 40.37 | 3.607 | 0.016 | 1.276 | 1.810 | 0.504 |
| test | 3237 | 43.85 | 2.306 | 0.010 | 0.822 | 1.141 | 0.332 |

Distinguish: corpus test **3237**; raw Gold rows **2676**; canonical unique Gold **2601**.

## Table 2 — IAA (PDF, n=100; keep)

| Metric | P | R | F1 / κ |
|---|---:|---:|---:|
| Strict exact span | 0.707 | 0.426 | 0.532 |
| Relaxed overlap | 0.829 | 0.500 | 0.624 |
| Token Cohen’s κ | — | — | 0.554 |

## Table 3 — PDF strict S-F1 (keep these paper cells)

| Model | Paper S-F1 | Repo typed (2676) | Repo collapsed (2676) | Status |
|---|---:|---:|---:|---|
| ChatGPT | 0.6700 | 0.6836 | **0.6703** | Match (collapsed) |
| Claude | 0.6300 | 0.5712 | 0.6062 | Dump incomplete |
| Kimi | 0.5700 | 0.5310 | 0.5618 | Dump incomplete |
| DeepSeek | 0.5130 | **0.5149** | 0.5479 | Match (typed) |
| Qwen | 0.2130 | 0.3442 | 0.3949 | Gap vs paper |
| JobBERT-skill | 0.0045 | — | **0.0045** | Match |
| JobBERT-knowledge | 0.0038 | — | **0.0038** | Match |

Do **not** retune Qwen toward 0.2130. Do **not** cite `*.eval_ner.json` (~0.004).

---

## NEW — Gold v2 unique-first (add a table; 2601 IDs)

Primary metric: **typed exact micro F1**. Relaxed: IoU≥0.5.

| Model | Paper S-F1 | typed exact | collapsed exact | typed relaxed | Align |
|---|---:|---:|---:|---:|---|
| ChatGPT | 0.6700 | 0.6365 | 0.6403 | **0.7221** | OK |
| DeepSeek | 0.5130 | 0.1327 | 0.3569 | 0.1798 | OK |
| Qwen | 0.2130 | 0.0791 | 0.1075 | 0.1272 | OK |
| JobBERT-skill | 0.0045 | 0.0000 | 0.0045 | 0.0000 | OK |
| JobBERT-knowledge | 0.0038 | 0.0000 | 0.0037 | 0.0000 | OK |
| Claude | 0.6300 | 0.2570 | 0.2952 | 0.3789* | Missing 98 IDs |
| Kimi | 0.5700 | 0.1651 | 0.3349 | 0.2130* | Missing 293 IDs |

\* Claude/Kimi relaxed treats missing Gold IDs as empty predictions. **Not eligible** for a complete main-table row until dumps are filled.

Caption must say Gold v2, unique-first, `cnss-lskt-1.2.0`.

## NEW — Per-domain typed exact F1 (Industry-OOD **proxy**)

Gold v2 domains: 人工智能招聘 1407 / 事业单位招聘 737 / 阿里云公开数据集 457.  
**No `year` field → do not claim Time-OOD.** This is domain breakdown, not a held-out industry split.

| System | 人工智能 | 阿里云 | 事业单位 |
|---|---:|---:|---:|
| ChatGPT | 0.6489 | 0.5650 | **0.7032** |
| DeepSeek | 0.1392 | 0.1293 | 0.0805 |
| Qwen | 0.0887 | 0.0646 | 0.0207 |
| JobBERT 3M ckpt65000 | **0.1323** | 0.1259 | 0.0150 |
| JobBERT 1M | 0.1287 | 0.1332 | 0.0181 |
| listed mix 1M | 0.1282 | 0.1240 | 0.0153 |
| domain-mix 1M (seed 42) | 0.1276 | **0.1372** | 0.0287 |
| RoBERTa-wwm v3 | 0.1242 | 0.1191 | 0.0115 |

Claim allowed: encoder **fails on 事业单位** (~0.015–0.029) vs ~0.13 on 人工智能/阿里云; ChatGPT is strongest on 事业单位 (0.7032). Domain-mix seed 42 is 0.0287 on 事业单位; still a failure mode.

## NEW — Encoder CRF ranking (Gold v2 typed exact; seed 42)

| Run | test F1 | dev F1 | vs 0.1224 |
|---|---:|---:|---|
| domain-mix 1M (seed 42) | **0.1234** | 0.3190 | +0.0010 |
| JobBERT 3M ckpt65000 | 0.1233 | 0.3205 | +0.0009 |
| JobBERT 1M + goldstyle v3 | **0.1224** | 0.3185 | baseline |
| human380 + v3 merge | 0.1207 | 0.3163 | −0.0017 |
| listed mix 1M | 0.1201 | 0.3257 | −0.0023 |
| JobBERT 3M final encoder | 0.1170 | 0.3209 | −0.0054 |
| JobBERT 3M ckpt100k | 0.1167 | 0.3207 | −0.0057 |
| JobBERT demo 80k | 0.1152 | 0.3231 | −0.0072 |
| RoBERTa-wwm goldstyle v3 | 0.1156 | 0.3210 | −0.0068 |

Encoder is a **weak baseline** (~0.12), not competitive with ChatGPT (0.6365 typed). listed mix 1M **lost**; **do not** add a listed-3M row. Domain-mix seed 42 is +0.0010 vs 1M.

## NEW — Encoder 3-seed typed exact (Gold v2; `cnss-lskt-1.2.0`)

| Run | seed 42 | seed 123 | seed 2026 | mean | std |
|---|---:|---:|---:|---:|---:|
| JobBERT 1M | 0.1224 | 0.1292 | 0.1348 | **0.1288** | 0.0062 |
| domain-mix 1M | 0.1234 | 0.1280 | 0.1294 | 0.1269 | 0.0031 |
| JobBERT 3M ckpt65000 | 0.1233 | 0.1295 | 0.1246 | 0.1258 | 0.0033 |
| RoBERTa-wwm v3 | 0.1156 | — | — | — | — |

3-seed mean: domain-mix 0.1269 **below** JobBERT 1M 0.1288. Do not scale domain-mix to 3M.

## Diagnostic — LSKT v4 SOP / jieba CWS (appendix; not Table 3)

Authorized 2026-08-25. CSV: `tables/sop_v4_cws_diagnostic.csv`.  
**Do not** mix these rows into PDF Table 3, the Gold v2 unique-first LLM table, the encoder 3-seed ranking, or the abstract SOTA sentence. Caption must name train silver, decode, and test gold.

| Pred | Train silver | Decode | Test gold | typed exact | IoU≥0.5 |
|---|---|---|---|---:|---:|
| JobBERT 1M | goldstyle v3 | raw | Gold v2 | 0.1224 | — |
| JobBERT 1M | SOP v4 | raw | Gold v2 | 0.1079 | 0.3320 |
| JobBERT 3M | SOP v4 | raw | Gold v2 | 0.1104 | 0.3404 |
| JobBERT 1M | SOP v4 | jieba post-hoc | Gold v2 | 0.1454 | 0.3411 |
| JobBERT 3M | SOP v4 | jieba post-hoc | Gold v2 | 0.1479 | 0.3470 |
| JobBERT 1M | SOP v4 | raw | SOP rule silver | 0.3170 | 0.5663 |
| JobBERT 3M | SOP v4 | raw | SOP rule silver | 0.3229 | 0.5624 |
| JobBERT 1M | SOP v4 | jieba post-hoc | SOP rule silver | 0.2609 | 0.5835 |
| JobBERT 1M | SOP v4 | jieba post-hoc | SOP-CWS silver | 0.4278 | 0.5960 |
| JobBERT 3M | SOP v4 | jieba post-hoc | SOP-CWS silver | 0.4341 | 0.5884 |

Allowed: SOP v4 train **lowers** Gold v2 vs goldstyle v3 (0.1079/0.1104 vs 0.1224). Jieba post-hoc **raises** Gold v2 exact of the same v4 preds (0.1454/0.1479). 0.3170 and ~0.43 are SOP-silver agreement, not human Gold v2. CWS retrain still running — no finished F1.

## Running / not yet a paper number

| Item | Status |
|---|---|
| RoBERTa-wwm v3 3-seed mean | seed 123 running; seed 2026 not started |
| Concept Accuracy | **Blocked** — no ESCO concept IDs; delete the claim |
| Time-OOD | **Blocked** — no year field; delete the claim |
| Claude/Kimi dump fill | **Blocked** (API HTML); do not fake labels |

## Wording patches (protocol freeze)

- “ESCO-aligned concept extraction” → “ESCO-derived LSKT span extraction”
- Delete Concept Accuracy / Time-OOD / long-tail-improvement claims unless a confirmed table exists
- Industry-OOD: only as the per-domain **proxy** table above, with that caveat
