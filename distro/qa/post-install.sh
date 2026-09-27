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
printf 'DKMS:\n'; dkms status 2>&1 || true
systemctl --failed --no-pager
simulation=$(apt-get -s autoremove 2>&1) || { printf '%s\n' "$simulation"; exit 1; }
printf '%s\n' "$simulation"
if printf '%s\n' "$simulation" | grep -Eq '^Remv (linux-(generic|image|headers)|amd64-microcode|intel-microcode|linux-firmware|cachuntu-defaults)'; then
  printf 'FAIL: autoremove propone quitar componentes esenciales\n' >&2
  failed=1
fi
dpkg-query -W xdg-desktop-portal xdg-desktop-portal-kde pipewire wireplumber 2>&1 || failed=1
journalctl -b -p err --no-pager 2>&1 | tail -n 80
if command -v nvidia-smi >/dev/null; then nvidia-smi || failed=1; fi
exit "$failed"
