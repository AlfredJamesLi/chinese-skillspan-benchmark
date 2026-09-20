"""Rebuild the manuscript profile from frozen private files or shared aggregates.

No training, model calls, scoring, or edits to annotation files.
"""
from pathlib import Path
from collections import Counter
import argparse, hashlib, json, csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from scipy.stats import gaussian_kde

TYPES = {'skills':'S', 'knowledge':'K', 'Tranversial SKills':'T',
         'Language_Skills&Knowledge':'L', **{s:s for s in 'LSKT'}}
SPECS = [
 ('B2 train','05_sft_b2_not_yet_gold150/labels_b2/train_b2.jsonl',2150,3646,'8921e5fc4b89a0fa83bd942f919c3325546b9938e099b6a13e378736b6717d2e'),
 ('B2 dev','05_sft_b2_not_yet_gold150/labels_b2/dev_b2.jsonl',169,345,'e67a3eb5229b94c6c1b552d5f40ece9ad362197236c20cd66b7f2600c9636fef'),
 ('Gold150','00_freeze/gold150_test.jsonl',150,663,'ca8db0bc386c24543fec845d42ea8e24883eb67b8ce75129ac1768c5c0310fd0')]
QA_HASH='e5a9f1ed64bcf28b3518954ccd5d8a1c60bcadf96c3a85fcc25a70da5a83b25f'
COLORS=['#0072B2','#56B4E9','#D55E00','#8064A2','#CC79A7']

def load(p,h):
    assert hashlib.sha256(p.read_bytes()).hexdigest()==h, str(p)
    return [json.loads(s) for s in p.read_text(encoding='utf-8-sig').splitlines() if s.strip()]

def pack(name,rows,source,sha,layer=None):
    inputs,spans,counts,types=[],[],[],Counter()
    for r in rows:
        text=r.get('text',r.get('sentence')); assert isinstance(text,str) and text
        labels=r['labels'][layer] if layer else r.get('label',r.get('spans'))
        assert len({tuple(x) for x in labels})==len(labels)
        inputs.append(len(text)); counts.append(len(labels))
        for a,b,t in labels:
            assert 0<=a<b<=len(text)
            spans.append(b-a); types[TYPES[t]]+=1
    def freq(xs): return {str(k):v for k,v in sorted(Counter(xs).items())}
    return dict(name=name,source=source,sha256=sha,n_records=len(rows),n_spans=len(spans),
                empty_records=counts.count(0),input_lengths=freq(inputs),span_lengths=freq(spans),
                spans_per_record=freq(counts),types={t:types[t] for t in 'LSKT'})

def expand(hist): return np.repeat([int(k) for k in hist],list(hist.values()))

def check(data):
    assert len(data['groups'])==5
    for g in data['groups']:
        assert sum(g['input_lengths'].values())==g['n_records']
        assert sum(g['span_lengths'].values())==g['n_spans']==sum(g['types'].values())
        assert sum(int(k)*v for k,v in g['spans_per_record'].items())==g['n_spans']
    assert data['groups'][2]['types']==dict(L=2,S=448,K=125,T=88)
    assert data['groups'][3]['input_lengths']==data['groups'][4]['input_lengths']
    assert [g['n_spans'] for g in data['groups']]==[3646,345,663,358,365]

