"""Audit stored source-document groups; never changes labels.

Usage: python audit_document_groups.py --corpus-dir DIR --new-sentences FILE
 --expanded-zip FILE --b2-train FILE --b2-dev FILE --gold150 FILE --output DIR

Corpus DIR contains train.json, dev.json and test.json. Output contains aggregate counts and input hashes only. Document IDs in separate source
namespaces are not assumed comparable without a crosswalk.
"""
import argparse,collections,hashlib,itertools,json,re,zipfile
from pathlib import Path
from recompute_data_audit import lines,txt,sid,aggressive,preparation_key,sha

def main():
 p=argparse.ArgumentParser()
 for name in ['corpus-dir','new-sentences','expanded-zip','b2-train','b2-dev','gold150','output']:p.add_argument('--'+name,type=Path,required=True)
 a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
 corpus={s:json.loads((a.corpus_dir/(s+'.json')).read_text(encoding='utf-8-sig')) for s in ['train','dev','test']}
 orig={sid(r):r for rr in corpus.values() for r in rr};new=lines(a.new_sentences.read_bytes());newmap={sid(r):r for r in new}
 b2={'train':lines(a.b2_train.read_bytes()),'dev':lines(a.b2_dev.read_bytes())};gold=lines(a.gold150.read_bytes())
 def doc(r):
  i=sid(r)
  if i in orig:return 'corpus::'+str(orig[i]['global_id'])
  if i in newmap:
   n=newmap[i];return 'expansion::'+n['source_file']+'::'+str(n['source_row_id'])
  return None
 def stat(rr):
  return {'n':len(rr),'mapped_document_ids':len({doc(r) for r in rr if doc(r)}),'unmapped':sum(doc(r) is None for r in rr),
    'source_domains':dict(collections.Counter(r.get('source_domain','unknown') for r in rr))}
 def overlap(aa,bb):
  aaids={doc(r) for r in aa if doc(r)};bbids={doc(r) for r in bb if doc(r)};shared=aaids&bbids
  return {'shared_document_ids':len(shared),'records_a_from_shared':sum(doc(r) in shared for r in aa),'records_b_from_shared':sum(doc(r) in shared for r in bb),
   'exact_text_shared':len({txt(r) for r in aa}&{txt(r) for r in bb}),
   'normalized_text_shared':len({aggressive(txt(r)) for r in aa}&{aggressive(txt(r)) for r in bb})}
 report={'schema':1,'input_sha256':{'corpus_'+s:sha((a.corpus_dir/(s+'.json')).read_bytes()) for s in corpus},
   'document_key':'Original corpus global_id; expansion source_file + source_row_id. Namespaces kept separate.',
   'limitations':['The two ID namespaces lack a source-document crosswalk; cross-namespace document non-overlap is not established.',
    'No manual labels or new test scores were created. This audit does not remove pretraining contamination uncertainty.']}
 report['input_sha256'].update({k:sha(getattr(a,k).read_bytes()) for k in ['new_sentences','expanded_zip','b2_train','b2_dev','gold150']})
 report['corpus']={s:stat(rr) for s,rr in corpus.items()}
 report['corpus_between_splits']={x+'__'+y:overlap(corpus[x],corpus[y]) for x,y in itertools.combinations(corpus,2)}
 report['prefix_validation']={'all_original_ids_match_global_id':all(sid(r).rsplit('-s',1)[0]==str(r['global_id']) for rr in corpus.values() for r in rr),
   'B2_ids_found_in_original':{s:sum(sid(r) in orig for r in rr) for s,rr in b2.items()},'Gold150_ids_found':sum(sid(r) in orig for r in gold)}
 report['B2']={'train_vs_dev':overlap(b2['train'],b2['dev']),'train_vs_gold150':overlap(b2['train'],gold),'dev_vs_gold150':overlap(b2['dev'],gold)}
 expanded={};report['expanded']={}
 with zipfile.ZipFile(a.expanded_zip) as z:
  for name in ['codex_9540','proxy_9646']:
   rr={s:lines(z.read('expanded_silver_splits_20260920/'+name+'/data/'+s+'.jsonl')) for s in ['train','val','test']}
   expanded[name]=rr;report['expanded'][name]={'partitions':{s:stat(r) for s,r in rr.items()},
    'between_partitions':{x+'__'+y:overlap(rr[x],rr[y]) for x,y in itertools.combinations(rr,2)},
    'against_Gold150':{s:overlap(r,gold) for s,r in rr.items()}}
 (a.output/'document_groups.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
