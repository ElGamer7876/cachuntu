#!/usr/bin/env python3
"""Exercise ISO checksum updates and reject incomplete checksum manifests."""
from pathlib import Path
import hashlib
import subprocess
import tempfile

updater = Path(__file__).resolve().parents[1] / 'update-md5sums.py'
with tempfile.TemporaryDirectory() as temporary:
    root = Path(temporary)
    squash, grub, sums = (root / name for name in ('squash', 'grub', 'md5sum.txt'))
    squash.write_bytes(b'filesystem fixture')
    grub.write_bytes(b'branded grub fixture')
    original = '0' * 32 + '  ./casper/filesystem.squashfs\n' + '0' * 32 + '  ./boot/grub/grub.cfg\n'
    sums.write_text(original)
    command = ['python3', str(updater), str(sums), str(squash), f'boot/grub/grub.cfg={grub}']
    subprocess.run(command, check=True)
    expected = hashlib.md5(squash.read_bytes()).hexdigest() + '  ./casper/filesystem.squashfs\n' + hashlib.md5(grub.read_bytes()).hexdigest() + '  ./boot/grub/grub.cfg\n'
    assert sums.read_text() == expected
    for invalid in [original.splitlines(keepends=True)[0], original + original.splitlines(keepends=True)[1]]:
        sums.write_text(invalid)
        assert subprocess.run(command, capture_output=True).returncode != 0
        assert sums.read_text() == invalid
print('ISO checksum replacement and invalid manifest checks passed.')
