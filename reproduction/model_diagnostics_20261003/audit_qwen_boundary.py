from pathlib import Path
from collections import Counter
import argparse, hashlib, json, math, runpy, statistics

def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def read_jsonl(path):
    return [json.loads(x) for x in Path(path).read_text(encoding='utf-8-sig').splitlines() if x.strip()]

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def save(path, value):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')

def independent_bio(tags):
    spans=[]; i=0
    while i<len(tags):
        if tags[i].startswith('B-'):
            typ=tags[i][2:]; j=i+1
            while j<len(tags) and tags[j]=='I-'+typ: j+=1
            spans.append((i,j,typ)); i=j
        else: i+=1
    return spans

def score_sets(pairs, boundary=False, selected=None):
    tp=fp=fn=0
    for gs,ps in pairs:
        if selected is not None:
            gs=[s for s in gs if s[2] in selected];ps=[s for s in ps if s[2] in selected]
        g=set((s[:2] if boundary else s) for s in gs)
        p=set((s[:2] if boundary else s) for s in ps)
        tp+=len(g&p);fp+=len(p-g);fn+=len(g-p)
    return {'tp':tp,'fp':fp,'fn':fn,'f1':2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0.0}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--pack',required=True);ap.add_argument('--scorer',required=True)
    ap.add_argument('--reported');ap.add_argument('--out',required=True)
    ap.add_argument('--encoder-gold')
    args=ap.parse_args();root=Path(args.pack);out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    report=read_json(args.reported) if args.reported else None;official=runpy.run_path(args.scorer)
    parser_path=root/'00_freeze/parser_occurrence_v1_1.py';parser=runpy.run_path(str(parser_path))
    goldpath=root/'00_freeze/gold150_test.jsonl';goldrows=read_jsonl(goldpath)
    goldmap={str(r['source_id']):r for r in goldrows}; assert len(goldrows)==len(goldmap)==150
    labels={'language':'L','knowledge':'K','skills':'S','transversal':'T','L':'L','K':'K','S':'S','T':'T'}
    observed=sorted({s[2] for r in goldrows for s in r['label']})
    # Explicit aliases are inspectable, never silently inferred from first letters.
    labels.update({'transversal competences':'T','transversal_competences':'T','transversal_competencies':'T'})
    labels.update({'Language_Skills&Knowledge':'L','Tranversial SKills':'T'})
    assert set(observed)<=set(labels),observed
    goldspans={rid:[(int(a),int(b),labels[t]) for a,b,t in r['label']] for rid,r in goldmap.items()}
    goldscore=root/'01_shared_prompt/preds/qwen25-14b-instruct/gold_for_score.jsonl'
    grow=read_jsonl(goldscore);gmap={str(r['id']):r for r in grow}; assert len(grow)==150 and set(gmap)==set(goldmap)
    for rid,r in goldmap.items():
        assert ''.join(gmap[rid]['tokens'])==r['text'],rid
        assert sorted(official['extract_spans'](gmap[rid],official['GOLD_FIELDS']))==sorted(goldspans[rid]),rid
        assert all(0<=a<b<=len(r['text']) for a,b,t in goldspans[rid])
        assert len(goldspans[rid])==len(set(goldspans[rid]))
    frozen=read_json(root/'00_freeze/FREEZE_REGISTRY.json')
    assert sha(goldpath)==frozen['gold150']['sha256']
    assert sha(parser_path)==frozen['frozen_files']['parser']['sha256']
    results={'kind':'independent offline audit of frozen accepted predictions; no training or model inference',
      'scorer':{'path':Path(args.scorer).name,'sha256':sha(args.scorer),'version':official['SCORER_VERSION'],
                'settings':{'align_mode':'official','require_exact_id_set':True,'n_boot':0},
                'boundary_definition':'Extract typed spans first, then collapse type and exact-match unique coordinates within each sentence; micro-aggregate sentence counts. This is collapsed_exact, not relaxed or token accuracy.'},
      'parser':{'path':parser_path.relative_to(root).as_posix(),'sha256':sha(parser_path),'matches_freeze_registry':True},
      'gold':{'path':goldpath.relative_to(root).as_posix(),'sha256':sha(goldpath),'n':150,'spans':sum(map(len,goldspans.values())),
              'types':dict(Counter(s[2] for row in goldspans.values() for s in row)),
              'empty_sentences':sum(not row for row in goldspans.values()),'score_format_path':goldscore.relative_to(root).as_posix(),
              'score_format_sha256':sha(goldscore),'original_vs_score_format_id_text_typed_spans_equal':True},'runs':{}}
    shared=read_json(root/'01_shared_prompt/scores/SCORE.json');sft=read_json(root/'02_sft/scores/GOLD150_SFT_SCORE_SUMMARY.json')
    paths={'no_adapter':root/'01_shared_prompt/preds/qwen25-14b-instruct/pred_for_score.jsonl'}
    paths.update({str(s):root/('02_sft/infer/seed%s/pred_for_score.jsonl'%s) for s in [42,43,44]})
    for key,path in paths.items():
        rows=read_jsonl(path);pm={str(r['id']):r for r in rows}
        assert len(rows)==len(pm)==150 and set(pm)==set(goldmap),key
        pairs=[];bad_i=0;empty=0;outcomes=Counter();dup_spans=0;dup_boundaries=0
        for rid,r in pm.items():
            assert ''.join(r['tokens'])==goldmap[rid]['text'],(key,rid)
            tags=r['pred_tags']; assert len(tags)==len(r['tokens'])
            assert all(t=='O' or t in {p+'-'+v for p in ['B','I'] for v in 'LKST'} for t in tags)
            bad_i+=sum(t.startswith('I-') and (i==0 or tags[i-1] not in ['B-'+t[2:],'I-'+t[2:]]) for i,t in enumerate(tags))
            ps=independent_bio(tags);assert ps==official['extract_spans'](r,official['PRED_FIELDS'])
            dup_spans+=len(ps)-len(set(ps));dup_boundaries+=len(ps)-len(set(s[:2] for s in ps))
            empty+=not ps;outcomes[r.get('outcome','unspecified')]+=1
            if r.get('format_failed') or r.get('outcome') in ['all_spans_rejected','format_failed']:assert not ps
            pairs.append((goldspans[rid],ps))
        assert bad_i==0
        off=official['score'](str(goldscore),str(path),align_mode='official',require_exact_id_set=True,n_boot=0)
        off['gold_path']=goldscore.relative_to(root).as_posix()
        off['pred_path']=path.relative_to(root).as_posix()
        save(out/'official_scores'/(key+'.json'),off)
        indep={'typed_exact':score_sets(pairs),'boundary':score_sets(pairs,True),
               'SK_combined_typed_exact':score_sets(pairs,selected={'S','K'})}
        for a,b in [('typed_exact','typed_exact'),('boundary','collapsed_exact')]:
            for k in ['tp','fp','fn','f1']:assert math.isclose(indep[a][k],off[b][k],abs_tol=1e-12),(key,a,k)
            if report:
                for k in ['tp','fp','fn','f1']:assert math.isclose(indep[a][k],report['runs'][key][a][k],abs_tol=1e-12),(key,a,k)
        archived=shared['rows']['qwen25-14b-instruct'] if key=='no_adapter' else sft['seeds'][key]
        for m in ['typed_exact','typed_relaxed']:
            assert math.isclose(off[m]['f1'],archived[m+'_f1'],abs_tol=1e-12),(key,m)
        if key=='no_adapter':
            raw=[read_json(p) for p in (root/'01_shared_prompt/raw/qwen25-14b-instruct').rglob('*.json')]
            raw=[r for r in raw if r.get('phase')=='formal']
        else:raw=read_jsonl(root/('02_sft/infer/seed%s/records.jsonl'%key))
        rawmap={str(r['id']):r for r in raw};assert len(raw)==150 and set(rawmap)==set(goldmap),(key,'raw coverage')
        rejected=Counter();same=0
        for rid,r in rawmap.items():
            replay=parser['parse_response'](r['content'],rid,goldmap[rid]['text'])
            spans=[(x['start'],x['end'],x['type']) for x in replay['spans']]
            assert sorted(spans)==sorted(independent_bio(pm[rid]['pred_tags'])),(key,rid,'parser replay')
            assert replay['outcome']==pm[rid]['outcome'],(key,rid,'outcome')
            assert replay['format_failed']==pm[rid]['format_failed']
            rejected.update(x['reason'] for x in replay['rejected']);same+=1
        results['runs'][key]={'prediction_path':path.relative_to(root).as_posix(),'prediction_sha256':sha(path),
          'sha_matches_new_report':sha(path)==report['runs'][key]['prediction_sha256'] if report else None,
          'n_scored':150,'n_missing':0,'n_extra':0,'n_duplicate_ids':0,'text_alignment_ok':True,
          'no_tag_padding_or_truncation_needed':True,'invalid_bio_continuations':bad_i,
          'accepted_duplicate_typed_spans':dup_spans,'accepted_duplicate_coordinates':dup_boundaries,
          'parser_replayed_rows':same,'parser_replay_matches':True,'outcomes':dict(outcomes),
          'rejected_candidates_by_reason':dict(rejected),'predicted_empty_sentences':empty,
          **indep,'typed_relaxed':off['typed_relaxed'],
          'official_and_independent_counts_agree':True,'archived_typed_exact_and_relaxed_reproduced':True}
    summaries={}
    for met in ['typed_exact','boundary','SK_combined_typed_exact','typed_relaxed']:
        vals=[results['runs'][str(s)][met]['f1'] for s in [42,43,44]]
        summaries[met]={'mean':statistics.mean(vals),'sample_sd':statistics.stdev(vals)}
        if report:
            for k in ['mean','sample_sd']:assert math.isclose(summaries[met][k],report['three_seed_summary'][met][k],abs_tol=1e-12)
    results['three_seed_summary']=summaries
    results['limits']=['Offline diagnostic rescoring of the same development-used Gold150; no independent blind model test.',
       'Boundary matching ignores type but preserves exact span coordinates; it is not classification accuracy or a pure boundary-error rate.',
       'Sample SD describes three training runs, not uncertainty across independently sampled test sets.',
       'Invalid candidates remain rejected exactly as in the frozen parser outputs; missing sentence coverage would be an error, not silently removed or filled.']
    if args.encoder_gold:
        erows=read_jsonl(args.encoder_gold);emap={str(r.get('id',r.get('source_id'))):r for r in erows}
        checks={'path':Path(args.encoder_gold).name,'sha256':sha(args.encoder_gold),'n':len(erows),
                'same_ids':len(erows)==len(emap)==150 and set(emap)==set(goldmap)}
        mismatch=[]
        if checks['same_ids']:
            for rid,r in emap.items():
                txt=r.get('text',r.get('sentence',''.join(r.get('tokens',[]))))
                if 'label' in r:esp=[(int(a),int(b),labels[t]) for a,b,t in r['label']]
                else:esp=official['extract_spans'](r,official['GOLD_FIELDS'])
                if txt!=goldmap[rid]['text'] or sorted(esp)!=sorted(goldspans[rid]):mismatch.append(rid)
        checks['mismatched_text_or_typed_spans']=mismatch
        checks['same_ids_text_and_LSKT_spans']=checks['same_ids'] and not mismatch
        results['encoder_gold_comparison']=checks
    results['supplied_report_checked']=bool(report)
    results['supplied_report_sha256']=sha(args.reported) if report else None
    results['passed']=all(r['official_and_independent_counts_agree'] and r['parser_replay_matches'] and (not report or r['sha_matches_new_report']) for r in results['runs'].values())
    save(out.parent/'qwen_boundary_audit_20261003.json',results)
    print(json.dumps({'passed':results['passed'],'three_seed_summary':summaries,'encoder_gold_comparison':results.get('encoder_gold_comparison')},indent=2))

if __name__=='__main__':main()
