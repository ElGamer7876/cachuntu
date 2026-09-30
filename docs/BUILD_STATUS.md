# Cachuntu 0.1 build status

Status: **branded 26.9.28.0 preview ISO built; installation is not yet validated**.

The new preview is based on the official Kubuntu 26.04.1 amd64 ISO, whose SHA256 was verified as `831e4d4bb85098339ba43d3502cd6619b27e76daf37246a084cd68a6413090b8`. Ubuntu 26.04 repositories remain the base; no Ubuntu 26.10 packages are mixed into the LTS branch.

The local artifact is `cachuntu-26.9.28.0-preview-amd64.iso`, SHA256 `b46ff70c43f3145856dbfce7738a627fc89909dc0065e7ba2e23bbef1fc3296c`. Its checksum file passed `sha256sum -c`. Xorriso reports both BIOS and UEFI boot entries. The embedded SquashFS passed its format check and contains Cachuntu `26.9.28.0` metapackages, Btrfs as the Calamares default, and the Inter font choice. It boots to the Kubuntu live selector in QEMU UEFI, but selecting Install returns to that selector; Calamares did not open. This ISO is not an installable Cachuntu preview.

The branded local artifact is `cachuntu-26.9.28.0-preview2-amd64.iso`, SHA256 `500a91d82a4ea9418b6d121dbe83aaf4d30f00f61fd5c633e3dfcc26358177b8`. Xorriso completed the image with BIOS and UEFI boot records and volume ID `CACHUNTU_26_9_28_0`. The Cachuntu branding is integrated in source: the original user-approved Canva logo, the dark navy/turquoise live welcome screen, Calamares product identity and slides, Cachuntu GRUB labels, SDDM theme, and KDE About Distribution page. Static checks and an offscreen PyQt launch passed. A QEMU UEFI session has been started for visual review; its boot and install result remain unverified. The build script applies the same changes in a clean future build. See `distro/BRANDING.md` for design provenance and the remaining font license limitation.

The earlier `26.9.27` ISO reached the live KDE desktop and Calamares in a QEMU UEFI VM. Its installation to a disposable QCOW2 failed while writing swap after C: ran out of space. That ISO predates the Btrfs default and font selection. No installed-system boot or postinstallation upgrade result is available.

The disposable QCOW2 is on C:. E: previously returned an input/output error during QCOW2 creation, so it is not being used for VM writes. A recent Windows bad-block event refers to `Harddisk2`; Windows currently maps E: to disk 1, so that event cannot be attributed to E: without more evidence. The ISO, checksum, and logs remain on C:. No physical disk or host bootloader was modified.

Release gates still open:

1. Verify the branded selector in the currently running QEMU UEFI session; diagnose why Calamares exited from the previous live selector, then test BIOS boot.
2. Install to a disposable QCOW2, confirm the Btrfs default, and boot the installed system without the ISO.
3. Run postinstallation QA, Ubuntu package upgrade, and portal, desktop, and optional package tests.
4. Exercise Secure Boot, DKMS, NVIDIA, and Dracut where hardware and virtual firmware allow meaningful tests.
5. Verify the Cachuntu branding in the booted ISO; the code and assets have passed static checks.

The local ISO is a test artifact, not a validated installable release.
