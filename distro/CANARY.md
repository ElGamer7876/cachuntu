# Cachuntu canary 26.10

This branch is reserved for amd64 compatibility testing with **Ubuntu 26.10**. It is not a package source for `lts/26.04` and is not published as an LTS edition.

Before producing a canary ISO, pin a complete official Kubuntu or Ubuntu 26.10 image by URL, date, and SHA256. Do not mix 26.10 packages into a 26.04 root filesystem or enable `-proposed` in user images.

Test KDE Plasma, GNOME, Calamares, kernel, initramfs, NetworkManager, PipeWire, desktop portals, firmware, DKMS, Secure Boot, and postinstallation upgrades on a QCOW2 disk. Transfer only code or configuration changes that are compatible with Ubuntu 26.04 and separately validated there.
