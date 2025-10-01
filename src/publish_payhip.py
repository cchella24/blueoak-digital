import os
from playwright.sync_api import sync_playwright

def publish(zip_path:str, cover_path:str, title:str, tagline:str, price:float)->str:
    email = os.environ["PAYHIP_EMAIL"]
    password = os.environ["PAYHIP_PASSWORD"]
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://payhip.com/auth/login")
        page.fill('input[name="email"]', email)
        page.fill('input[name="password"]', password)
        page.click('button[type="submit"]')
        page.wait_for_load_state("networkidle")
        page.goto("https://payhip.com/products/new/digital")
        page.wait_for_selector('input[name="title"]')
        page.fill('input[name="title"]', title)
        page.fill('textarea[name="description"]', tagline)
        page.fill('input[name="price"]', f"{price:.2f}")
        page.set_input_files('input[type="file"]', zip_path)
        try:
            page.set_input_files('input[name="cover"]', cover_path)
        except Exception:
            pass
        page.click('button[type="submit"]')
        page.wait_for_load_state("networkidle")
        url = None
        try:
            link = page.locator('a[href*="/p/"]').first
            url = link.get_attribute("href")
            if url and url.startswith("/"): url = "https://payhip.com"+url
        except Exception:
            pass
        browser.close()
    if not url:
        raise RuntimeError("Could not capture Payhip product URL.")
    return url
