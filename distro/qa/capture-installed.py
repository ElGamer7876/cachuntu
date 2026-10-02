#!/usr/bin/env python3
"""Capture post-install checks from the disposable QA guest, without editing it."""
import argparse
import json
import os
import subprocess
import urllib.request

parser = argparse.ArgumentParser()
parser.add_argument('--post-route', choices=('postinstall', 'reboot'), default='postinstall')
args = parser.parse_args()
if os.geteuid() != 0 or open('/etc/hostname').read().strip() != 'cachuntu-vm':
    raise SystemExit('Refusing: expected the disposable QA guest as root')

def run(argv, timeout=120):
    result = subprocess.run(argv, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, timeout=timeout)
    return {'status': result.returncode, 'output': result.stdout}

def upload(route, data):
    request = urllib.request.Request('http://10.0.2.2:38763/' + route,
                                    data=data, method='POST')
    with urllib.request.urlopen(request, timeout=15) as response:
        print(response.read().decode().strip(), route)

qa = run(['/usr/lib/cachuntu/post-install-qa'])
upload(args.post_route, qa['output'].encode())
user = os.environ.get('SUDO_USER', 'cachuntuqa')
uid = subprocess.check_output(['id', '-u', user], text=True).strip()
sessions = []
for line in run(['loginctl', 'list-sessions', '--no-legend', '--no-pager'])['output'].splitlines():
    session = line.split()[0]
    fields = run(['loginctl', 'show-session', session, '-p', 'Type', '-p', 'State',
                  '-p', 'Name', '-p', 'VTNr', '-p', 'Active'])['output']
    sessions.append(dict(line.split('=', 1) for line in fields.splitlines() if '=' in line))
report = {'post_install_status': qa['status'], 'sessions': sessions,
          'kernel': run(['uname', '-r']),
          'package_anchors': run(['dpkg-query', '-W', 'cachuntu-defaults',
                                  'cachuntu-branding', 'cachuntu-performance',
                                  'linux-generic', 'linux-firmware', 'network-manager']),
          'root': run(['findmnt', '-n', '-o', 'FSTYPE,OPTIONS', '/']),
          'plasma': run(['ps', '-C', 'plasmashell', '-C', 'kwin_wayland', '-o', 'pid,args']),
          'font': run(['runuser', '-u', user, '--', 'kreadconfig6', '--file', 'kdeglobals',
                       '--group', 'General', '--key', 'font']),
          'font_match': run(['runuser', '-u', user, '--', 'fc-match', 'sans-serif']),
          'failed_user_units': run(['runuser', '-u', user, '--', 'env',
                                    'XDG_RUNTIME_DIR=/run/user/' + uid,
                                    'DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/' + uid + '/bus',
                                    'systemctl', '--user', '--failed', '--no-pager'])}
upload('runtime', (json.dumps(report, indent=2) + '\n').encode())
print(json.dumps(report, indent=2))
raise SystemExit(qa['status'])
