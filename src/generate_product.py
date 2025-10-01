import random
from pathlib import Path
from typing import Dict
from utils import slugify, brand

def rule_based_outline(keyword:str)->str:
    sections = [
        ("Quick Start", [
            "Define your objective in one sentence.",
            "List 3 success metrics.",
            "Fill the template on the next page before you start."
        ]),
        ("Core Template Columns", [
            "Task | Owner | Start | End | Status | Notes"
        ]),
        ("Common Pitfalls & Fixes", [
            "Scope creep → Freeze scope; backlog new ideas.",
            "No owner → Assign a DRI; use initials.",
            "No deadlines → Add start/end; weekly review."
        ]),
        ("7-Day Action Plan", [
            "Day 1: Objectives & metrics.",
            "Day 2: Fill template.",
            "Day 3–5: Execute.",
            "Day 6: Review metrics.",
            "Day 7: Retro & improvements."
        ]),
        ("Pro Tips", [
            "Keep fields minimal.",
            "Batch updates once daily.",
            "Archive done items weekly."
        ])
    ]
    out = [f"# {keyword.title()} — Starter Kit ({brand()})\n"]
    for title, bullets in sections:
        out.append(f"\n## {title}\n")
        for b in bullets:
            out.append(f"- {b}")
    return "\n".join(out)

def choose_title_and_tagline(keyword:str):
    titles = [
        f"{keyword.title()} Planner",
        f"{keyword.title()} SOP Kit",
        f"{keyword.title()} Template Pack",
        f"{keyword.title()} Launch Checklist",
        f"{keyword.title()} Starter System"
    ]
    taglines = [
        "Start fast. Stay organized. Finish on time.",
        "A no-fluff template that gets work done.",
        "Plug-and-play framework for busy teams.",
        "Everything you need, nothing you don’t.",
        "Clarity, cadence, completion."
    ]
    return random.choice(titles), random.choice(taglines)

def build_product(keyword:str)->Dict:
    title, tagline = choose_title_and_tagline(keyword)
    content_md = rule_based_outline(keyword)
    slug = slugify(f"{title}-{random.randint(1000,9999)}")
    out_dir = Path(f"data/products/{slug}")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir/"content.md").write_text(content_md)
    (out_dir/"meta.json").write_text(__import__('json').dumps({
        "id": slug, "keyword": keyword, "title": title, "tagline": tagline
    }, indent=2))
    return {"dir": str(out_dir), "id": slug, "title": title, "tagline": tagline, "keyword": keyword}
