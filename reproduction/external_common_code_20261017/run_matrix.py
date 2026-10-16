"""Dispatch common-protocol experiments from immutable model revisions; default is a dry run."""
from pathlib import Path
import argparse,json,subprocess,sys
root=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--phase',choices=['smoke','full'],default='smoke');p.add_argument('--execute',action='store_true');p.add_argument('--output',type=Path,required=True);p.add_argument('--datasets',nargs='+',default=['skillspan','kompetencer','gnehm','green','sayfullina','fijo']);p.add_argument('--seeds',nargs='+',type=int,default=[42,43,44]);a=p.parse_args()
pins={r['model']:r['revision'] for r in json.loads((root/'models.json').read_text()) if r['status']=='metadata_verified'}
models=['FacebookAI/xlm-roberta-large','jjzha/esco-xlm-roberta-large']
jobs=[]
for data in a.datasets:
 for head in (['tags_skill','tags_knowledge'] if data in ('skillspan','kompetencer') else ['tags_skill']):
  for model in models:
   for seed in ([42] if a.phase=='smoke' else a.seeds):
    output=a.output/a.phase/data/head/model.split('/')[-1]/str(seed)
    cmd=[sys.executable,str(root/'run_common_encoder.py'),'--dataset',data,'--head',head,'--model',model,'--revision',pins[model],'--seed',str(seed),'--output',str(output)]
    if a.phase=='smoke':cmd.append('--smoke')
    jobs.append(cmd)
a.output.mkdir(parents=True,exist_ok=True);(a.output/(a.phase+'_jobs.json')).write_text(json.dumps(jobs,indent=2),encoding='utf-8')
print(str(len(jobs))+' jobs; '+('executing sequentially' if a.execute else 'dry run only'))
if a.execute:
 for cmd in jobs:subprocess.run(cmd,check=True)
