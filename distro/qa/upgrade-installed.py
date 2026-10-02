#!/usr/bin/env python3
"""Update only a disposable Cachuntu QA guest and capture the complete log."""
import os
from pathlib import Path
import shlex
import subprocess
import urllib.request

release = Path('/etc/os-release').read_text()
identity = dict(line.split('=', 1) for line in shlex.split(release, comments=True) if '=' in line)
root = subprocess.check_output(['findmnt', '-n', '-o', 'SOURCE', '/'], text=True)
if (os.geteuid() != 0 or identity.get('NAME') != 'Cachuntu'
        or identity.get('VERSION_CODENAME') != 'resolute'
        or root.strip() != '/dev/vda2[/@]'):
    raise SystemExit('Refusing: expected root inside the Cachuntu virtual guest')
if Path('/etc/hostname').read_text().strip() != 'cachuntu-vm':
    raise SystemExit('Refusing: expected disposable QA hostname')
sources = '\n'.join(p.read_text() for p in Path('/etc/apt').glob('sources.list*') if p.is_file())
sources += '\n'.join(p.read_text() for p in Path('/etc/apt/sources.list.d').glob('*') if p.suffix in ('.list', '.sources'))
if any(word in sources for word in ('stonking', '-proposed', 'devel')):
    raise SystemExit('Refusing: experimental APT source found')
env = dict(os.environ, LC_ALL='C', DEBIAN_FRONTEND='noninteractive')
log = Path('/tmp/cachuntu-upgrade.log')
status = 1
with log.open('w', buffering=1) as stream:
    def run(args, timeout=1800):
        stream.write('\nCOMMAND: ' + ' '.join(args) + '\n')
        result = subprocess.run(args, env=env, text=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, timeout=timeout)
        stream.write(result.stdout)
        stream.write('EXIT: ' + str(result.returncode) + '\n')
        if result.returncode:
            raise RuntimeError('Command failed: ' + args[0])
        return result.stdout
    try:
        run(['uname', '-r'])
        run(['apt-get', '-o', 'Acquire::ForceIPv4=true', '-o', 'APT::Update::Error-Mode=any', 'update'], 300)
        plan = run(['apt-get', '-s', 'full-upgrade'], 120)
        if any(line.startswith('Remv ') for line in plan.splitlines()):
            raise RuntimeError('Refusing automatic QA upgrade with package removals; inspect the plan')
        run(['apt-get', '-y', '-o', 'Dpkg::Options::=--force-confdef',
             '-o', 'Dpkg::Options::=--force-confold', 'full-upgrade'])
        if run(['dpkg', '--audit'], 120).strip():
            raise RuntimeError('Package audit is not empty')
        run(['/usr/lib/cachuntu/post-install-qa'], 300)
        run(['ls', '-lh', '/boot'])
        stream.write('\nUPGRADE_RESULT=PASS; reboot validation remains pending\n')
        status = 0
    except Exception as exc:
        stream.write('\nUPGRADE_RESULT=FAIL: ' + str(exc) + '\n')
request = urllib.request.Request('http://10.0.2.2:38763/upgrade', data=log.read_bytes(), method='POST')
with urllib.request.urlopen(request, timeout=30) as response:
    print(response.read().decode().strip())
print(log.read_text()[-5000:])
raise SystemExit(status)