def draw(data,out):
    check(data)
    plt.rcParams.update({'font.family':'Arial','font.size':10,'axes.labelsize':10,
      'axes.titlesize':11,'xtick.labelsize':9,'ytick.labelsize':9,
      'pdf.fonttype':42,'ps.fonttype':42,'svg.fonttype':'none',
      'text.color':'#243443','axes.labelcolor':'#243443','axes.edgecolor':'#A9B2BA',
      'xtick.color':'#48545F','ytick.color':'#48545F','axes.linewidth':.7})
    fig=plt.figure(figsize=(8.2,7.2),facecolor='white')
    gs=fig.add_gridspec(2,2,height_ratios=[1.65,1],left=.115,right=.98,top=.925,bottom=.085,hspace=.47,wspace=.35)
    bgrid=gs[0,1].subgridspec(2,1,height_ratios=[1,3.1],hspace=.20)
    ax=fig.add_subplot(gs[0,0]); full=fig.add_subplot(bgrid[0,0]); bv=fig.add_subplot(bgrid[1,0]); hm=fig.add_subplot(gs[1,:])
    groups=data['groups']
    for idx,ls in zip([0,1,2,3],['-','--','-.',':']):
        g=groups[idx]; x=np.sort(expand(g['input_lengths']))
        name=g['name'] if idx!=3 else 'QA150'
        ax.step(x,np.arange(1,len(x)+1)/len(x),where='post',color=COLORS[idx],ls=ls,lw=1.7,
                label=f"{name} (n={len(x):,})")
    ax.set_xscale('log'); ax.set_xticks([1,5,10,20,50,100,200,500,1000])
    ax.xaxis.set_major_formatter(ScalarFormatter()); ax.minorticks_off()
    ax.set_xlim(1,1000); ax.set_ylim(0,1.03); ax.set_yticks([0,.25,.5,.75,1],['0','25','50','75','100'])
    ax.set_xlabel('Input length (characters; log scale)'); ax.set_ylabel('Cumulative records (%)')
    ax.set_title('(a) Input length',loc='left',fontweight='bold',pad=12)
    ax.grid(axis='y',color='#E7EAEE',lw=.7); ax.set_axisbelow(True)
    ax.legend(loc='lower right',frameon=False,fontsize=8.5,labelspacing=.5,handlelength=2.2)
    ax.spines[['top','right']].set_visible(False)
    maxlen=0
    for i,g in enumerate(groups):
        v=expand(g['span_lengths']); maxlen=max(maxlen,max(v))
        # KDE evaluated only across observed integer-length support, no clipped observations.
        yy=np.linspace(min(v),max(v),300); d=gaussian_kde(v,bw_method='scott')(yy); w=.37*d/d.max()
        for panel,alpha in [(bv,.43),(full,.25)]:
            panel.fill_betweenx(yy,i-w,i+w,color=COLORS[i],alpha=alpha,lw=1.0,edgecolor=COLORS[i])
        full.text(i,max(v)+2,str(max(v)),ha='center',va='bottom',fontsize=8,color=COLORS[i])
        q1,med,q3=np.percentile(v,[25,50,75]); bv.plot([i,i],[q1,q3],lw=3,color=COLORS[i],solid_capstyle='round')
        bv.scatter(i,med,s=24,color='white',edgecolor=COLORS[i],lw=1.3,zorder=4)
    bv.set_xticks(range(5),['B2\ntrain','B2\ndev','Gold150','QA150\nA','QA150\nB'])
    # Zoom the viewport, never trim the data or recompute density on a truncated sample.
    bv.set_ylim(0,20); bv.set_yticks([0,5,10,15,20]); bv.set_ylabel('Span length (characters)')
    full.set_ylim(0,60);full.set_yticks([0,50]);full.set_xticks([])
    full.set_xlim(bv.get_xlim());full.spines[['top','right','bottom']].set_visible(False)
    full.set_title('(b) Annotated span length',loc='left',fontweight='bold',pad=15)
    full.text(.5,1.01,'Full range · numbers indicate maxima',transform=full.transAxes,ha='center',va='bottom',fontsize=8.2,color='#66737E')
    bv.set_title('Detail: 0–20 characters',loc='right',fontsize=8.5,pad=5,color='#66737E')
    bv.text(.5,-.24,'White dot: median · Thick line: middle 50%',transform=bv.transAxes,ha='center',va='top',fontsize=8.2,color='#66737E')
    bv.grid(axis='y',color='#E7EAEE',lw=.7); bv.set_axisbelow(True); bv.spines[['top','right']].set_visible(False)
    vals=np.array([[g['types'][t]/g['n_spans']*100 for t in 'LSKT'] for g in groups])
    im=hm.imshow(vals,cmap='Blues',vmin=0,vmax=70,aspect='auto')
    for i,g in enumerate(groups):
        for j,t in enumerate('LSKT'):
            val=vals[i,j]; hm.text(j,i,f"{val:.1f}%   ({g['types'][t]:,})",ha='center',va='center',fontsize=10,
                                  color='white' if val>44 else '#243443')
    hm.set_xticks(range(4),['L · Language','S · Occupational skills','K · Knowledge','T · Transversal'])
    hm.set_yticks(range(5),[f"{g['name']}  (n={g['n_spans']:,})" for g in groups])
    hm.set_title('(c) Competency composition',loc='left',fontweight='bold',pad=12)
    hm.set_xticks(np.arange(-.5,4,1),minor=True); hm.set_yticks(np.arange(-.5,5,1),minor=True)
    hm.grid(which='minor',color='white',lw=2.5);hm.tick_params(which='both',length=0)
    for sp in hm.spines.values(): sp.set_visible(False)
    hm.text(1,-.15,'Cells: % of spans within each row (count)',transform=hm.transAxes,ha='right',va='top',fontsize=8.5,color='#66737E')
    # Prevent long row labels from colliding with the margin; same plot width, larger left inset.
    pos=hm.get_position();hm.set_position([.255,pos.y0,.725,pos.height])
    for ext in ['pdf','svg','png']:
        fig.savefig(out/f'benchmark_profile.{ext}',dpi=300,bbox_inches='tight',pad_inches=.10)
    svg=out/'benchmark_profile.svg'
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text(encoding='utf-8').splitlines())+'\n',encoding='utf-8')
    plt.close(fig)
    from PIL import Image
    with Image.open(out/'benchmark_profile.png') as pic: pic.convert('L').save(out/'benchmark_profile_grayscale.png')

