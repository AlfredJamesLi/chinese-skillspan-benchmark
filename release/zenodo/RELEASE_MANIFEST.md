# Zenodo release manifest — Chinese-SkillSpan

Version: `[TODO: release version]`  
DOI: `[TODO: Zenodo DOI]`  
Generated from the local paper tree. Sizes and SHA-256 were computed in this workspace for files that exist. Files that must **not** be deposited are listed at the end.

**Text-containing JSON/JSONL is pending copyright confirmation** (see `DATA_AVAILABILITY.md`). They are listed as *intended* archive members only if the authors clear redistribution of advertisement wording.

---

## A. Documentation (no job-ad bulk text)

| Path | Purpose | Version | Bytes | SHA-256 |
|---|---|---|---:|---|
| `README.md` | Public repository read-me | draft docs | 14,676 | `740fbfa7b75e5f6a5dae88ef3789c74bef1f7404502d193386cc9ffdf04cf0b9` |
| `REPRODUCIBILITY.md` | Reproduction protocol | draft docs | 12,369 | `58ada5cad41f99467a6b3ef66104d39259fa7f2a20ba0cab960f362d21a838c8` |
| `DATA_AVAILABILITY.md` | Data-availability and rights | draft docs | 7,299 | `1fed8cc303ef01523f6946070252d75df4a9bf012188f5465fe9491863759b90` |
| `CITATION.cff` | Citation metadata | draft docs | 2,772 | `b626911591c9681b5df9c9c3795cc5ab1ed6461224ad5d04ec0eace759514f2b` |
| `CHANGELOG.md` | Version history | draft docs | 3,458 | `4c44c8c1d202d5524d0f1084f62b2145dae0b42dfb4ce1a26f085359c65050b7` |
| `CONTRIBUTING.md` | Contribution rules | draft docs | 3,271 | `5520db402bb3e0a25644d3dabdf399ee08de142c2cc6b208da1f8b44901f8e8a` |
| `requirements-repro.txt` | Scoring dependency | pinned `jieba>=0.42.1` | 273 | `28d5ac6f2d4f9ef3ff24b3f2414063c1dc4ac2e2f7f9c7914d64ad27a12940ca` |
| `docs/RELEASE_CHECKLIST.md` | Submission checklist | draft docs | 7,185 | `f5935230fc79c67df40cf30cbab66ce56282fd669842b9b570e507cc9a6a4ced` |
| `release/huggingface-model/README.md` | Model card | draft docs | 9,110 | `b074aaed2a2c2086adfdf45a052e3ba0962faeaa6deed17ae32610efed48577b` |
| `release/huggingface-dataset/README.md` | Dataset card | draft docs | 10,488 | `7f46192fc5b5566b4523bbf3cf3525de98210922b1ec153f59cca0f192b14bc6` |
| `release/zenodo/.zenodo.json` | Zenodo metadata | draft docs | 2,956 | `c3e67c69cf223cda34f79d5dcbd031c5dff9f356ed35aad865674a687705bb21` |
| `notes/handbooks/handbook_B_sop_v4.md` | Handbook B (Chinese) | `B.sop_v4.2.1` | 7,186 | `e9e7677b248d75ede523c2d53c6a55fe641aed4e3eb004bd59b8c16a7875751b` |
| `notes/handbooks/handbook_B_sop_v4.en.md` | Handbook B (English) | `B.sop_v4.2.1` | 4,446 | `aee5c4137b858e4e801548796c18a6516134fb64e3ec9dc5620319d2fceaa9ce` |

Also include other Handbook B addenda under `notes/handbooks/` that the authors select (`[TODO: enumerate overlap/adjudication files to ship]`).

---

## B. Code

| Path | Purpose | Version | Bytes | SHA-256 |
|---|---|---|---:|---|
| `scorer/score_lskt.py` | Official scorer | `cnss-lskt-1.2.0` | 16,513 | `90624fa545434ebe0442c3243709f5e64ef2f95f4ccbacdb5f5d0696b65d69a7` |
| `scorer/` (remainder) | Tests and helpers | `cnss-lskt-1.2.0` | `[TODO: per-file]` | `[TODO]` |
| `scripts/cws_snap.py` | Jieba snap | `[TODO]` | `[TODO]` | `[TODO]` |
| `scripts/eval_hybrid_cws_simhuman.py` | Paper-main table | `[TODO]` | `[TODO]` | `[TODO]` |
| `scripts/eval_hybrid_llm_old_dumps.py` | Frozen LLM rows | `[TODO]` | `[TODO]` | `[TODO]` |
| `scripts/train_cn_roberta_crf.py` | CRF trainer | `[TODO]` | `[TODO]` | `[TODO]` |

Ship the rest of `scripts/` only after laboratory absolute paths and credentials are removed. `[TODO: path sanitisation]`.

---

## C. Dataset files (contain advertisement sentences — rights pending)

