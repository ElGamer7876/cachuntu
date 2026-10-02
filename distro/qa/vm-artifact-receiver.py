#!/usr/bin/env python3
"""Receive bounded QA artifacts on localhost through the QEMU NAT host."""
import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import re

parser = argparse.ArgumentParser()
parser.add_argument('--output', type=Path, required=True)
parser.add_argument('--version', required=True)
args = parser.parse_args()
if not re.fullmatch(r'[0-9]+(?:\.[0-9]+){2,3}', args.version):
    parser.error('Expected a numeric Cachuntu version')
args.output.mkdir(parents=True, exist_ok=True)
names = {'/installer': 'calamares-live.log', '/postinstall': 'post-install.log',
         '/runtime': 'runtime.json', '/upgrade': 'upgrade.log', '/reboot': 'post-reboot.log'}

class Receiver(BaseHTTPRequestHandler):
    def do_POST(self):
        self.connection.settimeout(10)
        try:
            length = int(self.headers.get('Content-Length', '-1'))
        except ValueError:
            self.send_error(400)
            return
        if self.path not in names or not 0 <= length <= 16 * 1024 * 1024:
            self.send_error(400)
            return
        data = self.rfile.read(length)
        if len(data) != length:
            self.send_error(400)
            return
        target = args.output / (args.version + '-' + names[self.path])
        partial = target.with_suffix(target.suffix + '.part')
        partial.write_bytes(data)
        partial.replace(target)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Saved VM diagnostic artifact\n')

print('QA receiver: localhost:38763; fixed routes; POST only', flush=True)
HTTPServer(('127.0.0.1', 38763), Receiver).serve_forever()
