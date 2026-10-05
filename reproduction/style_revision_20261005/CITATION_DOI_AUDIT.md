# Citation and DOI audit

Verified: 2026-10-05T14:26:37.505679+00:00

## Outcome

- Checked all 68 bibliography entries; 45 are cited by the active manuscript. There are no undefined active citation keys.
- The three questioned 2026 publications exist in ACL Anthology and their current authors, titles, years, pages and DOIs match.
- All four active Zenodo DOIs resolve through the official API and their descriptions/file inventories match the roles stated in the paper. The concept DOI resolves to latest repository snapshot 22846011, as expected; the paper separately cites dataset v0.1.3.
- Three historical Zenodo records also exist and were checked separately.
- Only 9Reference.bib was edited by this audit. No scientific claims, names of experimental models, results, or artifact identifiers were changed.

## Changes

- `peng2015weibo`: Add verified publisher and permanent identifiers. Source: https://aclanthology.org/D15-1064/
- `chen2024jobsdf`: Complete the official NeurIPS proceedings page range and publisher. Source: https://proceedings.neurips.cc/paper_files/paper/2024/file/e997325c6f4045aa646c81e674076297-Bibtex-Datasets_and_Benchmarks_Track.bib
- `spanmarker`: Replace the stale URL, which returned HTTP 404, with the author-maintained repository. This entry is not cited in the active manuscript. Source: https://github.com/tomaarsen/SpanMarkerNER
- `spanmarker`: The author-maintained repository links the thesis; record the actual verification date. Source: https://github.com/tomaarsen/SpanMarkerNER
- `gollie2024`: Use the accessible official proceedings page; preserve the already verified volume, pages, and PDF-supported full author name. Source: https://proceedings.iclr.cc/paper_files/paper/4265-/bibtex
- `universalner`: Complete page metadata supplied by the official ICLR proceedings, consistently with GoLLIE. Source: https://proceedings.iclr.cc/paper_files/paper/2024/hash/34678d08b36076de986df95c5bbba92f-Abstract-Conference.html
- `landis1977measurement`: Add verified DOI to the uncited retained bibliography entry. Source: https://www.jstor.org/stable/i323041
- `liu2022cnership`: Replace the internal subject annotation with a verified DOI in this uncited retained entry. Source: https://api.crossref.org/works/10.1109%2FTKDE.2020.2981314

## Questioned 2026 references

| Entry | Verified pages | Official source |
|---|---|---|
| Kim et al. |37951–37964|https://aclanthology.org/2026.acl-long.1760/|
| Ul Haq et al. |524–548|https://aclanthology.org/2026.lrec-1.37/|
| De Santo et al. |877–885|https://aclanthology.org/2026.eacl-industry.65/|

## Every bibliography entry