| Path | Purpose | Version | Bytes | SHA-256 |
|---|---|---|---:|---|
| `data/corpus_splits/train.json` | Table 1 train (17,460) | Table 1 split | 42,645,522 | `0a24841b97416a0b50e80c5e848bc6b232be91c7bc2f81c05ddb937a2924a44b` |
| `data/corpus_splits/dev.json` | Table 1 dev (2,143) | Table 1 split | 5,647,111 | `ea0dabb8dbf295d4edc046fa2ecf9610d33557216095aa54ac9690a77954b1ac` |
| `data/corpus_splits/test.json` | Table 1 test (3,237) | Table 1 split | 10,653,736 | `263edc8b07db139f078f1023bad7f46dc2c6bf3e7ec1bdfb7cbccded2ded3142` |
| `data/gold_canonical_v2.jsonl` | Gold v2 (2,601) | v2 freeze | 5,370,667 | `7a26e32b89d4e501175cb96443e35e171cea08d91501d2a32779b96ee8504ff6` |
| `data/test_lskt_v4_cws_simhuman980_hybrid.jsonl` | Paper-main gold | V4 hybrid | 2,709,105 | `2ad6342d8b762cf1abb289295315e2521bec0c540f4320113409fceab0818d99` |
| `data/train_lskt_v4_silver.jsonl` | V4 CRF train silver | v4 silver | 13,853,137 | `1dbf8f447e82f2e4c2d3d5df26aaa357e53cfc39c9724d04ebb3188de747680e` |
| `data/dev_lskt_v4_silver.jsonl` | V4 CRF dev silver | v4 silver | 1,816,201 | `005d062f9c07f84f4fd9935a79e8dbb5599b440284f8230eed862eb0428fd637` |
| `data/train_goldstyle_v3.jsonl` | Appendix train | goldstyle v3 | 14,171,835 | `1643f360237e4b0dd3a4da8325bad0207a7fbe0f35da5e442d09b749d6681523` |
| `data/dev_goldstyle_v3.jsonl` | Appendix dev | goldstyle v3 | 1,861,640 | `d4357d90df918236a1a02c70a562a22efd375c7ce3771f7eae28a8150761ed9e` |
| `data/human_gold_page1_200.jsonl` | 200-sentence overlay | 2026-09-03 | 328,087 | `fcecb522fbdf6571caaaa02c592b6ba4a552c4a9cfa52a0ed1f36b0fe9617490` |

Optional supporting gold-construction files (`test_lskt_v4_simhuman980.jsonl`, `test_lskt_v4_cws_g2ids.jsonl`, `data/gold_adjudication_v2.json`): `[TODO: include or omit after a rights and size review]`.

---

## D. Frozen predictions and committed scores

| Path | Purpose | Version | Bytes | SHA-256 |
|---|---|---|---:|---|
| `data/frozen_preds/jobbert_3m_v4.jsonl` | Chinese JobBERT 3M v4 tags | v4 | 3,088,621 | `f073f7e696d03ad6cd1ce21177747a40a4148c1372635dc12f5683c9eb5b6bc9` |
| `data/frozen_preds/jobbert_1m_v4.jsonl` | Chinese JobBERT 1M v4 tags | v4 | 3,089,077 | `7169c2604dcadbbcd920a759074e69bc352303a6b41d5642d77024ce3d226f33` |
| `data/frozen_preds/jobbert_1m_v4_cws_retrain.jsonl` | 1M CWS-retrain tags | v4 | 3,085,433 | `f0b873345501c93dafdc0ac5547768f61a2c6bfc4f555cacc48b681bbf20fbbb` |
| `tables/hybrid_cws_simhuman980_all_models.csv` | Paper-main score table | committed | 4,058 | `448c1281c0027d9ec0a83b0d5c51c5f1d412ccf9fb64e4321a583c4a4b534c1e` |

LLM unique-first views under `reports/views/` (`ChatGPT_unique_first_v2.jsonl`, …): `[TODO: include if licence of model outputs and ad text allows]`.

---

## E. Do not deposit

| Path / pattern | Reason |
|---|---|
| `应届生招聘大数据*.csv`, `人工智能招聘大数据2025年.xlsx` | Raw platform exports; no confirmed redistribution right |
| `data/jobbert_*_sents.jsonl` | Reconstructed MLM corpora; same text-rights issue; large |
| `output/`, `runs/`, `chineseskillspan-jobert-pretrain/` | Checkpoints, caches; weights belong on Hugging Face after review |
| `.env`, tokens, `*credentials*` | Secrets |
| `venv/`, `__pycache__/`, `.ipynb_checkpoints/` | Generated |
| `REPRO_FROM_BAIDU.md`, `MODELS_CATALOG.md` as currently written | Personal cloud paths |
| IEEE Access / SRICL PDFs and `access_paper/` | Other project |
| `repartition_v1` as if it were main gold | Draft split; ship only with an explicit “not main” label if at all |

Chinese JobBERT **weights** should be a Hugging Face revision referenced from this record, not a 53 GB Zenodo blob, unless the authors choose otherwise after `[TODO: size and licence review]`.
