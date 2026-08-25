# Consultation prompt — LSKT definition, eval, and encoder F1 gap (Chinese-SkillSpan)

Paste the block below into **ChatGPT (o-series / GPT-5)** or **Codex**.  
Purpose: decide whether to redesign LSKT + operationalization, or keep Gold v2 and only change training/eval reporting.  
Do **not** invent F1; look up Zhang/SkillSpan numbers from papers.

This is the **Chinese-SkillSpan / Chinese Skill Benchmark** dataset paper, not IEEE Access / SRICL.

---

## PROMPT (copy from here)

You are a senior NLP dataset + evaluation reviewer (skill extraction / NER from job ads). I need a **decision memo**, not a rewrite of our paper.

### Who we are
We built **Chinese-SkillSpan**: span-level competency extraction from **Chinese job ads** using a flat 4-way scheme **LSKT** (L language / K knowledge / S skill / T trait), derived from ESCO-style competency types but **not** ESCO concept-ID linking. Venue target: **PeerJ Computer Science** (dataset paper). An older draft PDF filename still says DASFAA; ignore that as the target.

We are **not** asking you to import English six-corpus SRICL method results. Related work you **should** look up: Mike Zhang et al. **SkillSpan** (NAACL 2022), **JobBERT / JobBERTa** domain-adaptive MLM on job ads, Kompetencer, Green, FIJO, Sayfullina, Gnehm, Chinese resume/JD NER (e.g. character-level BIO, CLUENER-style), nested NER, and recent LLM-as-annotator papers (silver labels, model-in-the-loop gold).

### What we need you to decide
1. Is our **label definition + operationalization + metric** biased toward LLMs (especially GPT-4o), toward human–LLM agreement, or toward LLM–LLM agreement — at the expense of encoder/pretrained-model F1?
2. Given **Chinese** (no spaces; 事业单位招聘公告 vs 互联网 JD; character/token mismatch), should we **redesign LSKT** and the annotation SOP, or keep LSKT and change **eval / gold construction / train labels**?
3. Do we need a **new SOTA literature survey** before changing anything?
4. Is **encoder F1 ≥ 0.5** (or near Zhang JobBERT / mainstream skill-span encoder means) a **realistic target on the current Gold**, or only after a protocol change? Be explicit: which number is a dataset bug vs a model bug.

Cite papers with venue/year. If a number is uncertain, say so; do not average conflicting tables.

### Frozen facts from our server (do not “correct” these; treat as measurements)

**Gold construction (this is the load-bearing fact)**  
- Pipeline in our figure: Job postings → LLM silver (pilot GPT-4o, Claude-3.5, DeepSeek, Kimi; **ChatGPT chosen**) → human supervised consistency check in **Doccano** → Gold.  
- Doccano silver labels used prefixes like `SILVER_S` / `SILVER_T`. Converter strips `SILVER_`.  
- Timeline: GPT-4o test dump **2025-10-05** → Doccano silver merge **2025-10-06** → `admin_Baseline_test.jsonl` Gold **2025-10-16**.  
- On Gold v2 (2601 unique IDs): Doccano silver vs Gold **85.7% sentences identical**; span P/R ≈ **0.874 / 0.913**. Human edits were light.  
- GPT-4o dump vs Gold: **75.4%** sentences identical overall; typed exact micro F1 **0.6365** (collapsed 0.6403; relaxed IoU≥0.5 **0.7221**).  
- Same Gold, other models: DeepSeek typed **0.1327**, Qwen2.5-14B typed **0.0791**, Kimi incomplete.  
So ChatGPT’s high Table-3 number is **not** an independent SOTA. Treat it as **same-family annotator vs lightly edited gold**.

**Evaluation**  
- Official metric now: **typed exact micro F1**, scorer `cnss-lskt-1.2.0`, Gold `gold_canonical_v2.jsonl` (2601 IDs). Spans are `(start, end, type)` per sentence; **not** a global set of offsets (that bug inflated English JobBERT transfer to ~0.46; we rejected it).  
- Types L/K/S/T must match (typed). Collapsed-to-SKILL and IoU≥0.5 exist as secondary.  
- Paper Table 2 IAA (n=100, from PDF): strict exact F1 **0.532**, relaxed **0.624**, token κ **0.554**. Humans already disagree a lot under exact match.  
- Distinguish: corpus test 3237 sents; raw Doccano Gold 2676 rows; unique Gold 2601.

**Encoder (Chinese JobBERT-zh = RoBERTa-wwm-ext + JD MLM + CRF)**  
- Best seed-42: **0.1233** typed exact (3M MLM ckpt 65000). 1M DAPT **0.1224**. Vanilla RoBERTa-wwm **0.1156**. Listed-company mix 1M **lost** (0.1201).  
- Latest extra seed 123 (not yet in the paper table): ~**0.1295**. Still the same band.  
- Recall is the bottleneck (~P 0.18 / R 0.10; thousands of FN).  
- Per-domain: 人工智能/阿里云 ~**0.13**; **事业单位 ~0.015**. ChatGPT on 事业单位 ~**0.70** (again: gold family).  
- Train silver vs Gold: silver often **cuts mid-word** (e.g. `支持服`); Gold wants **complete noun phrases**, median length 4 chars/tokens, mean ~4.9. goldstyle v3 train rewrites silver toward Gold-length NPs (mean 6.7). Human80 under an older “whole duty clause = one S” rule had mean length **17.9** and disagreed with Gold.  
- English JobBERT **head transfer** onto Chinese BERT is ~**0.0045** (skill) / **0.0038** (knowledge) — keep as weak published baseline, not Zhang-scale DAPT.  
- Zhang-style DAPT: we did Chinese JD MLM at 1M and ~3M sentences (not claimed equal to Zhang’s 3.2M English recipe). Encoder still ~0.12. Domain-mix DAPT (raise 事业单位+阿里云) is **running, no F1 yet**.