| Key | Cited | Status / note | Source |
|---|---|---|---|
| `ILO_2020_OJVs_BigData` | Yes | verified Official PDF retrieved again; title, 2020 imprint, International Labour Office and volume editors are also verified in the same-day resource audit (resource_evidence/official_resources_audit.md). | https://www.ilo.org/sites/default/files/wcmsp5/groups/public/%40ed_emp/%40emp_ent/documents/publication/wcms_759330.pdf; https://www.ilo.org/sites/default/files/wcmsp5/groups/public/%40ed_emp/%40emp_ent/documents/publication/wcms_759330.pdf |
| `zhang2022skillspan` | Yes | verified The official PDF confirms the existing full middle names omitted by the abbreviated ACL-export metadata; no author change needed. | https://aclanthology.org/2022.naacl-main.366.bib |
| `smallm` | No | verified Crossref confirms2025,11(11),article460; last author deposited as Jiarui Lin while retained entry uses Jia-Rui Lin. Not a different person; full name orthography left unchanged. Uncited. | https://api.crossref.org/works/10.1007%2Fs40747-025-02074-6 |
| `oliveira` | No | verified Crossref distinguishes online2024 from print2025; current2025/volume33/pages361–381 match the print issue. Uncited. | https://api.crossref.org/works/10.1007%2Fs10506-023-09388-1 |
| `landis1977measurement` | No | verified; corrected/completed Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://api.crossref.org/works/10.2307%2F2529310 |
| `jensen2021deidentification` | No | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://aclanthology.org/2021.nodalida-main.21.bib |
| `ESCOv1_2_2024` | Yes | verified Official classification page resolves. The official ESCO version-history page confirms May 2024 release of v1.2.0. Its classification application may still display a temporary-error notice; this does not invalidate the bibliographic identity. | https://esco.ec.europa.eu/en/classification/skill_main; https://esco.ec.europa.eu/es/node/188 |
| `council2017eqf` | Yes | verified in earlier same-day audit; fresh content access unconfirmed This request returned a JavaScript/202 response. Exact title, OJ C189, pages15–28 and CELEX were verified in the earlier same-day official-resource audit; retain citation. Fresh direct content access remains unconfirmed. | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32017H0615(01); https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32017H0615(01) |
| `levrang2014esco` | Yes | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://api.crossref.org/works/10.1109%2FMC.2014.283 |
| `peng2015weibo` | Yes | verified; corrected/completed Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://aclanthology.org/D15-1064.bib |
| `cluener2020` | Yes | verified arXiv v4 confirms title and 2020 version. Official author display is Yu tong; retain the literal instead of guessing name order. | https://arxiv.org/abs/2001.04351v4 |
| `multiconer2023` | Yes | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://aclanthology.org/2023.semeval-1.310.bib |
| `liu2022cnership` | No | verified; corrected/completed Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://api.crossref.org/works/10.1109%2FTKDE.2020.2981314 |
| `globalpointer` | No | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://github.com/bojone/GlobalPointer |
| `spanmarker` | No | verified; corrected/completed Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://github.com/tomaarsen/span-marker; https://github.com/tomaarsen/SpanMarkerNER |
| `conneau2020xlmr` | Yes | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://aclanthology.org/2020.acl-main.747.bib |
| `gliner-naacl24` | Yes | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://aclanthology.org/2024.naacl-long.300.bib |
| `instructuie` | No | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://arxiv.org/abs/2304.08085 |
| `universalner` | Yes | verified; corrected/completed Official ICLR page confirms five authors,2024,volume2024,pages12276–12294. | https://proceedings.iclr.cc/paper_files/paper/2024/hash/34678d08b36076de986df95c5bbba92f-Abstract-Conference.html |
| `esco` | No | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://esco.ec.europa.eu/ |
| `senger2024survey` | Yes | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://aclanthology.org/2024.nlp4hr-1.1.bib |
| `cmner2024` | No | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://arxiv.org/abs/2402.13693 |
| `jensen2022kompetencer` | Yes | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://aclanthology.org/2022.lrec-1.46.bib |
| `mao2024legalner` | No | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://api.crossref.org/works/10.7717%2Fpeerj-cs.2428 |
| `bhola2020retrieving` | Yes | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://aclanthology.org/2020.coling-main.513.bib |
| `gnehm2022skills` | Yes | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://aclanthology.org/2022.nlpcss-1.2.bib |
| `sayfullina2018softskills` | Yes | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://api.crossref.org/works/10.1007%2F978-3-030-11027-7_15 |
| `zhang2022weak` | Yes | verified CEUR official proceedings and PDF confirm author order,title,workshop,year2022,volume3218; PDF is9pages without a printed continuous page range, so none invented. | https://ceur-ws.org/Vol-3218/RecSysHR2022-paper_10.pdf; https://ceur-ws.org/Vol-3218/ |
| `nguyen2024rethinking` | Yes | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://aclanthology.org/2024.nlp4hr-1.3.bib |
| `chen2021boundary` | Yes | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://aclanthology.org/2021.acl-short.4.bib |
| `devlin2019bert` | Yes | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://aclanthology.org/N19-1423.bib |
| `lafferty2001crf` | Yes | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://repository.upenn.edu/cis_papers/159 |
| `gururangan2020dapt` | Yes | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://aclanthology.org/2020.acl-main.740.bib |
| `ramponi2020domain` | No | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://aclanthology.org/2020.coling-main.603.bib |
| `dynamicner2025` | Yes | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://aclanthology.org/2025.emnlp-main.835.bib |
| `uie2022` | Yes | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://aclanthology.org/2022.acl-long.395.bib |
| `gollie2024` | Yes | verified; corrected/completed Official ICLR BibTeX confirms volume2024/pages47083–47107. PDF-supported Oier Lopez de Lacalle retained although metadata shortens the name. OpenReview browser challenge is not a missing publication. | https://openreview.net/forum?id=Y3wpuxd7u9; https://proceedings.iclr.cc/paper_files/paper/4265-/bibtex |
| `gptner2025` | Yes | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://aclanthology.org/2025.findings-naacl.239.bib |
| `ding2023annotator` | Yes | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://aclanthology.org/2023.acl-long.626.bib |
| `li2023coannotating` | Yes | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://aclanthology.org/2023.emnlp-main.92.bib |
| `tan2024llmannotation` | No | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://aclanthology.org/2024.emnlp-main.54.bib |
| `gilardi2023chatgpt` | No | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://api.crossref.org/works/10.1073%2Fpnas.2305016120 |
| `kim2026guidelines` | Yes | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://aclanthology.org/2026.acl-long.1760.bib |
| `ulhaq2026nerannotation` | Yes | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://aclanthology.org/2026.lrec-1.37.bib |
| `bender2018datastatements` | Yes | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://api.crossref.org/works/10.1162%2Ftacl_a_00041 |
| `gebru2021datasheets` | Yes | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://api.crossref.org/works/10.1145%2F3458723 |
| `artstein2008agreement` | Yes | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://api.crossref.org/works/10.1162%2Fcoli.07-034-R2 |
| `chen2024jobsdf` | Yes | verified; corrected/completed Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://api.crossref.org/works/10.52202%2F079017-4109; https://proceedings.neurips.cc/paper_files/paper/2024/file/e997325c6f4045aa646c81e674076297-Bibtex-Datasets_and_Benchmarks_Track.bib |
| `magron2024jobskape` | Yes | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://aclanthology.org/2024.nlp4hr-1.4.bib |
| `desanto2026skilllens` | Yes | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://aclanthology.org/2026.eacl-industry.65.bib |
| `zhong2023bertspan` | No | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://api.crossref.org/works/10.7717%2Fpeerj-cs.1535 |
| `Finkel2009` | No | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://aclanthology.org/D09-1015.bib |
| `Yu2020` | No | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://aclanthology.org/2020.acl-main.577.bib |
| `cao2021occupational` | Yes | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://api.crossref.org/works/10.1371%2Fjournal.pone.0253308 |
| `macrodataPlatform` | Yes | verified Official website returned HTTP200 with Chinese platform title. Its rendered dataset catalogue and source permissions were not audited here. | https://www.macrodatas.cn/ |
| `tianchiRecruitment163746` | Yes | verified Official page title identifies 招聘数据集 (Recruitment Dataset), ID163746. The translation note is transparent, not evidence of a fabricated title. Dataset licensing/access is outside this bibliographic check. | https://tianchi.aliyun.com/dataset/163746/ |
| `zhang2023escoxlmr` | Yes | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://aclanthology.org/2023.acl-long.662.bib |
| `zhang2024nnose` | Yes | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://aclanthology.org/2024.eacl-long.35.bib |
| `green2022benchmark` | No | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://aclanthology.org/2022.lrec-1.128.bib |
| `beauchemin2022fijo` | No | verified Crossref confirms authors,title,2022 and DOI; official metadata provides no continuous page range. Article identifier2022L34 retained. Uncited. | https://api.crossref.org/works/10.21428%2F594757db.858dd91f |
| `joshi2020spanbert` | No | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://aclanthology.org/2020.tacl-1.5.bib |
| `vandergoot2021machamp` | No | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://aclanthology.org/2021.eacl-demos.22.bib |
| `klie2024annotationquality` | Yes | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://aclanthology.org/2024.cl-3.1.bib |
| `hripcsak2005agreement` | Yes | verified Crossref omits the second author; publisher-supplied full text in PMC confirms George Hripcsak and Adam S Rothschild. Retain both authors and pages296–298. | https://api.crossref.org/works/10.1197%2Fjamia.M1733; https://pmc.ncbi.nlm.nih.gov/articles/PMC1090460/ |
| `gnehm2022transfer` | No | verified Official publisher/author metadata supports the bibliographic identity; title, author order, year and available page/DOI fields checked. | https://aclanthology.org/2022.lrec-1.414.bib |
| `hu2022lora` | Yes | verified Official Microsoft/LoRA repository citation confirms eight authors,title,ICLR2022 and OpenReview identifier. Browser challenge on the landing page does not invalidate citation. | https://openreview.net/forum?id=nZeVKeeFYf9; https://raw.githubusercontent.com/microsoft/LoRA/main/README.md |
| `qwen2025report` | Yes | verified arXiv v2 dates2025-01-03 support the cited2025 version; v1 was2024. Retain version-specific URL and established Qwen Team corporate attribution. | https://arxiv.org/abs/2412.15115v2 |
| `chung2021rembert` | No | verified Official OpenReview PDF search result confirms five authors,title and ICLR2021. Forum/API returned challenge/403; no DOI or proceedings pages invented. Uncited. | https://openreview.net/forum?id=xpFFI_NtgpW; https://api.openreview.net/notes?id=xpFFI_NtgpW; https://openreview.net/pdf?id=xpFFI_NtgpW |

