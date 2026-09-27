#!/usr/bin/env python3
"""Adapt Calamares in a copied Kubuntu live filesystem."""
from pathlib import Path
import sys
import yaml

root = Path(sys.argv[1])
cal = root / "etc/calamares"
settings_path = cal / "settings.conf"
settings = yaml.safe_load(settings_path.read_text())
assert settings["branding"] == "kubuntu"
assert "pkgselect" in settings["sequence"][0]["show"]
assert "packages" in settings["sequence"][1]["exec"]
instances = settings.setdefault("instances", [])
def instance(module, ident, config):
    entry = {"id": ident, "module": module, "config": config}
    if not any(i.get("id") == ident for i in instances):
        instances.append(entry)
instance("packagechooser", "desktop", "cachuntu-desktop.conf")
instance("packagechooser", "optional", "cachuntu-optional.conf")
instance("contextualprocess", "cachuntu_desktop_action", "cachuntu-desktop-action.conf")
show = settings["sequence"][0]["show"]
for item in ("packagechooser@desktop", "packagechooser@optional"):
    if item not in show:
        show.insert(show.index("partition"), item)
run = settings["sequence"][1]["exec"]
if "contextualprocess@cachuntu_desktop_action" not in run:
    run.insert(run.index("contextualprocess@pkgselect_action") + 1, "contextualprocess@cachuntu_desktop_action")
settings_path.write_text(yaml.safe_dump(settings, sort_keys=False, allow_unicode=True))
modules = cal / "modules"
desktop = {
    "mode": "required", "method": "legacy", "default": "plasma",
    "labels": {"step": "Desktop", "step[es]": "Escritorio"},
    "items": [
        {"id": "plasma", "name": "KDE Plasma", "name[es]": "KDE Plasma",
         "description": "Default. Flexible desktop with extensive customization.",
         "description[es]": "Predeterminado. Escritorio flexible con amplia personalización.",
         "screenshot": "/etc/calamares/branding/kubuntu/welcome.png"},
        {"id": "gnome", "name": "GNOME", "name[es]": "GNOME",
         "description": "Focused desktop. Adds GNOME and selects GDM; Plasma stays available.",
         "description[es]": "Escritorio sencillo. Añade GNOME y selecciona GDM; Plasma sigue disponible.",
         "screenshot": "/etc/calamares/branding/kubuntu/welcome.png"},
    ],
}
optional = {
    "mode": "optionalmultiple", "method": "packages",
    "labels": {"step": "Optional packages", "step[es]": "Paquetes opcionales"},
    "items": [
        {"id": "gaming", "name": "Gaming", "name[es]": "Juegos",
         "description": "GameMode and MangoHud. Internet needed during installation.",
         "description[es]": "GameMode y MangoHud. Requiere Internet durante la instalación.",
         "packages": ["gamemode", "mangohud"],
         "screenshot": "/etc/calamares/branding/kubuntu/welcome.png"},
        {"id": "multimedia", "name": "Multimedia",
         "description": "VLC and OBS Studio. Internet needed during installation.",
         "description[es]": "VLC y OBS Studio. Requiere Internet durante la instalación.",
         "packages": ["vlc", "obs-studio"],
         "screenshot": "/etc/calamares/branding/kubuntu/welcome.png"},
        {"id": "development", "name": "Development", "name[es]": "Desarrollo",
         "description": "Git and build-essential. Internet needed during installation.",
         "description[es]": "Git y build-essential. Requiere Internet durante la instalación.",
         "packages": ["git", "build-essential"],
         "screenshot": "/etc/calamares/branding/kubuntu/welcome.png"},
    ],
}
action = {
    "dontChroot": False, "timeout": 10800,
    "packagechooser_desktop": {
        "gnome": [
            "DEBIAN_FRONTEND=noninteractive apt-get update",
            "DEBIAN_FRONTEND=noninteractive apt-get -y install ubuntu-desktop gdm3 xdg-desktop-portal-gnome",
            "/bin/sh -c 'printf /usr/sbin/gdm3 > /etc/X11/default-display-manager'",
            "ln -sf /lib/systemd/system/gdm3.service /etc/systemd/system/display-manager.service",
        ]
    },
}
for filename, data in (
    ("cachuntu-desktop.conf", desktop),
    ("cachuntu-optional.conf", optional),
    ("cachuntu-desktop-action.conf", action),
):
    (modules / filename).write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True))
# Kubuntu's minimal preset uses an unconditional autoremove. Do not carry it
# into Cachuntu while kernel / HWE metapackage retention is under review.
preset = modules / "pkgselect_context.conf"
old = preset.read_text()
needle = '        - "apt-get -y autoremove"\n'
assert needle in old, "upstream pkgselect config changed; review before building"
preset.write_text(old.replace(needle, ""))
