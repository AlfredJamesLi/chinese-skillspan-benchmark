"""CPU data audit and train-only lexical control; not a published SOTA reproduction."""
from pathlib import Path
from collections import Counter,defaultdict
import json,hashlib,itertools,csv
ROOT=Path(__file__).resolve().parent
def read(p):return [json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]
def entities(tags):
 out=[];start=None;kind=None
 for i,t in enumerate(list(tags)+['O']):
  prefix=t.split('-',1)[0];typ=t.split('-',1)[1] if '-' in t else 'SPAN'
  if start is not None and (prefix not in ('I','E') or typ!=kind):out.append((start,i,kind));start=None
  if prefix in ('B','S') or (prefix in ('I','E') and start is None):start=i;kind=typ
  if prefix in ('S','E') and start is not None:out.append((start,i+1,kind));start=None
 return set(out)
def score(gold,pred):
 assert len(gold)==len(pred)
 tp=sum(len(g&p) for g,p in zip(gold,pred));ng=sum(map(len,gold));np=sum(map(len,pred))
 return {'tp':tp,'gold':ng,'pred':np,'precision':tp/np if np else 0,'recall':tp/ng if ng else 0,'f1':2*tp/(ng+np) if ng+np else 0}
def predict(tokens,lex):
 spans=set();i=0
 while i<len(tokens):
  match=None
  for words,typ in lex.get(tokens[i],[]):
   if tuple(tokens[i:i+len(words)])==words:match=(i,i+len(words),typ);break
  if match:spans.add(match);i=match[1]
  else:i+=1
 return spans
def main():
 audit={};results=[]
 for directory in sorted((ROOT/'data').iterdir()):
  manifest=json.loads((directory/'download_manifest.json').read_text())
  for f in manifest['files']:assert hashlib.sha256((directory/f['path']).read_bytes()).hexdigest()==f['sha256']
  sets={s:read(directory/(s+'.json')) for s in ('train','dev','test')}
  heads=[k for k in sets['train'][0] if k.startswith('tags_')]
  report={'revision':manifest['revision'],'heads':heads,'splits':{},'exact_token_overlap':{}}
  for split,rows in sets.items():
   for r in rows:
    assert r['tokens'] and all(len(r[h])==len(r['tokens']) for h in heads)
    assert all(t=='O' or t.split('-')[0] in ('B','I','E','S') for h in heads for t in r[h])
   report['splits'][split]={'sentences':len(rows),'max_words':max(len(r['tokens']) for r in rows),'sha256':hashlib.sha256((directory/(split+'.json')).read_bytes()).hexdigest(),'span_counts':{h:sum(len(entities(r[h])) for r in rows) for h in heads},'labels':{h:sorted({t for r in rows for t in r[h]}) for h in heads}}
  for a,b in itertools.combinations(sets,2):report['exact_token_overlap'][a+'__'+b]=len({tuple(r['tokens']) for r in sets[a]}&{tuple(r['tokens']) for r in sets[b]})
  # Fit exact, case-sensitive surface dictionary using training annotations only.
  for h in heads:
   counts=defaultdict(Counter)
   for r in sets['train']:
    for a,b,t in entities(r[h]):counts[tuple(r['tokens'][a:b])][t]+=1
   lex=defaultdict(list)
   for words,c in counts.items():lex[words[0]].append((words,sorted(c,key=lambda t:(-c[t],t))[0]))
   for k in lex:lex[k].sort(key=lambda x:(-len(x[0]),x[0],x[1]))
   for split in ('dev','test'):
    rows=sets[split];gold=[entities(r[h]) for r in rows];pred=[predict(r['tokens'],lex) for r in rows]
    results.append({'dataset':directory.name,'head':h,'split':split,'method':'train_only_exact_lexicon_longest_match',**score(gold,pred)})
    dest=ROOT/'lexicon_predictions'/directory.name;dest.mkdir(parents=True,exist_ok=True)
    with (dest/(split+'_'+h+'.jsonl')).open('w',encoding='utf-8') as f:
     for i,spans in enumerate(pred):f.write(json.dumps({'row':i,'spans':sorted(spans)},ensure_ascii=False)+'\n')
  audit[directory.name]=report
 (ROOT/'data_audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
 (ROOT/'lexicon_results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
 with (ROOT/'lexicon_results.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=results[0]);w.writeheader();w.writerows(results)
 print(json.dumps({k:{'counts':{s:v['sentences'] for s,v in r['splits'].items()},'overlap':r['exact_token_overlap']} for k,r in audit.items()},indent=2))
if __name__=='__main__':main()
