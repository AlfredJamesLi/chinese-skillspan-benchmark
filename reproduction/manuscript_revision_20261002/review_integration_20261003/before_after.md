# 主要修改前后对照

以下为源文件原文对照，保留LaTeX标记便于定位。实验结果与统计公式未改。摘要Results已在本轮前一步改好，本次整合保持其内容。

## W01

文件：`0main.tex`

**修改前**

```tex
A Chinese competency extraction benchmark must preserve source wording while addressing ambiguous span boundaries, coordination, and context-dependent categories.
```

**修改后**

```tex
Chinese job advertisements express competencies through coordinated phrases and context-dependent terms. Comparing extraction systems requires consistent decisions about their character boundaries and types.
```

## W04

文件：`0main.tex`

**修改前**

```tex
Original-text spans, a versioned handbook, and distinct human and Silver annotation layers support interpretable model comparisons and analysis of extraction errors.
```

**修改后**

```tex
Chinese-SkillSpan pairs source-text spans with explicit annotation rules and separate human and Silver labels, enabling model comparisons and inspection of boundary and type errors.
```

## W05

文件：`1Introduction.tex`

**修改前**

```tex
Skill-demand analysis and job--curriculum matching require both the requested competency and the words used to express it~\citep{bhola2020retrieving,gnehm2022skills}. Job Skill Named Entity Recognition (JobSkillNER) identifies these mentions and assigns a type to each span. Keeping the source wording allows readers to inspect decisions that a document-level skill inventory would conceal.
```

**修改后**

```tex
Document-level methods retrieve skills from predefined inventories~\citep{bhola2020retrieving}, whereas span extraction locates the words expressing a requirement~\citep{gnehm2022skills}. Job Skill Named Entity Recognition (JobSkillNER) identifies these mentions and assigns a type to each span. Keeping the source wording makes boundary and type assignments available for inspection.
```

## W06

文件：`1Introduction.tex`

**修改前**

```tex
The study asks three questions. How should Chinese mentions be delimited and typed when coordination, omitted predicates, and context defeat a word-based inventory? The handbook provides source-contiguous spans and positive and negative cases. What evidence supports the annotations? Independent blinded coding by three annotators is assessed separately from historical coding and assisted Silver review, with each layer's versions retained. How do models behave under these conventions? Matched Qwen adaptation, Chinese-supervised encoders, and boundary/type diagnostics examine performance on the frozen human reference.
```

**修改后**

```tex
The study addresses three linked questions: how to delimit and type Chinese competency mentions, how consistently annotators apply those rules, and how extraction models perform under the resulting conventions. The handbook supplies boundary and context rules with positive and negative examples. A separate three-annotator blinded study measures agreement under the final handbook, while historical coding and assisted review document reference construction and Silver quality checks. Matched Qwen adaptation and Chinese-supervised encoder comparisons assess model performance, with diagnostics for type, span length, and empty-reference sentences.
```

## W09

文件：`5Relatedwork.tex`

**修改前**

```tex
Chinese NER benchmarks address social media and fine-grained entity typing~\citep{peng2015weibo,cluener2020}, while multilingual benchmarks include noisy inputs and contextual type distinctions~\citep{multiconer2023,dynamicner2025}. The absence of explicit word delimiters makes boundary decisions especially consequential for Chinese extraction~\citep{chen2021boundary}. Domain-specific guidance can address additional problems: \citet{zhong2023bertspan}, for example, develop a rehabilitation-medicine corpus and investigate long and nested entities with BERT-Span. In recruitment text, annotators must also decide whether an expression denotes knowledge, an occupational action, or a transversal competence in its particular clause.
```

**修改后**

```tex
Chinese NER resources cover social-media text~\citep{peng2015weibo} and fine-grained entity categories~\citep{cluener2020}. Multilingual studies examine recognition in noisy text~\citep{multiconer2023} and changes in contextual entity types~\citep{dynamicner2025}. These tasks provide useful background, but do not specify how recruitment requirements should be divided into LSKT spans. Chinese boundary detection is complicated by the absence of explicit word delimiters~\citep{chen2021boundary}; recruitment annotation additionally distinguishes knowledge, occupational actions, and transversal competences within each clause.
```

## W20

文件：`2Framework.tex`

**修改前**

```tex
Human coding and model-assisted review address different quality questions. Independent coding tests whether annotators can apply the rules without a suggested answer; review checks labels proposed by a model. Historical coding informed the handbook and human reference, while the separate three-annotator study assesses independent blinded agreement under the final handbook. For the original Silver set, an initial sample was reviewed before bulk generation. Automated checks verified substrings, offsets, labels, and coverage; human review addressed interpretation.
```

**修改后**

