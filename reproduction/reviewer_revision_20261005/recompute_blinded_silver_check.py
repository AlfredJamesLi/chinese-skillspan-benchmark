"""Recompute descriptive Silver-versus-blinded-human agreement from frozen inputs.

Python 3.9+ standard library only. No training, inference, relabeling, or input writes.
--human-dir points to the directory containing sample_manifest.json and latest50_A/B/C.jsonl.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import statistics
import zipfile


def sha(data):
    return hashlib.sha256(data).hexdigest()


def records(data):
    return [json.loads(s) for s in data.decode('utf-8-sig').splitlines() if s.strip()]


def text(row):
    return row.get('text', row.get('sentence', ''))


def span_set(row, field):
    source = row[field]
    spans = [(s['start'], s['end'], s.get('label', s.get('type'))) if isinstance(s, dict) else tuple(s) for s in source]
    assert len(set(spans)) == len(spans), 'Duplicate span in input'
    previous_end = 0
    for start, end, label in sorted(spans):
        assert isinstance(start, int) and isinstance(end, int)
        assert 0 <= start < end <= len(text(row)) and start >= previous_end
        assert label in ('L', 'K', 'S', 'T')
        previous_end = end
    return set(spans)


def score(silver, human, source_to_study):
    typed_matches = boundary_matches = n_silver = n_human = 0
    for source_id in sorted(silver):
        s = silver[source_id]
        h = human[source_to_study[source_id]]
        assert text(s) == text(h), 'Source text differs; do not normalize offsets'
        ss, hs = span_set(s, 'spans'), span_set(h, 'label')
        n_silver += len(ss)
        n_human += len(hs)
        typed_matches += len(ss & hs)
        boundary_matches += len({x[:2] for x in ss} & {x[:2] for x in hs})
    denominator = n_silver + n_human
    assert denominator > 0
    return {
        'TP': typed_matches, 'FP': n_silver - typed_matches, 'FN': n_human - typed_matches,
        'n_silver_spans': n_silver, 'n_human_spans': n_human,
        'typed_exact_micro_F1': 2 * typed_matches / denominator,
        'boundary_exact_micro_F1': 2 * boundary_matches / denominator,
    }


def compute(review_zip, human_dir):
    human_bytes = {f'latest50_{c}.jsonl': (human_dir / f'latest50_{c}.jsonl').read_bytes() for c in 'ABC'}
    manifest_bytes = (human_dir / 'sample_manifest.json').read_bytes()
    manifest = json.loads(manifest_bytes.decode('utf-8-sig'))
    assert len(manifest) == 50
    source_to_study = {r['source_id']: r['study_id'] for r in manifest}
    assert len(source_to_study) == len(set(source_to_study.values())) == 50
    human = {}
    for c in 'ABC':
        rr = records(human_bytes[f'latest50_{c}.jsonl'])
        assert len(rr) == 50 and all(r['confirmed'] for r in rr)
        human[c] = {r['study_id']: r for r in rr}
        assert set(human[c]) == set(source_to_study.values())
        for r in rr:
            span_set(r, 'label')
    assert all(text(human[c][s]) == text(human['A'][s]) for c in 'BC' for s in human['A'])
    assert len({text(r) for r in human['A'].values()}) == 50
    results, member_hashes, retained_ids = {}, {}, {}
    expected = {'codex_9540': {'train': 8842, 'val': 348, 'test': 350},
                'proxy_9646': {'train': 8943, 'val': 351, 'test': 352}}
    with zipfile.ZipFile(review_zip) as z:
        for pool, sizes in expected.items():
            hits = []
            split_counts = {}
            for split, count in sizes.items():
                member = f'expanded_silver_splits_20260920/{pool}/data/{split}.jsonl'
                b = z.read(member)
                member_hashes[member] = sha(b)
                rr = records(b)
                assert len(rr) == count
                matched = [r for r in rr if r['id'] in source_to_study]
                hits.extend(matched)
                split_counts[split] = len(matched)
            silver = {r['id']: r for r in hits}
            assert len(hits) == len(silver) == 49
            assert all(r['status'] in ('candidate_complete', 'confirmed_empty') for r in hits)
            for r in hits:
                ss = span_set(r, 'spans')
                assert (r['status'] == 'confirmed_empty') == (len(ss) == 0)
            retained_ids[pool] = set(silver)
            by_coder = {c: score(silver, human[c], source_to_study) for c in 'ABC'}
            results[pool] = {
                'n_compared_sentences': 49,
                'n_absent_from_final_pool': 1,
                'absent_records_scored_as_empty': False,
                'sample_membership_by_split': split_counts,
                'retained_status_counts': dict(sorted(collections.Counter(r['status'] for r in hits).items())),
                'recorded_prompt_id_counts': dict(sorted(collections.Counter(r.get('prompt_id', 'unrecorded') for r in hits).items())),
                'by_annotator': by_coder,
                'mean_typed_exact_micro_F1': statistics.mean(v['typed_exact_micro_F1'] for v in by_coder.values()),
                'mean_boundary_exact_micro_F1': statistics.mean(v['boundary_exact_micro_F1'] for v in by_coder.values()),
            }
    assert retained_ids['codex_9540'] == retained_ids['proxy_9646']
    return {
        'schema': 1,
        'analysis': 'Post hoc within-sample agreement between frozen expanded Silver labels and three separate final-handbook human annotation layers.',
        'scope': 'Descriptive cross-version comparison; no adjudicated consensus reference and no population-level Silver-quality estimate. Primary human-reference model scores are unchanged.',
        'scoring': {'typed_exact': 'Pool exact boundary-and-type matches across the same retained sentences for each annotator; F1 = 2TP / (2TP + FP + FN).',
                    'mean': 'Arithmetic mean of the three per-annotator micro-F1 scores.',
                    'boundary_exact': 'Same calculation after dropping type from each span.',
                    'offsets': 'Unmodified Unicode-code-point offsets; no text normalization.'},
        'checks': {'formal_sample_sentences': 50, 'all_three_human_texts_identical': True,
                   'all_human_annotations_confirmed': True, 'all_scored_spans_valid_and_nonoverlapping': True,
                   'same_49_source_ids_in_both_pools': True, 'silver_texts_identical_to_all_human_layers': True,
                   'all_retained_statuses_candidate_complete_or_confirmed_empty': True},
        'human_snapshot': {'export_date': '2026-10-03', 'handbook': 'B.sop_v4.2.14',
                           'full_50_span_counts': {c: sum(len(r['label']) for r in human[c].values()) for c in 'ABC'}},
        'results': results,
        'inputs_sha256': {'review_zip': sha(review_zip.read_bytes()),
                          'human_files': {**{n: sha(b) for n, b in human_bytes.items()}, 'sample_manifest.json': sha(manifest_bytes)},
                          'expanded_members': member_hashes},
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--review-zip', type=Path, required=True)
    p.add_argument('--human-dir', type=Path, required=True)
    p.add_argument('--output', type=Path, default=Path('PUBLIC_BLINDED_SILVER_CHECK.json'))
    args = p.parse_args()
    result = compute(args.review_zip, args.human_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: {'n': v['n_compared_sentences'], 'mean_typed_exact_micro_F1': v['mean_typed_exact_micro_F1']} for k, v in result['results'].items()}, indent=2))


if __name__ == '__main__':
    main()
