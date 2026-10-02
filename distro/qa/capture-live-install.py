#!/usr/bin/env python3
"""Capture the disposable live guest's installer log through its local NAT."""
import pathlib
import subprocess
import urllib.request

print(subprocess.check_output(['ps', '-eo', 'pid,etime,args'], text=True)[-18000:])
paths = [pathlib.Path('/tmp/cachuntu-calamares-launch.log'),
         pathlib.Path('/root/.cache/calamares/session.log')]
for path in paths:
    if path.is_file():
        data = path.read_bytes()
        request = urllib.request.Request('http://10.0.2.2:38763/installer', data=data, method='POST')
        with urllib.request.urlopen(request, timeout=15) as response:
            print(response.read().decode().strip(), path, len(data))
        print(data.decode(errors='replace')[-6000:])
        break
else:
    raise SystemExit('Installer log not found')
