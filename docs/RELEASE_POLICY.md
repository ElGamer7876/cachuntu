# Cachuntu releases and support

The regular edition uses `year.month.day`, for example `26.9.27`. It is reviewed daily at 15:00 in Mexico City. Publish a new build only when verified changes warrant one.

Schedule an LTS build every April 1. LTS versions use `year.04.patch`: `27.04.1` is the first 2027 build, and urgent fixes increment the final number. Each Cachuntu LTS edition targets five years of support, subject to the support available for its Ubuntu base and the project's ability to maintain desktop packages. Ubuntu 26.04 LTS receives standard Ubuntu maintenance through April 2031, while Kubuntu 26.04 desktop maintenance ends in April 2029. Five-year Cachuntu support therefore requires a validated desktop maintenance or upgrade path before the Kubuntu deadline. This is an open release risk, not an established capability. A new annual Cachuntu tag does not require a new Ubuntu base.

`lts/26.04` uses Ubuntu 26.04 LTS repositories. `canary/26.10` tests Ubuntu 26.10 separately and never supplies packages to LTS. `main` contains the website and shared documentation.

The preview starts from the official Kubuntu 26.04.1 ISO, providing KDE Plasma and Calamares. GNOME is an installation option. Optional package groups cover gaming, multimedia, and development. An internet connection is required for selected packages that are absent from the ISO.

## Release gate

A release requires verified source and output checksums, live boot, installation to a virtual disk, a boot of the installed system, and postinstallation upgrade checks. Record any untested hardware paths such as Secure Boot, DKMS, or NVIDIA in the release notes.
