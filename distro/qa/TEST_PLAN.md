# Cachuntu 0.1 preview test plan

Use a new QCOW2 virtual disk in QEMU/KVM. Never select a physical disk.

1. Verify SHA256 for both the source and Cachuntu ISO. Run `python3 distro/qa/check-iso-checksums.py` before building. Verify the ISO md5sum list against the changed live filesystem and GRUB configuration; keep partial exports separate from release artifacts.
2. Boot in UEFI and BIOS. Confirm the Cachuntu welcome screen appears instead of a black screen, and verify that mouse clicks and keyboard Enter work. Try Cachuntu must open Plasma; Install Cachuntu must open Calamares. Run bash distro/qa/live-network.sh inside the guest and save its output to capture NetworkManager, routes, and Ubuntu mirror DNS failures. Check PipeWire, file chooser, and desktop portals.
3. Open Calamares. KDE Plasma and Cachuntu style (Inter) must be selected by default. GNOME, the desktop-default font, and the gaming, multimedia, and development groups must each have a description.
4. Check that Btrfs is the default filesystem for a new install, with ext4 and XFS still selectable. Install KDE to QCOW2, restart without the ISO, verify `cachuntu-defaults` and `linux-generic`, and run `sudo /usr/lib/cachuntu/post-install-qa`.
5. Check the installed KDE font, and repeat a small install with Desktop default to verify it does not receive the Cachuntu font override. Run `apt update && apt full-upgrade`, restart, and repeat QA. The portal check must report at least `xdg-desktop-portal 1.21.1+ds-1ubuntu3.1`, the Ubuntu 26.04 fix for USN-8287-2. Review `apt-get -s autoremove` before removing anything.
6. Test trash and restore, file open/save, screenshot, and PipeWire screen sharing. Repeat with Flatpak if installed.
7. Test GNOME and each optional group with and without network access. Choices absent from the ISO need internet access.
8. On suitable hardware or a VM with NVIDIA and Secure Boot, test MOK, DKMS, `nvidia-smi`, Wayland, and suspend/resume after a kernel upgrade.
9. Record `uname -r`, `systemctl --failed`, and `journalctl -b -p err` after each Ubuntu kernel update.

The Kubuntu 26.04.1 source ISO uses `initramfs-tools`. Evaluate Dracut only after installation, upgrade, and Secure Boot tests pass in a VM.

`python3 distro/qa/verify-iso-content.py IMAGE.iso --report IMAGE.validation.json`
checks every MD5 manifest entry through the ISO's file extents and records the
whole-image SHA256. It supports multi-extent files larger than 4 GiB and avoids
SquashFS mounting/extraction. Any missing, duplicate, malformed or mismatched
entry rejects the artifact before writing a success report. The builder runs
this check before creating its SHA256 sidecar. Runtime gates remain separate.

## Direct QEMU window (October 1 runner)

Use regular ISO and QCOW2 files. The runner uses KVM, 4 GiB RAM, UEFI,
virtio networking, an absolute USB tablet and the SDL window. It creates a
fresh 40 GiB QCOW2 and firmware state when the requested live-test disk does
not exist. It refuses another running QEMU instance or a non-QCOW2 image.
No physical disk or host bootloader is exposed. The QA directory is shared
read-only. The ISO export hash must be verified before starting the VM.

```bash
sudo bash distro/qa/run-qemu.sh \
  /mnt/c/Users/elgam/OneDrive/Documentos/ChatGPT/cachuntu/outputs/cachuntu-26.10.1.2-preview-amd64.iso \
  /mnt/e/Cachuntu-build/outputs/cachuntu-26.10.1.2-install.qcow2 live
# After guest shutdown and installation, boot without attaching the ISO:
sudo bash distro/qa/run-qemu.sh \
  /mnt/c/Users/elgam/OneDrive/Documentos/ChatGPT/cachuntu/outputs/cachuntu-26.10.1.2-preview-amd64.iso \
  /mnt/e/Cachuntu-build/outputs/cachuntu-26.10.1.2-install.qcow2 installed
```

The QMP socket is `/tmp/<QCOW2 basename without .qcow2>.qmp.sock`; pass it to
`qmp-guest.py --socket`. Set `CACHUNTU_QMP_SOCKET` to override it with another
Unix socket path on a Linux filesystem.
Use guest keyboard/mouse controls only after confirming the focused guest
screen. Launching the runner does not prove installation or runtime QA.

The recovered 26.10.1.2 artifact has a known Try-to-Plasma defect. Use the
corrected next candidate for the handoff/install gate. In a disposable KDE
guest, `bash distro/qa/check-live-session-exit.sh` checks that a temporary KWin
virtual backend exits when its session application closes. Also click Try in
the actual live welcome and confirm Plasma is running; the virtual test alone
does not establish the real display transition. Collect
`bash distro/qa/live-session-diagnostic.sh` when that transition fails.
