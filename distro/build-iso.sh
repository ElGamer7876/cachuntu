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
xorriso -osirrox on -indev "$source_iso" -extract /md5sum.txt "$scratch/md5sum.txt"
xorriso -osirrox on -indev "$source_iso" -extract /boot/grub/grub.cfg "$scratch/grub.cfg"
unsquashfs -d "$scratch/rootfs" "$scratch/base.squashfs"
rm -f -- "$scratch/base.squashfs"
curl --fail --location --retry 3 --output "$scratch/$INTER_DEB" "$INTER_URL"
printf '%s  %s\n' "$INTER_SHA256" "$scratch/$INTER_DEB" | sha256sum -c -
cp "$scratch/$INTER_DEB" "$scratch/rootfs/tmp/"
chroot "$scratch/rootfs" dpkg -i "/tmp/$INTER_DEB"
rm -f -- "$scratch/rootfs/tmp/$INTER_DEB"
bash "$repo/distro/packaging/build-debs.sh" "$scratch/debs"
mkdir -p "$scratch/rootfs/tmp/cachuntu-debs"
cp "$scratch"/debs/*.deb "$scratch/rootfs/tmp/cachuntu-debs/"
chroot "$scratch/rootfs" /bin/sh -c "dpkg -i /tmp/cachuntu-debs/*.deb"
rm -f -- "$scratch/rootfs/tmp/cachuntu-debs/"*.deb
rmdir "$scratch/rootfs/tmp/cachuntu-debs"
curl --fail --location --retry 3 --output "$scratch/$PORTAL_DEB" "$PORTAL_URL"
printf '%s  %s\n' "$PORTAL_SHA256" "$scratch/$PORTAL_DEB" | sha256sum -c -
cp "$scratch/$PORTAL_DEB" "$scratch/rootfs/tmp/"
chroot "$scratch/rootfs" dpkg -i "/tmp/$PORTAL_DEB"
rm -f -- "$scratch/rootfs/tmp/$PORTAL_DEB"
python3 "$repo/distro/configure-calamares.py" "$scratch/rootfs"
python3 "$repo/distro/brand-live.py" "$scratch/rootfs"
python3 "$repo/distro/brand-grub.py" "$scratch/grub.cfg"
chroot "$scratch/rootfs" /usr/bin/python3 -c 'from PyQt6.QtWidgets import QApplication'
python3 "$repo/distro/qa/check-branding.py" "$scratch/rootfs" "$scratch/grub.cfg"
cp "$repo/distro/qa/check-welcome-keyboard.py" "$scratch/rootfs/tmp/check-welcome-keyboard.py"
chroot "$scratch/rootfs" env QT_QPA_PLATFORM=offscreen /usr/bin/python3 /tmp/check-welcome-keyboard.py /usr/libexec/cachuntu-welcome.py
rm -f -- "$scratch/rootfs/tmp/check-welcome-keyboard.py" "$scratch/rootfs/tmp/cachuntu-calamares-launch.log"
mksquashfs "$scratch/rootfs" "$scratch/filesystem.squashfs" -noappend -comp zstd -Xcompression-level 9 -b 1M -processors 2 -mem 512M -mkfs-time 1780000000
python3 "$repo/distro/update-md5sums.py" "$scratch/md5sum.txt" "$scratch/filesystem.squashfs"
xorriso -indev "$source_iso" -outdev "$output_iso" -overwrite on -map "$scratch/filesystem.squashfs" /casper/filesystem.squashfs -map "$scratch/md5sum.txt" /md5sum.txt -map "$scratch/grub.cfg" /boot/grub/grub.cfg -volid "CACHUNTU_${CACHUNTU_VERSION//./_}" -boot_image any replay -commit
xorriso -indev "$output_iso" -ls /casper
sha256sum "$output_iso" | tee "${output_iso}.sha256"
echo "Build finished; retain scratch until QA passes: $scratch"
