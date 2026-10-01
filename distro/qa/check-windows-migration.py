#!/usr/bin/env python3
"""Exercise data integrity, conflicts, traversal and link rejection."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import zipfile

repo = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('migration', repo / 'distro/assets/windows-migration.py')
migration = importlib.util.module_from_spec(spec)
spec.loader.exec_module(migration)

def rejected(fn):
    try:
        fn()
    except (ValueError, KeyError):
        return
    raise AssertionError('Unsafe input was accepted')

with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    docs = root / 'documents'
    docs.mkdir()
    (docs / 'notes.txt').write_text('Cachuntu migration\n')
    (docs / 'photo.bin').write_bytes(bytes(range(256)))
    outside = root / 'outside.txt'
    outside.write_text('Do not migrate this linked file')
    (docs / 'linked.txt').symlink_to(outside)
    bundle = root / 'bundle.zip'
    summary = migration.export_bundle({'Documents': docs}, bundle)
    assert summary['files'] == 2 and len(summary['skipped']) == 1
    destination = root / 'imported'
    migration.import_bundle(bundle, destination)
    assert (destination / 'Documents/notes.txt').read_bytes() == (docs / 'notes.txt').read_bytes()
    assert (destination / 'Documents/photo.bin').read_bytes() == (docs / 'photo.bin').read_bytes()
    rejected(lambda: migration.import_bundle(bundle, destination))
    assert outside.read_text() == 'Do not migrate this linked file'
    for member in ('../outside.txt', '/tmp/outside.txt', 'Documents/../outside.txt', 'Documents\\outside.txt'):
        path = root / ('invalid-' + str(len(list(root.glob('invalid-*')))) + '.zip')
        content = b'data'
        with zipfile.ZipFile(path, 'w') as archive:
            archive.writestr(member, content)
            archive.writestr(migration.MANIFEST, json.dumps({'format': 1, 'files': [{'path': member, 'size': len(content), 'sha256': hashlib.sha256(content).hexdigest()}]}))
        rejected(lambda: migration.import_bundle(path, root / 'unsafe'))
        assert not (root / 'unsafe').exists()
    bad = root / 'tampered.zip'
    with zipfile.ZipFile(bad, 'w') as archive:
        archive.writestr('Documents/notes.txt', b'bad')
        archive.writestr(migration.MANIFEST, json.dumps({'format': 1, 'files': [{'path': 'Documents/notes.txt', 'size': 3, 'sha256': '0' * 64}]}))
    rejected(lambda: migration.import_bundle(bad, root / 'tampered'))
    assert (root / 'tampered/IMPORT_INCOMPLETE.txt').exists()
    assert outside.read_text() == 'Do not migrate this linked file'
print('Windows migration: integrity, no overwrite, traversal and links passed')
