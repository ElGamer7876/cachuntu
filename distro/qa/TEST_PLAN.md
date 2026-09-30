# Cachuntu 0.1 preview test plan

Use a new QCOW2 virtual disk in QEMU/KVM. Never select a physical disk.

1. Verify SHA256 for both the source and Cachuntu ISO.
2. Boot in UEFI and BIOS. Confirm the Cachuntu welcome screen appears instead of a black screen, and verify that mouse clicks and keyboard Enter work. Try Cachuntu must open Plasma; Install Cachuntu must open Calamares. Check NetworkManager, PipeWire, file chooser, and desktop portals.
3. Open Calamares. KDE Plasma and Cachuntu style (Inter) must be selected by default. GNOME, the desktop-default font, and the gaming, multimedia, and development groups must each have a description.
4. Check that Btrfs is the default filesystem for a new install, with ext4 and XFS still selectable. Install KDE to QCOW2, restart without the ISO, verify `cachuntu-defaults` and `linux-generic`, and run `sudo /usr/lib/cachuntu/post-install-qa`.
5. Check the installed KDE font, and repeat a small install with Desktop default to verify it does not receive the Cachuntu font override. Run `apt update && apt full-upgrade`, restart, and repeat QA. The portal check must report at least `xdg-desktop-portal 1.21.1+ds-1ubuntu3.1`, the Ubuntu 26.04 fix for USN-8287-2. Review `apt-get -s autoremove` before removing anything.
6. Test trash and restore, file open/save, screenshot, and PipeWire screen sharing. Repeat with Flatpak if installed.
7. Test GNOME and each optional group with and without network access. Choices absent from the ISO need internet access.
8. On suitable hardware or a VM with NVIDIA and Secure Boot, test MOK, DKMS, `nvidia-smi`, Wayland, and suspend/resume after a kernel upgrade.
9. Record `uname -r`, `systemctl --failed`, and `journalctl -b -p err` after each Ubuntu kernel update.

The Kubuntu 26.04.1 source ISO uses `initramfs-tools`. Evaluate Dracut only after installation, upgrade, and Secure Boot tests pass in a VM.
