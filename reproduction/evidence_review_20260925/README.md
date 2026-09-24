# Chinese-SkillSpan evidence review — 25 September 2026

This release accompanies the evidence-focused manuscript revision. It separates executed verification from outstanding annotation-history questions. It is not a new training run or a new blind annotation study.

## Chinese supervised encoder baselines (stable label `tab:external-chinese`)

The [pinned server audit](https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/tree/0c73207c0f9b00fa87f385b78bcb7342bd00bfcb/results_snapshots/table11_evidence_20260924) supplies six prediction files, actual training code, configurations, selection histories and checkpoint re-inference outputs. It calls the result Table 11 because that was the earlier manuscript number; this is Table 9 in the current revision.

[Local verification](CHINESE_ACCEPTANCE.json) rescored all six runs with cnss-lskt-1.2.0 and exactly reconstructed the reported metrics. Original Chinese texts and all Gold150 offsets were checked. Frozen B2 2,150/169 data hashes and NFC text isolation were checked; advertisement-level isolation is not established. Both encoders were fine-tuned with fresh BIO heads, without translation or English task-head transfer.

The ESCOXLM-R minus XLM-R exact-F1 difference is 0.016; a new paired sentence-bootstrap interval is [-0.003, 0.034] (10,000 draws, seed 20260924, fixed three training seeds). This post hoc interval includes zero. The two models' mean exact F1 remains 0.538 and 0.522. Do not interpret this as a significant advantage or compare macro-F1 with another model's micro-F1.

The six [public checkpoints](https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/blob/0c73207c0f9b00fa87f385b78bcb7342bd00bfcb/results_snapshots/table11_evidence_20260924/HF_RELEASE.md) were checked through live Hugging Face metadata and configurations; Hub weight digests match the release index. The [Zenodo audit deposit](https://doi.org/10.5281/zenodo.22937245) contains sidecars and evidence, not the multi-gigabyte weights. [Access verification](RELEASE_ACCESS.json) records exact Hub revisions. Local verification did not download/load weights or rerun training. Server re-inference files were compared to original predicted tags and matched.

## Annotation evidence

[Historical annotation layers](annotation_layers/README.md) are released with pseudonymized reviewer identities. [Existing blind coding verification](EXISTING_BLIND_IAA.json) reproduces the early 50-sentence study: 98 matches between 230 and 211 spans, F1 0.444 and character kappa 0.567. This work was not absent and must not be requested again merely because its audit was incomplete.

[Cohort reconciliation](COHORT_RECONCILIATION.json) distinguishes sample membership from repeated exports and stages. The author reports additional review stages whose exact file correspondence remains open. The author corrected the 15-sentence subset design: machine coding suggestions were available. Its perfect agreement is an assisted-review result, not blind reliability evidence. No extra human work is certified here. [Version compatibility](VERSION_COMPATIBILITY.md) records the named R23 difference and full candidate screening without claiming full semantic validation.

## Reproduction and claim boundaries

See [the paper-to-file index](../PAPER_INDEX.md) for current numbering, and [the existing process archive](../process_archive_20260924/README.md) for older table captions, individual seeds, selected epochs, and historical configurations. Qwen fixed-protocol adaptation is an end-to-end comparison; historical JobBERT supervision/selection and expanded-pool runs change multiple factors. External native-task results retain their own metrics and releases. No new independent test or all-model fair ranking is claimed.

## Execute the CPU check

Install NumPy, obtain the pinned server-audit folder linked above, then run `python rescore_chinese.py AUDIT_FOLDER OUTPUT_FOLDER`. The [portable script](rescore_chinese.py) was executed locally against all six files; its rebuilt metrics and interval match the published verification. It requires no model weights, GPU, or account credentials.
