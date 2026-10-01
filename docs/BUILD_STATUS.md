# Cachuntu 0.1 build status

Status: **the corrected 26.9.28.0 preview3 ISO is being assembled; installation is not yet validated**.

The base is the official Kubuntu 26.04.1 amd64 ISO, SHA256 `831e4d4bb85098339ba43d3502cd6619b27e76daf37246a084cd68a6413090b8`. The `lts/26.04` branch uses Ubuntu 26.04 repositories and does not mix Ubuntu 26.10 packages.

## Current correction

The preview2 live session reached KWin but showed a black screen. Its session log showed an interactive Python prompt: passing `/usr/bin/python3 /usr/libexec/cachuntu-welcome.py` to KWin did not pass the script argument to Python. The launcher now passes the executable welcome script as a single program. The script has executable permissions, and the branding check verifies both properties. Source commits: `e12f1d3` and `7e4ca4c`.

The corrected staged root filesystem passed the branding check and Python syntax parsing. Its new SquashFS passed `unsquashfs -s`: Zstandard compression, 1 MiB blocks, 245143 inodes. Compression is bounded to two workers and 512 MiB of SquashFS memory. This replaces the earlier XZ build, whose default memory allocation contributed to host paging and loss of free space on C:.

The artifact being assembled is `E:\Cachuntu-build\outputs\cachuntu-26.9.28.0-preview3-amd64.iso`. The environment restart interrupted its first assembly; that incomplete image is retained as `cachuntu-preview3-interrupted.iso.part`. The resumed assembly log is `cachuntu-preview3-xorriso-resumed.log`. No final ISO checksum or successful live-session result is available yet.

## Branding and installation settings

The image contains the original user-approved Canva logo, the dark navy/turquoise welcome screen, Calamares identity and slides, Cachuntu GRUB labels, SDDM theme, and KDE About Distribution page. KDE Plasma is the default; GNOME and gaming, multimedia, and development groups are selectable. Btrfs is the default filesystem. Inter is the available font choice; redistribution of TT Interphases still requires a suitable license. See `distro/BRANDING.md`.

## Earlier artifacts

- Preview2: `cachuntu-26.9.28.0-preview2-amd64.iso`, SHA256 `500a91d82a4ea9418b6d121dbe83aaf4d30f00f61fd5c633e3dfcc26358177b8`. BIOS and UEFI records were built, but its live welcome launcher is defective.
- Preview: `cachuntu-26.9.28.0-preview-amd64.iso`, SHA256 `b46ff70c43f3145856dbfce7738a627fc89909dc0065e7ba2e23bbef1fc3296c`. It reached the upstream selector; selecting Install returned to that selector.
- Earlier preview: `cachuntu-26.9.27-preview-amd64.iso`, SHA256 `9925424e08ef9f092c74436d728e10cbdfdd7a6cf51506abec671346c3de82be`. It reached KDE and Calamares; installation failed while writing swap when C: ran out of space.

The latter two ISO files were relocated to `E:\Cachuntu-build\outputs` with SHA256 verification. Preview2 and the disposable 32 GiB QCOW2 remain on C:. The QCOW2 is empty. E: previously returned an I/O error during QCOW2 creation, so VM writes have not been moved there. At the resumed assembly, C: had approximately 6 GiB free. No physical disk or host bootloader was modified.

## Remaining release gates

1. Finish preview3 assembly, record its SHA256, and verify boot records.
2. Boot once in QEMU UEFI with direct SDL display. Verify the welcome screen, keyboard and mouse, Plasma, and Calamares. Diagnose the guest DNS failures seen in the previous boot. Then verify BIOS boot.
3. Install to a disposable QCOW2 with adequate free space, confirm Btrfs, and boot without the ISO.
4. Run postinstallation QA, Ubuntu upgrade and reboot, desktop portals, PipeWire, and optional package tests. The portal regression fix from Ubuntu USN-8287-2 is already covered by the version check and functional test plan.
5. Test Secure Boot, DKMS, NVIDIA, and suspend/resume where meaningful. Keep the base's initramfs-tools until a Dracut migration passes installation and upgrade tests.

This is a test build, not a validated installable release.
