"""Offline audit of frozen DeepSeek responses; emits metadata only, never source text."""
import argparse
from collections import Counter
from pathlib import Path
import csv, hashlib, json, runpy

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def rows(p): return [json.loads(s) for s in p.read_text(encoding='utf-8-sig').splitlines() if s.strip()]

ap=argparse.ArgumentParser()
ap.add_argument('--pack',required=True,help='Frozen pack containing 00_freeze and 01_shared_prompt')
ap.add_argument('--scorer',required=True,help='Released score_lskt.py')
ap.add_argument('--out',required=True)
a=ap.parse_args();pack=Path(a.pack);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
parserpath=pack/'00_freeze/parser_occurrence_v1_1.py'
parser=runpy.run_path(str(parserpath));scorer=runpy.run_path(a.scorer)
goldpath=pack/'00_freeze/gold150_test.jsonl'
gold={str(r['source_id']):r for r in rows(goldpath)};assert len(gold)==150
report={'audit_date':'2026-10-05','scope':'Offline frozen-response audit, no new inference',
 'parser_sha256':sha(parserpath),'scorer_sha256':sha(Path(a.scorer)),
 'reference_sha256':sha(goldpath),'runs':{}}
all_meta=[]
for name in ['deepseek-v4-pro-think8192','deepseek-v4-pro-nothink']:
    pdir=pack/'01_shared_prompt/preds'/name
    preds={str(r['id']):r for r in rows(pdir/'pred_for_score.jsonl')}
    gs={str(r['id']):r for r in rows(pdir/'gold_for_score.jsonl')}
    assert set(preds)==set(gs)==set(gold)
    cp=pack/'01_shared_prompt/configs'/name/'CONFIG_FINGERPRINT.json';cfg=read(cp)
    assert cfg['parser_sha256']==sha(parserpath) and cfg['gold150_sha256']==sha(goldpath)
    raw={};extra=[];rawpaths=list((pack/'01_shared_prompt/raw'/name).rglob('*.json'))
    for p in rawpaths:
        r=read(p);rid=str(r['id'])
        if rid not in gold:extra.append(rid);continue
        assert rid not in raw,('duplicate formal response',rid)
        raw[rid]=(p,r)
    assert set(raw)==set(gold)
    meta=[];pairs=[];rejected=Counter()
    for rid,(p,r) in sorted(raw.items()):
        h=r['http'];rr=r['raw_response'];ch=rr['choices'][0];msg=ch['message']
        content=msg.get('content') or '';reasoning=msg.get('reasoning_content') or ''
        assert content==(h.get('content') or '') and reasoning==(h.get('reasoning_content') or '')
        assert ch['finish_reason']==h['finish_reason'] and rr['usage']==h['usage']
        replay=parser['parse_response'](content,rid,gold[rid]['text'])
        ps=scorer['extract_spans'](preds[rid],scorer['PRED_FIELDS'])
        g=scorer['extract_spans'](gs[rid],scorer['GOLD_FIELDS'])
        assert ''.join(preds[rid]['tokens'])==gold[rid]['text']==''.join(gs[rid]['tokens'])
        assert sorted((s['start'],s['end'],s['type']) for s in replay['spans'])==sorted(ps)
        assert replay['outcome']==preds[rid]['outcome'] and replay['format_failed']==preds[rid]['format_failed']
        rejected.update(s['reason'] for s in replay['rejected']);pairs.append((g,ps))
        u=rr['usage']
        m={'configuration':name,'id':rid,'raw_path':p.relative_to(pack).as_posix(),'raw_sha256':sha(p),
           'attempt':r['attempt'],'http_status':h['http_status'],'finish_reason':ch['finish_reason'],
           'http_error_present':bool(h.get('error')),'response_error_present':bool(rr.get('error')),
           'response_model':rr.get('model'),'final_content_characters':len(content),'reasoning_characters':len(reasoning),
           'completion_tokens':u.get('completion_tokens'),'reasoning_tokens':(u.get('completion_tokens_details') or {}).get('reasoning_tokens'),
           'truncated_flag':h.get('truncated'),'outcome':replay['outcome'],'parse_error':replay.get('parse_error'),
           'accepted_spans':len(ps),'rejected_spans':len(replay['rejected']),'reference_spans':len(g)}
        meta.append(m)
    all_meta.extend(meta);fails=[m for m in meta if m['outcome']=='format_failed']
    exact=scorer['micro_over_sentences'](pairs,scorer['match_exact'])
    relaxed=scorer['micro_over_sentences'](pairs,scorer['match_relaxed'])
    report['runs'][name]={'formal_records':len(meta),'raw_files':len(rawpaths),'excluded_non_reference_ids':extra,
      'config':{k:cfg[k] for k in ['request_model','base','chat_path','thinking','use_temperature','temperature','max_tokens']},
      'config_sha256':sha(cp),'prediction_sha256':sha(pdir/'pred_for_score.jsonl'),
      'all_parser_replays_match_frozen_predictions':True,'all_raw_response_fields_match_stored_summary':True,
      'http_status_counts':dict(Counter(m['http_status'] for m in meta)),
      'finish_reason_counts':dict(Counter(m['finish_reason'] for m in meta)),
      'outcomes':dict(Counter(m['outcome'] for m in meta)),
      'http_or_response_errors':sum(m['http_error_present'] or m['response_error_present'] for m in meta),
      'candidate_rejection_reasons':dict(rejected),'typed_exact':exact,'typed_relaxed':relaxed,
      'format_failures':{'n':len(fails),'all_http_200':all(m['http_status']==200 for m in fails),
        'all_finish_length':all(m['finish_reason']=='length' for m in fails),
        'all_final_content_empty':all(m['final_content_characters']==0 for m in fails),
        'all_reasoning_nonempty':all(m['reasoning_characters']>0 for m in fails),
        'completion_tokens_counts':dict(Counter(m['completion_tokens'] for m in fails)),
        'all_completion_tokens_are_reasoning':all(m['reasoning_tokens']==m['completion_tokens'] for m in fails),
        'parse_error_counts':dict(Counter(m['parse_error'] for m in fails)),
        'reference_spans':sum(m['reference_spans'] for m in fails),
        'reference_empty_sentences':sum(m['reference_spans']==0 for m in fails),
        'accepted_spans':sum(m['accepted_spans'] for m in fails),
        'rejected_candidates':sum(m['rejected_spans'] for m in fails)}}
assert report['runs']['deepseek-v4-pro-think8192']['format_failures']['n']==18
(out/'DEEPSEEK_FAILURE_AUDIT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
for fn,data in [('DEEPSEEK_RESPONSE_METADATA.csv',all_meta),('DEEPSEEK_FORMAT_FAILURE_METADATA.csv',[m for m in all_meta if m['outcome']=='format_failed'])]:
    with (out/fn).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(all_meta[0]));w.writeheader();w.writerows(data)
print(json.dumps(report,ensure_ascii=False,indent=2))
