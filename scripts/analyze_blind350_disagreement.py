"""Read two coder exports; emit aggregate-only pre-adjudication statistics.

Usage: python scripts/analyze_blind350_disagreement.py A.jsonl B.jsonl output.json
Arguments define analysis-local Coder A/B; no identities or input paths are emitted.
"""
import collections
import hashlib
import json
import sys
from pathlib import Path


def analyze(path_a, path_b):
    paths = [Path(path_a), Path(path_b)]
    layers = [[json.loads(s) for s in p.read_text(encoding='utf-8-sig').splitlines() if s.strip()] for p in paths]
    assert all(len(x) == 350 for x in layers)
    assert all(len({r['id'] for r in x}) == 350 for x in layers)
    bmap = {r['id']: r for r in layers[1]}
    counts = collections.Counter()
    swaps = collections.Counter()
    nested = collections.Counter()
    only = {c: collections.Counter() for c in 'AB'}
    chars = collections.Counter()
    for ra in layers[0]:
        rb = bmap[ra['id']]
        assert ra['text'] == rb['text']
        assert ra['meta']['confirmed'] is True and rb['meta']['confirmed'] is True
        aa, bb = [sorted(tuple(s) for s in r['label']) for r in (ra, rb)]
        text = ra['text']
        projected = []
        for spans in (aa, bb):
            assert len(spans) == len(set(spans))
            assert len(spans) == len({s[:2] for s in spans})
            labels = ['O'] * len(text)
            for start, end, typ in spans:
                assert 0 <= start < end <= len(text) and typ in 'LKST'
                assert all(x == 'O' for x in labels[start:end]), 'Overlapping within-coder spans require explicit projection policy'
                labels[start:end] = [typ] * (end-start)
            projected.append(labels)
        chars.update(zip(*projected))
        counts['sentences'] += 1
        counts['agree_sentences'] += aa == bb
        counts['both_empty'] += not aa and not bb
        counts['A_empty_B_nonempty'] += not aa and bool(bb)
        counts['B_empty_A_nonempty'] += not bb and bool(aa)
        counts['A_spans'] += len(aa)
        counts['B_spans'] += len(bb)
        counts['exact_matches'] += len(set(aa) & set(bb))
        counts['boundary_matches'] += len({s[:2] for s in aa} & {s[:2] for s in bb})
        kinds = set()
        for a in aa:
            for b in bb:
                if min(a[1], b[1]) <= max(a[0], b[0]):
                    continue
                if a[:2] == b[:2]:
                    if a[2] != b[2]:
                        swaps[a[2]+'->'+b[2]] += 1
                        kinds.add('same_boundary_type_difference')
                elif a[0] <= b[0] and b[1] <= a[1]:
                    key = 'B_inside_A:'+a[2]+'/'+b[2]
                    nested[key] += 1
                    kinds.add('B_inside_A')
                elif b[0] <= a[0] and a[1] <= b[1]:
                    key = 'A_inside_B:'+a[2]+'/'+b[2]
                    nested[key] += 1
                    kinds.add('A_inside_B')
                else:
                    kinds.add('partial_overlap')
                    counts['partial_overlap_pairs'] += 1
        for c, own, other in [('A', aa, bb), ('B', bb, aa)]:
            unmatched = [s for s in own if not any(min(s[1], t[1]) > max(s[0], t[0]) for t in other)]
            only[c].update(s[2] for s in unmatched)
            if unmatched:
                kinds.add(c+'_only_no_overlap')
        for kind in kinds:
            counts[kind+'_sentences'] += 1
    counts['disagree_sentences'] = counts['sentences']-counts['agree_sentences']
    n = sum(chars.values())
    marg_a, marg_b = collections.Counter(), collections.Counter()
    for (a,b), v in chars.items():
        marg_a[a] += v
        marg_b[b] += v
    observed = sum(v for (a,b),v in chars.items() if a == b)/n
    expected = sum(marg_a[t]*marg_b[t] for t in 'OLKST')/n**2
    pooled = marg_a + marg_b
    de = 1-sum(v*(v-1) for v in pooled.values())/(2*n*(2*n-1))
    metrics = {'exact_f1': 2*counts['exact_matches']/(counts['A_spans']+counts['B_spans']),
               'type_ignored_same_boundary_f1': 2*counts['boundary_matches']/(counts['A_spans']+counts['B_spans']),
               'character_n': n, 'character_accuracy': observed,
               'character_cohen_kappa': (observed-expected)/(1-expected),
               'character_nominal_krippendorff_alpha': 1-(1-observed)/de}
    return {'schema_version': 1, 'status': 'pre-adjudication disagreement',
            'scope': 'double-coded blind subset; analysis-local Coder A/B',
            'source_sha256': {c: hashlib.sha256(p.read_bytes()).hexdigest() for c,p in zip('AB',paths)},
            'verification': 'independently recomputed from both confirmed raw exports',
            'counts': dict(sorted(counts.items())), 'metrics': metrics,
            'same_boundary_type_swaps_A_to_B': dict(sorted(swaps.items())),
            'nested_all_pairs_A_type_B_type': dict(sorted(nested.items())),
            'no_overlap_spans_by_type': {c: dict(sorted(v.items())) for c,v in only.items()}}


if __name__ == '__main__':
    result = analyze(sys.argv[1], sys.argv[2])
    Path(sys.argv[3]).write_text(json.dumps(result, ensure_ascii=True, indent=2)+'\n', encoding='utf-8')
