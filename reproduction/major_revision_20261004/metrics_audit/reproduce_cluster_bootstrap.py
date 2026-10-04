"""Reproduce pointwise paired cluster intervals from sentence_counts.csv.

Run with Python 3 and NumPy, in any working directory. No model inference,
advertisement text, API credentials or private input paths are required.
"""
from pathlib import Path
import csv, json
import numpy as np

root=Path(__file__).resolve().parent
with (root/'sentence_counts.csv').open(encoding='utf-8',newline='') as f:
    rows=list(csv.DictReader(f))
models=sorted(set(r['run'] for r in rows))
groups=sorted(set(r['source_id_prefix'] for r in rows))
assert len(groups)==61
draw=np.random.default_rng(20261004).integers(0,len(groups),size=(10000,len(groups)))
boot={}; point={}
for model in models:
    rr=[r for r in rows if r['run']==model]
    assert len(rr)==150 and len({r['sentence_id'] for r in rr})==150
    c=np.array([[sum(int(r[k]) for r in rr if r['source_id_prefix']==g) for k in ['tp','pred','gold']] for g in groups])
    total=c.sum(axis=0);point[model]=2*total[0]/(total[1]+total[2])
    b=c[draw].sum(axis=1);boot[model]=2*b[:,0]/(b[:,1]+b[:,2])
comparisons=[('gpt_vs_deepseek',['gpt-5.6-terra'],['deepseek-v4-pro-nothink'])]
comparisons += [(f'lora_{s}',[f'LoRA_{s}'],['qwen25-14b-instruct']) for s in [42,43,44]]
comparisons += [('lora_mean',[f'LoRA_{s}' for s in [42,43,44]],['qwen25-14b-instruct']),('encoder_mean',[f'esco-xlm-roberta-large_{s}' for s in [42,43,44]],[f'xlm-roberta-large_{s}' for s in [42,43,44]])]
out=[]
for key,left,right in comparisons:
    d=np.mean([boot[k] for k in left],axis=0)-np.mean([boot[k] for k in right],axis=0)
    out.append({'key':key,'difference':float(np.mean([point[k] for k in left])-np.mean([point[k] for k in right])),'ci95':np.quantile(d,[.025,.975]).tolist(),'bonferroni_six_comparisons_ci':np.quantile(d,[.05/(2*6),1-.05/(2*6)]).tolist()})
expected_path=root/'cluster_bootstrap_and_macro_public.json'
if not expected_path.exists():expected_path=root/'cluster_bootstrap_and_macro.json'
expected=json.loads(expected_path.read_text(encoding='utf-8'))
for a,b in zip(out,expected['comparisons']):
    assert a['key']==b['key'] and np.allclose([a['difference'],*a['ci95']],[b['difference'],*b['ci95']],rtol=0,atol=1e-12)
for display,prefix in [('Qwen B2 LoRA','LoRA'),('XLM-R-large','xlm-roberta-large'),('ESCOXLM-R','esco-xlm-roberta-large')]:
    values=[]
    for seed in [42,43,44]:
        per=expected['runs'][f'{prefix}_{seed}']['per_type']
        values.append(float(np.mean([2*per[t]['tp']/(per[t]['pred']+per[t]['gold']) for t in 'KST'])))
    observed=[float(np.mean(values)),float(np.std(values,ddof=1))]
    target=expected['macro_KST'][display]
    assert np.allclose(observed,[target['mean'],target['sample_sd']],rtol=0,atol=1e-12)
(root/'cluster_reproduction_check.json').write_text(json.dumps({'independent_aggregation_reproduces_all':True,'comparisons':out,'bonferroni_note':'Exploratory family of six displayed comparisons; widened percentile intervals use alpha/6. These remain bootstrap approximations, conditional on the same fixed runs and reference.'},indent=2),encoding='utf-8')
print(json.dumps({'verified':True,'n_groups':61,'comparisons':out},indent=2))
