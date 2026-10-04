# Annotation roles and IAA50 membership

This revision clarifies how the benchmark's annotation layers are used. Human-finalized Gold150 labels provide the primary diagnostic model reference. Silver labels support training, checkpoint selection and supplementary generated-target agreement checks. The independent three-annotator study measures application of the final handbook; its individual layers are not adjudicated model-test labels.

The latest individual exports give mean typed exact F1 0.818, boundary F1 0.850, character alpha 0.907 and 34/50 fully agreed sentence-level span sets (11 empty). These results are unchanged by this revision. Earlier counts of 21/50 with 10 empty belong to the previous export snapshot.

## Membership of the formal agreement sample

| Frozen input | Identical IAA50 sentences |
|---|---:|
| B2 training (2,150) | 0 |
| B2 development (169) | 0 |
| Gold150 | 0 |
| Adopted expanded training | 46 |
| Adopted expanded validation | 2 |
| Adopted expanded Silver test | 1 |
| Alternative expanded training | 46 |
| Alternative expanded validation | 2 |
| Alternative expanded Silver test | 1 |

The checks agree by source ID, exact complete text, NFC and NFKC/whitespace/case normalization. The [audit and reproduction script](iaa50_split_audit/README.md) identify the frozen inputs and distinguish exact-sentence from source-document membership. The complete expanded inputs require authorized access and are not bundled here.

These intersections do not invalidate independent human coding with machine and peer labels hidden. They do prevent simply reclassifying the sample as an unseen test for the already trained expanded models. Later adjudication or removal from an input file cannot erase prior training exposure. A future evaluation requires frozen human targets and exposure checks for each evaluated model, including development and prompt examples. This revision performs no adjudication, retraining or new model scoring.

## Published precedents

[SkillSpan](https://aclanthology.org/2022.naacl-main.366/) uses expert human span annotation. [Kompetencer](https://aclanthology.org/2022.lrec-1.46/) combines human coarse spans with remotely assigned fine-grained labels; its English test labels remain Silver, whereas the Danish test labels were corrected. These examples support explicit distinctions between targets, not a blanket assertion that all benchmark labels must have the same origin.

[Current manuscript](../manuscript_revision_20261002/README.md) · [Latest individual annotations](../agreement/finalguide_abc_20261003/README.md) · [Earlier source-document checks](../major_revision_20261004/README.md)
