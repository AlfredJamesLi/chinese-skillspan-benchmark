"""Read-only aggregate audit of the frozen adopted Expanded Silver pool.

No source texts, row identifiers, labels, predictions or archive files are written.
The JobBERT dev file is a validation+test union, not an additional partition.
"""
from pathlib import Path
from collections import Counter
import argparse
import csv
import hashlib
import itertools
import json
import unicodedata
import zipfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source-zip', type=Path, required=True)
parser.add_argument('--reference-package', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
PACK = args.source_zip.resolve()
OLD = args.reference_package.resolve()
OUT = args.output.resolve()
OUT.mkdir(parents=True, exist_ok=True)
PREFIX = 'expanded_silver_splits_20260920/codex_9540/'
TYPES = 'LSKT'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def load(z, path):
    return [json.loads(line) for line in z.read(path).decode('utf-8-sig').splitlines() if line.strip()]

def normalize(text):
    return ''.join(unicodedata.normalize('NFKC', text).split()).casefold()

def histogram(items):
    return {str(key): value for key, value in sorted(Counter(items).items())}

def pack(name, rows):
    spans = [span for row in rows for span in row['spans']]
    counts = Counter(span[2] for span in spans)
    empty = sum(not row['spans'] for row in rows)
    return {
        'name': name, 'n_records': len(rows), 'n_spans': len(spans),
        'empty_records': empty, 'empty_percent': empty / len(rows) * 100,
        'types': {kind: counts[kind] for kind in TYPES},
        'type_percent': {kind: counts[kind] / len(spans) * 100 for kind in TYPES},
        'input_lengths': histogram(len(row['sentence']) for row in rows),
        'span_lengths': histogram(span[1] - span[0] for span in spans),
        'spans_per_record': histogram(len(row['spans']) for row in rows),
        'unique_ids': len({str(row['id']) for row in rows}),
        'duplicate_records_by': {
            'id': len(rows) - len({str(row['id']) for row in rows}),
            'exact_text': len(rows) - len({row['sentence'] for row in rows}),
            'nfc_text': len(rows) - len({unicodedata.normalize('NFC', row['sentence']) for row in rows}),
            'nfkc_casefold_no_whitespace_text': len(rows) - len({normalize(row['sentence']) for row in rows}),
        },
    }

report = {
    'schema': 1, 'pool': 'adopted Expanded Silver (Codex)',
    'counting_unit': 'frozen experimental records; no deduplication or relabeling',
    'length_unit': 'Unicode code points',
    'source_zip': {'path': PACK.name, 'sha256': sha(PACK.read_bytes())},
    'source_files': [], 'splits': [], 'checks': {},
    'scope': 'Complete adopted pool only; excludes alternative pool and sampled human-review labels.',
}
expected_zip_sha = '53490f44499887a3d1fc9d09f9d84e63013361fbdcb1cfb217a85f6a04b18617'
assert report['source_zip']['sha256'] == expected_zip_sha
report['checks']['zip_sha256_matches_frozen_receipt'] = True
with zipfile.ZipFile(PACK) as z, zipfile.ZipFile(OLD) as old:
    report['checks']['zip_crc_valid'] = z.testzip() is None
    split_metadata = json.loads(z.read(PREFIX + 'SPLIT.json'))
    original_manifest_path = 'CNSS_Qwen_Reproduction/expanded_silver/codex_seed42/data/SPLIT_IDS_MANIFEST.json'
    original_manifest = json.loads(old.read(original_manifest_path))
    report['independent_manifest'] = {
        'archive': OLD.name, 'member': original_manifest_path,
        'sha256': sha(old.read(original_manifest_path)),
    }
    split_rows = {}
    validation_counts = Counter()
    for split, expected, occurrence_name in [('train', 8842, 'train'), ('val', 348, 'dev'), ('test', 350, 'test')]:
        name = PREFIX + 'data/' + split + '.jsonl'
        rows = load(z, name)
        occname = PREFIX + 'data/' + occurrence_name + '_occurrence.jsonl'
        occ = load(z, occname)
        assert len(rows) == len(occ) == expected == original_manifest[split]['n']
        assert [str(row['id']) for row in rows] == [str(row['id']) for row in occ]
        assert sha(z.read(occname)) == original_manifest[split]['source_sha256']
        ids = load(old, 'CNSS_Qwen_Reproduction/expanded_silver/codex_seed42/data/split_ids_' + split + '.jsonl')
        assert [str(row['id']) for row in rows] == [str(row['id']) for row in ids]
        for row, target in zip(rows, occ):
            text, spans = row['sentence'], row['spans']
            assert isinstance(text, str) and text
            assert ''.join(row['tokens']) == text
            assert len({tuple(span) for span in spans}) == len(spans)
            tags = ['O'] * len(text)
            for start, end, kind in spans:
                assert isinstance(start, int) and isinstance(end, int)
                assert 0 <= start < end <= len(text) and kind in TYPES
                assert all(tag == 'O' for tag in tags[start:end])
                tags[start:end] = ['B-' + kind] + ['I-' + kind] * (end - start - 1)
            assert tags == row['list_of_selection_bio4']
            assert target['text'] == text
            offsets = [(span['start'], span['end'], span['type']) for span in target['source_spans_offset']]
            assert sorted(offsets) == sorted(tuple(span) for span in spans)
            resolved = []
            for target_span in target['target_spans']:
                piece = target_span['text']
                starts, cursor = [], 0
                assert piece
                while True:
                    start = text.find(piece, cursor)
                    if start < 0:
                        break
                    starts.append(start)
                    cursor = start + 1
                index = target_span['occurrence']
                assert isinstance(index, int) and 0 <= index < len(starts)
                resolved.append((starts[index], starts[index] + len(piece), target_span['type']))
            assert sorted(resolved) == sorted(offsets)
            assistant = json.loads(target['assistant'])
            assert str(assistant['id']) == str(row['id']) and assistant['spans'] == target['target_spans']
            validation_counts['records_checked'] += 1
            validation_counts['spans_checked'] += len(spans)
        group = pack(split, rows)
        group['source'] = name
        group['sha256'] = sha(z.read(name))
        group['occurrence_source'] = occname
        group['occurrence_sha256'] = sha(z.read(occname))
        report['source_files'].extend([
            {'member': name, 'sha256': group['sha256'], 'bytes': len(z.read(name))},
            {'member': occname, 'sha256': group['occurrence_sha256'], 'bytes': len(z.read(occname))},
        ])
        report['splits'].append(group)
        split_rows[split] = rows
    all_rows = split_rows['train'] + split_rows['val'] + split_rows['test']
    report['full_pool'] = pack('Expanded Silver', all_rows)
    assert len(all_rows) == 9540 == split_metadata['n_keep']
    assert report['full_pool']['unique_ids'] == 9540
    for field in ['n_records', 'n_spans', 'empty_records']:
        assert report['full_pool'][field] == sum(group[field] for group in report['splits'])
    for kind in TYPES:
        assert report['full_pool']['types'][kind] == sum(group['types'][kind] for group in report['splits'])
    for group in report['splits'] + [report['full_pool']]:
        assert sum(group['input_lengths'].values()) == group['n_records']
        assert sum(group['span_lengths'].values()) == group['n_spans'] == sum(group['types'].values())
        assert sum(group['spans_per_record'].values()) == group['n_records']
        assert sum(int(k) * v for k, v in group['spans_per_record'].items()) == group['n_spans']
        assert group['spans_per_record'].get('0', 0) == group['empty_records']
    jobbert_dev = load(z, PREFIX + 'data/dev.jsonl')
    expected_jobbert = {str(row['id']): row for row in split_rows['val'] + split_rows['test']}
    assert len(jobbert_dev) == 698
    assert {str(row['id']): row for row in jobbert_dev} == expected_jobbert
    report['checks']['jobbert_dev_is_val_plus_test_not_additional_records'] = True
    report['checks']['split_hashes_and_id_order_match_original_qwen_archive'] = True
    report['checks']['offsets_bio_tokens_occurrence_targets_and_assistant_json_agree'] = True
    report['checks'].update(validation_counts)
    report['checks']['count_sums_valid'] = True
    report['cross_split_overlap'] = {}
    for left, right in itertools.combinations(split_rows, 2):
        report['cross_split_overlap'][left + '__' + right] = {
            'id': len({str(r['id']) for r in split_rows[left]} & {str(r['id']) for r in split_rows[right]}),
            'exact_text': len({r['sentence'] for r in split_rows[left]} & {r['sentence'] for r in split_rows[right]}),
            'nfc_text': len({unicodedata.normalize('NFC', r['sentence']) for r in split_rows[left]} & {unicodedata.normalize('NFC', r['sentence']) for r in split_rows[right]}),
            'nfkc_casefold_no_whitespace_text': len({normalize(r['sentence']) for r in split_rows[left]} & {normalize(r['sentence']) for r in split_rows[right]}),
        }
report['checks']['success'] = True
(OUT / 'expanded_silver_profile.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
columns = ['subset', 'records', 'spans', 'empty_records', 'empty_percent', 'L', 'S', 'K', 'T']
with (OUT / 'expanded_silver_class_counts.csv').open('w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=columns)
    writer.writeheader()
    for group in report['splits'] + [report['full_pool']]:
        writer.writerow(dict(subset=group['name'], records=group['n_records'], spans=group['n_spans'],
            empty_records=group['empty_records'], empty_percent=group['empty_percent'], **group['types']))
print(json.dumps({
    'full_pool': {key: value for key, value in report['full_pool'].items() if key not in ['input_lengths', 'span_lengths', 'spans_per_record']},
    'splits': [{key: g[key] for key in ['name', 'n_records', 'n_spans', 'empty_records', 'empty_percent', 'types']} for g in report['splits']],
    'checks': report['checks'], 'cross_split_overlap': report['cross_split_overlap'],
}, indent=2))
