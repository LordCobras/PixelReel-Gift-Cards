#!/usr/bin/env python3
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import json, xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[2]
src=root/"releases/pixelgift_clean.ocmod.zip"
with ZipFile(src) as z:
    files={n:z.read(n) for n in z.namelist() if not n.endswith("/")}
cp="admin/controller/module/giftcard.php"
php=files[cp].decode()
assert "getModificationByCode('pixelgift_clean_admin_sidebar_v04')" in php
php=php.replace("getModificationByCode('pixelgift_clean_admin_sidebar_v04')","getModificationByCode('pixelgift_clean_sidebar')")
php=php.replace("        $this->load->language('extension/pixelgift_clean/module/giftcard');\n\n        $this->document->setTitle","        $this->load->language('extension/pixelgift_clean/module/giftcard');\n        $this->activateSidebar();\n\n        $this->document->setTitle",1)
files[cp]=php.encode()
xp="ocmod/pixelgift_clean_sidebar.ocmod.xml"
xml=files[xp].decode().replace("pixelgift_clean_admin_sidebar_v04","pixelgift_clean_sidebar").replace("<version>0.4.0</version>","<version>0.5.0</version>").replace("PixelReel Gift Cards — Admin Sidebar","PixelReel Gift Cards — Admin Sidebar v0.5")
ET.fromstring(xml)
files[xp]=xml.encode()
files["install.json"]=json.dumps({"name":"PixelReel Gift Cards — Sidebar Fix v0.5 (development)","version":"0.5.0","author":"PixelReel","link":"https://github.com/LordCobras/PixelReel-Gift-Cards"},indent=2).encode()
files["README.md"]=b"Development only. Sidebar fix: OpenCart modification DB code comes from XML basename pixelgift_clean_sidebar. Install module then refresh Extensions > Modifications. No checkout payment/PDF/email/redemption. Not for production gift card sales.\n"
with ZipFile(src,"w",ZIP_DEFLATED) as z:
    for n,b in files.items():z.writestr(n,b)
print("Built",src)
