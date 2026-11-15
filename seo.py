#!/usr/bin/env python3
"""Add canonical + social tags to every indexable page and rebuild sitemap.xml.
Safe to re-run: pages that already have a canonical link are left alone. Pages marked noindex
(unreleased apps) get nothing and stay out of the sitemap. Run from the repo root: ./seo.py"""
import glob, html, os, re

BASE = "https://apps.freshcoastrf.com"
INDEXABLE_SKIP = {"404.html"}

def canon_for(path):
    d, f = os.path.split(path)
    if f == "index.html":
        return f"{BASE}/{d}/" if d else f"{BASE}/"
    return f"{BASE}/{d}/{f[:-5]}"          # auto-trailing-slash serves privacy.html as /privacy

pages = [p.replace("\\", "/") for p in glob.glob("*.html") + glob.glob("*/*.html")]
pages = [p for p in pages if p not in INDEXABLE_SKIP and not p.startswith(("template/", "assets/", "tools/"))]

sitemap = []
for p in sorted(pages):
    s = open(p, encoding="utf-8").read()
    if "noindex" in s:
        continue
    canon = canon_for(p)
    if p.endswith("index.html"):
        sitemap.append(canon)
    if 'rel="canonical"' in s:
        continue
    tags = f'<link rel="canonical" href="{canon}">\n'
    if p.endswith("index.html"):                   # home page and each app overview get social tags
        slug = os.path.dirname(p)
        title = html.unescape(re.search(r"<title>(.*?)</title>", s).group(1))
        desc = html.unescape(re.search(r'<meta name="description" content="(.*?)">', s).group(1))
        img = f"{BASE}/assets/icons/{slug}.png" if slug else f"{BASE}/assets/favicon.png"
        q = lambda v: html.escape(v, quote=True)
        tags += (f'<meta property="og:type" content="website">\n'
                 f'<meta property="og:site_name" content="Fresh Coast RF">\n'
                 f'<meta property="og:title" content="{q(title)}">\n'
                 f'<meta property="og:description" content="{q(desc)}">\n'
                 f'<meta property="og:url" content="{canon}">\n'
                 f'<meta property="og:image" content="{img}">\n'
                 f'<meta name="twitter:card" content="summary">\n')
    m = re.search(r'<meta name="description" content=".*?">\n?', s)
    s = s[:m.end()] + ("" if m.group(0).endswith("\n") else "\n") + tags + s[m.end():]
    open(p, "w", encoding="utf-8", newline="").write(s)
    print("tagged", p)

with open("sitemap.xml", "w", encoding="utf-8", newline="\n") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for u in sitemap:
        f.write(f"  <url><loc>{u}</loc></url>\n")
    f.write("</urlset>\n")
print("sitemap:", len(sitemap), "urls")
