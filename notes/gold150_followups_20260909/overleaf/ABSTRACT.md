# Overleaf — Abstract draft (PeerJ style)

Limit: 500 words / 3,000 characters. No footnotes, no references except a critiqued DOI.  
Subheadings must be bold, followed by a period.

**Word count (body only, approx.):** 375 (under the 500-word / 3,000-character cap).

---

**Background.** Competency extraction from job advertisements is well studied in English, but Chinese recruitment text lacks a public, typed span benchmark with a frozen scorer. We introduce Chinese-SkillSpan, a sentence-level resource for flat, non-overlapping competency spans in four ESCO-derived types (language, knowledge, occupational skill, transversal skill; LSKT). The release does not include ESCO concept identifiers.

**Methods.** The corpus has 22,840 sentences (17,460 / 2,143 / 3,237). Paper-main evaluation uses 2,601 unique test IDs under a derived V4 hybrid protocol (980 rule-based SimHuman spans + 1,621 SOP–CWS spans), scored with `cnss-lskt-1.2.0`. Primary metrics are typed exact-span micro-F1 and typed relaxed F1 (IoU ≥ 0.5). We report a Chinese job-domain encoder (JobBERT-zh) with a character CRF, frozen instruction-model dumps with a jieba snap, and an official zero-shot SOP extract from Qwen2.5-14B-Instruct. A separate human overlay of 150 sentences (Gold150 = Challenge-100 + Audit-50) is used only for additional Silver-plus continuation experiments and is not an independent re-test of the same systems on the full 2,601 IDs. Standard deviations on Gold150 are n=3 sample SD, not test-set confidence intervals.

**Results.** On the V4 hybrid 2,601-ID test, JobBERT-zh 3M with jieba alignment reaches typed exact F1 0.4331 (1M: 0.4272). A frozen ChatGPT dump with the same snap is weaker on exact span (0.2854) but stronger on relaxed overlap (0.6249). Official Qwen SOP extract without LoRA is 0.1724 exact. Gold v2 ChatGPT typed exact 0.6365 is reported only as construction history and is not ranked against 0.4331. On Gold150, continuing JobBERT-zh 3M on Silver-plus v6a (2,156 / 169, sentence-level isolation, extended) yields B2 typed exact 0.5536±0.0054 (relaxed 0.6890±0.0085). The B2-versus-B1 gap on the smaller v3 list (+0.391) is larger than the B2 change from 1,382 to 2,156 training sentences (+0.024). JSON-offset LoRA on Qwen2.5-14B (not the SOP protocol) reaches 0.1215±0.0092 exact on the same Gold150 overlay.

**Conclusions.** Chinese-SkillSpan provides a frozen typed-span test, a public encoder baseline, and an explicit split between the V4 hybrid headline and a smaller human overlay. Encoder continuation is sensitive to the Silver-plus label scheme. JSON-offset LoRA remains a localisation-limited supplement and is not a substitute for the official SOP extract.

---

**Do not add to Results:** Concept Accuracy, Time-OOD, “label quality far exceeds data size”, P1/kNN F1, peel-rerun F1, SOP-on-Gold150 teacher F1, or a single SOTA ranking of 0.5536 vs 0.4331 vs 0.6365. P1 / SOP-on-Gold150 / peel go in the appendix only.