def main():
    p=argparse.ArgumentParser();p.add_argument('--evidence',type=Path);p.add_argument('--qa',type=Path)
    p.add_argument('--aggregate',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    a.output.mkdir(parents=True,exist_ok=True)
    if a.aggregate: data=json.loads(a.aggregate.read_text(encoding='utf-8'))
    else:
        assert a.evidence and a.qa
        groups=[]
        for name,rel,n,s,h in SPECS:
            g=pack(name,load(a.evidence/rel,h),rel,h);assert (g['n_records'],g['n_spans'])==(n,s);groups.append(g)
        rows=load(a.qa,QA_HASH);assert len(rows)==150 and len({r['id'] for r in rows})==150
        assert all(r['meta']['james1_confirmed'] and r['meta']['maple_confirmed'] for r in rows)
        for name,layer in [('QA150 A','james1'),('QA150 B','maple')]:
            groups.append(pack(name,rows,'QA150_all_layers.jsonl',QA_HASH,layer))
        data=dict(schema=1,unit='unmodified Unicode code points',groups=groups,
                  qa_design='Two reviewed label layers of the same 150 sentences; machine suggestions visible.',
                  scope='B2 Qwen manifest, Gold150, and QA150. Not a distribution of the expanded 9540-record pool.')
    check(data)
    (a.output/'benchmark_profile_data.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
    summary=[]
    for g in data['groups']:
        for field in ['input_lengths','span_lengths','spans_per_record']:
            v=expand(g[field]);summary.append(dict(group=g['name'],unit=field,n=len(v),min=int(min(v)),
                      q1=float(np.quantile(v,.25)),median=float(np.median(v)),q3=float(np.quantile(v,.75)),max=int(max(v)),mean=float(np.mean(v))))
    with (a.output/'benchmark_profile_summary.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
    draw(data,a.output); print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
