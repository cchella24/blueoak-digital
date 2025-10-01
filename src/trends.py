from pathlib import Path
import json, random
from pytrends.request import TrendReq

def fetch_keywords(seeds:list, geo="US", out_file="data/trends/latest.json", fallback=5):
    suggestions = []
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        for seed in seeds[:10]:
            pytrends.build_payload([seed], timeframe='today 12-m', geo=geo)
            related = pytrends.related_queries()
            for _,v in related.items():
                if not v or 'top' not in v or v['top'] is None:
                    continue
                for row in v['top'].to_dict('records')[:5]:
                    q = row.get('query','').strip().lower()
                    if q: suggestions.append(q)
    except Exception:
        suggestions = list(seeds)

    uniq = list({s:None for s in suggestions}.keys())
    random.shuffle(uniq)
    Path("data/trends").mkdir(parents=True, exist_ok=True)
    Path(out_file).write_text(json.dumps(uniq[:20], indent=2))
    return uniq[:10] if uniq else seeds[:fallback]
