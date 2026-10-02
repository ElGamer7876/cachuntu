#!/usr/bin/env bash
# Run in a disposable KDE guest. The virtual backend never takes over its display.
set -uo pipefail
log=$(mktemp /tmp/cachuntu-session-exit.XXXXXX.log)
start=$SECONDS
timeout 20s dbus-run-session -- kwin_wayland --virtual --no-lockscreen \
    --exit-with-session /bin/true >"$log" 2>&1
status=$?
elapsed=$((SECONDS-start))
echo "KWIN_SESSION_EXIT status=$status elapsed_seconds=$elapsed log=$log"
tail -8 "$log"
[[ $status == 0 && $elapsed -lt 20 ]]