**LSKT operationalization (current SOP)**  
- L: languages (英语, 普通话).  
- K: knowledge, degree, major, certificates, domain theory.  
- S: actionable skills, methods, tools, experience activities (Python, 网络管理).  
- T: soft skills / traits (沟通能力, 责任心).  
- Span = **continuous original substring**; **complete NP**, not mid-word fragments, **not** whole 岗位职责 clauses.  
- Do **not** label 报名/笔试/体检/公示 process, welfare, headcount-only lines → empty sentence.  
- Familiarity with tools/languages → S; majors/degrees → K.  
- Flat, non-overlapping, non-nested.

**Chinese-specific pain**  
- No whitespace; tokenizer (RoBERTa-wwm) ≠ character offsets used in Doccano.  
- 事业单位 texts are long **招聘公告**, not short JDs; Gold sentences are short excerpts (~47 chars) from those notices. Encoder fails here.  
- Ambiguous K vs S in Chinese (熟悉X / 掌握X / X专业 / X经验).

### Questions (answer in this order)

**A. Diagnosis (2–4 paragraphs)**  
Is 0.13 encoder F1 primarily (i) exact-match + 4-type scheme too strict, (ii) Gold is GPT-4o-shaped so encoders trained on different granularity cannot match, (iii) Chinese tokenization/domain, (iv) model/data scale, or (v) a mix? Rank them.

**B. Label ontology**  
Keep L/K/S/T, collapse to binary SKILL vs OTHER, switch to ESCO pillar/skill/knowledge/attitude, or allow nested/ overlapping spans? What do Zhang SkillSpan and Kompetencer actually annotate, and what F1 do **pretrained encoders** report there (exact table if you can cite)? Is 0.5 encoder F1 the right benchmark, or are we comparing seqeval token-F1 / collapsed SKILL to our typed exact span F1 (apples-to-oranges)?

**C. Operationalization for Chinese**  
Should SOP stay “complete NP, Gold-length ~4–12”, move to clause-level, or use two-layer labels (trigger verb + NP)? How to handle 熟悉/掌握/具备 and 事业单位 专业考查 sentences? Give 5 concrete Chinese examples with recommended spans.

**D. Who the scheme favors**  
Does exact typed F1 favor: GPT-4o (annotator family), human–human IAA, LLM–LLM, or encoders? If we want **human-aligned** gold, what must change (independent annotators who never see silver; dual IAA before seeing GPT; adjudication rubric)? If we want **encoder-reachable** gold, what must change (coarser types, relaxed primary metric, word-based spans)?

**E. Evaluation redesign (without pretending the old Table 3 never existed)**  
Recommend a **two-track** protocol:  
- Track 0: freeze current Gold v2 + typed exact (reproducibility).  
- Track 1: what new gold/metric would make encoder numbers comparable to SkillSpan/JobBERT literature.  
Should primary metric become collapsed SKILL, IoU≥0.5, or token-level seqeval? What would you expect JobBERT-zh F1 to do under each (qualitative: still ≪0.3 / maybe 0.3–0.5 / only if gold rebuilt)?

**F. Literature**  
List 8–12 papers we must re-read before redesigning (Zhang SkillSpan, JobBERT/JobBERTa, annotation guidelines for job-skill NER, Chinese NER without spaces, LLM-as-annotator bias). For each: one sentence on **what it implies for our 0.13 vs 0.5 question**.

**G. Decision**  
Pick **one**:  
1. Keep LSKT + Gold v2; report encoder as a weak baseline; add limitation that GPT-4o silver contaminated gold.  
2. Keep LSKT definition, **rebuild gold** with humans blinded to GPT.  
3. **Redesign types + SOP + metric**, then new gold.  
4. Hybrid: freeze v2 for the paper, start a v3 annotation study.  

Give a 4-week work plan (what not to spend GPU on). Do **not** recommend re-calling GPT-4o on the same gold as a “fairer ChatGPT score”. Do **not** claim Hybrid KEEP/DELETE on JobBERT spans will reach 0.5 while recall is ~0.10.

### Output format
- Verdict (1–2 sentences)  
- Ranked causes of the 0.13 gap  
- Keep vs redesign (option 1–4)  
- Metric recommendation (primary + secondary)  
- Chinese SOP changes (bullet list + 5 examples)  
- Paper limitation paragraph we could paste (English, ~120 words)  
- Reading list  
- 4-week plan  

If something is not knowable from public papers, say **unknown** rather than guessing our unpublished F1.

## End prompt
