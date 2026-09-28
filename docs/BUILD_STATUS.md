# Cachuntu 0.1 build status

Status: **26.9.27 live ISO built and UEFI boot verified; 26.9.28 image prepared; installation remains unverified**.

The preview ISO is based on the official Kubuntu 26.04.1 amd64 image, verified against SHA256 `831e4d4bb85098339ba43d3502cd6619b27e76daf37246a084cd68a6413090b8`. It retains Ubuntu 26.04 repositories. The remaster includes the three Cachuntu metapackages, KDE and GNOME installer choices, optional gaming/multimedia/development groups, the Ubuntu portal security fix, and removal of the automatic installer `apt autoremove` step.

The built ISO is `outputs/cachuntu-26.9.27-preview-amd64.iso`, SHA256 `9925424e08ef9f092c74436d728e10cbdfdd7a6cf51506abec671346c3de82be`. This checksum applies to the current ISO, not to later source changes. It booted in QEMU with UEFI/OVMF, reached the live desktop, and opened Calamares. A Btrfs install to a disposable QCOW2 reached 32% before the C: drive ran out of space. The VM was stopped and the disposable QCOW2 removed. No installed-system boot, upgrade, BIOS boot, or Secure Boot result is available yet.

The external E: drive returned an input/output error and disappeared while creating a QCOW2. Do not use it for build or test files until its stability is established. The ISO and its checksum remain on C:. No physical disk or host bootloader was touched.

Changes after this ISO was produced: the source now selects Btrfs by default and provides an Inter font choice as a freely redistributable preview substitute for TT Interphases. A 26.9.28 root filesystem with these changes was compressed successfully and its SquashFS header and Btrfs configuration were checked. The final 26.9.28 ISO still needs remastering and boot validation. TT Interphases must not be bundled without a redistribution license.

Release gates still open:

1. Remaster a new ISO with the prepared 26.9.28 SquashFS after enough C: space is available, then verify its checksum.
2. Boot the new ISO with UEFI and BIOS, then install to QCOW2 and boot the installed system without the ISO.
3. Run postinstallation QA, Ubuntu package upgrade, and portal/desktop/optional package tests.
4. Exercise Secure Boot, DKMS, NVIDIA, and Dracut only where hardware and virtual firmware support meaningful tests.

The current ISO is an early live preview, not a validated installable release.
