#!/usr/bin/env bash
set -euo pipefail
(( EUID == 0 )) || { echo "Run as root" >&2; exit 1; }
repo=$(cd "$(dirname "$0")/.." && pwd)
source "$repo/distro/release.env"
source_iso=${1:?official Kubuntu ISO path}
output_iso=${2:?Cachuntu ISO output path}
workdir=${3:?mounted ext4 workdir}
[[ -f "$source_iso" && ! -e "$output_iso" ]] || { echo "Source missing or output already exists" >&2; exit 1; }
[[ "$(basename "$source_iso")" == "$BASE_ISO" ]] || { echo "Unexpected base ISO" >&2; exit 1; }
[[ "$(findmnt -n -o FSTYPE -T "$workdir")" == ext4 ]] || { echo "Workdir must be ext4" >&2; exit 1; }
log="${BUILD_LOG:-${output_iso}.build.log}"
exec > >(tee -a "$log") 2>&1
echo "Verifying source ISO: $source_iso"
printf '%s  %s\n' "$BASE_SHA256" "$source_iso" | sha256sum -c -
scratch=$(mktemp -d "$workdir/cachuntu.XXXXXXXX")
echo "Cachuntu $CACHUNTU_VERSION build from $BASE_ISO"
echo "Scratch: $scratch"
xorriso -osirrox on -indev "$source_iso" -extract /casper/filesystem.squashfs "$scratch/base.squashfs"
unsquashfs -d "$scratch/rootfs" "$scratch/base.squashfs"
bash "$repo/distro/packaging/build-debs.sh" "$scratch/debs"
dpkg --root="$scratch/rootfs" -i "$scratch"/debs/*.deb
python3 "$repo/distro/configure-calamares.py" "$scratch/rootfs"
mksquashfs "$scratch/rootfs" "$scratch/filesystem.squashfs" -noappend -comp xz -b 1M -processors 4 -mkfs-time 1780000000
xorriso -indev "$source_iso" -outdev "$output_iso" -overwrite on -map "$scratch/filesystem.squashfs" /casper/filesystem.squashfs -boot_image any replay -commit
xorriso -indev "$output_iso" -ls /casper
sha256sum "$output_iso" | tee "${output_iso}.sha256"
echo "Build finished; retain scratch until QA passes: $scratch"
