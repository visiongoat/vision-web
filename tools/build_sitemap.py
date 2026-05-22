#!/usr/bin/env python3
import pathlib, datetime

SITE = "https://visiongo.at"
TODAY = "2026-05-13"
ROOT = pathlib.Path("/Users/mumiix/visiongo-new")

# Static main pages
main_urls = [
    ("/", 1.0, "weekly"),
    ("/leistungen.html", 0.9, "monthly"),
    ("/projekte.html", 0.95, "weekly"),
    ("/ueber-uns.html", 0.8, "monthly"),
    ("/karriere.html", 0.75, "weekly"),
    ("/kontakt.html", 0.85, "monthly"),
    ("/blog/", 0.95, "daily"),
]

# Product pages
product_urls = [
    ("/projekte/megaradio.html", 0.9, "monthly", "megaradio"),
    ("/projekte/scanup.html", 0.9, "monthly", "scanup"),
    ("/projekte/esimfo.html", 0.9, "monthly", "esimfo"),
    ("/projekte/taxihub.html", 0.9, "monthly", "taxihub"),
    ("/projekte/snake-online.html", 0.9, "monthly", "snake"),
]

# Service anchors
anchors = ["mobile", "softwareentwicklung", "cloud", "ki", "sicherheit", "produkt"]

# Legal
legal = [
    ("/impressum.html", 0.3, "yearly"),
    ("/datenschutz.html", 0.3, "yearly"),
]

# Blog posts (auto-discover)
blog_files = sorted((ROOT / "blog").glob("*.html"))
blog_post_urls = [f"/blog/{f.name}" for f in blog_files if f.name != "index.html"]

# Categories
cat_files = sorted((ROOT / "blog" / "kategorie").glob("*.html"))
cat_urls = [f"/blog/kategorie/{f.name}" for f in cat_files]

lines = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
         '        xmlns:xhtml="http://www.w3.org/1999/xhtml"',
         '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
         '']

def url(loc, lastmod, priority, changefreq, image_loc=None, image_title=None):
    out = [f'  <url>',
           f'    <loc>{SITE}{loc}</loc>',
           f'    <lastmod>{lastmod}</lastmod>',
           f'    <changefreq>{changefreq}</changefreq>',
           f'    <priority>{priority}</priority>',
           f'    <xhtml:link rel="alternate" hreflang="de-AT" href="{SITE}{loc}" />']
    if image_loc:
        out.append('    <image:image>')
        out.append(f'      <image:loc>{SITE}{image_loc}</image:loc>')
        if image_title:
            out.append(f'      <image:title>{image_title}</image:title>')
        out.append('    </image:image>')
    out.append('  </url>')
    return '\n'.join(out)

# Main
lines.append('  <!-- Main pages -->')
for loc, prio, cf in main_urls:
    lines.append(url(loc, TODAY, prio, cf))

# Products
lines.append('')
lines.append('  <!-- Products -->')
for loc, prio, cf, slug in product_urls:
    lines.append(url(loc, TODAY, prio, cf, f"/assets/og/{slug}.svg", f"Vision GO {slug.capitalize()}"))

# Service anchors
lines.append('')
lines.append('  <!-- Service anchors -->')
for a in anchors:
    lines.append(url(f"/leistungen.html#{a}", TODAY, 0.6, "monthly"))

# Blog posts
lines.append('')
lines.append('  <!-- Blog posts -->')
for f in blog_files:
    if f.name == "index.html":
        continue
    slug = f.stem
    img_loc = f"/assets/blog/post-{slug}.svg"
    lines.append(url(f"/blog/{f.name}", TODAY, 0.85, "weekly", img_loc, slug.replace('-', ' ').title()))

# Categories
lines.append('')
lines.append('  <!-- Blog categories -->')
for f in cat_files:
    slug = f.stem
    img_loc = f"/assets/blog/cat-{slug}.svg"
    lines.append(url(f"/blog/kategorie/{f.name}", TODAY, 0.7, "weekly", img_loc, f"Kategorie {slug}"))

# Legal
lines.append('')
lines.append('  <!-- Legal -->')
for loc, prio, cf in legal:
    lines.append(url(loc, TODAY, prio, cf))

lines.append('')
lines.append('</urlset>')

(ROOT / "sitemap.xml").write_text('\n'.join(lines), encoding="utf-8")
print(f"✓ Sitemap with {len(main_urls) + len(product_urls) + len(anchors) + len(blog_post_urls) + len(cat_urls) + len(legal)} URLs")
