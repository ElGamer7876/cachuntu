# Pruebas de Cachuntu 0.1 preview

Usar un disco QCOW2 nuevo dentro de QEMU/KVM; nunca un disco físico.

1. Verificar SHA256 de la ISO fuente y Cachuntu.
2. Arrancar en UEFI y BIOS. Confirmar Plasma live, NetworkManager,
   PipeWire, selector de archivos y portales.
3. Abrir Calamares. KDE Plasma debe estar preseleccionado; GNOME y los
   grupos Gaming, multimedia y desarrollo deben mostrar descripción.
4. Instalar KDE en QCOW2, reiniciar sin ISO, verificar `cachuntu-defaults`
   y `linux-generic`. Ejecutar `sudo /usr/lib/cachuntu/post-install-qa`.
5. Ejecutar `apt update && apt full-upgrade`, reiniciar y repetir QA.
   Revisar `apt-get -s autoremove` antes de cualquier limpieza.
6. Probar papelera/restauración, abrir/guardar, captura y compartir
   pantalla mediante PipeWire. Repetir con Flatpak si está instalado.
7. Probar GNOME y cada grupo opcional, con y sin red. Las opciones que
   no están en la ISO necesitan Internet.
8. En hardware o VM con NVIDIA y Secure Boot: comprobar MOK, DKMS,
   `nvidia-smi`, Wayland y suspensión tras actualizar el kernel.
9. Registrar `uname -r`, `systemctl --failed` y `journalctl -b -p err`
   tras cada actualización de kernel Ubuntu.

La ISO Kubuntu 26.04.1 fuente usa `initramfs-tools`. Evaluar Dracut solo
después de validar instalación, actualización y Secure Boot en VM.
