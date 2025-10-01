from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pathlib import Path
import textwrap, datetime as dt
from utils import brand

def wrap(text, width=92):
    return [l for line in text.splitlines() for l in textwrap.wrap(line, width=width) or [""]]

def render_pdf(product_dir:str, title:str):
    content_md = Path(product_dir,"content.md").read_text()
    pdf_path = Path(product_dir,"product.pdf")
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    W,H = letter
    margin = 54
    y = H - 72
    c.setFont("Helvetica-Bold", 22); c.drawString(margin, y, title); y -= 30
    c.setFont("Helvetica", 11)
    for line in wrap(content_md, 95):
        if y < 72:
            c.showPage(); y = H - 72; c.setFont("Helvetica", 11)
        c.drawString(margin, y, line); y -= 14
    c.setFont("Helvetica-Oblique", 9)
    c.drawRightString(W-54, 40, f"© {dt.datetime.utcnow().year} {brand()}")
    c.showPage(); c.save()
    return str(pdf_path)
