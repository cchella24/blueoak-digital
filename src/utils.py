import os, json, re, time, datetime as dt
from pathlib import Path

def env(name, default=None):
    return os.environ.get(name, default)

def slugify(s:str)->str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+","-",s).strip("-")
    return s[:80]

def read_json(p):
    p = Path(p)
    return json.loads(p.read_text()) if p.exists() else []

def write_json(p, data):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2))

def now_iso():
    return dt.datetime.utcnow().replace(microsecond=0).isoformat()+"Z"

def brand():
    return env("BRAND_NAME","BlueOak Digital")

def price_usd():
    return float(env("DEFAULT_PRICE_USD","9.00"))
