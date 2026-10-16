# Chinese-SkillSpan code materials, revision 1 (17 October 2026)

Version `code-materials-20261017.1` extends the original `code-materials-20261017` release, without moving that historical tag. It includes the [server-B addendum and usage guide](../server_b_code_addendum_20261017/README.md), updates the current code-entry inventory, and publishes the [data-access correction](../../docs/data_access_correction_20261017.md). All previous code/material links remain valid. No experimental results, models, datasets or manuscript conclusions are changed.

The previously missing five JobBERT continuation entry files and local dependencies are now included. B-side native configuration files and launchers are supplied, but the received MaChAmp patch is truncated and must not be applied. The original Qwen no-adapter generator, some native-task launch/configuration or upstream-revision bindings, and historical JobBERT/other runtime records remain unresolved. This is an audited source release, not certification of complete end-to-end reproducibility.

Read the addendum's [AUDIT.json](../server_b_code_addendum_20261017/AUDIT.json) for checksum and static-check results. The earlier release's [validation record](../code_release_20261017/VALIDATION.json) describes its own prior checks; it does not certify the new scripts. The companion validator checks current file hashes and documentation links. No training, inference or prediction rescoring was performed for this revision.

Use [CITATION.cff](CITATION.cff) and the resolved commit of tag `code-materials-20261017.1` for this code snapshot. This creates no new DOI and does not change the contents of existing dataset/model Zenodo records. For PeerJ, an accompanying source ZIP may be supplied as a supplemental Dataset with a legend containing the word "code".

Complete expanded recruitment texts and labels are not distributed. Access to third-party texts remains subject to original-provider terms; current source releases may not reproduce the exact historical pools. See [DATA_AVAILABILITY.md](../../DATA_AVAILABILITY.md).
