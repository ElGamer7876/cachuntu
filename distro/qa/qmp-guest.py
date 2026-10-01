#!/usr/bin/env python3
"""Inspect and operate only the disposable Cachuntu QEMU guest through QMP."""
import argparse
import json
import socket
import subprocess
import time

p = argparse.ArgumentParser()
p.add_argument('--socket', default='/home/elgam/cachuntu/.cache/cachuntu-preview3-qmp.sock')
p.add_argument('--hmp')
p.add_argument('--text')
p.add_argument('--type-only', action='store_true', help='Type text without Return')
p.add_argument('--click', nargs=2, type=int, metavar=('X', 'Y'))
p.add_argument('--screenshot', help='PNG path on the host filesystem')
a = p.parse_args()
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.settimeout(10)
s.connect(a.socket)
f = s.makefile('rwb', buffering=0)
json.loads(f.readline())

def call(command, arguments=None):
    request = {'execute': command}
    if arguments is not None:
        request['arguments'] = arguments
    f.write((json.dumps(request) + '\n').encode())
    while True:
        response = json.loads(f.readline())
        if 'error' in response:
            raise RuntimeError(response['error'])
        if 'return' in response:
            return response['return']

call('qmp_capabilities')
def send_keys(combo, hold=0.08):
    codes = combo.split('-')
    # QEMU schedules modifier releases together with each chord.
    call('send-key', {'keys': [{'type': 'qcode', 'data': code} for code in codes], 'hold-time': int(hold * 1000)})
    time.sleep(hold + 0.12)

if a.hmp:
    if a.hmp.startswith('sendkey '):
        fields = a.hmp.split()
        send_keys(fields[1], int(fields[2]) / 1000 if len(fields) > 2 else 0.08)
    else:
        print(call('human-monitor-command', {'command-line': a.hmp}))
if a.text is not None:
    time.sleep(0.5)
    keys = {' ': 'spc', '-': 'minus', '/': 'slash', '_': 'shift-minus', '.': 'dot', '=': 'equal', ',': 'comma'}
    for char in a.text:
        if not (char.isascii() and (char.isalpha() or char.isdigit() or char in keys)):
            raise ValueError(f'Unsupported guest typing character: {char!r}')
        key = 'shift-' + char.lower() if char.isupper() else keys.get(char, char)
        send_keys(key, 0.12)
    if not a.type_only:
        send_keys('ret')
    time.sleep(1)
if a.click:
    x, y = a.click
    if not (0 <= x <= 32767 and 0 <= y <= 32767):
        raise ValueError('Guest tablet coordinates must be between 0 and 32767')
    call('input-send-event', {'events': [
        {'type': 'abs', 'data': {'axis': 'x', 'value': x}},
        {'type': 'abs', 'data': {'axis': 'y', 'value': y}},
    ]})
    time.sleep(0.1)
    call('input-send-event', {'events': [
        {'type': 'btn', 'data': {'button': 'left', 'down': True}},
    ]})
    time.sleep(0.1)
    call('input-send-event', {'events': [
        {'type': 'btn', 'data': {'button': 'left', 'down': False}},
    ]})
if a.screenshot:
    time.sleep(2)
    call('human-monitor-command', {'command-line': 'screendump ' + a.screenshot + '.ppm'})
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', a.screenshot + '.ppm', a.screenshot], check=True)
s.close()
