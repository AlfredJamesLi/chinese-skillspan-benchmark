"""Verify external-task inputs; optionally fetch missing files at frozen revisions.

Added for the 2026-10-17 code release. This is not a historical experiment script.
Only public Hugging Face dataset sources recorded in the retained manifests are
used. Source-specific access and reuse terms continue to apply.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import quote, urlsplit
from urllib.request import Request, urlopen


HERE = Path(__file__).resolve().parent


def checked_path(root, relative):
    rel = PurePosixPath(relative)
    if rel.is_absolute() or not rel.parts or any(p in ('..', '.') for p in rel.parts) or '\\' in relative or ':' in relative:
        raise ValueError('Unsafe manifest path: ' + relative)
    target = (root / Path(*rel.parts)).resolve()
    target.relative_to(root.resolve())
    return target


def matches(content, record):
    return len(content) == record['bytes'] and hashlib.sha256(content).hexdigest() == record['sha256']


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-root', type=Path, default=HERE / 'data', help='Directory containing one subdirectory per dataset.')
    parser.add_argument('--download', action='store_true', help='Fetch missing files only; never replace an existing file.')
    args = parser.parse_args(argv)
    reports = []
    manifests = sorted((HERE / 'data').glob('*/download_manifest.json'))
    for manifest_path in manifests:
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        name = manifest_path.parent.name
        if manifest['dataset'] != name:
            raise ValueError('Dataset name disagrees with manifest directory')
        source = manifest['source'].rstrip('/')
        parsed = urlsplit(source)
        if parsed.scheme != 'https' or parsed.netloc != 'huggingface.co' or not re.fullmatch(r'/datasets/[\w.-]+/[\w.-]+', parsed.path) or parsed.query or parsed.fragment:
            raise ValueError('Unexpected source: ' + source)
        revision = manifest['revision']
        if not re.fullmatch(r'[0-9a-f]{40}', revision):
            raise ValueError('An immutable 40-character revision is required')
        root = checked_path(args.data_root, name)
        for record in manifest['files']:
            path = checked_path(root, record['path'])
            status = 'missing'
            if path.exists():
                status = 'verified' if matches(path.read_bytes(), record) else 'checksum_mismatch'
            elif args.download:
                url = source + '/resolve/' + revision + '/' + quote(record['path'], safe='/')
                try:
                    request = Request(url, headers={'User-Agent': 'Chinese-SkillSpan-code-materials-20261017'})
                    with urlopen(request, timeout=60) as response:
                        content = response.read(record['bytes'] + 1)
                    if not matches(content, record):
                        status = 'download_checksum_mismatch'
                    else:
                        path.parent.mkdir(parents=True, exist_ok=True)
                        # Exclusive creation prevents replacement if another process
                        # creates this file while the download is in progress.
                        with path.open('xb') as output:
                            output.write(content)
                        status = 'downloaded_and_verified'
                except (OSError, ValueError) as error:
                    status = 'download_failed: ' + str(error)
            reports.append({'dataset': name, 'file': record['path'], 'status': status})
    ok = bool(manifests) and all(r['status'] in ('verified', 'downloaded_and_verified') for r in reports)
    print(json.dumps({'ok': ok, 'manifests': len(manifests), 'files': reports}, indent=2))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
