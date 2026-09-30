#!/usr/bin/env python3
"""Replace the live ISO's visible Kubuntu GRUB labels with Cachuntu labels."""

from pathlib import Path
import sys

path = Path(sys.argv[1])
text = path.read_text()
assert 'Try or Install Kubuntu' in text or 'Try or Install Cachuntu' in text
text = text.replace('Try or Install Kubuntu', 'Try or Install Cachuntu')
text = text.replace('Kubuntu (safe graphics)', 'Cachuntu (safe graphics)')
# The upstream live initrd still contains Kubuntu's Plymouth art. Keep its
# splash disabled until a Cachuntu initrd theme is built and verified.
text = text.replace('--- quiet splash', '--- quiet')
path.write_text(text)
