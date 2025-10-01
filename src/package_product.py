from pathlib import Path
import zipfile, json

def make_zip(product_dir:str):
    meta = json.loads(Path(product_dir,"meta.json").read_text())
    zpath = Path(product_dir, f"{meta['id']}.zip")
    with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
        for p in ["content.md","product.pdf","cover.jpg","meta.json"]:
            z.write(Path(product_dir,p), arcname=p)
    return str(zpath)
