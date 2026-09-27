# Sistema base de Cachuntu

Preview 0.1: base Ubuntu 26.04.1 amd64 mediante la ISO oficial Kubuntu para
KDE Plasma y Calamares. `distro/release.env` fija URL y SHA256 de la
fuente. El flujo instala tres metapaquetes propios en el sistema live que
Calamares copia al sistema instalado.

El instalador ofrece KDE Plasma (predeterminado), GNOME y grupos opcionales
Gaming, multimedia y desarrollo. GNOME agrega paquetes y lo hace el
escritorio de inicio; Plasma sigue disponible. Las opciones adicionales
necesitan Internet durante la instalación. El preset mínimo de Kubuntu se
adapta para quitar su `apt-get -y autoremove` automático.

En un Ubuntu Linux con espacio suficiente y permisos de root:

```bash
sudo bash distro/prepare-workdir.sh /mnt/e/Cachuntu-build/work.ext4 /mnt/cachuntu-work
sudo bash distro/build-iso.sh /mnt/e/Cachuntu-build/kubuntu-26.04.1-desktop-amd64.iso /mnt/e/Cachuntu-build/cachuntu-26.9.27-preview-amd64.iso /mnt/cachuntu-work
```

Requisitos: `xorriso`, `squashfs-tools`, `python3-yaml`, `dpkg-dev`.
Los scripts verifican la fuente antes de escribir. El segundo script se niega
a sobrescribir una ISO existente. El área temporal requiere ext4 y queda
conservada para diagnósticos. No se usa una partición ni un bootloader del host.

Estado: la construcción y la instalación en QEMU/KVM se deben validar
antes de anunciar una ISO pública. Véase `distro/qa/TEST_PLAN.md`.
