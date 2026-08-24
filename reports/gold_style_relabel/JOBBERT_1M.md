# JobBERTa-zh 1M mid-rung corpus (not paper numbers)

Corpus: `data/jobbert_1m_sents.jsonl` (1,000,000 unique sentences).  
Sources: the two totals under `chineseskillspan-jobert-pretrain/`.  
Leak filter: exact train + dev + test + Gold v2 sentences dropped (20,603).  
Did not overwrite `train.json` or Gold v2.

## Mix decision

Follow **corpus train** (应届生 59.06% / 人工智能 40.94%).  
Do **not** match Gold/test: those are 人工智能 + 阿里云 + 事业单位, and 应届生 is absent. 事业单位 / 阿里云 DAPT is a later corpus step.

MLM is **standard token masking** (HF whole-word mask cannot batch this local BertTokenizer’s offset_mapping; first Slurm job died on that). Method still matches Zhang JobBERTa (RoBERTa + job-ad MLM).

Launch (adasparse Python, 2-GPU DDP when `CUDA_VISIBLE_DEVICES` has two cards):

```bash
CUDA_VISIBLE_DEVICES=0,1 bash Chinese_skill_benchmark_Paper/scripts/run_jobbert_zh_1m.sh
```
