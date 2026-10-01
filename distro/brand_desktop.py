"""Build the Cachuntu desktop identity from the approved Canva logo."""
import base64
import json
from pathlib import Path
import shutil

def apply(root: Path, assets: Path):
    wallpaper = root / 'usr/share/wallpapers/Cachuntu'
    images = wallpaper / 'contents/images'
    images.mkdir(parents=True, exist_ok=True)
    logo = base64.b64encode((assets / 'cachuntu-logo.png').read_bytes()).decode()
    (images / '1920x1080.svg').write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1920" height="1080" viewBox="0 0 1920 1080">
<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#061326"/><stop offset="1" stop-color="#112c43"/></linearGradient></defs>
<rect width="1920" height="1080" fill="url(#bg)"/>
<path d="M0 850L1920 150M0 1080L1920 380" stroke="#23c6d7" opacity=".08" stroke-width="100"/>
<image x="730" y="245" width="460" height="460" preserveAspectRatio="xMidYMid meet" xlink:href="data:image/png;base64,{logo}"/>
<text x="960" y="780" fill="#edf8ff" font-family="Inter,sans-serif" font-size="64" text-anchor="middle">Cachuntu</text>
<text x="960" y="840" fill="#8eb6cc" font-family="Inter,sans-serif" font-size="24" text-anchor="middle">Ubuntu foundation · Your desktop, your choice</text></svg>''')
    (wallpaper / 'metadata.json').write_text(json.dumps({'KPlugin': {'Id': 'Cachuntu', 'Name': 'Cachuntu', 'Authors': [{'Name': 'Cachuntu Project'}]}}))
    themes = root / 'usr/share/plasma/look-and-feel'
    theme = themes / 'org.cachuntu.desktop'
    shutil.copytree(themes / 'org.kubuntu.desktop', theme, dirs_exist_ok=True)
    metadata = theme / 'metadata.json'
    data = json.loads(metadata.read_text())
    data['KPlugin'].update(Id='org.cachuntu.desktop', Name='Cachuntu', Description='Cachuntu KDE desktop', Website='https://github.com/ElGamer7876/cachuntu')
    metadata.write_text(json.dumps(data, indent=2) + '\n')
    defaults = theme / 'contents/defaults'
    defaults.write_text(defaults.read_text().replace('ColorScheme=BreezeLight', 'ColorScheme=BreezeDark').replace('name=kubuntu', 'name=breeze-dark').replace('Image=Kubuntu', 'Image=Cachuntu'))
    layout = theme / 'contents/layouts/org.kde.plasma.desktop-layout.js'
    layout.write_text(layout.read_text().replace('file:///usr/share/wallpapers/Kubuntu#day-night', 'file:///usr/share/wallpapers/Cachuntu/contents/images/1920x1080.svg').replace("writeConfig( 'DynamicMode', 1 )", "writeConfig( 'DynamicMode', 0 )"))
    # New users inherit the system theme; font selection may add General keys.
    globals_path = root / 'etc/xdg/kdeglobals'
    existing = globals_path.read_text() if globals_path.exists() else ''
    if 'LookAndFeelPackage=' in existing:
        import re
        existing = re.sub(r'(?m)^LookAndFeelPackage=.*$', 'LookAndFeelPackage=org.cachuntu.desktop', existing)
    elif '[KDE]' in existing:
        existing = existing.replace('[KDE]', '[KDE]\nLookAndFeelPackage=org.cachuntu.desktop', 1)
    else:
        existing += '\n[KDE]\nLookAndFeelPackage=org.cachuntu.desktop\n'
    globals_path.write_text(existing)
    home = root / 'usr/share/applications/org.kubuntu.web.home.desktop'
    if home.exists():
        text = home.read_text().replace('Kubuntu Website', 'Cachuntu Project').replace('https://kubuntu.org', 'https://github.com/ElGamer7876/cachuntu').replace('https://www.kubuntu.org', 'https://github.com/ElGamer7876/cachuntu')
        home.write_text(text)
