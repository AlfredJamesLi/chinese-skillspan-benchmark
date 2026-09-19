# Codex prompt — Zenodo Qwen pack + DAS update (2026-09-19)

Operator: copy **everything below the line** into **one** Codex message.  
Host: server B `DS210039`, workspace `/home/guojingli3/Chinese-Skillspan-Benchmark`.  
GitHub push from B fails (no `gh` login). If a public-clone commit is needed, fetch on A (`DS209213`, key `id_ed25519_b_to_a`) and push `origin` from A. Do not git-push silver jsonl or the 826 MiB zip.

Overleaf Table H Codex-swap **0.5854 / 0.7032** is already in `submission_peerj_20260909/overleaf/`. Do **not** reopen Tables A–D. This prompt is the archive update after the Cursor export.

---

You are continuing the Chinese-SkillSpan PeerJ CS deposit. Cursor already exported existing Qwen experiments. Your job is: **verify the zip, upload it to Zenodo as a new record, then write the DOI into Data Availability**. Do not train, re-infer, call a model API, or edit frozen labels/predictions.

## 1. Verify the local pack before any upload

```
/home/guojingli3/Chinese-Skillspan-Benchmark/CNSS_Qwen_Reproduction.zip
```

Required:

| Field | Value |
|---

## 0. File access (laptop Codex; servers A/B unreachable)

Do not SSH to DS210039 / DS209213. Download the zip to this machine:

```
https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/releases/download/qwen-repro-pack-20260919/CNSS_Qwen_Reproduction.zip
```

Or: `gh release download qwen-repro-pack-20260919 -R AlfredJamesLi/chinese-skillspan-benchmark -D %USERPROFILE%\Downloads`

SHA256 must be `e1098b42fdf6302b451152530449f5c9666d7cd44a829189b7434988634709e8` (865168457 bytes).

Docs (no unzip required): `docs/codex_qwen_repro_20260919/` on branch `codex/qwen-repro-handoff-20260919`.
Read `LICENSE_NOTICE.md` and `CONTENTS_NOTE.md` before choosing a Zenodo licence. Gold150 freeze *is* in the zip; do not claim the pack has no advertisement sentences. Expanded-silver training jsonl is absent.

This GitHub pre-release is a transfer channel only. It is not Zenodo v0.1.3 and is not a CC-BY author grant.

|---|
| Size | **865168457** bytes |
| SHA256 | `e1098b42fdf6302b451152530449f5c9666d7cd44a829189b7434988634709e8` |
| Unpacked tree | `/home/guojingli3/Chinese-Skillspan-Benchmark/CNSS_Qwen_Reproduction/` |
| Receipt | `CNSS_Qwen_Reproduction/offline_score_receipt.json` |

If `sha256sum` of the zip does not match, **stop**. Do not upload a rebuilt zip. Do not re-run training or Gold150 generation.

Offline scores already matched; do not re-score unless you only re-read the receipt. Primary cells (do not round in metadata beyond what the paper already prints):

- B2 seed 42 epoch 2: Gold150 exact **0.4995663486556808**
- B2 seed 43 epoch 2: **0.5632858340318525**
- B2 seed 44 epoch 1: **0.5581787521079258**
- three-seed mean ± sample SD: **0.5403 ± 0.0354**
- Proxy pool 9,646 keep (8,943/351/352) seed 42 epoch 1: **0.5966386554621848** (paper 0.5966 / 0.7126)
- Codex pool 9,540 keep (8,842/348/350) seed 42 epoch 1, jobs 8132/8133: **0.5854063018242122** (paper 0.5854 / 0.7032)

These are **not** JSON-offset **0.1215 ± 0.0092**. Hash agreement is not re-inference verification.

## 2. Zenodo: new record, not a dataset version bump

Create a **new** Zenodo deposition. Do **not** add this zip to:

- v0.1.1 `10.5281/zenodo.22288338`
- v0.1.2 `10.5281/zenodo.22685143`
- v0.1.3 `10.5281/zenodo.22698504`
- v0.1.4 / concept `10.5281/zenodo.22288337` GitHub-hook ingest
- any new `v0.1.5` of the corpus tree

Suggested title:

`Chinese-SkillSpan Qwen2.5-14B-Instruct LoRA reproduction pack (shared-handbook B2 and pooled-silver students)`

Suggested description (keep the licence warning):

Frozen LoRA adapters, train/infer configs, checkpoint-selection records, and Gold150 predictions for Chinese-SkillSpan Qwen2.5-14B-Instruct occurrence students. Protocol files keep historical `DRAFT` names. Offline scoring used `eval_gold150_ext.py --protocol shared_prompt` on unmodified 150-row predictions. This record is not the 22,840-sentence corpus archive and is not Zenodo v0.1.3. Base weights of Qwen2.5-14B-Instruct are not included. Expanded-silver sentence jsonl and original advertisement dumps are not included. Do not treat the record licence as CC-BY on job-advertisement wording or on the adapters.

Upload **only**:

1. `CNSS_Qwen_Reproduction.zip`
2. optionally `CNSS_Qwen_Reproduction.zip.sha256`

Do **not** upload: Silver jsonl, WAVE3/Run2500 dumps, base-model shards, `.env`, private chats, unrelated Slurm logs, Overleaf PDF, GitHub tags.

### Licence metadata (mandatory)

