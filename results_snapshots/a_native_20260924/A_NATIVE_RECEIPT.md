# A native receipt — DS209213 — 2026-09-24 11:45 +08

Host confirmed: **DS209213 / 144.214.209.213**. Not DS210039. Overleaf not modified here. B job 8558 not touched. Work root: `/home/guojingli3/cnss_a_native_20260922/`. Canonical receipt: **this file on A**.

Do not write to `/home/guojingli3/cnss_external_benchmarks_20260921`. Linear-head common-protocol scores from B are **not** native Rerun.

Machine-readable: `$ROOT/results.jsonl` (`track=native`) and `$ROOT/paper_ready_a_native_20260924.json`. Duplicate historical rows may exist in the append-only jsonl; scored `runs/.../*.macro_f1.json` and NNOSE `test_*.tsv` are the values below.

## Environment

| item | value | status |
|------|--------|--------|
| GPU | 4× A100 80GB sm_80; idle pick ≥40 GiB; never GPU0/1 while other vLLM held them | ok |
| driver / CUDA (nvidia-smi) | 555.42.06 / 12.5 | recorded |
| Kompetencer env | `$ROOT/env_kompetencer39` Python **3.9.25**, torch **1.8.1+cu111**, allennlp **2.8.0**, transformers **4.12.5**, numpy **1.23.5** | completed |
| NNOSE env | `$ROOT/env_nnose` Python 3.9.25, torch **1.10.1+cu113**, faiss **1.7.2**, transformers **4.26.1**, adapter-transformers 3.2.0 | completed |
| NNOSE pin restore | pyarrow **11.0.0**, fsspec **2023.1.0**, huggingface-hub **0.12.1**, numpy **1.24.2**, scipy **1.10.1**, pandas **1.5.3** | completed |
| HF_HOME | `$ROOT/hf_cache` | used |
| Slurm | account=student, LocalQ, MaxJobs=1, `--gres=gpu:2` then `--gres=gpu:1` for the last cell | legal sbatch |

Python 3.8 `$ROOT/env_kompetencer` abandoned (`cached_path` / `functools.cache`). Not torch 2.x.

## Slurm chain (A native)

| JobID | name | state | elapsed | notes |
|------:|------|--------|---------|-------|
| 51282 | a_nnose_gs | COMPLETED 0:0 | 03:49:27 | NNOSE green + sayfullina JobBERT |
| 51283 | a_enda_rem | COMPLETED 0:0 | 01:13:14 | enda *training* archives; predict failed (missing `--dataset`) |
| 51284 | a_jobberta | COMPLETED 0:0 | 09:17:38 | NNOSE JobBERTa skillspan/green/sayfullina |
| 51331 | a_enda_pred | COMPLETED 0:0 | ~00:03:16 | enda predict+score; rembert seed 8749520 skipped (leftover `weights.th`) |
| 51332 | a_enda_c3 | COMPLETED 0:0 | 00:00:50 | rembert enda seed 8749520 after extracting `vocabulary/` |

Cancelled: 51069 (dead `DependencyNeverSatisfied` queue); 51330 (script overwrote `CUDA_VISIBLE_DEVICES` to physical GPU0 — scancelled immediately).

## Data

`kompetencer/mtp/data -> ../data`. All nonempty rows used.

| file | nonempty rows |
|------|----------------:|
| 1_en_train.tsv | 9472 |
| 2_da_train.tsv | 138 |
| 3_en_dev.tsv | 1577 |
| da_test.tsv | 784 |
| en_test.tsv | 1578 |

NNOSE in-tree json (not B common-protocol HF json); sources revision `afc785b664a5cbec445f6ac5cac45cd97c76b3d7`.

| dataset | test.json sentences |
|---------|--------------------:|
| skillspan | 3569 |
| green | 335 |
| sayfullina | 1851 |

## Model IDs

- **google/rembert** `65da5133da36e29dfca67d4f0dd9f7f9db21b563`
- **jjzha/dajobbert-base-cased** Hub redirects to **uncased** `b9970acc053d487415f781dbe0df06344377fc44`. **Not a cased exact reproduction.**
- **jjzha/jobbert-base-cased** `eee1c8da6200fbaf2e2dcba53d54f6363f7a16dd`
- **jjzha/jobberta-base** `6b2dd2512ecb55cda081433b4bb273d7c596e105` (downloaded; not relabeled from JobBERT)

## Status board

