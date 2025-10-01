from pathlib import Path
import json, random

def fetch_keywords(seeds:list, geo="US", out_file="data/trends/latest.json", fallback=5):
    """
    Offline-safe trends fetch. Tries pytrends; if import OR network fails,
    falls back to provided seeds. Always writes a JSON file and returns a list.
    """
    suggestions = []
    try:
        # Try importing here so the file loads even if pytrends isn't installed.
        from pytrends.request import TrendReq  # noqa: F401
        pytrends = TrendReq(hl='en-US', tz=360)
        for seed in seeds[:10]:
            pytrends.build_payload([seed], timeframe='today 12-m', geo=geo)
            related = pytrends.related_queries()
            for _, v in related.items():
                if not v or 'top' not in v or v['top'] is None:
                    continue
                for row in v['top'].to_dict('records')[:5]:
                    q = (row.get('query') or '').strip().lower()
                    if q:
                        suggestions.append(q)
    except Exception:
        # Any import or network error → just use seeds
        suggestions = list(seeds)

    # Dedup, shuffle, persist
    uniq = list({s: None for s in suggestions}.keys()) or list(seeds)
    random.shuffle(uniq)
    Path("data/trends").mkdir(parents=True, exist_ok=True)
    Path(out_file).write_text(json.dumps(uniq[:20], indent=2))
    return uniq[:10] if uniq else seeds[:fallback]
