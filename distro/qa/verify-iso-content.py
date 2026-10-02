#!/usr/bin/env python3
"""Hash ISO file extents without mounting or extracting the large live image."""
import argparse
import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('iso', type=Path)
p.add_argument('--report', type=Path, required=True)
a = p.parse_args()
assert a.iso.is_file(), 'ISO must be a regular file'
size = a.iso.stat().st_size
result = subprocess.run(['xorriso', '-indev', str(a.iso), '-find', '/',
                         '-type', 'f', '-exec', 'report_sections', '--'],
                        check=True, capture_output=True, text=True)
extents = {}
for line in result.stdout.splitlines():
    if not line.startswith('File data lba: '):
        continue
    fields = next(csv.reader([line.removeprefix('File data lba: ')],
                             quotechar="'", skipinitialspace=True))
    assert len(fields) == 5, line
    index, lba, blocks, length = map(int, fields[:4])
    name = fields[4]
    assert name.startswith('/') and '..' not in Path(name).parts
    parts = extents.setdefault(name, [])
    assert index == len(parts), f'Unexpected extent order: {name}'
    assert 0 <= length <= blocks * 2048 and lba >= 0
    assert lba * 2048 + length <= size, f'Out of bounds: {name}'
    parts.append((lba * 2048, length))

with a.iso.open('rb') as stream:
    def chunks(name):
        assert name in extents, f'Missing ISO file: {name}'
        for offset, remaining in extents[name]:
            stream.seek(offset)
            while remaining:
                data = stream.read(min(4 * 1024 * 1024, remaining))
                assert data, f'Short read: {name}'
                remaining -= len(data)
                yield data

    manifest = b''.join(chunks('/md5sum.txt')).decode('utf-8')
    seen = set()
    for line in manifest.splitlines():
        match = re.fullmatch(r'([0-9a-fA-F]{32})  (?:\./)?(.+)', line)
        assert match, f'Invalid checksum entry: {line}'
        expected, relative = match.groups()
        name = '/' + relative
        assert name not in seen and '..' not in Path(name).parts
        seen.add(name)
        digest = hashlib.md5()
        for data in chunks(name):
            digest.update(data)
        assert digest.hexdigest() == expected.lower(), f'Checksum mismatch: {name}'
    assert len(seen) > 0, 'Empty checksum manifest'
    stream.seek(0)
    digest = hashlib.file_digest(stream, 'sha256').hexdigest()

report = {'iso': str(a.iso.resolve()), 'bytes': size, 'sha256': digest,
          'manifest_files_checked': len(seen), 'iso_content_validation': 'passed',
          'runtime_validation': 'not_assessed'}
a.report.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
