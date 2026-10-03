"""Rebuild full-precision metric tables from the archived scoring records.

Usage: python summarize_metrics.py --records official_scores --out summaries
Uses only the Python standard library. Does not train or run a model.
"""
from pathlib import Path
import argparse,csv,json,statistics,math

def summarize(root,out):
    root=Path(root);out=Path(out);out.mkdir(parents=True,exist_ok=True)
    runs=[]
    for model,seeds in [('qwen_no_adapter',['single']),('qwen_b2_lora',['42','43','44']),('xlm-roberta-large',['42','43','44']),('esco-xlm-roberta-large',['42','43','44'])]:
        for seed in seeds:
            d=json.loads((root/model/(seed+'.json')).read_text(encoding='utf8'))
            assert d['scorer_version']=='cnss-lskt-1.2.0' and d['align_mode']=='official'
            assert d['alignment_ok'] and d['eligible_for_main_table']
            assert d['gold_n_rows']==d['n_matched']==150
            assert d['n_missing']==d['n_extra']==d['n_duplicate_gold_preds']==0
            all_metrics=[('typed_exact','all',d['typed_exact']),('typed_relaxed','all',d['typed_relaxed']),('boundary_exact','all',d['collapsed_exact'])]
            for t in 'LKST':
                all_metrics.extend([('typed_exact',t,d['per_type_exact'][t]),('typed_relaxed',t,d['per_type_relaxed'][t])])
            for metric,typ,c in all_metrics:
                tp,fp,fn=(c[k] for k in ['tp','fp','fn'])
                f=2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0.0
                assert math.isclose(f,c['f1'],abs_tol=1e-12)
                if typ!='all':assert tp+fn=={'L':2,'K':125,'S':448,'T':88}[typ]
                runs.append({'model':model,'seed':seed,'metric':metric,'type':typ,'tp':tp,'fp':fp,'fn':fn,'precision':c['precision'],'recall':c['recall'],'f1':c['f1'],'reference_spans':tp+fn})
    with (out/'per_run_metrics.csv').open('w',encoding='utf8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(runs[0]));w.writeheader();w.writerows(runs)
    keys=list(dict.fromkeys((r['model'],r['metric'],r['type']) for r in runs));rows=[]
    for model,metric,typ in keys:
        group=[r for r in runs if (r['model'],r['metric'],r['type'])==(model,metric,typ)]
        v=[r['f1'] for r in group]
        rows.append({'model':model,'metric':metric,'type':typ,'n_runs':len(v),'seeds':','.join(r['seed'] for r in group),'mean':statistics.mean(v),'sample_sd':statistics.stdev(v) if len(v)>1 else None,'reference_spans':group[0]['reference_spans']})
    (out/'summary.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
    with (out/'summary.csv').open('w',encoding='utf8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    return rows

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--records',default='official_scores');p.add_argument('--out',default='summaries');a=p.parse_args()
    rows=summarize(a.records,a.out);print('Verified 10 runs on 150 sentences; wrote',len(rows),'full-precision summaries.')
