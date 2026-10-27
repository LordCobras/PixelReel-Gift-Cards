#!/usr/bin/env python3
"""Build v0.3 development installer from the v0.2 baseline kept in this repository."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import json, xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[2]
src = root / "development/pixelgift_clean.ocmod.zip"
xml = (root / "development/v03/pixelgift_clean_sidebar.ocmod.xml").read_bytes()
ET.fromstring(xml)
out = root / "releases/pixelgift_clean.ocmod.zip"
out.parent.mkdir(exist_ok=True)
with ZipFile(src) as archive:
    files = {name: archive.read(name) for name in archive.namelist() if not name.endswith("/")}
twig_path = "admin/view/template/module/giftcard.twig"
twig = files[twig_path].decode("utf-8")
old = '</div>\n</div>\n\n<div class="container-fluid">\n<div class="card"><div class="card-header">Manual gift card code generation'
new = '</div>\n\n<div class="container-fluid" id="giftcard-cards">\n<div class="card"><div class="card-header">Manual gift card code generation'
if old not in twig:
    raise RuntimeError("Unexpected v0.2 template structure")
twig = twig.replace(old, new, 1)
twig = twig.replace('<div class="container-fluid">', '<div class="container-fluid" id="giftcard-settings">', 1)
twig = twig.replace("{{ footer }}", "</div>\n{{ footer }}", 1)
files[twig_path] = twig.encode()
files["ocmod/pixelgift_clean_sidebar.ocmod.xml"] = xml
files["install.json"] = json.dumps({
    "name": "PixelReel Gift Cards — Admin Sidebar (development)",
    "version": "0.3.0", "author": "PixelReel",
    "link": "https://github.com/LordCobras/PixelReel-Gift-Cards"
}, indent=2).encode()
files["README.md"] = b"Development build only. One-time gift card checkout redemption, PDF and email NOT implemented. DO NOT SELL gift cards with this version. Install OCMOD and refresh Modifications.\n"
with ZipFile(out, "w", ZIP_DEFLATED) as archive:
    for name, data in files.items():
        archive.writestr(name, data)
print(out, out.stat().st_size)
