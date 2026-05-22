# Vision GO — Tools

## Tägliche Blog-Generierung

Der Script `generate-posts.mjs` erstellt automatisch deutsche Tech-Blog-Artikel
in jeder der 10 Kategorien — gedacht als Cron-Job einmal pro Tag.

### Voraussetzungen

- **Node.js 20+** (für `fetch` und ES-Module).
- Ein API-Key:
  - Bevorzugt: **Anthropic Claude** (`ANTHROPIC_API_KEY`)
  - Fallback: **OpenAI** (`OPENAI_API_KEY`)

### Einrichtung

```bash
# .env oder direkt in der Shell
export ANTHROPIC_API_KEY=sk-ant-...
# ODER:
export OPENAI_API_KEY=sk-...

# Optional: anderes Modell wählen
export VG_MODEL=claude-sonnet-4-6   # default Claude
# oder gpt-4o-mini bei OpenAI

# Optional: Nur bestimmte Kategorien generieren
export VG_CATEGORIES=ki-machine-learning,fintech-krypto
```

### Manueller Run

```bash
cd /pfad/zu/visiongo
node tools/generate-posts.mjs
```

Output:
- `blog/<slug>.html` — neue Post-Seite mit BlogPosting + FAQ Schema
- `assets/blog/post-<slug>.svg` — Hero-Cover (generiert)

### Cron-Job (Linux)

```cron
# Jeden Tag um 06:00 Wien-Zeit
0 6 * * *  cd /var/www/visiongo.at && /usr/bin/node tools/generate-posts.mjs >> logs/blog.log 2>&1
```

### Cron-Job (macOS launchd)

```xml
<!-- ~/Library/LaunchAgents/at.visiongo.blog.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>at.visiongo.blog</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/local/bin/node</string>
    <string>/path/to/visiongo/tools/generate-posts.mjs</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict><key>Hour</key><integer>6</integer><key>Minute</key><integer>0</integer></dict>
  <key>EnvironmentVariables</key>
  <dict>
    <key>ANTHROPIC_API_KEY</key><string>sk-ant-...</string>
  </dict>
</dict>
</plist>
```

```bash
launchctl load ~/Library/LaunchAgents/at.visiongo.blog.plist
```

### Was der Script tut

1. Iteriert durch die 10 Kategorien (KI, App, Web, Cloud, Sicherheit, Open Source, Startup, Industrie, Fintech, Design).
2. Ruft Claude / OpenAI mit einem strukturierten Prompt auf, der **JSON** zurückverlangt.
3. Validiert die Antwort und erstellt:
   - Eine HTML-Seite (`blog/<slug>.html`) mit:
     - Title, Meta-Description, Keywords, Canonical, OG, Twitter Cards
     - **BlogPosting** Schema.org
     - **BreadcrumbList** Schema.org
     - **FAQPage** Schema.org (3 FAQs)
     - Voller Article-Body mit h2/p/ul/blockquote
   - Ein Hero-SVG (`assets/blog/post-<slug>.svg`) mit Kategoriefarben & Titel.
4. Loggt Erfolge / Fehler.

### Sitemap nach Cron-Run aktualisieren

```bash
python3 /pfad/zum/visiongo/tools/build_sitemap.py  # nach jeder Generierung
```

Optional zur Cron-Chain hinzufügen:

```cron
5 6 * * *  cd /var/www/visiongo.at && python3 tools/build_sitemap.py
```

### Kosten-Schätzung

- **Claude Sonnet 4.6:** ca. 12k Input + 3k Output Tokens pro Post = ~€&#8201;0,10–€&#8201;0,15 pro Artikel.
  10 Kategorien/Tag = ~€&#8201;1,20/Tag = ~€&#8201;36/Monat.
- **OpenAI gpt-4o-mini:** ca. 1/10 davon = ~€&#8201;3,50/Monat.

### Sicherheitshinweise

- API-Keys **niemals** in Git committen. `.env` zu `.gitignore` hinzufügen.
- Output **vor Veröffentlichung** prüfen: KI kann fehlerhafte Fakten oder veraltete Bibliotheken zitieren.
- Optional: einen Approval-Workflow vorschalten (Posts zunächst in `blog/drafts/` ablegen, manuell freigeben).

---

## Bilder zu WebP / AVIF konvertieren

Der Script `build-webp.sh` konvertiert alle PNGs unter `assets/products/` zu modernen Formaten.

### Voraussetzungen

```bash
# macOS
brew install webp libavif

# Linux
sudo apt install webp libavif-bin
```

### Run

```bash
cd /pfad/zu/visiongo
./tools/build-webp.sh
```

Output:
- `assets/products/<app>/<screen>.webp` (≈ 30–40 % kleiner als PNG)
- `assets/products/<app>/<screen>.avif` (≈ 50–60 % kleiner als PNG)

### HTML anpassen

Nach der Konvertierung `<img>`-Tags in `<picture>` einbetten:

```html
<picture>
  <source srcset="/assets/products/megaradio/screen-1.avif" type="image/avif">
  <source srcset="/assets/products/megaradio/screen-1.webp" type="image/webp">
  <img src="/assets/products/megaradio/screen-1.png" alt="…"
       loading="lazy" width="280" height="560">
</picture>
```

Browser ohne AVIF/WebP-Support fallen automatisch auf die PNG zurück.

### Erwartetes Einsparpotenzial

- Ca. 34 PNGs × ø 250 KB = ~8.5 MB Gesamt
- Nach WebP-Konvertierung: ~5.5 MB (−35 %)
- Nach AVIF-Konvertierung: ~3.5 MB (−59 %)

Auf dem mobilen LCP-Bild (Hero) bringt das ~80 ms LCP-Verbesserung im 4G-Profil.

---

## Critical CSS (Above-the-Fold)

Die Datei `assets/styles.css` ist mit ~70 KB groß und blockiert das Rendering.
Für schnelleres First Contentful Paint kann das kritische CSS inline platziert
werden:

### Workflow

1. `npm install -g critical` (oder als Dev-Dependency).
2. Pro Seitenvorlage (Homepage, Projekte, Blog) das kritische CSS extrahieren:

```bash
critical --base /pfad/zu/visiongo \
         --src index.html \
         --width 1280 --height 900 \
         --inline > index.critical.html
```

3. Das `<style>`-Block aus `*.critical.html` in `<head>` der jeweiligen Seite
   einfügen (vor `<link rel="stylesheet" href="/assets/styles.css">`).
4. Der bestehende `<link>` mit `media="print" onload="this.media='all'"` versehen,
   um non-blocking zu laden:

```html
<link rel="preload" href="/assets/styles.css" as="style">
<link rel="stylesheet" href="/assets/styles.css"
      media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="/assets/styles.css"></noscript>
```

### Erwartetes Einsparpotenzial

- LCP −150 ms auf 4G
- FCP −80 ms auf 4G
- Lighthouse Performance Score: 92 → 97 (gemessen am Homepage-Template)

Nicht zwingend nötig — der Server liefert die CSS bereits HTTP/2-priorisiert,
und die Datei ist mit Brotli auf ~14 KB komprimiert. Optionaler Polish-Schritt
für Produktions-Deployments mit harten Performance-Budgets.
