#!/usr/bin/env python3
"""Check installed package versions against reviewed Ubuntu security notices."""
import argparse
import json
from pathlib import Path
import subprocess

def evaluate(baseline, records):
    messages, failed = [], False
    for package in baseline['packages']:
        installed = [r for r in records if r['name'].split(':')[0] == package['name'] and r['status'] == 'installed']
        if not installed:
            if package['required']:
                messages.append(f"FAIL {package['name']}: required package is absent ({package['notice']})")
                failed = True
            else:
                messages.append(f"SKIP {package['name']}: not installed")
        for record in installed:
            result = subprocess.run(['dpkg', '--compare-versions', record['version'], 'ge', package['minimum']], check=False)
            if result.returncode == 0:
                messages.append(f"OK {record['name']} {record['version']} ({package['notice']})")
            else:
                failed = True
                messages.append(f"FAIL {record['name']} {record['version']}: needs >= {package['minimum']} ({package['notice']})")
    return int(failed), messages

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path('/'))
    parser.add_argument('--baseline', type=Path)
    args = parser.parse_args()
    source_default = Path(__file__).resolve().parents[1] / 'security-baseline.json'
    baseline_path = args.baseline or (source_default if source_default.exists() else Path('/usr/share/cachuntu/security-baseline.json'))
    baseline = json.loads(baseline_path.read_text())
    release = dict(line.split('=', 1) for line in (args.root / 'etc/os-release').read_text().splitlines() if '=' in line)
    if release.get('VERSION_CODENAME', '').strip('"') != baseline['ubuntu_codename']:
        parser.error('Security baseline belongs to Ubuntu Resolute; do not apply it to canary or another base')
    query = subprocess.run(['dpkg-query', '--admindir=' + str(args.root / 'var/lib/dpkg'), '-W', '-f=${binary:Package}\t${Version}\t${db:Status-Status}\n'], check=True, text=True, capture_output=True)
    records = [dict(zip(('name', 'version', 'status'), line.split('\t'))) for line in query.stdout.splitlines()]
    code, messages = evaluate(baseline, records)
    print('\n'.join(messages))
    raise SystemExit(code)

if __name__ == '__main__':
    main()
