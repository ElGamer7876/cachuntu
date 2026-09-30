# Cachuntu installer branding

The installer follows the approved [Cachuntu Calamares design board](https://canva.link/5kirb83nhhfy5qv). The logo in `assets/cachuntu-logo.png` comes from the [original Cachuntu logo design](https://canva.link/86zvogsp73infz0). Do not substitute a similarly named logo.

The palette uses a deep navy background (`#061326`), turquoise accent (`#4DE4D1`), and pale text (`#F0F7FF`). The live welcome screen uses these colors, the original logo, and explicit Install and Try actions. Calamares uses Cachuntu product names, logo, sidebar colors, and installation slides. GRUB displays Cachuntu menu entries. SDDM and KDE's About Distribution page also display Cachuntu.

The board is a design reference, not a set of executable installer screens. Calamares still owns its form controls and accessibility behavior. The source distribution and package repositories remain Ubuntu 26.04 LTS; the build input is the official Kubuntu 26.04.1 image. Internal upstream package names and source attribution should not be rewritten.

The live GRUB entries omit Plymouth's `splash` option because the inherited live initrd still contains Kubuntu splash art. A dedicated Cachuntu Plymouth theme and rebuilt initrd are pending.

Inter is the preview typeface. TT Interphases remains excluded until redistribution rights for an ISO are established. The installed user may select the desktop's default font instead.
