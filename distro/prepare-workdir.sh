#!/usr/bin/env bash
set -euo pipefail
(( EUID == 0 )) || { echo "Run as root" >&2; exit 1; }
image=${1:?ext4 image path, e.g. /mnt/e/Cachuntu-build/work.ext4}
mountpoint=${2:?mount path, e.g. /mnt/cachuntu-work}
case "$image" in /mnt/*/Cachuntu-build/work.ext4) ;; *) echo "Refusing unexpected image path" >&2; exit 1;; esac
if [[ ! -e "$image" ]]; then
  truncate -s 32G "$image"
  mkfs.ext4 -q -F "$image"
fi
mkdir -p "$mountpoint"
if ! mountpoint -q "$mountpoint"; then mount -o loop "$image" "$mountpoint"; fi
test "$(findmnt -n -o FSTYPE -T "$mountpoint")" = ext4
echo "$mountpoint is ready"
