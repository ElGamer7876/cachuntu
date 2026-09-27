# Cachuntu 0.1 preview test plan

Use a new QCOW2 virtual disk in QEMU/KVM. Never select a physical disk.

1. Verify SHA256 for both the source and Cachuntu ISO.
2. Boot in UEFI and BIOS. Check the live Plasma session, NetworkManager, PipeWire, file chooser, and desktop portals.
3. Open Calamares. KDE Plasma must be selected by default. GNOME and the gaming, multimedia, and development groups must each have a description.
4. Install KDE to QCOW2, restart without the ISO, verify `cachuntu-defaults` and `linux-generic`, and run `sudo /usr/lib/cachuntu/post-install-qa`.
5. Run `apt update && apt full-upgrade`, restart, and repeat QA. Review `apt-get -s autoremove` before removing anything.
6. Test trash and restore, file open/save, screenshot, and PipeWire screen sharing. Repeat with Flatpak if installed.
7. Test GNOME and each optional group with and without network access. Choices absent from the ISO need internet access.
8. On suitable hardware or a VM with NVIDIA and Secure Boot, test MOK, DKMS, `nvidia-smi`, Wayland, and suspend/resume after a kernel upgrade.
9. Record `uname -r`, `systemctl --failed`, and `journalctl -b -p err` after each Ubuntu kernel update.

The Kubuntu 26.04.1 source ISO uses `initramfs-tools`. Evaluate Dracut only after installation, upgrade, and Secure Boot tests pass in a VM.