Zenodo’s default `cc-by-4.0` is **wrong** for this record. Set licence to **Other (Non-Commercial)** or **other** / custom, and put `LICENSE_NOTICE.md` from inside the zip as the governing notice:

- Eval scripts / scorer in the pack: Apache-2.0 (public clone software grant).
- Qwen2.5-14B-Instruct base: Apache-2.0 as recorded on the local snapshot (`third_party/Qwen2.5-14B-Instruct.LICENSE`). Base weights not in the zip.
- LoRA adapters: author research artifacts; **not** a CC-BY grant. PEFT-generated `README.md` `license: apache-2.0` stubs are not an author licence.
- Gold150 freeze is already in v0.1.3; this zip copies it only for scoring.
- Job-advertisement wording and full public-API Silver text are **not** in this zip and must not be added.

If the Zenodo UI forces a Creative Commons menu item, pick the closest **non-CC-BY** option and state in the description that the author grant is `LICENSE_NOTICE.md`, not the hook default.

### Auth / publish

Use an existing Zenodo token if already configured on this host. Do not print the token. If no token exists, **stop** and report that; do not invent a DOI.

Publish the record (not draft-only) unless the token lacks rights — then leave it draft and return the deposition URL.

After publish, record:

- version DOI
- record URL
- concept DOI if Zenodo minted one **for this new record** (do not reuse `22288337`)
- displayed licence string
- file checksum Zenodo shows vs `e1098b42…`

## 3. Overleaf Data Availability (only after a real DOI)

Overleaf project: https://www.overleaf.com/project/68fe17a53e53a7f800e4f2b4

Replace any sentence that still says **“Qwen LoRA adapters are not published.”** Do not change Tables A–D cells. Do not add 0.5966 / 0.5854 / 9,646 / 9,540 to the Abstract. Table H may already list the Codex-swap row; leave F1s as 0.5854 / 0.7032.

Insert one DAS sentence (fill `DOI_VERSION`):

> Qwen2.5-14B-Instruct LoRA adapters for the shared-handbook B2 three-seed student (Gold150 typed exact 0.5403±0.0354) and the two pooled-silver students (proxy 0.5966; Codex-swap 0.5854) are archived at https://doi.org/DOI_VERSION. That record is not Zenodo v0.1.3 and does not contain Qwen base weights or expanded-silver sentence files. Adapter reuse follows the pack `LICENSE_NOTICE.md` and the Qwen2.5-14B-Instruct Apache-2.0 base-model terms; it is not a CC-BY grant on advertisements.

Keep:

- Gold150 / v6a_nocross first freeze: v0.1.3 `10.5281/zenodo.22698504`
- Corpus snapshot: v0.1.1 `10.5281/zenodo.22288338` and/or concept `10.5281/zenodo.22288337` as already in the manuscript
- JobBERT-zh: `AlfredJames/jobbert-zh`; B2 continuation `AlfredJames/jobbert-zh-v6a`
- Isolation: sentence-level
- Shared-handbook 0.5403±0.0354 remains a **different protocol** from Table C 0.1215±0.0092

Compile. Quote the Data Availability paragraph in your final message.

## 4. Public GitHub (docs only, no adapters)

Public repo: `AlfredJamesLi/chinese-skillspan-benchmark`.

Allowed: a short `docs/` or `DATA_AVAILABILITY.md` sentence pointing at the **new** Zenodo DOI, plus zip SHA256.  
Forbidden: commit `CNSS_Qwen_Reproduction.zip`, adapters, or any new Silver jsonl.  
Do not retag `v0.1.3` or `v0.1.4`. Do not trigger a GitHub-Release ingest that would dump adapters onto concept DOI `22288337`.

B cannot `gh` login. Push via A if you actually change the public clone. If you cannot push, leave the patch on B and report the path; do not claim GitHub is updated.

## 5. PeerJ zip (optional, only if DAS DOI is real)

If you refresh `submission_peerj_20260909` / a dated preview zip, update DAS wording only. Do not bundle 7,936 / 9,646 / 9,540 silver jsonl. Do not write “10,000”.

## Frozen numbers (never rewrite)

| Claim | Keep |
|---|---|
| V4 hybrid JobBERT 3M | 0.4331 |
| JobBERT v6a B2 Gold150 | 0.5536±0.0054 |
| Qwen JSON-offset P0 | 0.1215±0.0092 |
| SOP extract, no LoRA | 0.1724 |
| Shared-handbook LoRA | 0.5403±0.0354 (different protocol) |
| Gold150 SHA-256 | starts `ca8db0bc` |

Do **not** rank 0.5536 / 0.5403 / 0.4331 / 0.1215 / 0.5966 / 0.5854 in one SOTA sentence.  
Do **not** say Codex-2500 improves the pooled student (0.5854 < 0.5966).  
Do **not** write dual-teacher / 双老师 / GPT distillation / human cover 500.  
Do **not** edit `notes/confirmed-results.md`.

## Done when you return

1. Zip SHA256 re-check (pass/fail).
2. Zenodo version DOI + record URL, or a stop reason (no token / checksum mismatch).
3. Licence actually displayed on Zenodo (must not be an unremarked CC-BY author grant).
4. Overleaf DAS paragraph if DOI exists.
5. GitHub: pushed / patch-only-on-B / not attempted.
6. Confirmation that silver jsonl, ads, and Qwen base weights were not uploaded.
