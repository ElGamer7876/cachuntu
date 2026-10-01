#!/usr/bin/env python3
"""Install the signed-index-derived Resolute package lock into a build root."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
from urllib.parse import urlsplit


def run(*args):
    return subprocess.check_output(args, text=True).strip()


def install(root, cache, lock_path):
    lock = json.loads(lock_path.read_text())
    if lock['ubuntu_codename'] != 'resolute':
        raise ValueError('Only Resolute security packages are permitted')
    os_release = (root / 'etc/os-release').read_text()
    if not re.search(r'^VERSION_CODENAME=[\"\']?resolute[\"\']?$', os_release, re.M):
        raise ValueError('Target must be Ubuntu Resolute')
    cache.mkdir(parents=True, exist_ok=True)
    packages = []
    seen = set()
    for item in lock['packages']:
        name = item['file']
        url = urlsplit(item['url'])
        if (name != Path(name).name or not name.endswith('.deb') or
                not re.fullmatch(r'[a-zA-Z0-9_.%+:-]+', name) or name in seen):
            raise ValueError('Invalid or duplicate archive filename')
        seen.add(name)
        if (url.scheme != 'https' or url.netloc not in ('archive.ubuntu.com', 'security.ubuntu.com')
                or not url.path.startswith('/ubuntu/pool/') or url.query or url.fragment):
            raise ValueError('Package must come from an official Ubuntu HTTPS pool')
        if item['architecture'] not in ('amd64', 'all') or not re.fullmatch(r'[0-9a-f]{64}', item['sha256']):
            raise ValueError('Invalid architecture or SHA256')
        archive = cache / name
        if not archive.exists():
            subprocess.run(['curl', '--fail', '--location', '--retry', '3',
                            '--proto', '=https', '--proto-redir', '=https',
                            '--output', str(archive), item['url']], check=True)
        with archive.open('rb') as stream:
            digest = hashlib.file_digest(stream, 'sha256').hexdigest()
        if digest != item['sha256']:
            raise ValueError(f'SHA256 mismatch: {name}')
        for field, expected in (('Package', item['name']), ('Version', item['version']),
                                ('Architecture', item['architecture'])):
            if run('dpkg-deb', '-f', str(archive), field) != expected:
                raise ValueError(f'{field} mismatch: {name}')
        print(f'Verified security package: {item["name"]} {item["version"]}', flush=True)
        packages.append(archive)
    if not packages:
        raise ValueError('Security lock is empty')
    policy = root / 'usr/sbin/policy-rc.d'
    if policy.exists() or policy.is_symlink():
        raise ValueError('Unexpected existing build service policy; preserve it explicitly')
    stage = root / 'tmp/cachuntu-security-debs'
    stage.mkdir(exist_ok=False)
    try:
        for archive in packages:
            shutil.copyfile(archive, stage / archive.name)
        policy.write_text('#!/bin/sh\nexit 101\n')
        policy.chmod(0o755)
        subprocess.run(['chroot', str(root), 'env', 'DEBIAN_FRONTEND=noninteractive',
                        'dpkg', '-i', *('/tmp/cachuntu-security-debs/' + p.name for p in packages)], check=True)
        audit = run('chroot', str(root), 'dpkg', '--audit')
        if audit:
            raise ValueError(f'Unfinished package configuration: {audit}')
        installed_lock = root / 'usr/share/cachuntu/security-updates.lock.json'
        installed_lock.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(lock_path, installed_lock)
    finally:
        if policy.exists():
            policy.unlink()
        shutil.rmtree(stage)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--cache', type=Path, required=True)
    parser.add_argument('--lock', type=Path, default=Path(__file__).with_name('security-updates.lock.json'))
    args = parser.parse_args()
    install(args.root.resolve(), args.cache.resolve(), args.lock.resolve())
