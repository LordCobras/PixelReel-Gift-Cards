#!/usr/bin/env python3
"""Build OpenCart PixelReel v0.4 development ZIP; filename is significant."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import json
import xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[2]
source=root/"development/pixelgift_clean.ocmod.zip"
with ZipFile(source) as z:
    files={n:z.read(n) for n in z.namelist() if not n.endswith("/")}
controller="admin/controller/module/giftcard.php"
php=files[controller].decode()
needle="    public function index(): void {"
assert needle in php
method="""    private function activateSidebar(): void {
        $this->load->model('setting/modification');
        $modification = $this->model_setting_modification->getModificationByCode('pixelgift_clean_admin_sidebar_v04');
        if ($modification && !(int)$modification['status']) {
            $this->model_setting_modification->editStatus((int)$modification['modification_id'], true);
        }
    }

"""
php=php.replace(needle,method+needle,1)
php=php.replace("    public function install(): void {","    public function install(): void {\n        $this->activateSidebar();",1)
php=php.replace("            $json['success'] = $this->language->get('text_success');",
"""            if ((int)($this->request->post['module_giftcard_status'] ?? 0)) {
                $this->activateSidebar();
            }
            $json['success'] = $this->language->get('text_success') . ' Refresh Extensions > Modifications once to display the sidebar.';""",1)
files[controller]=php.encode()
sidebar=(root/"development/v03/pixelgift_clean_sidebar.ocmod.xml").read_text().replace("pixelgift_clean_admin_sidebar_v03","pixelgift_clean_admin_sidebar_v04").replace("<version>0.3.0</version>","<version>0.4.0</version>").replace("$this->config->get('module_giftcard_status') && $this->user->hasPermission","$this->user->hasPermission")
ET.fromstring(sidebar)
files["ocmod/pixelgift_clean_sidebar.ocmod.xml"]=sidebar.encode()
twig="admin/view/template/module/giftcard.twig"
view=files[twig].decode()
old="</div>\n</div>\n\n<div class=\"container-fluid\">\n<div class=\"card\"><div class=\"card-header\">Manual gift card code generation"
new="</div>\n\n<div class=\"container-fluid\" id=\"giftcard-cards\">\n<div class=\"card\"><div class=\"card-header\">Manual gift card code generation"
assert old in view
view=view.replace(old,new,1).replace('<div class="container-fluid">','<div class="container-fluid" id="giftcard-settings">',1).replace("{{ footer }}","</div>\n{{ footer }}",1)
files[twig]=view.encode()
files["install.json"]=json.dumps({"name":"PixelReel Gift Cards — Admin Sidebar Fix (development)","version":"0.4.0","author":"PixelReel","link":"https://github.com/LordCobras/PixelReel-Gift-Cards"},indent=2).encode()
files["README.md"]=b"Development only. The sidebar OCMOD auto-enables when module is installed. Refresh Extensions > Modifications after install. No customer checkout, redemption, PDFs or email; do not sell cards with this version.\n"
out=root/"releases/pixelgift_clean.ocmod.zip"
out.parent.mkdir(exist_ok=True)
with ZipFile(out,"w",ZIP_DEFLATED) as z:
    for name,data in files.items(): z.writestr(name,data)
print(f"Created {out} ({out.stat().st_size} bytes)")
