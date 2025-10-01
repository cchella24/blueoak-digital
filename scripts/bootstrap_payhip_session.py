# scripts/bootstrap_payhip_session.py
# Run locally, headed. Logs you into Payhip once and saves storage state to .auth/payhip.json
from playwright.sync_api import sync_playwright
from pathlib import Path

def main():
    Path(".auth").mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        context = p.chromium.launch_persistent_context(
            user_data_dir=".auth/profile",
            headless=False
        )
        page = context.new_page()
        page.goto("https://payhip.com/auth/login", wait_until="networkidle")
        print("==> Please complete login in the browser window.")
        print("    If a cookie banner appears, accept it. If 2FA is enabled, enter the code.")
        page.wait_for_timeout(30000)  # give yourself time to log in
        # Navigate to dashboard to ensure auth cookies are set
        page.goto("https://payhip.com/dashboard", wait_until="networkidle")
        # Save storage state snapshot
        context.storage_state(path=".auth/payhip.json")
        print("Saved session to .auth/payhip.json")
        context.close()
        browser.close()

if __name__ == "__main__":
    main()
