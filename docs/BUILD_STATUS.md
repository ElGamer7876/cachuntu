# Cachuntu 0.1 build status

Updated: 2026-10-01. **26.10.1.0 ISO export passed SHA256. Btrfs installation completed. The installed Plasma Wayland desktop booted on a diagnostic overlay with 4 GiB RAM. Upgrade validation is blocked by E: disappearing and Btrfs I/O errors.**

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
- `2d1fedb`: align the first filesystem selector entry with the Btrfs default; gate desktop, font, optional-group, and filesystem defaults in future builds. This source change is newer than the exported ISO. The exported installer showed ext4 in the selector while its actual plan and mounted target used Btrfs. A fixture reproduced the old mismatch and passed with the corrected configuration.

All three staged Cachuntu metapackages are `26.10.1.0~preview1`. Branding and Qt keyboard checks passed. The corrected ISO booted in QEMU/KVM UEFI through the direct SDL window. Return opened Calamares successfully. KDE Plasma and Inter were selected by default, with GNOME, desktop fonts, and all three optional groups present. The installation summary and live `findmnt` confirmed Btrfs on the 40 GiB QCOW2, with `@`, `@home`, and `@swap` subvolumes. Live network QA passed with exit status 0; the guest reported no failed system units at this stage.

## Build and storage

The corrected export target is `E:\Cachuntu-build\outputs\cachuntu-26.10.1.0-preview2-amd64.iso`.

Local SHA256: `f3f58ac5b2d63acffcccf65c9da4a461b8bf1b4b7732ec78b4bd96d0781f0bd0`. The exported ISO matches this SHA256. Compression had already completed before the attempted memory pause; the earlier status was incorrect. A stale checksum for the branded GRUB configuration was found and fixed without recompressing the filesystem. Extracting GRUB and md5sum.txt from the final local ISO confirmed that their checksums match. The updater now covers every explicitly mapped file and has tests for missing and duplicate entries.

The initial Windows UNC export stalled. It was terminated and its output retained as `cachuntu-26.10.1.0-unc-interrupted.iso.part`; it is not a release artifact. The corrected export uses WSL's E: mount and writes `.part` until the full SHA256 matches. VirtualDJ was closed with permission. Firefox remains open.

Temporary files are reused to limit additional C: allocation. The compression loop device is backed exclusively by a verified temporary file. The prior preview3 ISO and SquashFS remain on E:. Completed images are exported to E: and verified against the local SHA256.

`E:\Cachuntu-build\outputs\cachuntu-26.10.1.0-install.qcow2` contains the completed 40 GiB virtual Btrfs installation. Earlier E: I/O failures remain documented; later ISO exports passed SHA256 and no matching disk-provider error/warning appeared in the four-hour check before this build. Physical disk health is not established by these checks. No physical disk or host bootloader was modified.

## Evidence and remaining gates

Build logs: `E:\Cachuntu-build\outputs\build-26.10.1.0.log` and WSL `.cache/build/cachuntu.nnioCeKf/build-26.10.1.0.log`. Windows task workspace guest logs: `preview3-network.log`, `preview3-calamares.log`, `preview3-calamares-probe.log`, and `preview3-wayland-session.log`. Screenshots: `vm-preview3.png` and `vm-calamares-probe.png`.

1. ISO assembly, export SHA256, and BIOS/UEFI boot record inspection completed. Runtime BIOS boot is still pending.
2. UEFI live boot, Return activation, Calamares launch, and default choices verified. QMP keyboard input works with slower typing. Pointer coordinate alignment required diagnosis; clicks selected the virtual disk installation mode. The filesystem selector display mismatch is fixed in source for the next candidate.
3. Install to QCOW2 and boot without the ISO; run postinstallation QA, Ubuntu upgrade/reboot, autoremove simulation, portals, and PipeWire tests.
4. Verify BIOS boot, a clean build, and bit-for-bit reproducibility. This rebuild reuses a prepared root filesystem.
5. Test Secure Boot, DKMS, NVIDIA, and suspend/resume where meaningful. Retain initramfs-tools until a Dracut migration passes installation and upgrade tests.

Inter is the available font choice; TT Interphases redistribution requires a suitable license. See `distro/BRANDING.md` and `distro/qa/TEST_PLAN.md`.

## Current installed-system evidence

Calamares reported completion:succeeded at 14:37:07. The installed Btrfs root has `@`, `@home`, and `@swap`; the test user is `cachuntuqa`. The ISO was ejected before the first installed boot. The original 2560 MiB boot did not yield a usable desktop during the observation window. Its journal contained a Plasma splash timeout and a missing pam_sss module warning; the latter was not reproduced in the subsequent running guest. No PAM authentication bypass was applied.

An external QCOW2 snapshot preserved the installed disk. A diagnostic boot of `cachuntu-26.10.1.0-debug-overlay.qcow2` with 4096 MiB reached Plasma; `loginctl show-session 1` reported `Type=wayland`, `State=active`. A QMP screenshot confirms the desktop and Konsole. This is a diagnostic boot with the installed kernel/initrd and a temporary serial debug shell, not a completed normal-reboot test. The debug shell is confined to that launcher; it is not configured in the source ISO or installed GRUB.

Post-install QA confirmed cachuntu-defaults, linux-generic, NetworkManager, the display manager and update-initramfs. Autoremove simulation removed no packages. PipeWire 1.6.2-1ubuntu1.1, WirePlumber 0.5.13-1ubuntu1 and XDG Desktop Portal 1.21.1+ds-1ubuntu3.1 were present. No failed system units appeared during this check, although the journal retained a user-session splash timeout and Bluetooth OBEX warnings. Secure Boot was unsupported in this VM configuration; DKMS and NVIDIA were absent. Runtime portal interactions/audio still require validation.

The font chooser wrote Inter settings, and kreadconfig6 confirmed Inter for the installed test user. However, dconf-cli was missing, leaving `/etc/dconf/db/local` absent. Installing dconf-cli and running dconf update created the database. The source now declares and hash-pins this official Ubuntu dependency, fails font setup if the database is absent and checks it in post-install QA. A prepared-root test passed and retained LookAndFeelPackage when applying the font choice.

New source includes a Cachuntu dark desktop theme and SVG wallpaper embedding the approved Canva logo, plus the personal-file migration prototype documented in WINDOWS_MIGRATION.md. Branding, shell syntax, metapackage builds and migration integrity/security fixtures passed. These changes and the Btrfs selector correction are newer than the exported ISO. The old ISO desktop still shows Kubuntu wallpaper/links and Plymouth branding; the new theme needs a fresh user/ISO visual test, and Plymouth replacement remains pending.

The guest's apt-get update succeeded against Resolute repositories. apt-get upgrade began but was interrupted while unpacking packages: Btrfs reported errno=-5 in write_all_supers/device barriers and Windows no longer exposed E:. QEMU was paused immediately and then closed. The interrupted update is confined to the debug overlay; do not merge that overlay into the preserved installation. Its temporary debug boot does not constitute a verified upgrade/reboot. Do not resume writes to E: until storage is available and stable.

Evidence in the Windows workspace: `26.10.1.0-calamares.log`, `installed-offline-inspection.log`, `installed-serial-diagnostic.log`, `calamares-completed-26.10.1.0.png` and `installed-plasma-26.10.1.0.png`. Earlier live boot logs contain no errors and do not describe the installed boot. The final ISO SHA256 remains `f3f58ac5b2d63acffcccf65c9da4a461b8bf1b4b7732ec78b4bd96d0781f0bd0`.