| cell | status |
|------|--------|
| rembert × da_classification × 5 × 20ep | **completed** |
| dajobbert × da_classification × 5 × 20ep | **completed** |
| rembert × en_classification × 5 × 20ep | **completed** |
| dajobbert × en_classification × 5 × 20ep | **completed** |
| rembert × enda_classification × 5 × 20ep | **completed** (predict with `--dataset`) |
| dajobbert × enda_classification × 5 × 20ep | **completed** |
| NNOSE SkillSpan / green / sayfullina × JobBERT | **completed** (seed 113412, in-dataset datastore) |
| NNOSE SkillSpan / green / sayfullina × JobBERTa | **completed** |
| BERT / JobBERT / DaBERT Kompetencer classification | **not_started** → Overleaf Rerun **unavailable** |
| NNOSE ∀D (`DATASTORE=AD`) | **not this run** |
| Gnehm 2022 EDU/EXP/LNG | blocked (no original input) |
| commercial API | blocked |

## Metric

**Kompetencer Rerun:** sklearn `f1_score(..., average="macro")`, scale **0–1**, n=784 (`da_test`) / 1578 (`en_test`). **Not** span-F1. **Not** B common-protocol token-span. Mean ± **sample SD (ddof=1)**, n=5.

Also record **weighted** F1 because `kompetencer/plot_results.py` ylabel is “Weighted macro-F1”. Rerun column stays sklearn-macro.

**NNOSE Rerun:** seqeval span F1, scale 0–1. Single seed **113412** — **no fake SD**. Freeze k/λ/T on **dev**, evaluate **test.json** once. Linear head and kNN both reported. In-dataset train-only datastore (`datastore_100_*`), **not** ∀D.

---

## 1. dajobbert × da_classification × 5 — completed

### da_test (main, n=784)

| c | seed | sklearn macro-F1 | weighted-F1 | pred SHA256 |
|---|------|----------------:|------------:|-------------|
| 1 | 3477689 | 0.18597929445469044 | 0.3835620434779473 | `d0adc10dbb7b5a00e35b55315163eca09f6b47e6c7160751270ed8234ba3552c` |
| 2 | 4213916 | 0.18015787909960598 | 0.39256821992947133 | `324b4ef2c0d7cd8ad9535446fae6e3b764bfed9bacf74dbafa5a23a36ee248fd` |
| 3 | 8749520 | 0.14010197231791652 | 0.359051499153013 | `134d5d63c9d5af1230a6f51a126e59d84187cf1465b3a6d1ed8337846df9a989` |
| 4 | 6828303 | 0.17181932169537634 | 0.3668139092506226 | `942cbfdfcd0342739141d81b8dae32cb3fa57f296546dbe1d0dca63f57a59042` |
| 5 | 9364029 | 0.23415043753628328 | 0.42452134787369306 | `8829c991a14985f46c93147e0ae5997f1f4d63d06453eca690c32e1ceb2abd06` |

**Mean ± sample SD:** sklearn macro **0.18244 ± 0.03390**; weighted **0.38530 ± 0.02562**.

en_test extra: sklearn macro **0.06430 ± 0.01156**.

---

## 2. rembert × da_classification × 5 — completed

| c | seed | sklearn macro da_test | weighted da_test |
|---|------|----------------------:|-----------------:|
| 1 | 3477689 | 0.033156056752221885 | 0.15095292666078367 |
| 2 | 4213916 | 0.17763551646515707 | 0.36027086786545254 |
| 3 | 8749520 | 0.003595125678440626 | 0.001741 |
| 4 | 6828303 | 0.013354436640617274 | 0.050590 |
| 5 | 9364029 | 0.02361842477174357 | 0.099021 |

**Mean ± sample SD:** sklearn macro **0.05027 ± 0.07205**; weighted **0.13252 ± 0.13888**. Large seed variance (including near-zero seeds).

---

## 3. dajobbert × en_classification × 5 — completed (EN train/dev, DA test)

**da_test:** sklearn macro **0.23157 ± 0.02817**; weighted **0.29005 ± 0.01987**.  
**en_test:** sklearn macro **0.53938 ± 0.01046**.

---

## 4. rembert × en_classification × 5 — completed

Seed 5 (`9364029`): SIGKILL at epoch 9; MaChAmp `--resume`; best_epoch **19**.

**da_test:** sklearn macro **0.26123 ± 0.01865**; weighted **0.34265 ± 0.04013**.  
**en_test:** sklearn macro **0.55153 ± 0.01700**.

---

## 5. enda_classification × 5 — completed (EN+DA train)

