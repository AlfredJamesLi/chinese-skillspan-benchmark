"""Recompute agreement from immutable, pseudonymized pre-discussion exports.

Run: python recompute.py [output.json]. Requires Python 3.9+ and NumPy.
The bundled manifest identifies one sentence per advertisement. Bootstrap is
stratified by source, conditional on the observed sample and these three coders.
"""
from pathlib import Path
import json,sys,itertools,collections
import numpy as np

ROOT=Path(__file__).resolve().parent
TYPES='OLKST';PAIRS=list(itertools.combinations(range(3),2))
def rows(name):
 a=[json.loads(s) for s in (ROOT/'data'/name).read_text(encoding='utf-8').splitlines() if s]
 return sorted(a,key=lambda x:x['study_id'])
def f1(m,n):return 2*m/n if n else None
def prepare():
 raw=[rows('frozen50_'+c+'.jsonl') for c in 'ABC'];assert all(len(x)==50 for x in raw)
 assert all([(r['study_id'],r['text']) for r in x]==[(r['study_id'],r['text']) for r in raw[0]] for x in raw)
 spans=[[set(map(tuple,r['label'])) for r in x] for x in raw]
 feats=[];chars=[]
 for k,r in enumerate(raw[0]):
  char=np.zeros((3,len(r['text'])),dtype=int)
  for c in range(3):
   assert raw[c][k]['confirmed']
   prev=0
   for a,b,t in sorted(spans[c][k]):
    assert 0<=a<b<=len(r['text']) and a>=prev and t in TYPES[1:];prev=b
    char[c,a:b]=TYPES.index(t)
  counts=np.array([np.bincount(x,minlength=5) for x in char])
  matches=[len(spans[a][k]&spans[b][k]) for a,b in PAIRS]
  den=[len(spans[a][k])+len(spans[b][k]) for a,b in PAIRS]
  bm=[len({x[:2] for x in spans[a][k]}&{x[:2] for x in spans[b][k]}) for a,b in PAIRS]
  disagreement=sum(np.count_nonzero(char[a]!=char[b]) for a,b in PAIRS)
  feats.append(matches+den+bm+[len(r['text']),disagreement]+list(counts.sum(axis=0)))
  chars.append(char)
 return raw,spans,chars,np.array(feats,dtype=float)
def aggregate(s):
 typed=2*s[...,0:3]/s[...,3:6];bound=2*s[...,6:9]/s[...,3:6]
 nchar=s[...,9];do=s[...,10]/(3*nchar);marg=s[...,11:16];total=3*nchar
 de=(total*total-(marg*marg).sum(axis=-1))/(total*(total-1))
 alpha=1-do/de
 return np.concatenate([typed,bound,typed.mean(axis=-1)[...,None],bound.mean(axis=-1)[...,None],alpha[...,None]],axis=-1)
def cohen(x,y):
 n=len(x);cx=np.bincount(x,minlength=5);cy=np.bincount(y,minlength=5)
 po=float(np.mean(x==y));pe=float(np.dot(cx/n,cy/n))
 return (po-pe)/(1-pe) if pe!=1 else None
