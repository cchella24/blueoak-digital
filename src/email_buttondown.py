import requests

BASE = "https://api.buttondown.email/v1"

def create_campaign_draft(api_key:str, subject:str, body_html:str):
    r = requests.post(f"{BASE}/campaigns",
        headers={"Authorization": f"Token {api_key}"},
        json={"subject": subject, "body": body_html, "status": "draft"})
    r.raise_for_status()
    return r.json()
