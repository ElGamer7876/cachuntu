#!/usr/bin/env python3
"""Replace the live ISO's visible Kubuntu GRUB labels with Cachuntu labels."""

from pathlib import Path
import sys

path = Path(sys.argv[1])
text = path.read_text()
assert 'Try or Install Kubuntu' in text
text = text.replace('Try or Install Kubuntu', 'Try or Install Cachuntu')
text = text.replace('Kubuntu (safe graphics)', 'Cachuntu (safe graphics)')
path.write_text(text)
