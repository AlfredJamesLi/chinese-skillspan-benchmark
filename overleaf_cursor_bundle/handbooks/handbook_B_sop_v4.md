# 手册 B — LSKT v4 SOP（论文主协议）· 一页

**手册版本：** `B.sop_v4.1`（2026-08-28）。重叠裁决见 `handbook_B_overlap_adjudication.md`；规则日志 `LSKT_V4_RULE_CHANGELOG.md`。新 LLM 提示词：`prompts/LSKT_V4_ANNOTATION_PROMPT.txt`。

**用途：** 论文 **主评测** 的操作性定义（短跨度、禁半词、jieba 词边界）。绑定：训练银标 `train_lskt_v4_silver`；测试金标 `data/test_lskt_v4_cws_simhuman980_hybrid.jsonl`（2601 = **980 SimHuman rule_v4** + **1621 SOP-CWS**，与 Gold v2 **同一批 ID**，预测与金标都 jieba snap）。  
**不是** 人工 Doccano Gold，**不要覆盖** `gold_canonical_v2.jsonl`。980 句是规则叠加，不是按本手册做完的全量人标。

**LLM：** P2 主表仍用**旧 dump** 事后 jieba，不是官方 `gpt-4o` 的 SOP 重呼。SOP extract 提示词（`PROMPT_gpt4o_sop_extract.txt`）与本手册一致，只作诊断表。

## 标签（仍是四类；评测可投影）

| 标签 | 含义 | 例 | 投影到 Zhang |
|---|---|---|---|
| L | 语种词（不是证书） | 英语、英文、普通话 | → KNOWLEDGE |
| K | 学历、专业、**证书**、领域知识 | 本科及以上学历、计算机专业、**大学英语6级** | → KNOWLEDGE |
| S | 工具、方法、可执行职业技能 | Python、Excel、维护、测试 | → SKILL |
| T | 软技能、特质 | 沟通能力、责任心、抗压能力 | → SKILL |

## 跨度（短、完整、原文）

1. 连续原文；禁止半词（`支持服`、`操作系统的问`）。  
2. **短而独立，优先 2–8 字/token**：`Python`、`计算机专业`、`沟通能力`。不要整段岗位职责一条 S。  
3. 顿号/逗号/「和、与、或」连接的能力 **各自一条**。  
4. 「熟悉 / 掌握 / 了解 / 精通 / 具备」**只标后面的对象**，不标这些动词。  
5. 编程语言、框架、办公软件、具体工具 → **S**。不要把 Spring/Python 标成 K。  
6. 大学英语6级等英语**等级证书 → K**；光秃「英文」才是 **L**。  
7. 报名、体检、公示、资格审查、福利、五险一金、班次、地点、鸡汤 → **空句** `spans: []`。  
8. 不标：形象外貌、身体健康、年限数字（只留能力本身）、非司机岗驾照。  
9. 平坦不重叠。一条跨度一个类型。L–K–S–T 只是口诀，**不是**优先级；禁止 `L > S > K > T`。  
10. `SQL`：岗位里可执行使用 → **S**；明确要求原理/理论 → **K**。  
11. 人工字符偏移是权威（`sentence[start:end] == span`）。jieba 只做校验或派生视图，不是标注员，也不自动生成 Gold。潜在同界/嵌套/交叉写入裁决日志，**不要**写进主层 Gold。详见 `handbook_B_overlap_adjudication.md`。

## 对照例

| 句 | 手册 B | 不要 |
|---|---|---|
| 熟悉使用Word，Excel，PPT等办公软件 | Word S，Excel S，PPT S | 标「熟悉使用」；或收成一条长 S |
| 本科及以上学历，大学英语6级 | 两段都 **K** | 六级标 L |
| 维护和支持服务 | `维护` S + `支持服务` S（或完整词边界） | `支持服` |
| 五险一金，带薪年假 | `[]` | 硬标福利 |

**主结果（仅 P2）：** JobBERT 3M v4+jieba typed exact **0.4331**；冻结 ChatGPT dump+jieba exact **0.2854** / relaxed **0.6249**。禁止写成「超过 Gold v2 上的 ChatGPT 0.6365」。
