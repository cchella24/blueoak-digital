from pathlib import Path
import os, json, yaml
from utils import read_json, write_json, brand, price_usd, now_iso
from trends import fetch_keywords
from generate_product import build_product
from render_pdf import render_pdf
from cover_art import make_cover
from package_product import make_zip

def main():
    cfg = yaml.safe_load(Path("config/config.example.yaml").read_text())
    seeds = cfg["trends"]["seeds"]
    kws = fetch_keywords(seeds, cfg["trends"]["geo"])
    keyword = (kws[0] if kws else seeds[0]).strip()

    # Build product artifacts
    prod = build_product(keyword)
    render_pdf(prod["dir"], prod["title"])
    cover = make_cover(prod["dir"], prod["title"], prod["tagline"])
    bundle = make_zip(prod["dir"])

    # Decide publish or dry-run
    payhip_email = os.getenv("PAYHIP_EMAIL","placeholder")
    payhip_pass  = os.getenv("PAYHIP_PASSWORD","placeholder")
    real_publish = all(v and v.lower()!="placeholder" for v in [payhip_email, payhip_pass])

    if real_publish:
        from publish_payhip import publish as publish_payhip
        checkout_url = publish_payhip(bundle, cover, prod["title"], prod["tagline"], price_usd())
    else:
        checkout_url = "#"  # dry-run (no external publish)

    # Update catalog (docs/products.json)
    items = read_json("docs/products.json")
    record = {
        "id": prod["id"],
        "title": prod["title"],
        "tagline": prod["tagline"],
        "price_usd": f"{price_usd():.2f}",
        "checkout_url": checkout_url,
        "cover_url": f"https://raw.githubusercontent.com/{os.getenv('GITHUB_REPOSITORY')}/main/data/products/{prod['id']}/cover.jpg",
        "created_at": now_iso()
    }
    items.insert(0, record)
    write_json("docs/products.json", items)

    # Save a little metadata log
    Path("data/products", prod["id"], "publish.json").write_text(json.dumps(record, indent=2))

if __name__ == "__main__":
    main()