## Zenodo DOI records

| DOI | Status | Record / role |
|---|---|---|
| 10.5281/zenodo.22288337 | verified | [Chinese-SkillSpan: Repository snapshot for Qwen reproduction (qwen-repro-pack-20260919)](https://zenodo.org/records/22846011) |
| 10.5281/zenodo.22698504 | verified | [Chinese-SkillSpan: Corpus, human reference set, and Silver training/development sets (v0.1.3)](https://zenodo.org/records/22698504) |
| 10.5281/zenodo.22851581 | verified | [Chinese-SkillSpan: Qwen2.5-14B-Instruct LoRA adapters and reproduction materials](https://zenodo.org/records/22851581) |
| 10.5281/zenodo.22942441 | verified | [Chinese-SkillSpan: Reproduction materials for Silver fine-tuned XLM-R and ESCOXLM-R (three seeds)](https://zenodo.org/records/22942441) |
| 10.5281/zenodo.22288338 | verified historical version; not active citation | [Chinese-SkillSpan: A Benchmark for Competency Span Extraction from Chinese Job Advertisements](https://zenodo.org/records/22288338) |
| 10.5281/zenodo.22685143 | verified historical version; not active citation | [Chinese-SkillSpan: A Benchmark for Competency Span Extraction from Chinese Job Advertisements](https://zenodo.org/records/22685143) |
| 10.5281/zenodo.22937245 | verified historical version; not active citation | [Chinese-SkillSpan: Reproduction materials for Silver fine-tuned XLM-R and ESCOXLM-R (three seeds)](https://zenodo.org/records/22937245) |

## Limitations

- Bibliographic identity and metadata audit, not a re-review of every substantive citation claim.
- HTTP200 alone was not counted as sufficient metadata evidence; challenges distinguished from content.
- No checkpoint or dataset archive payloads were downloaded or revalidated in this DOI check.
