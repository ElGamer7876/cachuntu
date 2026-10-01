#!/usr/bin/env bash
set -u
failed=0
installed() { test "$(dpkg-query -W -f='${Status}' "$1" 2>/dev/null)" = 'install ok installed'; }
check() { if "$@"; then printf 'OK %s\n' "$*"; else printf 'FAIL %s\n' "$*" >&2; failed=1; fi; }
check installed cachuntu-defaults
check installed linux-generic
check systemctl is-active --quiet NetworkManager
check systemctl is-active --quiet display-manager
if command -v dracut >/dev/null; then check command -v dracut; else check command -v update-initramfs; fi
printf 'Kernel: '; uname -r
printf 'Secure Boot: '; mokutil --sb-state 2>&1 || true
if command -v dkms >/dev/null; then printf 'DKMS:\n'; dkms status; else printf 'SKIP DKMS: not installed in this guest\n'; fi
# A font profile that references a missing compiled database affects every
# dconf consumer, including Plasma portal helpers and GTK applications.
if [[ -f /etc/dconf/profile/user ]] && grep -qx 'system-db:local' /etc/dconf/profile/user; then
  check test -s /etc/dconf/db/local
fi
systemctl --failed --no-pager
simulation=$(apt-get -s autoremove 2>&1) || { printf '%s\n' "$simulation"; exit 1; }
printf '%s\n' "$simulation"
if printf '%s\n' "$simulation" | grep -Eq '^Remv (linux-(generic|image|headers)|amd64-microcode|intel-microcode|linux-firmware|cachuntu-defaults)'; then
  printf 'FAIL: autoremove would remove essential components\n' >&2
  failed=1
fi
dpkg-query -W xdg-desktop-portal xdg-desktop-portal-kde pipewire wireplumber 2>&1 || failed=1
portal_version=$(dpkg-query -W -f='${Version}' xdg-desktop-portal 2>/dev/null) || portal_version=""
if [[ -n "$portal_version" ]] && dpkg --compare-versions "$portal_version" ge "1.21.1+ds-1ubuntu3.1"; then
  printf 'OK XDG Desktop Portal regression fix: %s\n' "$portal_version"
else
  printf 'FAIL XDG Desktop Portal needs Ubuntu USN-8287-2 fix (installed: %s)\n' "$portal_version" >&2
  failed=1
fi
journalctl -b -p err --no-pager 2>&1 | tail -n 80
if command -v nvidia-smi >/dev/null; then nvidia-smi || failed=1; fi
exit "$failed"