```tex
Historical human coding informed the handbook and the frozen reference. For the original Silver set, an initial sample of model-proposed labels was reviewed before bulk generation. Automated checks verified substrings, offsets, labels, and coverage; human review addressed interpretation.
```

文件：`tex/annotation_quality_R12.tex`

**修改前**

```tex
Agreement must be measured without shared suggestions if it is to assess how consistently annotators apply the handbook. We therefore report the independent blinded study in Table~\ref{tab:quality-main}. Historical coding and assisted-review studies used different samples and rules; their scores cannot be read as a longitudinal improvement in independent reliability (\hyperref[app:b]{Appendix B}).
```

**修改后**

```tex
Independent coding assesses whether annotators can apply the handbook without machine or peer suggestions; assisted review evaluates proposed labels. We report final-handbook agreement from the separate three-annotator blinded study (Table~\ref{tab:quality-main}). Historical coding and review used different samples and handbook versions (\hyperref[app:b]{Appendix B}), so their scores do not measure a longitudinal change in independent reliability.
```

## W21

文件：`2Framework.tex`

**修改前**

```tex
Human coding and model-assisted review address different quality questions. Independent coding tests whether annotators can apply the rules without a suggested answer; review checks labels proposed by a model. Historical coding informed the handbook and human reference, while the separate three-annotator study assesses independent blinded agreement under the final handbook. For the original Silver set, an initial sample was reviewed before bulk generation. Automated checks verified substrings, offsets, labels, and coverage; human review addressed interpretation.
```

**修改后**

```tex
Historical human coding informed the handbook and the frozen reference. For the original Silver set, an initial sample of model-proposed labels was reviewed before bulk generation. Automated checks verified substrings, offsets, labels, and coverage; human review addressed interpretation.
```

文件：`tex/annotation_quality_R12.tex`

**修改前**

```tex
Agreement must be measured without shared suggestions if it is to assess how consistently annotators apply the handbook. We therefore report the independent blinded study in Table~\ref{tab:quality-main}. Historical coding and assisted-review studies used different samples and rules; their scores cannot be read as a longitudinal improvement in independent reliability (\hyperref[app:b]{Appendix B}).
```

**修改后**

```tex
Independent coding assesses whether annotators can apply the handbook without machine or peer suggestions; assisted review evaluates proposed labels. We report final-handbook agreement from the separate three-annotator blinded study (Table~\ref{tab:quality-main}). Historical coding and review used different samples and handbook versions (\hyperref[app:b]{Appendix B}), so their scores do not measure a longitudinal change in independent reliability.
```

## W32

文件：`3Experiments.tex`

**修改前**

```tex
 These findings support retaining both span-level and character-level agreement measures.
```

**修改后**

```tex
(删除重复句；相应事实保留在其专门章节)
```

## W41

文件：`tex/appendix_A_guide_R19.tex`

**修改前**

```tex
Figure~\ref{fig:illustrative-annotations} and Tables~\ref{tab:guide-types}--\ref{tab:guide-scope} illustrate current decisions; they are teaching materials rather than a relabeling of historical data.
```

**修改后**

```tex
Figure~\ref{fig:illustrative-annotations} reproduces frozen v4.2.10 human-reference annotations, whereas Tables~\ref{tab:guide-types}--\ref{tab:guide-scope} illustrate decisions under the current v4.2.14 handbook. Later rule amendments do not retrospectively alter the historical annotations or reported scores.
```

## W56

文件：`tex/external_benchmarks/paper_A_native.tex`

**修改前**

```tex
For Kompetencer, MaChAmp used a 20-epoch budget
```

**修改后**

```tex
For Kompetencer, we compared DaJobBERT with RemBERT~\citep{chung2021rembert}. MaChAmp used a 20-epoch budget
```

文件：`tex/external_benchmarks/paper_A_native.tex`

**修改前**

```tex
DaJobBERT resolved to an uncased checkpoint, and the metric differs from the original weighted score; neither detail supports a matched replication claim.
```

**修改后**

```tex
The recorded DaJobBERT initialization is \href{https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/blob/b84f218b7142c97ab03a60499a9b30e7ec332cab/results_snapshots/a_native_20260924/A_NATIVE_RECEIPT.md}{\texttt{jjzha/dajobbert-base-uncased}}; the linked receipt retains its full revision. Together with the unweighted metric, this makes the experiment a task-specific rerun rather than a matched reproduction of the original cased setting.
```

## 文献元数据及任务出处

- `multiconer2023`（R14）：已核对并修正元数据。
- `gnehm2022transfer`（R16）：新增方法或数据出处。
- `cluener2020`（R40）：已核对并修正元数据。
- `hu2022lora`（N01）：新增方法或数据出处。
- `qwen2025report`（N02）：新增方法或数据出处。
- `chung2021rembert`（N03）：新增方法或数据出处。