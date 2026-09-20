# Data sources and collection

Chinese-SkillSpan combines recruitment texts obtained through three acquisition routes:

| Route | Source | Acquisition |
|---|---|---|
| Commercial collections | [MacroData (马克数据网)](https://www.macrodatas.cn/), operated by 重庆马禾锐信息科技有限公司 | Purchased recruitment collections |
| Research-team collection | Public recruitment pages across regions of China | Researcher-selected URLs and scheduled web collection |
| Hosted dataset | [招聘数据集 / Recruitment Dataset, ID 163746](https://tianchi.aliyun.com/dataset/163746/) on Alibaba Cloud Tianchi | Dataset obtained through the Tianchi platform |

## Public-institution recruitment collection

Team members manually identified recruitment pages on government and public-sector portals, university and hospital websites, and public recruitment platforms. They registered the selected URLs in a crawling framework, which revisited these sources on weekly or monthly schedules. Retrieved records retained announcement titles, source names, source URLs, listed publication dates, and geographic metadata where available. The records were subsequently screened and cleaned to construct the public-institution subset.

A recruitment platform may host or repost an announcement from another institution. Source names and retrieval URLs are therefore retained separately. Listed publication dates describe the announcements, not the dates on which the crawler retrieved them.

## Citation and scope

Use the MacroData platform name and the specific Tianchi dataset page when describing acquisition. The Tianchi title above is provided in Chinese with an English translation; the platform is not asserted to be the original collector. The research-team collection is described in the manuscript Methods.

Acquisition routes and the manuscript's four source collections describe different aspects of the corpus. This overview does not establish the source composition of every pretraining or experimental split. Use the corresponding experiment manifests for sample identity and split membership.

Source attribution does not change access or reuse permissions. Consult [data access](../DATA_AVAILABILITY.md) and the applicable source terms. This documentation update does not add raw vendor exports, crawler archives, or complete expanded-Silver training texts to the public repository.
