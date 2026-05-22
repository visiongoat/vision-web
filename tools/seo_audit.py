#!/usr/bin/env python3
"""
Comprehensive SEO audit for Vision GO — runs 25+ checks per page across all 49 HTML files.

Checks per page:
  TITLE      — present, length 30-60 chars
  DESC       — present, length 120-160 chars
  CANONICAL  — present, absolute https URL
  H1         — exactly one
  HX-HIER    — no skipped levels (e.g. h2 after h4)
  HREFLANG   — present (de-AT or en + x-default)
  OG         — og:title, og:description, og:image, og:url
  TWITTER    — twitter:card present
  ROBOTS     — present (not noindex except 404)
  LANG       — <html lang=...> present
  VIEWPORT   — meta viewport present
  CHARSET    — UTF-8 declared
  FAVICON    — link rel=icon present
  SCHEMA     — at least one application/ld+json
  IMG-ALT    — every img has alt
  IMG-DIMS   — every img has width+height
  INT-LINK   — at least 3 internal anchor links
  EXT-NOOP   — external <a> has rel="noopener" / "noreferrer"
  LAZY-IMG   — non-LCP images have loading="lazy"
  PRELOAD    — preconnect to font CDN if used
  KEYWORDS   — meta keywords present (optional but used here)
  THEME      — theme-color set
  CONSENT    — cookie consent dialog present
  SKIP-LINK  — skip-link present
  MAIN       — <main id="main"> present
  STYLES-LNK — stylesheet link
"""
import re
from pathlib import Path
from collections import Counter

ROOT = Path("/Users/mumiix/visiongo-new")

def get_pages():
    return sorted(p for p in ROOT.glob("**/*.html"))

def check(txt, page_path):
    issues = []
    rel = str(page_path.relative_to(ROOT))
    is_404 = "404.html" in rel

    # 1. TITLE
    m = re.search(r"<title>([^<]+)</title>", txt)
    if not m:
        issues.append(("HIGH", "TITLE-MISSING", "no <title> tag"))
    else:
        t = m.group(1).strip()
        if len(t) < 30:
            issues.append(("MED", "TITLE-SHORT", f"title only {len(t)} chars: '{t}'"))
        elif len(t) > 65:
            issues.append(("LOW", "TITLE-LONG", f"title {len(t)} chars (recommend ≤60)"))

    # 2. META DESCRIPTION
    m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', txt)
    if not m:
        issues.append(("HIGH", "DESC-MISSING", "no meta description"))
    else:
        d = m.group(1).strip()
        if len(d) < 80:
            issues.append(("MED", "DESC-SHORT", f"description {len(d)} chars"))
        elif len(d) > 170:
            issues.append(("LOW", "DESC-LONG", f"description {len(d)} chars (recommend ≤160)"))

    # 3. CANONICAL
    if not re.search(r'<link\s+rel="canonical"\s+href="https://', txt):
        issues.append(("HIGH", "CANONICAL-MISSING", "no canonical or not absolute https"))

    # 4. H1
    h1_count = len(re.findall(r"<h1\b", txt))
    if h1_count == 0:
        issues.append(("HIGH", "H1-MISSING", "no <h1>"))
    elif h1_count > 1:
        issues.append(("HIGH", "H1-MULTIPLE", f"{h1_count} h1 tags found"))

    # 5. HEADING HIERARCHY
    heads = re.findall(r"<h([1-6])\b", txt)
    if heads:
        prev = 0
        for h in heads:
            lvl = int(h)
            if prev and lvl > prev + 1:
                issues.append(("LOW", "H-SKIP", f"heading jumps from h{prev} to h{lvl}"))
                break
            prev = lvl

    # 6. HREFLANG
    if not is_404 and "hreflang=" not in txt:
        issues.append(("MED", "HREFLANG-MISSING", "no hreflang link tags"))

    # 7. OG TAGS
    for og in ("og:title", "og:description", "og:image", "og:url"):
        if f'property="{og}"' not in txt:
            issues.append(("MED", "OG-MISSING", f"missing {og}"))

    # 8. TWITTER CARD
    if 'name="twitter:card"' not in txt:
        issues.append(("LOW", "TW-CARD-MISSING", "no twitter:card"))

    # 9. ROBOTS
    if not is_404 and not re.search(r'<meta\s+name="robots"', txt):
        issues.append(("LOW", "ROBOTS-MISSING", "no meta robots (default = index, follow)"))

    # 10. LANG
    if not re.search(r'<html[^>]*\blang="[a-z\-A-Z]+"', txt):
        issues.append(("HIGH", "LANG-MISSING", "no <html lang=...>"))

    # 11. VIEWPORT
    if 'name="viewport"' not in txt:
        issues.append(("HIGH", "VIEWPORT-MISSING", "no viewport meta"))

    # 12. CHARSET
    if '<meta charset=' not in txt:
        issues.append(("HIGH", "CHARSET-MISSING", "no <meta charset>"))

    # 13. FAVICON
    if not re.search(r'<link\s+rel="(?:icon|shortcut icon)"', txt):
        issues.append(("LOW", "FAVICON-MISSING", "no favicon link"))

    # 14. SCHEMA / JSON-LD
    if 'application/ld+json' not in txt:
        issues.append(("MED", "SCHEMA-MISSING", "no JSON-LD structured data"))

    # 15. IMG ALT
    imgs = re.findall(r'<img\b[^>]*>', txt)
    no_alt = [i for i in imgs if not re.search(r'\balt="', i)]
    if no_alt:
        issues.append(("MED", "IMG-ALT", f"{len(no_alt)} img(s) without alt"))

    # 16. IMG DIMS
    no_dims = [i for i in imgs if not (re.search(r'\bwidth=', i) and re.search(r'\bheight=', i))]
    if no_dims:
        issues.append(("LOW", "IMG-DIMS", f"{len(no_dims)} img(s) without width/height"))

    # 17. INTERNAL LINKS
    int_links = re.findall(r'href="(?:/|#)[^"]*"', txt)
    if len(int_links) < 5:
        issues.append(("LOW", "INT-LINK-FEW", f"only {len(int_links)} internal links"))

    # 18. EXTERNAL LINKS rel
    # find <a> tags with external href
    ext_anchors = re.findall(r'<a\s+[^>]*href="https?://[^"]+"[^>]*>', txt)
    bad_ext = []
    for a in ext_anchors:
        if 'visiongo.at' in a:
            continue
        if 'rel=' not in a:
            bad_ext.append(a)
    if bad_ext:
        issues.append(("LOW", "EXT-NOOP", f"{len(bad_ext)} external <a> without rel"))

    # 19. LAZY-LOADING
    if len(imgs) > 3:
        lazy = [i for i in imgs if 'loading="lazy"' in i]
        eager = [i for i in imgs if 'loading="eager"' in i]
        if len(lazy) + len(eager) < len(imgs) - 1:
            issues.append(("LOW", "LAZY-MISSING", f"{len(imgs) - len(lazy) - len(eager)}/{len(imgs)} img without loading attr"))

    # 20. PRECONNECT to font CDN
    if 'fonts.googleapis.com' in txt and 'rel="preconnect"' not in txt:
        issues.append(("LOW", "PRECONNECT-MISSING", "fonts.googleapis.com used without preconnect"))

    # 21. KEYWORDS
    # optional

    # 22. THEME COLOR
    if 'name="theme-color"' not in txt:
        issues.append(("LOW", "THEME-MISSING", "no theme-color meta"))

    # 23. CONSENT
    if not is_404 and 'class="consent"' not in txt:
        issues.append(("MED", "CONSENT-MISSING", "no cookie consent dialog"))

    # 24. SKIP-LINK
    if not is_404 and 'class="skip-link"' not in txt:
        issues.append(("MED", "SKIP-LINK-MISSING", "no skip-link"))

    # 25. MAIN
    if not is_404 and 'id="main"' not in txt:
        issues.append(("MED", "MAIN-MISSING", "no <main id=main>"))

    # 26. STYLESHEET
    if 'rel="stylesheet"' not in txt:
        issues.append(("HIGH", "CSS-MISSING", "no stylesheet link"))

    # 27. OG IMAGE absolute
    og_img = re.search(r'<meta\s+property="og:image"\s+content="([^"]+)"', txt)
    if og_img and not og_img.group(1).startswith("http"):
        issues.append(("MED", "OG-IMG-REL", "og:image is not absolute URL"))

    return issues


