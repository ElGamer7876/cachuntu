#!/usr/bin/env python3
"""Check that the first installer choices agree with their declared defaults."""
from pathlib import Path
import sys
import yaml

modules = Path(sys.argv[1]) / 'etc/calamares/modules'
def load(name):
    return yaml.safe_load((modules / name).read_text())

partition = load('partition.conf')
assert partition['defaultFileSystemType'] == 'btrfs'
assert partition['availableFileSystemTypes'][0] == 'btrfs'
assert set(partition['availableFileSystemTypes']) == {'btrfs', 'ext4', 'xfs'}
desktop = load('cachuntu-desktop.conf')
assert desktop['default'] == 'plasma'
assert {item['id'] for item in desktop['items']} == {'plasma', 'gnome'}
assert all(item.get('description') for item in desktop['items'])
font = load('cachuntu-font.conf')
assert font['default'] == 'cachuntu'
assert {item['id'] for item in font['items']} == {'cachuntu', 'desktop'}
optional = load('cachuntu-optional.conf')
assert optional['mode'] == 'optionalmultiple'
assert {item['id'] for item in optional['items']} == {'gaming', 'multimedia', 'development'}
assert all(item.get('description') and item.get('packages') for item in optional['items'])
print('Installer filesystem, desktop, font, and optional choices: OK')