enda is multilingual. `predict.py` **requires** `--dataset Danish_Jobs` / `English_Jobs`. Job 51283 trained archives but wrote no `.out` until 51331/51332.

### dajobbert enda — da_test (n=784)

| seed | sklearn macro | weighted | pred SHA256 |
|------|-------------:|---------:|-------------|
| 3477689 | 0.3218307289475126 | 0.5165941907433432 | `dea812a2f05facf35ee2c0de0a9c5f16fa6ec7861fdace8519aca66e1fbe6f30` |
| 4213916 | 0.35395004781694733 | 0.5329075607954364 | `af7077a4e3006e03ce27e51a7260bbf283706d718fd3661b5af5bee79392af89` |
| 8749520 | 0.32333516217974756 | 0.5067750703103713 | `45afc8c53ad3a2f43e4d1e673830d6941d15b631aac664db33626f5c66c8c355` |
| 6828303 | 0.34284037605759105 | 0.5125348187328426 | `a2f8bf6199b853a38fd7ad8fb51fe0d0f5690d0bfd89618248812381cf49959a` |
| 9364029 | 0.360140111097696 | 0.5191556296491412 | `c5b44333687e27f9d25ec564285f659001c8e9f2e613f8bb20309417cc7306f9` |

**da_test mean ± sd:** sklearn macro **0.34042 ± 0.01743**; weighted **0.51759 ± 0.00975**.  
**en_test mean ± sd:** sklearn macro **0.52895 ± 0.00829**; weighted **0.61512 ± 0.00423**.

### rembert enda — da_test (n=784)  ← LREC plot bar “RemBERT (EN+DA)”

| seed | sklearn macro | weighted | pred SHA256 |
|------|-------------:|---------:|-------------|
| 3477689 | 0.33354029846937894 | 0.4778520920205295 | `8c0c116a8b8095bec6a8334526e49ac79894c76c2b1fc444f1e7d56758736c24` |
| 4213916 | 0.30250178562296776 | 0.4677489786082622 | `128e9c88017692c95443388e920d0bc470729fd1d5b9c2abeef3d7450c44b423` |
| 8749520 | 0.30611822041092496 | 0.4559053234598501 | `0803b3a16cbcf6e9bba44c40a07fb106fab0a11ff846ad7a04d1652cfc5b026e` |
| 6828303 | 0.2993816328815962 | 0.4571978374122174 | `18dabca0d230f08b512239f7477a3f7a6533079c0515a5589b2896b11106896c` |
| 9364029 | 0.34015003757622514 | 0.4792962643890202 | `14879674472f9e168776e9027fca6871a846e194066d9fb8888cecc21dad6430` |

**da_test mean ± sd:** sklearn macro **0.31634 ± 0.01902**; weighted **0.46760 ± 0.01103**.  
**en_test mean ± sd:** sklearn macro **0.55443 ± 0.01437**; weighted **0.64088 ± 0.00701**.

---

## 6. NNOSE — completed (in-dataset datastore, seed 113412)

Not B common-protocol linear head. Not MaChAmp CRF. Sweep freeze on **dev**; test once.

| dataset | model | ckpt | frozen k, λ, T | test n | linear F1 | knn F1 |
|---------|-------|------|----------------|-------:|----------:|-------:|
| SkillSpan | JobBERT | epoch_17 | 16, 0.25, 3.0 | 3569 | **0.6129447063866267** | **0.6122536418166239** |
| SkillSpan | JobBERTa | epoch_6 | 8, 0.4, 0.5 | 3569 | **0.6306194323596437** | **0.624871107444834** |
| Green | JobBERT | epoch_1 | 128, 0.2, 2.0 | 335 | **0.4910591471801926** | **0.5003445899379738** |
| Green | JobBERTa | epoch_3 | 128, 0.5, 0.5 | 335 | **0.46586910626319494** | **0.4847625797306875** |
| Sayfullina | JobBERT | epoch_7 | 16, 0.85, 0.5 | 1851 | **0.896969696969697** | **0.8959537572254336** |
| Sayfullina | JobBERTa | epoch_6 | 128, 0.6, 0.1 | 1851 | **0.9152815013404826** | **0.9120469083155651** |

Prediction SHA256:

