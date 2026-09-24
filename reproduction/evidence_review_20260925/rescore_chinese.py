"""Rebuild Chinese encoder scores from the published audit folder; no GPU needed.
Usage: python rescore_chinese.py AUDIT_FOLDER OUTPUT_FOLDER
Dependency: numpy. AUDIT_FOLDER contains code/, data_manifest/, runs_lightweight/.
"""
from pathlib import Path
import argparse, json, runpy, hashlib, statistics
import numpy as np

def load(path):
    return [json.loads(x) for x in path.read_text(encoding='utf-8-sig').splitlines() if x.strip()]

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('audit',type=Path);ap.add_argument('output',type=Path)
    a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=True)
    scorer=runpy.run_path(str(a.audit/'code/adapters/score_lskt.py'))
    raw=load(a.audit/'data_manifest/gold150_test.jsonl');gold={r['source_id']:r for r in raw}
    types={'knowledge':'K','skills':'S','Tranversial SKills':'T','Language_Skills&Knowledge':'L','K':'K','S':'S','T':'T','L':'L'}
    all_counts={};summary={};order=None
    for model in ['xlm-roberta-large','esco-xlm-roberta-large']:
        all_counts[model]=[];values=[]
        for seed in [42,43,44]:
            folder=a.audit/'runs_lightweight'/model/str(seed)
            gpath=folder/'gold150_gold.bio.jsonl';ppath=folder/'gold150_predictions.jsonl'
            gr=load(gpath);pr=load(ppath);pred={r['id']:r for r in pr}
            ids=[r['id'] for r in gr]
            assert len(gr)==len(pr)==len(pred)==150 and set(ids)==set(pred)==set(gold)
            if order is None:order=ids
            assert ids==order
            counts=[]
            for r in gr:
                p=pred[r['id']];original=gold[r['id']]
                assert ''.join(r['tokens'])==''.join(p['tokens'])==original['text']
                assert len(p['list_of_selection_bio4'])==len(original['text'])
                gs=scorer['extract_spans'](r,scorer['GOLD_FIELDS'])
                ps=scorer['extract_spans'](p,scorer['PRED_FIELDS'])
                assert set(gs)=={(s,e,types[t]) for s,e,t in original['label']}
                c=scorer['match_exact'](gs,ps);counts.append([c['tp'],c['pred'],c['gold']])
            report=scorer['score'](str(gpath),str(ppath),n_boot=0,require_exact_id_set=True)
            old=json.loads((folder/'gold150_official.json').read_text())
            for k in ['typed_exact','typed_relaxed','collapsed_exact','per_type_exact']:
                assert report[k]==old[k],(model,seed,k)
            history=json.loads((folder/'history.json').read_text())
            selected=max(history,key=lambda x:x['dev']['f1'])['epoch']
            assert selected==json.loads((folder/'result.json').read_text())['best_epoch']
            v=[report['typed_exact']['f1'],report['typed_relaxed']['f1'],report['collapsed_exact']['f1'],statistics.mean(x['f1'] for x in report['per_type_exact'].values())]
            values.append(v);all_counts[model].append(counts)
            (a.output/f'{model}_{seed}.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
        summary[model]={'mean':np.mean(values,axis=0).tolist(),'sample_sd':np.std(values,axis=0,ddof=1).tolist()}
    x=np.array(all_counts['xlm-roberta-large']);y=np.array(all_counts['esco-xlm-roberta-large'])
    draws=np.random.default_rng(20260924).integers(0,150,size=(10000,150));diff=[]
    for idx in draws:
        xx=x[:,idx,:].sum(axis=1);yy=y[:,idx,:].sum(axis=1)
        diff.append(float(np.mean(2*yy[:,0]/(yy[:,1]+yy[:,2])-2*xx[:,0]/(xx[:,1]+xx[:,2]))))
    result={'summary':summary,'paired_ci95':np.quantile(diff,[.025,.975]).tolist(),'resamples':10000,'seed':20260924,'unit':'sentence, conditional on fixed training seeds; no advertisement clustering or multiplicity adjustment','scorer_sha256':hashlib.sha256((a.audit/'code/adapters/score_lskt.py').read_bytes()).hexdigest(),'scope':'Prediction rescoring and development-history check; no training or checkpoint inference'}
    (a.output/'summary.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
