# Cachuntu 0.1 build status

Updated: 2026-10-01. **26.10.1.0 ISO assembly is complete. Export verification and VM installation are in progress. Installation remains unvalidated.**

The base remains Kubuntu 26.04.1 amd64, SHA256 `831e4d4bb85098339ba43d3502cd6619b27e76daf37246a084cd68a6413090b8`. Cachuntu `26.10.1.0` is a calendar version. The `lts/26.04` branch uses Ubuntu 26.04 repositories without Ubuntu 26.10 packages.

## Completed artifact and guest checks

`E:\Cachuntu-build\outputs\cachuntu-26.9.28.0-preview3-amd64.iso`

SHA256: `3f2ae72e58e759e95a0349609507c418e78665dc2a3bad2f9744042661e0194e`. The export matched the local image. Xorriso verified BIOS and UEFI records and volume ID `CACHUNTU_26_9_28_0`.

QEMU UEFI with direct SDL display reached the branded welcome screen. The mouse worked. Enter did not activate the buttons, and Install failed because sudo discarded XAUTHORITY. A diagnostic launch preserving the display credentials opened branded Calamares; its storage, RAM, root, and Internet requirements passed. The unmodified preview3 ISO still has these launcher defects and is not a validated installable release.

Live network QA returned exit status 0, including NetworkManager, default route, and both Ubuntu mirror DNS checks. The earlier DNS failures occurred in the inherited Casper initramfs stage before the live network was ready; the resulting boot delay remains a known issue.

## Corrected source

- `e12f1d3`: executable welcome script passed as one program to KWin, fixing the Python REPL and black screen.
- `7e4ca4c`: Zstandard compression with two workers and 512 MiB limit.
- `8970100`: live network diagnostic and earlier build notes.
- `ee5366f`: shared installer launcher preserving DISPLAY, XAUTHORITY, XDG_RUNTIME_DIR, and WAYLAND_DISPLAY; Return activation on both welcome buttons; real Qt event test in the build gate.
- `2add71d`: version 26.10.1.0 and refreshed branding version text.
- `d1fec1f`: refresh the branded GRUB checksum and reject incomplete ISO checksum manifests.

All three staged Cachuntu metapackages are `26.10.1.0~preview1`. Branding and Qt keyboard checks passed. A fresh image containing the fixes still needs runtime validation.

## Build and storage

The corrected export target is `E:\Cachuntu-build\outputs\cachuntu-26.10.1.0-preview2-amd64.iso`.

Local SHA256: `f3f58ac5b2d63acffcccf65c9da4a461b8bf1b4b7732ec78b4bd96d0781f0bd0`. Export verification is pending. Compression had already completed before the attempted memory pause; the earlier status was incorrect. A stale checksum for the branded GRUB configuration was found and fixed without recompressing the filesystem. Extracting GRUB and md5sum.txt from the final local ISO confirmed that their checksums match. The updater now covers every explicitly mapped file and has tests for missing and duplicate entries.

The initial Windows UNC export stalled. It was terminated and its output retained as `cachuntu-26.10.1.0-unc-interrupted.iso.part`; it is not a release artifact. The corrected export uses WSL's E: mount and writes `.part` until the full SHA256 matches. VirtualDJ was closed with permission. Firefox remains open.

Temporary files are reused to limit additional C: allocation. The compression loop device is backed exclusively by a verified temporary file. The prior preview3 ISO and SquashFS remain on E:. Completed images are exported to E: and verified against the local SHA256.

`E:\Cachuntu-build\outputs\cachuntu-26.10.1.0-install.qcow2` is a new empty 40 GiB virtual disk. Earlier E: I/O failures remain documented; later ISO exports passed SHA256 and no matching disk-provider error/warning appeared in the four-hour check before this build. Physical disk health is not established by these checks. No physical disk or host bootloader was modified.

## Evidence and remaining gates

Build logs: `E:\Cachuntu-build\outputs\build-26.10.1.0.log` and WSL `.cache/build/cachuntu.nnioCeKf/build-26.10.1.0.log`. Windows task workspace guest logs: `preview3-network.log`, `preview3-calamares.log`, `preview3-calamares-probe.log`, and `preview3-wayland-session.log`. Screenshots: `vm-preview3.png` and `vm-calamares-probe.png`.

1. Complete the new ISO, export, SHA256, and boot record inspection.
2. Verify keyboard/mouse, Calamares, Plasma, desktop/font/optional choices, and Btrfs default in the corrected ISO.
3. Install to QCOW2 and boot without the ISO; run postinstallation QA, Ubuntu upgrade/reboot, autoremove simulation, portals, and PipeWire tests.
4. Verify BIOS boot, a clean build, and bit-for-bit reproducibility. This rebuild reuses a prepared root filesystem.
5. Test Secure Boot, DKMS, NVIDIA, and suspend/resume where meaningful. Retain initramfs-tools until a Dracut migration passes installation and upgrade tests.

Inter is the available font choice; TT Interphases redistribution requires a suitable license. See `distro/BRANDING.md` and `distro/qa/TEST_PLAN.md`.
