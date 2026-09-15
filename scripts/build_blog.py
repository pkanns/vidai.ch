#!/usr/bin/env python3
"""
Regenerates the "Vom Blog" card row in index.html from
assets/data/blog-posts.txt — a plain list of post URLs, one per line.

Usage:
    python3 scripts/build_blog.py

Edit assets/data/blog-posts.txt — one URL per line, in display order.
Add or remove lines to change which posts show. Blank lines and lines
starting with # are ignored. Then re-run this script — it fetches each
URL, pulls the title/description/image straight from the post's own
page, and rewrites only the card row in index.html. Requires internet
access to palani.ch when you run it.
"""
import html
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "assets" / "data" / "blog-posts.txt"
INDEX_HTML_PATH = ROOT / "index.html"

BLOG_START = "<!-- BLOG:START -->"
BLOG_END = "<!-- BLOG:END -->"

H1_RE = re.compile(r"<h1[^>]*>(.*?)</h1>", re.IGNORECASE | re.DOTALL)
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
OG_TITLE_RE = re.compile(
    r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\'](.*?)["\']', re.IGNORECASE
)
DESCRIPTION_RE = re.compile(
    r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', re.IGNORECASE
)
OG_DESCRIPTION_RE = re.compile(
    r'<meta[^>]+property=["\']og:description["\'][^>]+content=["\'](.*?)["\']', re.IGNORECASE
)
OG_IMAGE_RE = re.compile(
    r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\'](.*?)["\']', re.IGNORECASE
)
TAG_RE = re.compile(r"<[^>]+>")


def clean(text: str) -> str:
    return html.unescape(TAG_RE.sub("", text)).strip()


def attr_escape(text: str) -> str:
    return text.replace('"', "&quot;")


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8", errors="replace")


def extract_post(url: str) -> dict:
    page = fetch(url)

    h1_match = H1_RE.search(page)
    og_title_match = OG_TITLE_RE.search(page)
    title_match = TITLE_RE.search(page)
    title = (
        clean(h1_match.group(1)) if h1_match
        else clean(og_title_match.group(1)) if og_title_match
        else clean(title_match.group(1)) if title_match
        else url
    )

    desc_match = DESCRIPTION_RE.search(page)
    og_desc_match = OG_DESCRIPTION_RE.search(page)
    description = (
        clean(desc_match.group(1)) if desc_match
        else clean(og_desc_match.group(1)) if og_desc_match
        else ""
    )

    image_match = OG_IMAGE_RE.search(page)
    image = html.unescape(image_match.group(1)) if image_match else ""

    return {"url": url, "title": title, "description": description, "image": image}


def render_card(post: dict) -> str:
    return (
        f'          <a class="blog-card" href="{post["url"]}" target="_blank" rel="noopener">\n'
        f'            <div class="blog-card-img">\n'
        f'              <img src="{post["image"]}" alt="{attr_escape(post["title"])}" loading="lazy" />\n'
        f'            </div>\n'
        f'            <div class="blog-card-body">\n'
        f'              <h4>{post["title"]}</h4>\n'
        f'              <p>{post["description"]}</p>\n'
        f'            </div>\n'
        f'          </a>'
    )


def load_urls():
    lines = DATA_PATH.read_text(encoding="utf-8").splitlines()
    return [
        line.strip()
        for line in lines
        if line.strip() and not line.strip().startswith("#")
    ]


def main():
    urls = load_urls()
    print(f"Fetching {len(urls)} post(s)...")
    posts = []
    for url in urls:
        print(f"  {url}")
        posts.append(extract_post(url))

    cards_html = f"{BLOG_START}\n\n" + "\n\n".join(render_card(p) for p in posts) + f"\n          {BLOG_END}"

    html_content = INDEX_HTML_PATH.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(BLOG_START) + r".*?" + re.escape(BLOG_END), re.DOTALL)
    new_html, n = pattern.subn(cards_html, html_content, count=1)
    if n != 1:
        raise SystemExit("Could not find BLOG:START / BLOG:END markers in index.html")

    INDEX_HTML_PATH.write_text(new_html, encoding="utf-8")
    print(f"index.html regenerated with {len(posts)} post(s).")


if __name__ == "__main__":
    main()
