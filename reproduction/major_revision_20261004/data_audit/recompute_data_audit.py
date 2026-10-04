"""Read-only count/overlap audit. No labels, splits, or model scores are changed.

Usage: python recompute_data_audit.py --config INPUTS.json --output audit.json
INPUTS keys: train_b2, dev_b2, gold150, expanded_zip, qa100_manifest,
            prep_composition, latest50_manifest (all local file paths).
Outputs contain counts, identifiers and hashes, never sentence texts.
"""
import argparse, collections, hashlib, itertools, json, re, unicodedata, zipfile
from pathlib import Path

def sha(b): return hashlib.sha256(b).hexdigest()
def lines(b): return [json.loads(s) for s in b.decode('utf-8-sig').splitlines() if s.strip()]
def txt(r): return r.get('text', r.get('sentence', ''))
def sid(r): return str(r.get('source_id', r.get('meta',{}).get('source_id',r.get('id'))))
def nfc(s): return unicodedata.normalize('NFC',s)
def aggressive(s): return ''.join(unicodedata.normalize('NFKC',s).split()).casefold()
def preparation_key(s): return ''.join(nfc(s).split()).strip(' ，,、:：;；')
def ad_id(r):
    m=re.fullmatch(r'(\d+)-s\d+',sid(r))
    return m.group(1) if m else None
def ix(rs):
    return {'id':{sid(r) for r in rs}, 'exact_text':{txt(r) for r in rs},
            'NFC_text':{nfc(txt(r)) for r in rs},'NFKC_no_space_casefold':{aggressive(txt(r)) for r in rs}}
def stats(rs):
    x=ix(rs); ads=collections.Counter(ad_id(r) for r in rs if ad_id(r))
    return {'records':len(rs),'unique':{k:len(v) for k,v in x.items()},
            'excess_duplicate_records':{k:len(rs)-len(v) for k,v in x.items()},
            'numeric_ad_prefix_records':sum(ads.values()),'numeric_ad_prefix_groups':len(ads),
            'without_numeric_ad_prefix':sum(ad_id(r) is None for r in rs)}