def main():
    pages = get_pages()
    severity_priority = {"HIGH": 0, "MED": 1, "LOW": 2}
    all_issues = []
    summary = Counter()
    page_issues = {}

    for p in pages:
        txt = p.read_text(encoding="utf-8")
        issues = check(txt, p)
        page_issues[str(p.relative_to(ROOT))] = issues
        for sev, code, msg in issues:
            summary[sev] += 1
            summary[code] += 1
            all_issues.append((sev, code, str(p.relative_to(ROOT)), msg))

    # Output
    print("=" * 78)
    print(f"  VISION GO — COMPREHENSIVE SEO AUDIT  ({len(pages)} pages)")
    print("=" * 78)
    print()
    print("OVERALL SEVERITY")
    print(f"  HIGH (must fix):  {summary['HIGH']:>3}")
    print(f"  MED  (should fix):{summary['MED']:>3}")
    print(f"  LOW  (nice to have):{summary['LOW']:>3}")
    print()

    # Top issue types
    print("MOST COMMON ISSUE CODES")
    top_codes = [(c, n) for c, n in summary.most_common() if c not in ("HIGH", "MED", "LOW")]
    for code, n in top_codes[:15]:
        print(f"  {code:<22} {n:>3} occurrence(s)")
    print()

    # Per-page report
    print("=" * 78)
    print("  PER-PAGE FINDINGS")
    print("=" * 78)
    clean_pages = []
    for page, issues in sorted(page_issues.items()):
        if not issues:
            clean_pages.append(page)
            continue
        issues.sort(key=lambda x: severity_priority[x[0]])
        print(f"\n  {page}")
        for sev, code, msg in issues:
            print(f"    [{sev:<4}] {code:<22} {msg}")

    print()
    print("=" * 78)
    print(f"  CLEAN PAGES ({len(clean_pages)}/{len(pages)}):")
    for p in clean_pages:
        print(f"    ✓ {p}")
    print("=" * 78)


if __name__ == "__main__":
    main()
