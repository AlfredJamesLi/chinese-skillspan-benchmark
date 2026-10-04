"""Recheck frozen experiment identity and source-document key semantics.

Usage: python recheck_manifest_identity.py --config INPUTS.json
 --qwen-archive ARCHIVE --corpus-dir DIR --output RESULT.json
INPUTS is the same local path configuration used by recompute_data_audit.py.
This read-only check never changes labels or split membership.
"""
import argparse,collections,json,zipfile
from pathlib import Path
from recompute_data_audit import lines,txt,sid,sha,nfc

def main():
 p=argparse.ArgumentParser()
 for x in ['config','qwen-archive','corpus-dir','output']:p.add_argument('--'+x,type=Path,required=True)
 a=p.parse_args();c=json.loads(a.config.read_text(encoding='utf-8'))
 sources={k:Path(c[k]).read_bytes() for k in ['train_b2','dev_b2','gold150']}
 datasets={k:lines(v) for k,v in sources.items()}
 corpus={s:json.loads((a.corpus_dir/(s+'.json')).read_text(encoding='utf-8-sig')) for s in ['train','dev','test']}
 original={sid(r):r for rr in corpus.values() for r in rr};groups=collections.defaultdict(list)
 for r in original.values():groups[str(r['global_id'])].append(r)
 result={'scope':'Recheck of input identity, previous prevention scope, and document-group interpretation.',
   'not_claimed':['Previous anti-leakage work was absent or invalid','143 Gold150 sentence texts occurred in training','Measured effect size of shared source documents'],
   'original_key_checks':{'groups':len(groups),'all_prefixes_equal_global_id':all(sid(r).rsplit('-s',1)[0]==str(r['global_id']) for r in original.values()),
    'title_variation_within_groups':sum(len({str(r.get('title'))for r in rr})>1 for rr in groups.values()),
    'source_domain_variation_within_groups':sum(len({r.get('source_domain')for r in rr})>1 for rr in groups.values()),
    'unique_sentence_orders_within_groups':all(len({r['sentence_order']for r in rr})==len(rr)for rr in groups.values())},
   'join_checks':{},'experiment_identity':{}}
 for name,rs in datasets.items():
  matches=[r for r in rs if sid(r) in original]
  result['join_checks'][name]={'records':len(rs),'ids_found':len(matches),
   'complete_text_equal_to_original_by_id':sum(txt(r)==txt(original[sid(r)]) for r in matches),
   'NFC_text_equal_to_original_by_id':sum(nfc(txt(r))==nfc(txt(original[sid(r)])) for r in matches),
   'nonmatching_text_ids':[sid(r)for r in matches if txt(r)!=txt(original[sid(r)])],
   'exact_text_elsewhere_for_mismatched_ids':{
      sid(r):[{'sentence_id':sid(o),'global_id':str(o['global_id'])} for o in original.values() if txt(o)==txt(r)]
      for r in matches if txt(r)!=txt(original[sid(r)])}}
 with zipfile.ZipFile(a.qwen_archive) as q,zipfile.ZipFile(c['expanded_zip']) as z:
  prefix='CNSS_Qwen_Reproduction/'
  member=prefix+'shared_guidelines_b2/configs/DATA_MANIFEST.json';b=q.read(member);manifest=json.loads(b)
  result['experiment_identity']['B2']={'archive_member':member,'manifest_sha256':sha(b),'recorded_isolation_wording':manifest['isolation_wording'],
   'recorded_list_name':manifest['list_name'],'source_files':{k:{'observed_sha256':sha(sources[k]),'receipt_sha256':manifest['source'][k+'.jsonl']['sha256'],
     'matches':sha(sources[k])==manifest['source'][k+'.jsonl']['sha256']} for k in ['train_b2','dev_b2']},
   'Gold150_hash_matches_receipt':sha(sources['gold150'])==manifest['gold150']['sha256'],
   'prior_gold_checks':manifest['gold150'],'prior_train_dev_id_overlap':manifest['train_dev_id_overlap'],
   'prior_train_dev_NFC_overlap':manifest['train_dev_nfc_sentence_cross_after_nocross'],
   'previously_removed_training_ids':manifest['dropped_v6a_cross_split_ids_absent']}
  for variant,packed in [('codex_9540','codex_seed42'),('proxy_9646','proxy_seed42')]:
   member=prefix+'expanded_silver/'+packed+'/data/SPLIT_IDS_MANIFEST.json';m=json.loads(q.read(member));summary={}
   for split in ['train','val','test']:
    base='expanded_silver_splits_20260920/'+variant+'/data/'
    actual=z.read(base+m[split]['source_file']);occ=lines(actual);bio=lines(z.read(base+split+'.jsonl'))
    summary[split]={'observed_occurrence_sha256':sha(actual),'receipt_source_sha256':m[split]['source_sha256'],
       'matches_receipt':sha(actual)==m[split]['source_sha256'], 'n_matches':len(occ)==m[split]['n'],
       'BIO_and_occurrence_ordered_ids_match':[sid(r)for r in occ]==[sid(r)for r in bio],
       'BIO_and_occurrence_ordered_complete_texts_match':[txt(r)for r in occ]==[txt(r)for r in bio]}
   result['experiment_identity'][variant]={'archive_member':member,'partitions':summary}
  for name in ['train_b2','dev_b2']:assert result['experiment_identity']['B2']['source_files'][name]['matches']
  for name in ['codex_9540','proxy_9646']:
   assert all(all(v[k] for k in ['matches_receipt','n_matches','BIO_and_occurrence_ordered_ids_match','BIO_and_occurrence_ordered_complete_texts_match']) for v in result['experiment_identity'][name]['partitions'].values())
 result['interpretation']='The original corpus posting split and the later sentence-isolated supervised experiments are different versions. Existing prevention checks remain valid within their stated scope. Shared source-document groups in later experimental splits are a separate restriction on unseen-document interpretation; they do not demonstrate identical test sentences in training or quantify score inflation.'
 a.output.parent.mkdir(exist_ok=True,parents=True);a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