| cell | linear | knn |
|------|--------|-----|
| skillspan JobBERT | `d1845568964a5e14a1048532ae212483638f7f51ad2b6774f5733d86cef508fa` | `719061b71e69f97c7fc7c980c8c2cf903e0f4171c2b2ff7f2c901eef9083306f` |
| skillspan JobBERTa | `b79c2aa9ed9740a0eb504457171f9f070e101a99373b01af080253e10acb4e09` | `0ba4facf8034cc7a15f7b3745ad4944eeefb5ccf6f33a30a0d0f832c907279a4` |
| green JobBERT | `a1a080d00ea793b27bf83b4bfb3a4863f410bc4e511f7cc5c07287fa0f3cc50a` | `d29b312f9b5e9a347cf7a788ce21f6b755f28c4304ddb72a86f5ae9e0610a723` |
| green JobBERTa | `2f1ea5e18980f643e9a506ee9eb18763e285f0b8fe2bdce275f873842882a5b7` | `de183cfa4b8666071ea737918d6bcf2f7574328310ef05236f22aa5793ddc7dd` |
| sayfullina JobBERT | `e427f60a93162fdaded9b754872b4edb7df33973d6c4cbb5df013725fabb31fc` | `9e01bc0cd01e95601492de5de63096543211ef0ce304fb0bcc7703cbf345f42b` |
| sayfullina JobBERTa | `a8b51dce91700f71d1854703467de99439ba83aa74613f9e687cc6aa66d04be4` | `86b002d3c68fd4f3507c2bb6149844f20318d6acb6f0ff9197b4bbf12ed8cf65` |

kNN did **not** exceed the linear head on SkillSpan or Sayfullina; it did on Green. Observation only — not a paper conclusion. **Do not copy EACL Published into Rerun.** Table/row/scale match: **current cannot judge**.

---

## Published (citation-only; **not** copied into Rerun)

Zhang, Jensen, Plank. Kompetencer. LREC 2022. https://aclanthology.org/2022.lrec-1.46  
Hardcoded in `kompetencer/plot_results.py` `da_test["f1_macro"]`, ylabel **“Weighted macro-F1”**:

| plot bar | da_test mean | da_test std |
|----------|-------------:|------------:|
| BERT (EN) | 0.03756 | 0.00821 |
| JobBERT (EN) | 0.06335 | 0.00545 |
| RemBERT (EN) | 0.35439 | 0.02080 |
| DaBERT (DA) | 0.19894 | 0.05789 |
| **DaJobBERT (DA)** | **0.39457** | 0.02052 |
| RemBERT (DA) | 0.16573 | 0.14142 |
| RemBERT (EN+DA) | 0.47182 | 0.01354 |

NNOSE Published: EACL 2024 Zhang et al.

## Can we judge alignment with published classification numbers?

**Current cannot judge** a full official-matrix match to the LREC plot as a single number:

- AllenNLP dataset metric is **macro-f1**. sklearn **macro** for DaJobBERT few-shot da_test is **0.182 ± 0.034**, far from plot **0.395**.
- Plot ylabel is **Weighted macro-F1**. Our weighted DaJobBERT (DA) **0.385 ± 0.026** is numerically close to 0.395 ± 0.021, but Hub cased id is uncased `b9970acc`, and **Rerun stays sklearn-macro**.
- RemBERT (EN+DA) sklearn **0.316 ± 0.019** / weighted **0.468 ± 0.011** vs plot **0.472 ± 0.014**: weighted is close; still not declared a match.
- RemBERT zero-shot (EN→DA) sklearn **0.261 ± 0.019** / weighted **0.343 ± 0.040** vs plot RemBERT (EN) 0.354 ± 0.021: weighted closer; not a match declaration.
- BERT / JobBERT / DaBERT classification **not rerun**.

Rerun is never filled with Published. Failed/pending cells are `unavailable` / `Pending`, not 0.

## Protocol differences already known

- Python 3.9.25 instead of original likely 3.7/3.8.
- AllenNLP checklist extra absent (import patched).
- RemBERT from local pin, not live Hub `main`.
- DaJobBERT cased Hub id ≡ uncased `b9970acc`.
- RemBERT `train.py` in-process predict OOM; test preds from separate `predict.py`.
- rembert en c=5: SIGKILL; MaChAmp `--resume` (best_epoch 19).
- enda predict needs `--dataset`; 51283 archives reused.
- rembert enda seed 8749520: leftover `weights.th` skipped tar extract; vocabulary extracted then scored (51332).
- NNOSE in-dataset datastore, not official `DATASTORE=AD`.
- NNOSE env packages drifted then restored to `environment.yml` before STAGE1.
- Training after 51069 cancel used legal `sbatch --gres=gpu:2`.
