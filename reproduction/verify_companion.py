#!/usr/bin/env python3
"""Validate companion presentation artifacts; never run models or rescore predictions."""
from pathlib import Path
from urllib.parse import unquote
import csv, hashlib, json, math, re, statistics, sys, posixpath

ROOT=Path(__file__).resolve().parents[1]
def readcsv(p):
    with (ROOT/p).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def require(ok,message):
    if not ok:raise ValueError(message)
def main():
    manifest=json.loads((ROOT/'reproduction/companion_manifest.json').read_text(encoding='utf8'))
    for entry in manifest['files']:
        f=ROOT/entry['path']
        require(f.is_file(),f"Missing: {entry['path']}")
        require(hashlib.sha256(f.read_bytes()).hexdigest()==entry['sha256'],f"Hash mismatch: {entry['path']}")
    outcomes=readcsv('reproduction/output_outcomes/shared_guideline_output_outcomes.csv')
    require(len(outcomes)==9,'Expected nine output-outcome rows')
    for r in outcomes:
        require(sum(int(r[k]) for k in ['valid_nonempty','empty','partial','all_spans_rejected','format_failure','missing'])==int(r['reference_sentences'])==150,'Output row total')
    empty=readcsv('reproduction/qwen_diagnostics/empty_reference.csv')
    require([int(x['fp_spans']) for x in empty]==[19,6,4,0],'FP spans')
    require([int(x['sentences_with_fp']) for x in empty]==[2,2,1,0],'FP sentences')
    require([int(x['legal_empty_outputs']) for x in empty]==[6,6,7,8],'Legal empty outputs')
    q=readcsv('reproduction/current_results/qwen_runs.csv')
    vals=[float(x['typed_exact_f1']) for x in q]
    require([r['seed'] for r in q]==['42','43','44'],'Seed identity')
    require(f'{statistics.mean(vals):.4f}'=='0.5403' and f'{statistics.stdev(vals):.4f}'=='0.0354','Mean/sample SD')
    shared=readcsv('reproduction/current_results/inference.csv')
    require([f"{float(r['typed_exact_f1']):.4f}" for r in shared]==['0.6667','0.6469','0.5977','0.5914','0.5716','0.3612'],'Table 5 values')
    a=json.loads((ROOT/'reproduction/agreement/calculation.json').read_text(encoding='utf8'))['typed']
    require(sum(a['confusion'].values())==2571,'Character count')
    po=sum(v for k,v in a['confusion'].items() if k.split('|')[0]==k.split('|')[1])/2571
    pe=sum(v/2571*a['marginal_Coder_A'].get(k,0)/2571 for k,v in a['marginal_Coder_B'].items())
    require(math.isclose(po,a['p_o']) and math.isclose(pe,a['p_e']) and f'{(po-pe)/(1-pe):.4f}'=='0.5673','Kappa arithmetic')
    relocation=json.loads((ROOT/'reproduction/experimental_notes/RELOCATION_MAP.json').read_text(encoding='utf8'))
    require(len(relocation)==81,'Passage map count')
    require(len(readcsv('reproduction/paper_names.csv'))==28,'Name map count')
    # Working documentation only. Historical source snapshots preserve original paths.
    remote_paths=set()
    if len(sys.argv)>1:
        tree=json.loads(Path(sys.argv[1]).read_text(encoding="utf8"))
        remote_paths={x["path"] for x in tree["tree"]}
    broken=[];links=0
    for e in manifest['files']:
        rel=e['path']
        if not rel.endswith('.md') or rel in manifest['historical_link_context']:continue
        s=(ROOT/rel).read_text(encoding='utf-8-sig')
        s=re.sub(r'```.*?```','',s,flags=re.S)
        for m in re.finditer(r'\]\(([^\s)]+)(?:\s+"[^"]*")?\)',s):
            target=unquote(m.group(1)).split('#')[0]
            if not target or re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',target):continue
            links+=1
            p=(ROOT/rel).parent/target
            key=posixpath.normpath(posixpath.join(posixpath.dirname(rel),target))
            if not p.exists() and key not in remote_paths:broken.append((rel,target))
    require(not broken,f'Broken local paths: {broken}')
    print(json.dumps({'files_hashed':len(manifest['files']),'output_rows':9,'relocated_passages':81,'name_mappings':28,'local_links_checked':links,'checks':'passed','models_called':False,'predictions_rescored':False},ensure_ascii=False,indent=2))
    return 0
if __name__=='__main__':
    sys.exit(main())
