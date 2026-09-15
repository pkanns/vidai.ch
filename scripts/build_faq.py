#!/usr/bin/env python3
"""
Regenerates faq.html (visible FAQ list + JSON-LD FAQPage schema) from
assets/data/faq-data.csv — the single source of truth for FAQ content.

Usage:
    python3 scripts/build_faq.py

Edit assets/data/faq-data.csv (two columns: question, answer — opens
as a table in Excel/Numbers/Google Sheets), then re-run this script.
It rewrites only the two FAQ-content regions in faq.html; the header,
styles, hero copy, and footer are left untouched.
"""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "assets" / "data" / "faq-data.csv"
FAQ_HTML_PATH = ROOT / "faq.html"

LIST_START = "<!-- FAQ:LIST:START -->"
LIST_END = "<!-- FAQ:LIST:END -->"

TAG_RE = re.compile(r"<[^>]+>")


def strip_html(html: str) -> str:
    """Strip tags for the JSON-LD plain-text answer, unescaping &amp; etc."""
    text = TAG_RE.sub("", html)
    text = text.replace("&amp;", "&")
    return text


def render_visible_list(items):
    blocks = []
    for item in items:
        blocks.append(
            f'      <div class="faq-item">\n'
            f'        <h2>{item["question"]}</h2>\n'
            f'        <p>\n'
            f'          {item["answer_html"]}\n'
            f'        </p>\n'
            f'      </div>'
        )
    return "\n\n".join(blocks)


def render_json_ld_entity(items):
    entities = []
    for item in items:
        entities.append({
            "@type": "Question",
            "name": item["question"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": strip_html(item["answer_html"]),
            },
        })
    return entities


def load_items():
    with DATA_PATH.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        items = []
        for row in reader:
            question = (row.get("question") or "").strip()
            answer = (row.get("answer") or "").strip()
            if not question:
                continue
            items.append({"question": question, "answer_html": answer})
        return items


def main():
    items = load_items()

    html = FAQ_HTML_PATH.read_text(encoding="utf-8")

    # 1. Replace the visible FAQ list between the markers.
    new_list_html = f"{LIST_START}\n{render_visible_list(items)}\n      {LIST_END}"
    pattern = re.compile(
        re.escape(LIST_START) + r".*?" + re.escape(LIST_END), re.DOTALL
    )
    html, n = pattern.subn(new_list_html, html, count=1)
    if n != 1:
        raise SystemExit("Could not find FAQ:LIST markers in faq.html")

    # 2. Replace the JSON-LD mainEntity array by parsing/rewriting the
    #    <script type="application/ld+json"> block as JSON.
    script_re = re.compile(
        r'(<script type="application/ld\+json">\s*)(\{.*?\})(\s*</script>)',
        re.DOTALL,
    )
    match = script_re.search(html)
    if not match:
        raise SystemExit("Could not find JSON-LD script block in faq.html")

    ld_json = json.loads(match.group(2))
    for node in ld_json.get("@graph", []):
        if node.get("@type") == "FAQPage":
            node["mainEntity"] = render_json_ld_entity(items)

    new_ld_json_str = json.dumps(ld_json, indent=4, ensure_ascii=False)
    # Re-indent to match the original block's indentation (2 extra spaces).
    new_ld_json_str = "\n".join(
        "  " + line if line.strip() else line
        for line in new_ld_json_str.splitlines()
    )

    html = html[: match.start()] + match.group(1) + new_ld_json_str + match.group(3) + html[match.end():]

    FAQ_HTML_PATH.write_text(html, encoding="utf-8")
    print(f"faq.html regenerated from {len(items)} FAQ entries.")


if __name__ == "__main__":
    main()
