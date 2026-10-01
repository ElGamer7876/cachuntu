#!/usr/bin/env python3
"""Check visible Cachuntu branding in an unpacked live filesystem."""

from pathlib import Path
import sys
import yaml

root = Path(sys.argv[1])
grub = Path(sys.argv[2])
settings = yaml.safe_load((root / "etc/calamares/settings.conf").read_text())
assert settings["branding"] == "cachuntu"
brand = root / "etc/calamares/branding/cachuntu"
assert (brand / "logo.png").is_file()
assert "productName: Cachuntu" in (brand / "branding.desc").read_text()
assert "Kubuntu" not in (brand / "show.qml").read_text()
assert "Install Cachuntu" in (root / "usr/libexec/cachuntu-welcome.py").read_text()
assert (root / "usr/libexec/cachuntu-welcome.py").stat().st_mode & 0o111
assert (root / "usr/libexec/cachuntu-launch-installer").stat().st_mode & 0o111
assert "--preserve-env=DISPLAY,XAUTHORITY,XDG_RUNTIME_DIR,WAYLAND_DISPLAY" in (root / "usr/libexec/cachuntu-launch-installer").read_text()
assert "Exec=/usr/libexec/cachuntu-launch-installer" in (root / "usr/share/applications/kubuntu-calamares.desktop").read_text()
live_start = (root / "usr/libexec/start-kubuntu-live-env").read_text()
assert "kubuntu-installer-prompt" not in live_start
assert "kwin_wayland --xwayland --no-lockscreen /usr/libexec/cachuntu-welcome.py" in live_start
assert "Name=Install Cachuntu" in (root / "usr/share/applications/kubuntu-calamares.desktop").read_text()
assert "Name=Cachuntu" in (root / "etc/xdg/kcm-about-distrorc").read_text()
assert "Current=cachuntu" in (root / "etc/sddm.conf.d/20-kubuntu.conf").read_text()
assert (root / "usr/share/sddm/themes/cachuntu/theme.conf").is_file()
assert "Try or Install Cachuntu" in grub.read_text()
assert "Try or Install Kubuntu" not in grub.read_text()
assert " quiet splash" not in grub.read_text()
assert (root / "usr/share/wallpapers/Cachuntu/contents/images/1920x1080.svg").is_file()
theme = root / "usr/share/plasma/look-and-feel/org.cachuntu.desktop"
assert 'Image=Cachuntu' in (theme / 'contents/defaults').read_text()
assert 'file:///usr/share/wallpapers/Kubuntu#day-night' not in (theme / 'contents/layouts/org.kde.plasma.desktop-layout.js').read_text()
assert 'LookAndFeelPackage=org.cachuntu.desktop' in (root / 'etc/xdg/kdeglobals').read_text()
png = root / 'usr/share/wallpapers/Cachuntu/contents/images/1920x1080.png'
import struct
header = png.read_bytes()[:24]
assert header[:8] == b'\x89PNG\r\n\x1a\n'
assert struct.unpack('>II', header[16:24]) == (1920, 1080)
assert 'images/1920x1080.png' in (theme / 'contents/layouts/org.kde.plasma.desktop-layout.js').read_text()
print("Visible installer and boot branding: OK")
