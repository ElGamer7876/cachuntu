#!/usr/bin/env bash
set -euo pipefail
repo=$(cd "$(dirname "$0")/../.." && pwd)
source "$repo/distro/release.env"
out="${1:?output directory}"
mkdir -p "$out"
build_one() {
  local name=$1 depends=$2 description=$3
  local stage
  stage=$(mktemp -d)
  mkdir -p "$stage/DEBIAN" "$stage/usr/share/doc/$name"
  cat >"$stage/DEBIAN/control" <<EOF
Package: $name
Version: ${CACHUNTU_VERSION}~preview1
Section: metapackages
Priority: optional
Architecture: all
Maintainer: Cachuntu Project <noreply@example.invalid>
Depends: $depends
Description: $description
EOF
  printf 'Cachuntu %s preview\n' "$CACHUNTU_VERSION" >"$stage/usr/share/doc/$name/README"
  if [[ "$name" == cachuntu-defaults ]]; then
    mkdir -p "$stage/usr/lib/cachuntu"
    cp "$repo/distro/qa/post-install.sh" "$stage/usr/lib/cachuntu/post-install-qa"
    chmod 0755 "$stage/usr/lib/cachuntu/post-install-qa"
  fi
  SOURCE_DATE_EPOCH=${SOURCE_DATE_EPOCH:-1780000000} dpkg-deb --root-owner-group --build "$stage" "$out/${name}_${CACHUNTU_VERSION}~preview1_all.deb" >/dev/null
  rm -rf -- "$stage"
}
build_one cachuntu-defaults 'plasma-desktop, sddm, linux-generic, linux-firmware, network-manager, pipewire, wireplumber, xdg-desktop-portal, xdg-desktop-portal-kde' 'Cachuntu KDE desktop and Ubuntu hardware update anchors'
build_one cachuntu-branding 'cachuntu-defaults' 'Cachuntu preview identity metadata'
build_one cachuntu-performance 'cachuntu-defaults' 'Cachuntu performance profile placeholder with safe Ubuntu defaults'
sha256sum "$out"/*.deb >"$out/SHA256SUMS"
