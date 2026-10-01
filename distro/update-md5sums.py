#!/usr/bin/env python3
"""Refresh checksums for each file replaced in an Ubuntu live ISO."""

import hashlib
from pathlib import Path
import sys

checksum_file = Path(sys.argv[1])
replacements = {"casper/filesystem.squashfs": Path(sys.argv[2])}
for mapping in sys.argv[3:]:
    iso_path, local_path = mapping.split("=", 1)
    iso_path = iso_path.removeprefix("/").removeprefix("./")
    if iso_path in replacements:
        raise SystemExit(f"Duplicate replacement: {iso_path}")
    replacements[iso_path] = Path(local_path)

lines = checksum_file.read_text().splitlines(keepends=True)
for iso_path, local_path in replacements.items():
    matches = []
    for index, line in enumerate(lines):
        fields = line.strip().split(maxsplit=1)
        if len(fields) == 2 and fields[1].lstrip("*").removeprefix("./") == iso_path:
            matches.append(index)
    if len(matches) != 1:
        raise SystemExit(f"Expected one {iso_path} entry in {checksum_file}, found {len(matches)}")
    with local_path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "md5").hexdigest()
    index = matches[0]
    lines[index] = digest + lines[index][32:]
    print(f"Updated ISO md5sum entry: {iso_path}: {digest}")

checksum_file.write_text("".join(lines))
