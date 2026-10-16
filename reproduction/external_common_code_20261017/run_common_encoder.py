"""New controlled token-classification comparison, NOT an exact MaChAmp/NNOSE replication.
Keeps the downloaded native splits and label streams; saves dev-selected models and predictions.
Run on the training server. Imports of GPU libraries are delayed so --help works locally.
"""
from pathlib import Path
import argparse,json,hashlib,random,platform,time,subprocess
from audit_and_lexicon import read,entities,score

def arguments():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--dataset',required=True,choices=['skillspan','kompetencer','gnehm','green','sayfullina','fijo'])
 p.add_argument('--model',required=True);p.add_argument('--revision',required=True,help='Immutable Hugging Face commit SHA')
 p.add_argument('--head',default='tags_skill',choices=['tags_skill','tags_knowledge'])
 p.add_argument('--seed',type=int,default=42);p.add_argument('--epochs',type=int,default=20)
 p.add_argument('--batch-size',type=int,default=8);p.add_argument('--lr',type=float,default=2e-5)
 p.add_argument('--output',type=Path,required=True);p.add_argument('--smoke',action='store_true',help='Training/dev smoke check only; never evaluates test')
 return p.parse_args()

def main():
 a=arguments()
 import torch,numpy as np,transformers
 from transformers import AutoTokenizer,AutoModelForTokenClassification,DataCollatorForTokenClassification,get_linear_schedule_with_warmup
 assert len(a.revision)==40 and all(c in '0123456789abcdef' for c in a.revision),'Use an immutable model revision'
 assert a.epochs>0 and a.batch_size>0
 root=Path(__file__).resolve().parent;data=root/'data'/a.dataset
 manifest=json.loads((data/'download_manifest.json').read_text())
 for f in manifest['files']:assert hashlib.sha256((data/f['path']).read_bytes()).hexdigest()==f['sha256']
 rows={s:read(data/(s+'.json')) for s in ('train','dev','test')}
 assert all(a.head in r for split in rows.values() for r in split)
 labels=sorted({t for r in rows['train'] for t in r[a.head]});ids={t:i for i,t in enumerate(labels)}
 if a.smoke:rows={s:v[:16] for s,v in rows.items() if s!='test'};a.epochs=1
 assert 'O' in ids
 for split in rows.values():assert all(t in ids for r in split for t in r[a.head]),'Unseen label: verify the native label schema'
 a.output.mkdir(parents=True,exist_ok=True)
 assert not (a.output/'config.json').exists(),'Use a new output directory; do not overwrite a run'
 random.seed(a.seed);np.random.seed(a.seed);torch.manual_seed(a.seed)
 if torch.cuda.is_available():torch.cuda.manual_seed_all(a.seed)
 device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')
 assert device.type=='cuda','Run neural experiments on the GPU server, not this laptop'
 torch.backends.cudnn.deterministic=True;torch.backends.cudnn.benchmark=False
 tokenizer=AutoTokenizer.from_pretrained(a.model,revision=a.revision,use_fast=True,add_prefix_space=True)
 model=AutoModelForTokenClassification.from_pretrained(a.model,revision=a.revision,num_labels=len(labels),id2label=dict(enumerate(labels)),label2id=ids).to(device)
 limit=min(512,int(getattr(model.config,'max_position_embeddings',512))-2)
 def encode_split(records):
  pieces=[];meta=[]
  for row,r in enumerate(records):
   start=0
   while start<len(r['tokens']):
    stop=min(start+128,len(r['tokens']))
    while True:
     encoded=tokenizer(r['tokens'][start:stop],is_split_into_words=True,truncation=False)
     if len(encoded['input_ids'])<=limit:break
     assert stop-start>1,'One source token exceeds model limit; needs an explicit protocol'
     stop=start+(stop-start)//2
    wordids=encoded.word_ids();first={}
    for pos,w in enumerate(wordids):
     if w is not None and w not in first:first[w]=pos
    assert set(first)==set(range(stop-start)),'Tokenizer discarded a source word'
    encoded['labels']=[-100]*len(wordids)
    for w,pos in first.items():encoded['labels'][pos]=ids[r[a.head][start+w]]
    pieces.append(dict(encoded));meta.append((row,start,stop,first));start=stop
  return pieces,meta
 encoded={s:encode_split(rs) for s,rs in rows.items()}
 collator=DataCollatorForTokenClassification(tokenizer)
 def loader(items,shuffle=False):
  return torch.utils.data.DataLoader(items,batch_size=a.batch_size,shuffle=shuffle,collate_fn=collator,generator=torch.Generator().manual_seed(a.seed))
 def evaluate(split):
  model.eval();pred=[['O']*len(r['tokens']) for r in rows[split]];cursor=0
  with torch.no_grad():
   for batch in loader(encoded[split][0]):
    outputs=model(**{k:v.to(device) for k,v in batch.items() if k!='labels'}).logits.argmax(-1).cpu().tolist()
    for output in outputs:
     row,start,stop,first=encoded[split][1][cursor];cursor+=1
     for w,pos in first.items():pred[row][start+w]=labels[output[pos]]
  assert cursor==len(encoded[split][1])
  return score([entities(r[a.head]) for r in rows[split]],[entities(p) for p in pred]),pred
 config={**vars(a),'output':str(a.output),'method':'common_encoder_linear_head_native_BIO_first_subword','claim':'new controlled baseline; not exact reproduction of published SOTA',
  'dataset_revision':manifest['revision'],'data_hashes':manifest['files'],'labels':labels,'max_sequence_length':limit,'chunk_word_limit':128,
  'split_counts':{s:len(v) for s,v in rows.items()},'chunk_counts':{s:len(v[0]) for s,v in encoded.items()},
  'selection':'highest dev strict span/type micro-F1; earliest epoch wins ties','test_used_for_selection':False,
  'python':platform.python_version(),'torch':torch.__version__,'transformers':transformers.__version__,
  'gpu':torch.cuda.get_device_name(0),'cuda':torch.version.cuda,'started_unix':time.time()}
 (a.output/'config.json').write_text(json.dumps(config,indent=2),encoding='utf-8')
 train=loader(encoded['train'][0],shuffle=True);steps=len(train)*a.epochs
 optimizer=torch.optim.AdamW(model.parameters(),lr=a.lr,weight_decay=.01)
 scheduler=get_linear_schedule_with_warmup(optimizer,int(.1*steps),steps)
 best=-1;history=[]
 for epoch in range(1,a.epochs+1):
  model.train();losses=[]
  for batch in train:
   optimizer.zero_grad();loss=model(**{k:v.to(device) for k,v in batch.items()}).loss
   assert torch.isfinite(loss);loss.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),1.0)
   optimizer.step();scheduler.step();losses.append(loss.item())
  metrics,_=evaluate('dev');history.append({'epoch':epoch,'train_loss':float(np.mean(losses)),'dev':metrics})
  print(json.dumps(history[-1]),flush=True)
  if metrics['f1']>best:
   best=metrics['f1'];best_epoch=epoch;model.save_pretrained(a.output/'best');tokenizer.save_pretrained(a.output/'best')
  (a.output/'history.json').write_text(json.dumps(history,indent=2),encoding='utf-8')
 del model;torch.cuda.empty_cache();model=AutoModelForTokenClassification.from_pretrained(a.output/'best').to(device)
 result={'status':'smoke_only' if a.smoke else 'completed','best_epoch':best_epoch,'dev_selection_f1':best}
 for split in ['dev'] if a.smoke else ['dev','test']:
  metrics,pred=evaluate(split);result[split]=metrics
  with (a.output/(split+'_predictions.jsonl')).open('w',encoding='utf-8') as f:
   for i,tags in enumerate(pred):f.write(json.dumps({'row':i,'source_idx':rows[split][i].get('idx'),'predicted_tags':tags},ensure_ascii=False)+'\n')
 (a.output/'result.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
 print(json.dumps(result),flush=True)
if __name__=='__main__':main()
