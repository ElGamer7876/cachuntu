#!/usr/bin/env bash
# Run inside the live VM; save stdout/stderr with tee for the build record.
set -u
failed=0
check() {
    if "$@"; then
        printf 'OK %s\n' "$*"
    else
        printf 'FAIL %s\n' "$*" >&2
        failed=1
    fi
}

check systemctl is-active NetworkManager
check nmcli general status
nmcli device status
ip -brief address
ip route
ip -6 route
if ! { ip route show default; ip -6 route show default; } | grep -q '^default '; then
    printf 'FAIL no default route\n' >&2
    failed=1
fi
resolvectl status || cat /etc/resolv.conf
check timeout 15 getent ahosts archive.ubuntu.com
check timeout 15 getent ahosts security.ubuntu.com
exit "$failed"
