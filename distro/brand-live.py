#!/usr/bin/env python3
"""Apply Cachuntu's installer identity to a copied Kubuntu live filesystem."""

from pathlib import Path
import shutil
import sys
import yaml

root = Path(sys.argv[1])
assets = Path(__file__).resolve().parent / "assets"
release = dict(line.split("=", 1) for line in (assets.parent / "release.env").read_text().splitlines()
               if line and not line.startswith("#") and "=" in line)
version = release["CACHUNTU_VERSION"]
cal = root / "etc/calamares"
settings_path = cal / "settings.conf"
settings = yaml.safe_load(settings_path.read_text())
assert settings["branding"] in ("kubuntu", "cachuntu")
settings["branding"] = "cachuntu"
settings_path.write_text(yaml.safe_dump(settings, sort_keys=False, allow_unicode=True))

branding = cal / "branding/cachuntu"
branding.mkdir(parents=True, exist_ok=True)
for name in ("logo.png", "icon.png", "welcome.png"):
    shutil.copyfile(assets / "cachuntu-logo.png", branding / name)
for name in ("branding.desc", "show.qml"):
    shutil.copyfile(assets / name, branding / name)
(branding / "branding.desc").write_text((branding / "branding.desc").read_text().replace("@VERSION@", version))
for config in (cal / "modules").glob("cachuntu-*.conf"):
    text = config.read_text()
    config.write_text(text.replace("/branding/kubuntu/welcome.png", "/branding/cachuntu/welcome.png"))

shutil.copyfile(assets / "cachuntu-logo.png", root / "usr/share/pixmaps/cachuntu-logo.png")
welcome = root / "usr/libexec/cachuntu-welcome.py"
shutil.copyfile(assets / "welcome.py", welcome)
welcome.chmod(0o755)
start = root / "usr/libexec/start-kubuntu-live-env"
script = start.read_text().replace("Starts the Kubuntu Live Environment.", "Starts the Cachuntu Live Environment.")
assert "kubuntu-installer-prompt" in script or "/usr/libexec/cachuntu-welcome.py" in script
start.write_text(script.replace("kubuntu-installer-prompt", "/usr/libexec/cachuntu-welcome.py"))

desktop = root / "usr/share/applications/kubuntu-calamares.desktop"
text = desktop.read_text().replace("Kubuntu", "Cachuntu").replace("kubuntu", "Cachuntu")
text = text.replace("Icon=system-software-install", "Icon=cachuntu-logo")
desktop.write_text(text)
session = root / "usr/share/wayland-sessions/kubuntu-live-environment.desktop"
session.write_text(session.read_text().replace("Kubuntu", "Cachuntu"))

about = root / "etc/xdg/kcm-about-distrorc"
text = about.read_text()
text = text.replace("LogoPath=/usr/share/plasma/avatars/kubuntu-bug.png", "LogoPath=/usr/share/pixmaps/cachuntu-logo.png")
text = text.replace("Name=Kubuntu", "Name=Cachuntu")
text = text.replace("Version=26.04 LTS", f"Version={version} Preview")
text = text.replace("Website=https://www.kubuntu.org", "Website=https://github.com/ElGamer7876/cachuntu")
about.write_text(text)

themes = root / "usr/share/sddm/themes"
shutil.copytree(themes / "breeze", themes / "cachuntu", dirs_exist_ok=True)
theme_config = themes / "cachuntu/theme.conf"
text = theme_config.read_text()
text = text.replace("showlogo=hidden", "showlogo=shown")
text = text.replace("logo=/usr/share/sddm/themes/breeze/default-logo.svg", "logo=/usr/share/pixmaps/cachuntu-logo.png")
text = text.replace("type=image", "type=color")
text = text.replace("color=#1d99f3", "color=#061326")
theme_config.write_text(text)
sddm = root / "etc/sddm.conf.d/20-kubuntu.conf"
sddm.write_text(sddm.read_text().replace("Current=kubuntu", "Current=cachuntu"))

welcome_conf = cal / "modules/welcome.conf"
welcome_conf.write_text(welcome_conf.read_text().replace(
    "showDonateUrl: https://kubuntu.org/donate/", "# Cachuntu preview does not offer a donation link."))

os_release = root / "etc/os-release"
text = os_release.read_text()
text = text.replace('PRETTY_NAME="Ubuntu 26.04.1 LTS"', f'PRETTY_NAME="Cachuntu {version} Preview"')
text = text.replace('NAME="Ubuntu"', 'NAME="Cachuntu"')
text = text.replace("ID_LIKE=debian", "ID_LIKE=ubuntu debian")
text = text.replace("LOGO=ubuntu-logo", "LOGO=cachuntu-logo")
os_release.write_text(text)
