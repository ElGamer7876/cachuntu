# Cachuntu 0.1 build status

Status: **blocked before remastering**. No Cachuntu ISO has been produced or published.

The official Kubuntu 26.04.1 amd64 source ISO was downloaded and independently verified against the pinned SHA256 `831e4d4bb85098339ba43d3502cd6619b27e76daf37246a084cd68a6413090b8` using Windows and WSL. A second checksum read inside the build script failed with an input/output error when the external work drive disconnected. Windows reported disk controller errors. The drive reappeared, but it was reported hot; avoid further large reads or writes until stable storage is available.

Completed checks:

- Distribution shell scripts pass `bash -n`.
- The Calamares configuration script passes Python compilation and a dry run against the Kubuntu settings package.
- The three Cachuntu metapackages build as Debian packages.
- Markdown and release notes use English by default.

Pending release gates:

1. Build and SHA256 verify the Cachuntu ISO on stable storage.
2. Boot the live system in UEFI and BIOS.
3. Install to a QCOW2 virtual disk and boot without the ISO.
4. Upgrade the installed system and run postinstallation QA.
5. Test GNOME, optional package groups, portals, and applicable Secure Boot/DKMS/NVIDIA paths.

The build must not be announced as functional until these gates pass.

