#!/usr/bin/env python3
"""Verify rejection of outdated, absent, unconfigured and multiarch packages."""
import importlib.util
from pathlib import Path
spec = importlib.util.spec_from_file_location('security', Path(__file__).with_name('check-security-baseline.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
baseline = {'packages': [{'name': 'library', 'minimum': '1:2.0-1ubuntu0.2', 'required': True, 'notice': 'fixture'}, {'name': 'optional', 'minimum': '2.0', 'required': False, 'notice': 'fixture'}]}
def record(version, status='installed', name='library:amd64'):
    return {'name': name, 'version': version, 'status': status}
assert module.evaluate(baseline, [record('1:2.0-1ubuntu0.2')])[0] == 0
assert module.evaluate(baseline, [record('1:2.0-1ubuntu0.3')])[0] == 0
assert module.evaluate(baseline, [record('2.0-1ubuntu0.3')])[0] == 1
assert module.evaluate(baseline, [record('1:2.0-1ubuntu0.1')])[0] == 1
assert module.evaluate(baseline, [record('1:2.0-1ubuntu0.2', 'unpacked')])[0] == 1
assert module.evaluate(baseline, [record('1:2.0-1ubuntu0.2'), record('1:2.0-1ubuntu0.1', name='library:i386')])[0] == 1
assert module.evaluate(baseline, [record('1:2.0-1ubuntu0.2'), record('1.9', name='optional:amd64')])[0] == 1
assert module.evaluate(baseline, [])[0] == 1
print('Security baseline: version epochs, missing, unconfigured, optional and multiarch cases passed')