def main():
 raw,spans,chars,feat=prepare();val=aggregate(feat.sum(axis=0));pairs={}
 for i,(a,b) in enumerate(PAIRS):
  x=np.concatenate([c[a] for c in chars]);y=np.concatenate([c[b] for c in chars])
  per={}
  for t in TYPES[1:]:
   sa=[{s for s in v if s[2]==t} for v in spans[a]];sb=[{s for s in v if s[2]==t} for v in spans[b]]
   na=sum(map(len,sa));nb=sum(map(len,sb));m=sum(len(u&v) for u,v in zip(sa,sb))
   per[t]={'n_first':na,'n_second':nb,'matches':m,'f1':f1(m,na+nb)}
  diff=collections.Counter()
  for u,v in zip(spans[a],spans[b]):
   du={s[:2]:s[2] for s in u};dv={s[:2]:s[2] for s in v}
   for bounds in du.keys()&dv.keys():
    if du[bounds]!=dv[bounds]:diff[du[bounds]+'->'+dv[bounds]]+=1
  pairs['ABC'[a]+'-'+'ABC'[b]]={'span_counts':[sum(map(len,spans[a])),sum(map(len,spans[b]))],'typed_matches':int(feat[:,i].sum()),'typed_exact_f1':float(val[i]),'boundary_matches':int(feat[:,6+i].sum()),'boundary_f1':float(val[3+i]),'exact_sentences':sum(u==v for u,v in zip(spans[a],spans[b])),'both_empty':sum(not u and not v for u,v in zip(spans[a],spans[b])),'character_kappa':cohen(x,y),'character_kappa_excluding_both_O':cohen(x[(x!=0)|(y!=0)],y[(x!=0)|(y!=0)]),'per_type':per,'same_boundary_type_disagreements':dict(diff)}
 man=json.loads((ROOT/'data/sample_manifest.json').read_text(encoding='utf-8'));mm={r['study_id']:r for r in man}
 assert len({r['advertisement_id'] for r in man})==len(man)==50
 layers=[mm[r['study_id']]['source_domain'] for r in raw[0]]
 groups=[np.array([i for i,v in enumerate(layers) if v==l]) for l in sorted(set(layers))]
 rng=np.random.default_rng(20260927)
 idx=np.concatenate([rng.choice(g,size=(10000,len(g)),replace=True) for g in groups],axis=1)
 with np.errstate(divide='ignore',invalid='ignore'):boot=aggregate(feat[idx].sum(axis=1))
 names=['typed_AB','typed_AC','typed_BC','boundary_AB','boundary_AC','boundary_BC','mean_typed','mean_boundary','alpha']
 intervals={}
 for k,n in enumerate(names):
  finite=np.isfinite(boot[:,k]);intervals[n]={'ci95':np.quantile(boot[finite,k],[.025,.975]).tolist() if finite.any() else None,'undefined_resamples':int((~finite).sum())}
 for i,k in enumerate(pairs):pairs[k]['typed_ci95']=intervals[names[i]]['ci95'];pairs[k]['boundary_ci95']=intervals[names[3+i]]['ci95']
 triple=sum(a==b==c for a,b,c in zip(*spans));empty=sum(not a and not b and not c for a,b,c in zip(*spans))
 allchars=np.concatenate(chars,axis=1);ct=np.bincount(allchars.flatten(),minlength=5);do=feat[:,10].sum()/(3*feat[:,9].sum());de=1-sum((ct/ct.sum())**2)
 out={'n_sentences':50,'n_coders':3,'span_counts':{c:sum(map(len,spans[i])) for i,c in enumerate('ABC')},'n_characters':int(feat[:,9].sum()),'source_counts':dict(collections.Counter(layers)),'pairs':pairs,'mean_typed_exact_f1':float(val[6]),'mean_boundary_f1':float(val[7]),'three_rater_character_alpha':float(val[8]),'three_rater_fleiss_kappa':float(1-do/de),'all_three_exact_sentences':triple,'all_three_empty_sentences':empty,'O_character_fraction':{c:float(np.mean(allchars[i]==0)) for i,c in enumerate('ABC')},'intervals':intervals,'bootstrap':{'resamples':10000,'seed':20260927,'rng':'numpy.random.default_rng (PCG64)','numpy_version':np.__version__,'unit':'sentence (one per recorded advertisement)','stratification':'source_domain, fixed observed source counts','method':'percentile 95%','conditioned_on':'these three coders and the observed source mixture','not_design_weighted':True}}
 # Training comparison is descriptive only, excluded from formal estimates.
 a,b=rows('separate15_A.jsonl'),rows('separate15_C.jsonl');assert [(r['study_id'],r['text']) for r in a]==[(r['study_id'],r['text']) for r in b]
 aa=[set(map(tuple,r['label'])) for r in a];bb=[set(map(tuple,r['label'])) for r in b]
 na=sum(map(len,aa));nb=sum(map(len,bb));mt=sum(len(x&y) for x,y in zip(aa,bb));bm=sum(len({s[:2] for s in x}&{s[:2] for s in y}) for x,y in zip(aa,bb))
 out['training15_AC']={'n':15,'span_counts':[na,nb],'matches':mt,'typed_f1':f1(mt,na+nb),'boundary_f1':f1(bm,na+nb),'exact_sentences':sum(x==y for x,y in zip(aa,bb)),'role':'training, excluded from formal reliability'}
 target=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'recomputed_metrics.json'
 target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({k:out[k] for k in ['mean_typed_exact_f1','mean_boundary_f1','three_rater_character_alpha','intervals','training15_AC']},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
