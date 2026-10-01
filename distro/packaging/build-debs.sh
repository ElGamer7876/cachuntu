#!/usr/bin/env bash
set -euo pipefail
repo=$(cd "$(dirname "$0")/../.." && pwd)
source "$repo/distro/release.env"
out="${1:?output directory}"
if [[ "$CACHUNTU_CHANNEL" == lts ]]; then
  [[ "$CACHUNTU_VERSION" =~ ^[0-9]{2}\.[0-9]{2}\.[0-9]+$ ]] || { echo "LTS version must be year.month.patch" >&2; exit 2; }
else
  [[ "$CACHUNTU_VERSION" =~ ^[0-9]{2}\.[0-9]{1,2}\.[0-9]{1,2}\.[0-9]+$ ]] || { echo "Preview and regular versions must be year.month.day.patch" >&2; exit 2; }
fi
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
  if [[ "$name" == cachuntu-branding ]]; then
    mkdir -p "$stage/usr/lib/cachuntu"
    cp "$repo/distro/packaging/select-font.sh" "$stage/usr/lib/cachuntu/select-font"
    chmod 0755 "$stage/usr/lib/cachuntu/select-font"
  fi
  if [[ "$name" == cachuntu-defaults ]]; then
    mkdir -p "$stage/usr/lib/cachuntu"
    cp "$repo/distro/qa/post-install.sh" "$stage/usr/lib/cachuntu/post-install-qa"
    chmod 0755 "$stage/usr/lib/cachuntu/post-install-qa"
    mkdir -p "$stage/usr/share/cachuntu"
    cp "$repo/distro/security-baseline.json" "$stage/usr/share/cachuntu/security-baseline.json"
    cp "$repo/distro/qa/check-security-baseline.py" "$stage/usr/lib/cachuntu/check-security-baseline"
    chmod 0755 "$stage/usr/lib/cachuntu/check-security-baseline"
    mkdir -p "$stage/usr/bin"
    cp "$repo/distro/assets/windows-migration.py" "$stage/usr/bin/cachuntu-migrate"
    chmod 0755 "$stage/usr/bin/cachuntu-migrate"
  fi
  SOURCE_DATE_EPOCH=${SOURCE_DATE_EPOCH:-1780000000} dpkg-deb --root-owner-group --build "$stage" "$out/${name}_${CACHUNTU_VERSION}~preview1_all.deb" >/dev/null
  rm -rf -- "$stage"
}
build_one cachuntu-defaults 'python3, openssh-client, plasma-desktop, sddm, linux-generic, linux-firmware, network-manager, pipewire, wireplumber, xdg-desktop-portal, xdg-desktop-portal-kde' 'Cachuntu KDE desktop and Ubuntu hardware update anchors'
build_one cachuntu-branding 'cachuntu-defaults, fonts-inter, dconf-cli' 'Cachuntu preview identity metadata'
build_one cachuntu-performance 'cachuntu-defaults' 'Cachuntu performance profile placeholder with safe Ubuntu defaults'
sha256sum "$out"/*.deb >"$out/SHA256SUMS"
