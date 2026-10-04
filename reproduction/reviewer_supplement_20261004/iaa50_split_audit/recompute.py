"""Read-only IAA50 membership audit; outputs aggregate counts and file hashes only.

Usage: python recompute.py --inputs local_input_paths.json --output audit.json
Input paths are deliberately separated from the publishable output.
"""
from pathlib import Path
import argparse, collections, hashlib, itertools, json, unicodedata, zipfile

def sha(b): return hashlib.sha256(b).hexdigest()
def rows(b): return [json.loads(s) for s in b.decode('utf-8-sig').splitlines() if s.strip()]
def sid(r): return str(r.get('source_id', r.get('meta', {}).get('source_id', r.get('id'))))
def text(r): return r.get('text', r.get('sentence', ''))
def norm(s): return ''.join(unicodedata.normalize('NFKC', s).split()).casefold()
def keys(rr):
    return {'id': {sid(r) for r in rr}, 'exact_text': {text(r) for r in rr},
            'NFC_text': {unicodedata.normalize('NFC', text(r)) for r in rr},
            'NFKC_no_space_casefold_text': {norm(text(r)) for r in rr}}

def main():
    p=argparse.ArgumentParser(); p.add_argument('--inputs', type=Path, required=True); p.add_argument('--output', type=Path, required=True); a=p.parse_args()
    cfg=json.loads(a.inputs.read_text(encoding='utf-8'))
    content={k:Path(v).read_bytes() for k,v in cfg['files'].items()}
    manifest=json.loads(content['manifest']); mm={r['study_id']:r for r in manifest}
    raw={c:sorted(rows(content['coder_'+c]),key=lambda r:r['study_id']) for c in 'ABC'}
    assert all(len(v)==50 for v in raw.values())
    assert all([(r['study_id'],r['text']) for r in v]==[(r['study_id'],r['text']) for r in raw['A']] for v in raw.values())
    reference=[dict(r,source_id=mm[r['study_id']]['source_id']) for r in raw['A']]
    refkeys=keys(reference)
    report={'schema':1,'scope':'Read-only audit of existing independent-coder exports against frozen experimental inputs; no labels or model scores created.',
            'inputs_sha256':{k:sha(v) for k,v in content.items()},
            'sample':{'n':50,'distinct_source_ids':len(refkeys['id']),'distinct_exact_texts':len(refkeys['exact_text']),
                      'distinct_recorded_advertisements':len({r['advertisement_id'] for r in manifest}),
                      'source_counts':dict(collections.Counter(r['source_domain'] for r in manifest))}}
    new=rows(content['new_sentences']); newmap={sid(r):r for r in new}
    def doc(r):
        v=newmap.get(sid(r))
        return (v['source_file'],str(v['source_row_id'])) if v else None
    refdocs={doc(r) for r in reference if doc(r)}
    assert len(refdocs)==50
    assert all(mm[r['study_id']]['advertisement_id']=='::'.join(doc(r)) for r in reference)
    report['sample']['all_recorded_advertisements_match_source_file_and_row']=True
    def compare(rr):
        kk=keys(rr); dd={doc(r) for r in rr if doc(r)}; common=dd&refdocs
        return {'records':len(rr),'distinct_shared_sentence_keys':{k:len(refkeys[k]&kk[k]) for k in kk},
                'sample_records_matched':{k:sum((sid(r) if k=='id' else text(r) if k=='exact_text' else unicodedata.normalize('NFC',text(r)) if k=='NFC_text' else norm(text(r))) in kk[k] for r in reference) for k in kk},
                'shared_recorded_expansion_advertisement_groups':len(common),
                'document_scope':'Only expansion source_file+source_row_id keys are comparable here; cross-namespace original-corpus document identity is not inferred.'}
    report['B2_and_human_reference']={k:compare(rows(content[k])) for k in ['B2_train','B2_dev','Gold150']}
    report['expanded']={}
    with zipfile.ZipFile(cfg['files']['expanded_zip']) as z:
        for archive_name,name in [('codex_9540','adopted_Codex_9540'),('proxy_9646','alternative_API_9646')]:
            vv={}; allrows=[]
            for s in ['train','val','test']:
                member='expanded_silver_splits_20260920/'+archive_name+'/data/'+s+'.jsonl'
                b=z.read(member); rr=rows(b); allrows+=rr
                vv[s]={'member_sha256':sha(b),**compare(rr)}
            vv['combined']=compare(allrows); report['expanded'][name]=vv
    prior=json.loads(content['prior_data_audit']); identity=json.loads(content['experiment_identity_recheck'])
    same_b2=all(sha(content[k])==prior['source_hashes'][v] for k,v in [('B2_train','train_b2'),('B2_dev','dev_b2'),('Gold150','gold150')])
    same_expanded=all(report['expanded'][name][s]['member_sha256']==prior['expanded'][old]['member_hashes'][s]
        for old,name in [('codex_9540','adopted_Codex_9540'),('proxy_9646','alternative_API_9646')] for s in ['train','val','test'])
    training_identity=all(identity['experiment_identity'][v]['partitions'][s]['matches_receipt'] and
        identity['experiment_identity'][v]['partitions'][s]['BIO_and_occurrence_ordered_complete_texts_match']
        for v in ['codex_9540','proxy_9646'] for s in ['train','val','test'])
    assert same_b2 and same_expanded and training_identity
    report['provenance_verification']={'B2_and_Gold150_hashes_match_prior_frozen_audit':same_b2,
        'all_six_expanded_member_hashes_match_prior_frozen_audit':same_expanded,
        'prior_audit_verified_expanded_BIO_ids_and_texts_against_Qwen_training_manifest_inputs':training_identity}
    spans={c:[set(map(tuple,r['label'])) for r in raw[c]] for c in raw}
    f=[];bf=[]
    for c,d in itertools.combinations('ABC',2):
        den=sum(map(len,spans[c]))+sum(map(len,spans[d]))
        f.append(2*sum(len(x&y) for x,y in zip(spans[c],spans[d]))/den)
        bf.append(2*sum(len({z[:2] for z in x}&{z[:2] for z in y}) for x,y in zip(spans[c],spans[d]))/den)
    report['agreement_recomputed']={'span_counts':{c:sum(map(len,v)) for c,v in spans.items()},
        'mean_pairwise_typed_exact_F1':sum(f)/3,'mean_pairwise_boundary_F1':sum(bf)/3,
        'all_three_identical_sentences':sum(x==y==z for x,y,z in zip(spans['A'],spans['B'],spans['C'])),
        'all_three_empty_sentences':sum(not x and not y and not z for x,y,z in zip(spans['A'],spans['B'],spans['C'])),
        'L_spans_per_coder':{c:sum(s[2]=='L' for rr in spans[c] for s in rr) for c in spans},
        'label_stage':'Independent annotations with individual self-review, as clarified by the authors; no adjudicated consensus gold created.'}
    report['archived_prompt_checks']={}
    for name,path in cfg['prompts'].items():
        b=Path(path).read_bytes(); st=b.decode('utf-8-sig')
        report['archived_prompt_checks'][name]={'sha256':sha(b),'sample_complete_text_occurs_verbatim':sum(text(r) in st for r in reference),
            'sample_complete_text_occurs_NFC':sum(unicodedata.normalize('NFC',text(r)) in unicodedata.normalize('NFC',st) for r in reference),
            'sample_complete_text_occurs_NFKC_no_space_casefold':sum(norm(text(r)) in norm(st) for r in reference)}
    report['prompt_scope']='Checks only the listed archived prompt files for complete sample sentences, not every earlier chat/session, partial example, or unarchived teacher context. Zero matches is not proof of universal prompt-example exclusion.'
    report['interpretation']=['This is an annotation-agreement sample, not a scored model test set.',
      'Adjudication alone cannot make this sample an independent test of the already trained expanded models, because 46 sample sentences occur verbatim in each archived expanded training split and another two occur in validation.',
      'The observed expanded-training overlap does not invalidate blinded human inter-annotator agreement; human-label independence and model-training isolation are different requirements.',
      'No complete training/prompt-exposure clearance is claimed for an independent test. No new test or consensus labels are manufactured.']
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'output':str(a.output),'agreement':report['agreement_recomputed'],'overlaps':{k:{s:v['distinct_shared_sentence_keys']['exact_text'] for s,v in vv.items()} for k,vv in report['expanded'].items()}},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
