from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from utils import brand

def make_cover(product_dir:str, title:str, tagline:str):
    w,h = 1400,1960
    img = Image.new("RGB",(w,h), "#0e1f2e")
    d = ImageDraw.Draw(img)
    d.rectangle([0,140,w,560], fill="#194b78")
    try:
        font_title = ImageFont.truetype("arial.ttf", 72)
        font_tag  = ImageFont.truetype("arial.ttf", 36)
        font_brand= ImageFont.truetype("arial.ttf", 28)
    except Exception:
        font_title = ImageFont.load_default()
        font_tag   = ImageFont.load_default()
        font_brand = ImageFont.load_default()
    d.text((70,300), title[:40], font=font_title, fill="#ffffff")
    d.text((70,400), tagline[:60], font=font_tag,  fill="#b6d7f2")
    d.text((70,1860), brand(),    font=font_brand, fill="#b6d7f2")
    out = Path(product_dir,"cover.jpg"); img.save(out, quality=92)
    return str(out)
