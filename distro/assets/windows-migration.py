#!/usr/bin/env python3
"""Export personal folders and inspect/import a verified Cachuntu ZIP bundle."""
import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import zipfile

GROUPS = ('Documents', 'Pictures', 'Music', 'Videos')
MANIFEST = 'cachuntu-migration.json'

def linked(path):
    info = path.lstat()
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, 'st_file_attributes', 0) & 0x400)

def export_bundle(sources, output):
    output = Path(output).absolute()
    entries, skipped = [], []
    with zipfile.ZipFile(output, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=1) as bundle:
        for group, source in sources.items():
            base = Path(source).resolve(strict=True)
            if not base.is_dir():
                raise ValueError(f'{group}: source must be a directory')
            for directory, dirs, files in os.walk(base, followlinks=False):
                for name in list(dirs):
                    path = Path(directory) / name
                    if linked(path):
                        dirs.remove(name)
                        skipped.append(str(path))
                for name in files:
                    path = Path(directory) / name
                    if path.absolute() == output:
                        continue
                    if linked(path) or not path.is_file():
                        skipped.append(str(path))
                        continue
                    relative = path.resolve().relative_to(base)
                    member = PurePosixPath(group, *relative.parts).as_posix()
                    digest, size = hashlib.sha256(), 0
                    with path.open('rb') as src, bundle.open(member, 'w', force_zip64=True) as dst:
                        while chunk := src.read(1024 * 1024):
                            dst.write(chunk)
                            digest.update(chunk)
                            size += len(chunk)
                    entries.append({'path': member, 'size': size, 'sha256': digest.hexdigest()})
        bundle.writestr(MANIFEST, json.dumps({'format': 1, 'files': entries, 'skipped': skipped}, indent=2))
    return {'files': len(entries), 'bytes': sum(e['size'] for e in entries), 'skipped': skipped}

def inspect_bundle(bundle):
    infos = bundle.infolist()
    names = [item.filename for item in infos]
    if len(set(names)) != len(names):
        raise ValueError('Duplicate archive paths')
    info = bundle.getinfo(MANIFEST)
    if info.file_size > 16 * 1024 * 1024:
        raise ValueError('Manifest too large')
    data = json.loads(bundle.read(MANIFEST))
    if data.get('format') != 1 or not isinstance(data.get('files'), list):
        raise ValueError('Unsupported migration manifest')
    entries, seen = data['files'], set()
    for entry in entries:
        name = entry['path']
        path = PurePosixPath(name)
        if (not isinstance(name, str) or '\\' in name or ':' in name or '\x00' in name
                or path.is_absolute() or len(path.parts) < 2 or path.parts[0] not in GROUPS
                or any(part in ('', '.', '..') for part in name.split('/')) or name in seen):
            raise ValueError(f'Unsafe migration path: {name!r}')
        seen.add(name)
        info = bundle.getinfo(name)
        if stat.S_ISLNK(info.external_attr >> 16) or info.is_dir():
            raise ValueError(f'Links and directory entries are not supported: {name}')
        if type(entry['size']) is not int or entry['size'] < 0 or entry['size'] != info.file_size:
            raise ValueError(f'Invalid size: {name}')
        if not re.fullmatch('[0-9a-f]{64}', entry['sha256']):
            raise ValueError(f'Invalid checksum: {name}')
    if set(names) != seen | {MANIFEST}:
        raise ValueError('Archive contains files absent from the manifest')
    return data

def import_bundle(source, destination):
    destination = Path(destination).absolute()
    with zipfile.ZipFile(source) as bundle:
        data = inspect_bundle(bundle)
        total = sum(e['size'] for e in data['files'])
        if destination.exists() or destination.is_symlink():
            raise ValueError('Choose a new destination folder; existing folders are never overwritten')
        if total + 64 * 1024 * 1024 > shutil.disk_usage(destination.parent).free:
            raise ValueError('Insufficient free space for this migration')
        destination.mkdir(mode=0o700)
        try:
            for entry in data['files']:
                target = destination.joinpath(*PurePosixPath(entry['path']).parts)
                target.parent.mkdir(parents=True, exist_ok=True)
                digest = hashlib.sha256()
                with bundle.open(entry['path']) as src, target.open('xb') as dst:
                    os.chmod(target, 0o600)
                    while chunk := src.read(1024 * 1024):
                        dst.write(chunk)
                        digest.update(chunk)
                if digest.hexdigest() != entry['sha256']:
                    raise ValueError(f'Checksum mismatch: {entry["path"]}')
            (destination / MANIFEST).write_text(json.dumps(data, indent=2))
        except Exception:
            # Retain incomplete data for inspection, never remove user files.
            (destination / 'IMPORT_INCOMPLETE.txt').write_text('Import failed. Do not treat this folder as a completed migration.\n')
            raise
    return {'destination': str(destination), 'files': len(data['files']), 'bytes': total}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_subparsers(dest='action', required=True)
    export = actions.add_parser('export', help='Run on Windows or an accessible Windows backup')
    for group in GROUPS:
        export.add_argument('--' + group.lower())
    export.add_argument('--output', required=True)
    plan = actions.add_parser('plan', help='Inspect a bundle without copying personal files')
    plan.add_argument('bundle')
    apply = actions.add_parser('import', help='Copy into a new folder, validating every checksum')
    apply.add_argument('bundle')
    apply.add_argument('--destination', default=str(Path.home() / ('Windows-import-' + datetime.now().strftime('%Y%m%d-%H%M%S'))))
    ssh = actions.add_parser('fetch-ssh', help='Fetch an exported ZIP through OpenSSH/SFTP')
    ssh.add_argument('--host', required=True, help='user@hostname, with SSH already configured')
    ssh.add_argument('--remote-file', required=True)
    ssh.add_argument('--output', required=True)
    args = parser.parse_args()
    if args.action == 'export':
        sources = {g: getattr(args, g.lower()) for g in GROUPS if getattr(args, g.lower())}
        if not sources:
            parser.error('Select at least one personal folder')
        result = export_bundle(sources, args.output)
    elif args.action == 'plan':
        with zipfile.ZipFile(args.bundle) as bundle:
            result = inspect_bundle(bundle)
    elif args.action == 'import':
        result = import_bundle(args.bundle, args.destination)
    else:
        if not re.fullmatch(r'[A-Za-z0-9_.-]+@[A-Za-z0-9][A-Za-z0-9.-]*', args.host):
            parser.error('Expected user@hostname')
        if not re.fullmatch(r'[A-Za-z0-9 /_.()-]+', args.remote_file) or not args.remote_file.endswith('.zip'):
            parser.error('Use a ZIP path without shell metacharacters, for example Migration/cachuntu.zip')
        output = Path(args.output).absolute()
        # An exclusive directory avoids overwriting an existing downloaded bundle.
        stage = output.parent / (output.name + '.download')
        if output.exists():
            parser.error('Output already exists')
        stage.mkdir(mode=0o700)
        incoming = stage / 'bundle.zip'
        subprocess.run(['scp', '-o', 'StrictHostKeyChecking=ask', '--', args.host + ':' + args.remote_file, str(incoming)], check=True)
        with zipfile.ZipFile(incoming) as bundle:
            inspect_bundle(bundle)
        # Exclusive publication; do not replace a file created during download.
        with incoming.open('rb') as src, output.open('xb') as dst:
            shutil.copyfileobj(src, dst)
        incoming.unlink()
        stage.rmdir()
        result = {'bundle': str(output), 'status': 'downloaded; run plan before import'}
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
