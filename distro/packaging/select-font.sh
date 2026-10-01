#!/usr/bin/env bash
set -euo pipefail

case "${1:-}" in
  cachuntu)
    dpkg-query -W -f='${Status}' fonts-inter | grep -qx 'install ok installed'
    mkdir -p /etc/fonts/conf.d /etc/xdg /etc/dconf/db/local.d /etc/dconf/profile
    rm -f -- /etc/fonts/conf.d/60-cachuntu-font.conf
    cat >/etc/fonts/conf.d/99-cachuntu-font.conf <<'XML'
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
  <match target="pattern">
    <test name="family" compare="eq"><string>sans-serif</string></test>
    <edit name="family" mode="prepend" binding="strong"><string>Inter</string></edit>
  </match>
</fontconfig>
XML
    for key in font menuFont toolBarFont; do
      kwriteconfig6 --file /etc/xdg/kdeglobals --group General --key "$key" 'Inter,10,-1,5,50,0,0,0,0,0'
    done
    kwriteconfig6 --file /etc/xdg/kdeglobals --group General --key smallestReadableFont 'Inter,8,-1,5,50,0,0,0,0,0'
    cat >/etc/dconf/profile/user <<'PROFILE'
user-db:user
system-db:local
PROFILE
    cat >/etc/dconf/db/local.d/00-cachuntu-font <<'DCONF'
[org/gnome/desktop/interface]
font-name='Inter 11'
document-font-name='Inter 11'
DCONF
    # A profile must never reference an absent compiled database.
    dconf update
    test -s /etc/dconf/db/local
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
