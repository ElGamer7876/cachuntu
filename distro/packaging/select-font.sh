#!/usr/bin/env bash
set -euo pipefail

case "${1:-}" in
  cachuntu)
    dpkg-query -W -f='${Status}' fonts-inter | grep -qx 'install ok installed'
    mkdir -p /etc/fonts/conf.d /etc/xdg /etc/dconf/db/local.d /etc/dconf/profile
    cat >/etc/fonts/conf.d/60-cachuntu-font.conf <<'XML'
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
  <alias>
    <family>sans-serif</family>
    <prefer><family>Inter</family></prefer>
  </alias>
</fontconfig>
XML
    cat >/etc/xdg/kdeglobals <<'KDE'
[General]
font=Inter,10,-1,5,50,0,0,0,0,0
menuFont=Inter,10,-1,5,50,0,0,0,0,0
toolBarFont=Inter,10,-1,5,50,0,0,0,0,0
smallestReadableFont=Inter,8,-1,5,50,0,0,0,0,0
KDE
    cat >/etc/dconf/profile/user <<'PROFILE'
user-db:user
system-db:local
PROFILE
    cat >/etc/dconf/db/local.d/00-cachuntu-font <<'DCONF'
[org/gnome/desktop/interface]
font-name='Inter 11'
document-font-name='Inter 11'
DCONF
    if command -v dconf >/dev/null 2>&1; then dconf update; fi
    if command -v fc-cache >/dev/null 2>&1; then fc-cache -f; fi
    ;;
  desktop)
    # The base image has no Cachuntu font override to apply.
    ;;
  *)
    echo "Usage: cachuntu-select-font {cachuntu|desktop}" >&2
    exit 2
    ;;
esac