def overlap(a,b):
    ai,bi=ix(a),ix(b); aa={ad_id(r) for r in a if ad_id(r)};ba={ad_id(r) for r in b if ad_id(r)}
    common=aa&ba
    return {'sentence_keys':{k:len(ai[k]&bi[k]) for k in ai},
      'numeric_ad_prefix':{'shared_groups':len(common),'records_a':sum(ad_id(r) in common for r in a),
       'records_b':sum(ad_id(r) in common for r in b),'shared_ids':sorted(common)},
      'scope':'Numeric ID prefixes are grouping evidence, not a verified source-document crosswalk; sp10k IDs are excluded.'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    inputs=json.loads(a.config.read_text(encoding='utf-8')); contents={k:Path(v).read_bytes() for k,v in inputs.items()}
    report={'schema':1,'source_hashes':{k:sha(v) for k,v in contents.items()},'scope':'Frozen-file audit only; no new human annotations or model inference.'}
    train,dev,gold=(lines(contents[k]) for k in ['train_b2','dev_b2','gold150'])
    groups={'B2_train':train,'B2_dev':dev,'Gold150':gold}
    report['original']= {k:stats(v) for k,v in groups.items()}
    report['original_overlap']={x+'__'+y:overlap(groups[x],groups[y]) for x,y in itertools.combinations(groups,2)}
    allold=train+dev;keys={preparation_key(txt(r)) for r in allold}
    tiny={'。','！','？',"';","']",']',"'",'；','，'}
    valid={t for t in keys if t and len(t)>=6 and t not in tiny}
    report['B2_preparation']={'records':len(allold),'raw_NFC_unique':len({nfc(txt(r)) for r in allold}),
        'preparation_key_unique':len(keys),'valid_preparation_key_unique':len(valid),
        'unique_rejected_by_preparation_filter':len(keys)-len(valid),
        'definition':'NFC, remove all whitespace, trim edge space/comma/list-separator/colon/semicolon; then minimum length 6 and punctuation-only exclusion.'}
    prefix='expanded_silver_splits_20260920/'
    report['expanded']={}
    with zipfile.ZipFile(inputs['expanded_zip']) as z:
        for variant in ['codex_9540','proxy_9646']:
            base=prefix+variant+'/'
            split=json.loads(z.read(base+'SPLIT.json'))
            rs={s:lines(z.read(base+'data/'+s+'.jsonl')) for s in ['train','val','test']}
            allrows=sum(rs.values(),[]); mixes=dict(collections.Counter(r.get('mix_source','unrecorded') for r in allrows))
            old=[r for r in allrows if r.get('mix_source')=='v6a_nocross_b2']
            otherold=[r for r in old if preparation_key(txt(r)) not in valid]
            result={'member_hashes':{s:sha(z.read(base+'data/'+s+'.jsonl')) for s in rs},
               'actual_mix_source_counts':mixes,'all':stats(allrows),'per_split':{s:stats(r) for s,r in rs.items()},
               'between_splits':{x+'__'+y:overlap(rs[x],rs[y]) for x,y in itertools.combinations(rs,2)},
               'against_Gold150':{s:overlap(rr,gold) for s,rr in rs.items()},
               'old_rows_outside_preparation_valid_keys':{'n':len(otherold),'ids':[sid(r) for r in otherold],
                 'lengths':[len(preparation_key(txt(r))) for r in otherold]}}
            # Receipt-field check is separate from observed final JSONL source counts.
            assert len(allrows)==split['n_keep']
            assert len(old)==split['n_v6a_unique']
            report['expanded'][variant]=result
    qa=json.loads(contents['qa100_manifest']);prep=json.loads(contents['prep_composition'])
    report['QA100_sampling']={'registry':qa['registry_n'],'excluded_A100':qa['a100_n'],
       'excluded_prior_pilot100':qa['qa_frame']['pilot100_excluded_from_qa_frame'],
       'excluded_pending':qa['qa_frame']['pending_excluded_from_qa_frame'],
       'eligible':qa['qa_frame']['n'],'sample':qa['sample'],
       'stratum_population_sum':sum(x['N_h'] for x in qa['strata']),
       'sample_size_sum':sum(x['n_h'] for x in qa['strata']),
       'zero_probability_population':sum(x['N_h'] for x in qa['strata'] if not x['n_h'])}
    assert qa['registry_n']-qa['a100_n']-qa['qa_frame']['pilot100_excluded_from_qa_frame']-qa['qa_frame']['pending_excluded_from_qa_frame']==qa['qa_frame']['n']
    mf=json.loads(contents['latest50_manifest'])
    report['latest50_sampling']={'n':len(mf),'distinct_advertisement_ids':len({r['advertisement_id'] for r in mf}),
       'source_counts':dict(collections.Counter(r['source_domain'] for r in mf)),
       'B2_id_overlap':len({r['source_id'] for r in mf}&{sid(r) for r in allold}),
       'Gold150_id_overlap':len({r['source_id'] for r in mf}&{sid(r) for r in gold}),
       'complete_candidate_frame_available':False,
       'note':'Sample manifest alone cannot rerun the selection or verify every exclusion. This is an agreement sample, not a new model test.'}
    report['preparation_vs_final']={'planned_old_valid':prep['sentences']['old_unique_valid_v6a'],
       'planned_new':prep['sentences']['new_unlabeled_topup'],'planned_total':prep['n_10k'],
       'final_old':2077,'wave12_candidates':3620,'wave12_kept':3407,'wave3_candidates':1816,'wave3_kept':1703,
       'codex_2500_kept':2353,'alternative_2500_kept':2459,
       'codex_final_arithmetic':2077+3407+1703+2353,'alternative_final_arithmetic':2077+3407+1703+2459,
       'apparent_313_gap':(3620-3407)+(1816-1703)-(2077-2064),
       'note':'The 10,000 preparatory target and final pools apply different old-Silver admission criteria. A single subtraction from 10,000 conflates stages.'}
    # Publishing raw source paths or sentence texts is intentionally avoided.
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'output':str(a.output),'original':report['original'],'B2_preparation':report['B2_preparation'],
       'original_overlap':report['original_overlap'],'expanded_mix':{k:v['actual_mix_source_counts'] for k,v in report['expanded'].items()},
       'qa':report['QA100_sampling'],'preparation_vs_final':report['preparation_vs_final']},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
