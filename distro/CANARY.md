# Cachuntu canary 26.10

Esta rama se reserva para pruebas de compatibilidad con **Ubuntu 26.10**
amd64. No es una fuente de paquetes para `lts/26.04` y no se publica
como edición LTS.

La Beta de Ubuntu 26.10 está prevista para octubre de 2026. Antes de
generar una ISO canary, fijar una imagen oficial completa de Kubuntu/Ubuntu
26.10 por URL, fecha y SHA256. No mezclar paquetes 26.10 en una raíz 26.04
ni habilitar `-proposed` en imágenes para usuarios.

Probar KDE Plasma, GNOME, Calamares, kernel, initramfs, NetworkManager,
PipeWire, portales, firmware, DKMS, Secure Boot y actualización
postinstalación en QCOW2. Llevar a LTS solo cambios de código o
configuración compatibles con Ubuntu 26.04 y validados allí por separado.
