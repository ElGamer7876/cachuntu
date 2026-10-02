#!/usr/bin/env bash
set -uo pipefail
echo '=== Plasma processes ==='
ps -C kwin_wayland -C startplasma-wayland -C plasmashell -o pid,args
echo '=== Sessions ==='
loginctl list-sessions --no-pager
echo '=== Failed user units ==='
systemctl --user --failed --no-pager
echo '=== Recent session warnings ==='
journalctl --user -b -p warning --no-pager -n 8
