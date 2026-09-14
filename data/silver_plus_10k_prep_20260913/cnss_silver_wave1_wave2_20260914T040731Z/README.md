# Chinese-SkillSpan wave1 + wave2 候选 Silver 数据包

完成情况：wave1 与 wave2 各1810条、73批，共3620条、146批。两波标注调用已结束；wave3的1816条尚未标注，不在本包中。

## 训练入口

`data/train_candidates_3407.jsonl`：3407条模型候选记录，已排除全部213条待裁决记录。其中2383条有技能跨度，1024条为空跨度的负例。不要无意丢弃这些负例。

`data/all_candidates_3620.jsonl`：全部3620条，包含待裁决项，用于归档与复核；不建议直接将此文件全部作为确定标签训练。

`review/adjudication_required_213.jsonl`：213条完整待裁决记录，共254项争议。未决类型中的S仍是占位值。本次不更改标签或替用户裁决。

## 格式

UTF-8 JSONL，每行一个完整JSON对象：id、text、spans、status、note、issues。原文逐字符保留。spans元素为start、end、text、label；start/end是从0开始、左闭右开的Unicode码点偏移，满足Python `text[start:end] == span['text']`，不是UTF-8字节位置或JavaScript UTF-16位置。标签为L/K/S/T。负例spans为空数组。未做分词、BIO转换或训练/验证/测试切分。

新增text字段由对应输入按ID精确连接。公开原始输出schema位于support/output_schema.json，它对应批次的records封装格式；本包JSONL每行是带原文的单条记录，不能直接拿整个JSONL去验证该批次schema。

## 核验与来源

3620个唯一ID，无完全重复文本，与保留2500条ID交集为0。146批schema、ID顺序、原文切片、偏移、非重叠、状态及来源映射校验通过。train文件与review文件不相交，并完整覆盖all文件。JSONL写出后逐条回读一致。

固定源提交：e09f608964f3510d5de4a62e5f6d96472904556c。公开提示词SHA-256：b6223e9a2e9b02afa19cba79ba908766d9240acb233723fbe6f53b40e6b04fd6。每条来源在source_mapping.jsonl；原始及校验后批次输出、校验记录、更正记录和两波完成报告在provenance/。所有包内文件校验值见CHECKSUMS.sha256，原始来源文件的读入快照见provenance/source_snapshot.json。

这些仍是模型候选Silver，尚未经过人工准确率验收。上游“3M之外”、与项目Gold/正式验证测试集的排除证据未在此包中核验；本包不声称完成该项项目级审计。本次只打包，不运行训练、不改已有实验划分、不修改源仓库、不推送或上传数据。
