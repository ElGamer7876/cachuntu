#!/usr/bin/env bash
set -euo pipefail
# QEMU uses regular image files only. No host disks are passed through.
iso=${1:?ISO path}
disk=${2:?QCOW2 path}
mode=${3:-live}
[[ "$mode" == live || "$mode" == installed ]] || { echo 'Mode must be live or installed' >&2; exit 2; }
[[ "$iso" == /*.iso && -f "$iso" && "$disk" == /*.qcow2 ]] || { echo 'Use absolute ISO/QCOW2 file paths' >&2; exit 2; }
[[ "$iso$disk" != *,* ]] || { echo 'Image paths must not contain commas' >&2; exit 2; }
[[ -r /dev/kvm && -w /dev/kvm ]] || { echo 'KVM access is required; use sudo inside WSL if needed' >&2; exit 2; }
if pgrep -a qemu-system; then echo 'Another QEMU VM is running' >&2; exit 2; fi
qa=$(cd "$(dirname "$0")" && pwd)
output=$(dirname "$disk")
[[ -d "$output" ]] || { echo 'QCOW2 output directory must exist' >&2; exit 2; }
vars="${disk}.OVMF_VARS.fd"
if [[ ! -e "$disk" ]]; then
  [[ "$mode" == live && ! -e "$vars" ]] || { echo 'Installed mode requires an existing VM disk and firmware state' >&2; exit 2; }
  qemu-img create -f qcow2 "$disk" 40G
  cp /usr/share/OVMF/OVMF_VARS_4M.fd "$vars"
fi
[[ -f "$disk" && -f "$vars" ]] || { echo 'VM image or firmware state is not a regular file' >&2; exit 2; }
qemu-img info --output=json "$disk" | python3 -c 'import json,sys; assert json.load(sys.stdin)["format"] == "qcow2"'
media=()
order=c
if [[ "$mode" == live ]]; then
  media=(-drive "file=$iso,media=cdrom,if=ide,readonly=on")
  order=d
fi
socket="${CACHUNTU_QMP_SOCKET:-/tmp/$(basename "$disk" .qcow2).qmp.sock}"
export SDL_VIDEO_WINDOW_POS=50,50
exec qemu-system-x86_64 \
  -name "Cachuntu-$(basename "$disk" .qcow2)" \
  -machine q35,vmport=off -accel kvm -m 4096 -smp 2 \
  -device virtio-rng-pci -device qemu-xhci -device usb-tablet -device virtio-vga \
  -drive if=pflash,format=raw,unit=0,readonly=on,file=/usr/share/OVMF/OVMF_CODE_4M.fd \
  -drive "if=pflash,format=raw,unit=1,file=$vars" \
  -drive "file=$disk,if=virtio,format=qcow2" "${media[@]}" \
  -boot "order=$order,menu=on" \
  -netdev user,id=net0 -device virtio-net-pci,netdev=net0 \
  -virtfs "local,path=$qa,mount_tag=cachuntuqa,security_model=none,readonly=on" \
  -display sdl,gl=off -monitor none \
  -qmp "unix:$socket,server=on,wait=off" >"${disk}.qemu.log" 2>&1
