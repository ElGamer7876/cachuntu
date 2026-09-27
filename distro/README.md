# Cachuntu distribution build

Cachuntu 0.1 preview uses Ubuntu 26.04.1 amd64 through the official Kubuntu ISO, which supplies KDE Plasma and Calamares. `distro/release.env` pins the source URL and SHA256. The build installs three Cachuntu metapackages in the live filesystem for Calamares to copy to the installed system.

The installer offers KDE Plasma by default and GNOME as an alternative. Optional package groups cover gaming, multimedia, and development. Installing additional packages requires internet access. The Kubuntu minimal preset is adjusted to remove its automatic `apt-get -y autoremove` step.

On an Ubuntu Linux host with sufficient space and root access:

```bash
sudo bash distro/prepare-workdir.sh /mnt/e/Cachuntu-build/work.ext4 /mnt/cachuntu-work
sudo bash distro/build-iso.sh /mnt/e/Cachuntu-build/kubuntu-26.04.1-desktop-amd64.iso /mnt/e/Cachuntu-build/cachuntu-26.9.27-preview-amd64.iso /mnt/cachuntu-work
```

Requirements: `xorriso`, `squashfs-tools`, `python3-yaml`, and `dpkg-dev`. The scripts verify the source before writing and refuse to overwrite an existing output ISO. The scratch area must use ext4 and is retained for diagnostics. No host partition or bootloader is used.

The ISO build and QEMU/KVM installation must pass [the test plan](qa/TEST_PLAN.md) before announcing a public release.
