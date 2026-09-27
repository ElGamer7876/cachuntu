#!/usr/bin/env python3
"""Update the live filesystem entry in an Ubuntu ISO md5sum list."""

import hashlib
from pathlib import Path
import sys

checksum_file = Path(sys.argv[1])
squashfs = Path(sys.argv[2])
with squashfs.open("rb") as stream:
    digest = hashlib.file_digest(stream, "md5").hexdigest()

lines = checksum_file.read_text().splitlines(keepends=True)
matches = []
for index, line in enumerate(lines):
    fields = line.strip().split(maxsplit=1)
    if len(fields) != 2:
        continue
    path = fields[1].lstrip("*")
    if path.removeprefix("./") == "casper/filesystem.squashfs":
        matches.append(index)

if len(matches) != 1:
    raise SystemExit(f"Expected one squashfs entry in {checksum_file}, found {len(matches)}")

index = matches[0]
line = lines[index]
lines[index] = digest + line[32:]
checksum_file.write_text("".join(lines))
print(f"Updated ISO md5sum entry: {digest}")

