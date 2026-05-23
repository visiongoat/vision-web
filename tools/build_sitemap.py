#!/usr/bin/env python3
"""
build_sitemap.py — Professional sitemap.xml generator for Vision GO.

- Auto-discovers all *.html under the repo root.
- Excludes 404.html (noindex).
- Reads <lastmod> from git log timestamps where available, else file mtime.
- Sets sensible default priority/changefreq per section.
- Wires bidirectional hreflang between DE and EN equivalents.
- Adds <image:image> for product/blog covers.
- Validates the resulting XML.

Run:
    python3 tools/build_sitemap.py

Output:
    sitemap.xml (overwritten)
"""
from __future__ import annotations
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

SITE = "https://visiongo.at"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "sitemap.xml"

# Section priority/changefreq defaults (prefix match, longest wins)
SECTION_DEFAULTS = {
    "/index.html":          (1.0,  "weekly"),
    "/leistungen.html":     (0.9,  "monthly"),
    "/projekte.html":       (0.95, "weekly"),
    "/ueber-uns.html":      (0.8,  "monthly"),
    "/karriere.html":       (0.75, "weekly"),
    "/kontakt.html":        (0.85, "monthly"),
    "/roadmap.html":        (0.7,  "weekly"),
    "/agb.html":            (0.4,  "yearly"),
    "/datenschutz.html":    (0.4,  "yearly"),
    "/impressum.html":      (0.4,  "yearly"),
    "/projekte/":           (0.9,  "monthly"),
    "/releases/":           (0.7,  "monthly"),
    "/blog/index.html":     (0.95, "daily"),
    "/blog/kategorie/":     (0.7,  "weekly"),
    "/blog/":               (0.8,  "monthly"),
    "/en/index.html":       (0.85, "weekly"),
    "/en/":                 (0.75, "monthly"),
}

# Bidirectional hreflang map: canonical loc → (en_url, de_url)
HREFLANG_PAIRS = {
    "/":                    ("/en/",              "/"),
    "/leistungen.html":     ("/en/services.html", "/leistungen.html"),
    "/projekte.html":       ("/en/work.html",     "/projekte.html"),
    "/ueber-uns.html":      ("/en/about.html",    "/ueber-uns.html"),
    "/kontakt.html":        ("/en/contact.html",  "/kontakt.html"),
    "/datenschutz.html":    ("/en/privacy.html",  "/datenschutz.html"),
    "/agb.html":            ("/en/terms.html",    "/agb.html"),
    "/en/":                 ("/en/",              "/"),
    "/en/services.html":    ("/en/services.html", "/leistungen.html"),
    "/en/work.html":        ("/en/work.html",     "/projekte.html"),
    "/en/about.html":       ("/en/about.html",    "/ueber-uns.html"),
    "/en/contact.html":     ("/en/contact.html",  "/kontakt.html"),
    "/en/privacy.html":     ("/en/privacy.html",  "/datenschutz.html"),
    "/en/terms.html":       ("/en/terms.html",    "/agb.html"),
}

# Pages mapped to an image asset
IMAGE_MAP = {
    "/projekte/megaradio.html":    ("/assets/og/megaradio.svg",  "MegaRadio — Live Radio"),
    "/projekte/scanup.html":       ("/assets/og/scanup.svg",     "ScanUp — Document Scanner"),
    "/projekte/esimfo.html":       ("/assets/og/esimfo.svg",     "eSIMfo — Travel eSIM"),
    "/projekte/taxihub.html":      ("/assets/og/taxihub.svg",    "TaxiHub — Taxi Platform Vienna"),
    "/projekte/snake-online.html": ("/assets/og/snake.svg",      "Online Snake — Multiplayer Game"),
}


def git_lastmod(rel_path: Path) -> Optional[str]:
    try:
        out = subprocess.check_output(
            ["git", "log", "-1", "--format=%aI", "--", str(rel_path)],
            cwd=ROOT, stderr=subprocess.DEVNULL, text=True
        ).strip()
        if out:
            return out[:10]
    except Exception:
        pass
    return None


def file_lastmod(p: Path) -> str:
    git = git_lastmod(p.relative_to(ROOT))
    if git:
        return git
    ts = datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc)
    return ts.strftime("%Y-%m-%d")


def section_defaults(loc: str) -> tuple[float, str]:
    # Try exact match first (with /index.html for root paths)
    candidates = [loc]
    if loc.endswith("/"):
        candidates.append(loc + "index.html")
    for c in candidates:
        if c in SECTION_DEFAULTS:
            return SECTION_DEFAULTS[c]
    # Then prefix match — longest wins
    best, best_len = (0.5, "monthly"), -1
    for prefix, val in SECTION_DEFAULTS.items():
        if prefix.endswith("/") and loc.startswith(prefix) and len(prefix) > best_len:
            best, best_len = val, len(prefix)
    return best


def url_for(rel_path: Path) -> str:
    rel = rel_path.relative_to(ROOT).as_posix()
    if rel.endswith("/index.html"):
        rel = rel[:-len("index.html")]
    return "/" + rel if not rel.startswith("/") else rel


def discover_pages():
    skip = {"404.html"}
    pages = []
    for p in sorted(ROOT.glob("**/*.html")):
        if any(part.startswith(".") for part in p.relative_to(ROOT).parts):
            continue
        if p.name in skip:
            continue
        pages.append(p)
    return pages


def build():
    NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
    XHTML = "http://www.w3.org/1999/xhtml"
    IMG = "http://www.google.com/schemas/sitemap-image/1.1"

    # Build XML manually to control namespace prefixes (cleaner output)
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<urlset xmlns="{NS}"',
        f'        xmlns:xhtml="{XHTML}"',
        f'        xmlns:image="{IMG}">',
        ''
    ]

    total = 0
    for p in discover_pages():
        loc = url_for(p)
        full_loc = SITE + loc
        prio, freq = section_defaults(loc)
        lastmod = file_lastmod(p)

        lines.append('  <url>')
        lines.append(f'    <loc>{full_loc}</loc>')
        lines.append(f'    <lastmod>{lastmod}</lastmod>')
        lines.append(f'    <changefreq>{freq}</changefreq>')
        lines.append(f'    <priority>{prio:.2f}</priority>')

        # hreflang
        if loc in HREFLANG_PAIRS:
            en, de = HREFLANG_PAIRS[loc]
            lines.append(f'    <xhtml:link rel="alternate" hreflang="de-AT" href="{SITE}{de}" />')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{SITE}{en}" />')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{de}" />')
        else:
            lang = "en" if loc.startswith("/en/") else "de-AT"
            lines.append(f'    <xhtml:link rel="alternate" hreflang="{lang}" href="{full_loc}" />')

        # Image (for product pages)
        if loc in IMAGE_MAP:
            img_path, img_title = IMAGE_MAP[loc]
            lines.append('    <image:image>')
            lines.append(f'      <image:loc>{SITE}{img_path}</image:loc>')
            lines.append(f'      <image:title>{img_title}</image:title>')
            lines.append('    </image:image>')

        lines.append('  </url>')
        total += 1

    lines.append('')
    lines.append('</urlset>')
    OUT.write_text("\n".join(lines), encoding="utf-8")

    # Validate
    try:
        ET.parse(OUT)
        print("✓ Valid XML")
    except Exception as e:
        print(f"× INVALID XML: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"✓ Wrote {OUT.relative_to(ROOT)} with {total} URLs")
    return total


if __name__ == "__main__":
    build()
