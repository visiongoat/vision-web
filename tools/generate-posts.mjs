#!/usr/bin/env node
/**
 * Vision GO — Daily Blog Post Generator
 * ---------------------------------------
 * Generates one new German tech-blog post per category per day using
 * the Anthropic Claude API (or OpenAI as a fallback).
 *
 * USAGE:
 *   1. Setze die API Keys in der Umgebung:
 *        export ANTHROPIC_API_KEY=sk-ant-...
 *        # ODER
 *        export OPENAI_API_KEY=sk-...
 *
 *   2. (Optional) Wähle Modell und Kategorien:
 *        export VG_MODEL=claude-sonnet-4-6           # default
 *        export VG_CATEGORIES=ki-machine-learning    # comma-separated, default: all
 *
 *   3. Run:
 *        node tools/generate-posts.mjs
 *
 *   4. Nach dem Run wird sitemap.xml und feed.xml neu aufgebaut.
 *
 * Output:
 *   - Erstellt blog/<slug>.html mit BlogPosting + FAQ Schema
 *   - Erstellt assets/blog/post-<slug>.svg (Hero-Cover)
 *   - Aktualisiert blog/index.html, blog/feed.xml, sitemap.xml
 *
 * Lege diesen Script als Cron-Job an:
 *   0 6 * * *  cd /var/www/visiongo.at && node tools/generate-posts.mjs >> logs/blog.log 2>&1
 */

import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import process from 'node:process';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const SITE = 'https://visiongo.at';

// ============================================================
// 10 KATEGORIEN (gespiegelt aus build_blog.py)
// ============================================================
const CATEGORIES = [
  { slug: 'ki-machine-learning', name: 'KI & Machine Learning', color1: '#5B21B6', color2: '#1E0A3C', accent: '#A78BFA' },
  { slug: 'app-entwicklung', name: 'App-Entwicklung', color1: '#0F766E', color2: '#082F2A', accent: '#5EEAD4' },
  { slug: 'web-entwicklung', name: 'Web-Entwicklung', color1: '#1D4ED8', color2: '#0A1F4E', accent: '#93C5FD' },
  { slug: 'cloud-devops', name: 'Cloud & DevOps', color1: '#0369A1', color2: '#0A1F2E', accent: '#7DD3FC' },
  { slug: 'it-sicherheit', name: 'IT-Sicherheit & Datenschutz', color1: '#B91C1C', color2: '#3F0808', accent: '#FCA5A5' },
  { slug: 'open-source', name: 'Open Source', color1: '#15803D', color2: '#052E16', accent: '#86EFAC' },
  { slug: 'startup-produkt', name: 'Startup & Produkt', color1: '#C2410C', color2: '#43130C', accent: '#FDBA74' },
  { slug: 'industrie-iot', name: 'Industrie & IoT', color1: '#7C2D12', color2: '#1C0F08', accent: '#FDBA74' },
  { slug: 'fintech-krypto', name: 'Fintech & Krypto', color1: '#A16207', color2: '#2A1D04', accent: '#FDE68A' },
  { slug: 'design-ux', name: 'Design & UX', color1: '#86198F', color2: '#280B33', accent: '#F0ABFC' },
];

// ============================================================
// PROMPT — gibt JSON zurück mit allen Feldern für eine Post-Seite
// ============================================================
const PROMPT_TEMPLATE = (categoryName, today) => `Du schreibst einen technischen Blog-Artikel auf Deutsch für ein Wiener Software-Studio (Vision GO).

KATEGORIE: ${categoryName}
DATUM: ${today}

VORGABEN:
- Aktuelle, originelle Inhalte. Keine generischen "10 Tipps"-Listen, keine Marketing-Phrasen.
- Schreibstil: nüchtern, ehrlich, Studio-Werkstatt-Perspektive. Wir sind Praktiker — wir schreiben, was wir messen können.
- Länge: 700-1000 Wörter im body.
- DACH-Kontext bevorzugt (Österreich, Deutschland, Schweiz). DSGVO, EU-Hosting, lokale Anbieter.
- Konkrete Zahlen, Tools, Bibliotheken. Keine Allgemeinplätze.
- 3 FAQ-Einträge am Ende.

LIEFERE NUR JSON, keinen anderen Text:

{
  "slug": "kurz-deutsch-kebab-case-25-zeichen-max",
  "title": "Klarer SEO-Titel, max 75 Zeichen",
  "subtitle": "1-Satz-Lead, max 140 Zeichen",
  "description": "Meta description, 150-160 Zeichen, deutsch",
  "keywords": "kommagetrennte, deutsche, suchbegriffe",
  "read_min": 6,
  "tags": ["Tag1", "Tag2", "Tag3", "Tag4"],
  "body": [
    ["h2", "Erste Überschrift"],
    ["p", "Erster Absatz mit <strong>Hervorhebungen</strong> und konkreten Zahlen."],
    ["p", "Weiterer Absatz."],
    ["h2", "Zweite Überschrift"],
    ["p", "..."],
    ["ul", ["Punkt 1 mit <strong>Detail</strong>", "Punkt 2", "Punkt 3"]],
    ["h2", "Dritte Überschrift"],
    ["p", "..."],
    ["blockquote", "Ein griffiges, zitierwürdiges Zitat."],
    ["p", "Schluss-Absatz mit Empfehlung."]
  ],
  "faq": [
    ["Frage 1?", "Klare Antwort, 1-2 Sätze."],
    ["Frage 2?", "Klare Antwort."],
    ["Frage 3?", "Klare Antwort."]
  ]
}

WICHTIG: Verwende deutsche „doppelte Anführungszeichen" (U+201E und U+201D), keine ASCII-Anführungszeichen innerhalb der Texte.`;

// ============================================================
// API CALLS
// ============================================================
async function callAnthropic(prompt, model = 'claude-sonnet-4-6') {
  const key = process.env.ANTHROPIC_API_KEY;
  if (!key) throw new Error('ANTHROPIC_API_KEY nicht gesetzt');

  const res = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': key,
      'anthropic-version': '2023-06-01',
    },
    body: JSON.stringify({
      model,
      max_tokens: 4000,
      messages: [{ role: 'user', content: prompt }],
    }),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Anthropic ${res.status}: ${text}`);
  }
  const data = await res.json();
  return data.content[0].text;
}

async function callOpenAI(prompt, model = 'gpt-4o-mini') {
  const key = process.env.OPENAI_API_KEY;
  if (!key) throw new Error('OPENAI_API_KEY nicht gesetzt');

  const res = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${key}`,
    },
    body: JSON.stringify({
      model,
      max_tokens: 4000,
      messages: [{ role: 'user', content: prompt }],
      response_format: { type: 'json_object' },
    }),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`OpenAI ${res.status}: ${text}`);
  }
  const data = await res.json();
  return data.choices[0].message.content;
}

async function generatePost(category, today) {
  const prompt = PROMPT_TEMPLATE(category.name, today);

  let raw;
  if (process.env.ANTHROPIC_API_KEY) {
    console.log(`  → Anthropic für "${category.name}"`);
    raw = await callAnthropic(prompt, process.env.VG_MODEL || 'claude-sonnet-4-6');
  } else if (process.env.OPENAI_API_KEY) {
    console.log(`  → OpenAI für "${category.name}"`);
    raw = await callOpenAI(prompt, process.env.VG_MODEL || 'gpt-4o-mini');
  } else {
    throw new Error('Keine API-Keys gesetzt (ANTHROPIC_API_KEY oder OPENAI_API_KEY)');
  }

  // Extract JSON from possibly fenced response
  const jsonMatch = raw.match(/\{[\s\S]*\}/);
  if (!jsonMatch) throw new Error('Kein JSON in API-Antwort gefunden');
  return JSON.parse(jsonMatch[0]);
}

// ============================================================
// RENDERERS (gespiegelt aus build_blog.py)
// ============================================================
function esc(s) {
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function fmtDate(iso) {
  const months = ['Januar','Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember'];
  const d = new Date(iso);
  return `${d.getDate()}. ${months[d.getMonth()]} ${d.getFullYear()}`;
}

function renderBody(blocks) {
  return blocks.map(([kind, val]) => {
    if (kind === 'h2') return `        <h2>${val}</h2>`;
    if (kind === 'h3') return `        <h3>${val}</h3>`;
    if (kind === 'p') return `        <p>${val}</p>`;
    if (kind === 'blockquote') return `        <blockquote>„${val}"</blockquote>`;
    if (kind === 'ul') return `        <ul>\n${val.map(x => `          <li>${x}</li>`).join('\n')}\n        </ul>`;
    if (kind === 'ol') return `        <ol>\n${val.map(x => `          <li>${x}</li>`).join('\n')}\n        </ol>`;
    return '';
  }).join('\n');
}

function postCoverSvg(post, cat) {
  const title = post.title;
  const words = title.split(' ');
  let lines = [];
  let current = '';
  for (const w of words) {
    if ((current + ' ' + w).length > 30) {
      lines.push(current.trim());
      current = w;
    } else current = (current + ' ' + w).trim();
  }
  if (current) lines.push(current);
  lines = lines.slice(0, 3);

  const tspans = lines.map((line, i) => `<tspan x="80" dy="${i === 0 ? 0 : 80}">${esc(line)}</tspan>`).join('');

  return `<svg viewBox="0 0 1200 675" xmlns="http://www.w3.org/2000/svg" fill="none">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="${cat.color2}"/>
      <stop offset="1" stop-color="${cat.color1}"/>
    </linearGradient>
    <radialGradient id="glow" cx="0.85" cy="0.3" r="0.55">
      <stop offset="0" stop-color="${cat.accent}" stop-opacity="0.30"/>
      <stop offset="1" stop-color="${cat.accent}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="1200" height="675" fill="url(#g)"/>
  <rect width="1200" height="675" fill="url(#glow)"/>
  <text x="80" y="90" font-family="Inter" font-size="14" fill="${cat.accent}" letter-spacing="3" font-weight="600">${esc(cat.name.toUpperCase())}</text>
  <text y="240" font-family="Inter" font-size="64" font-weight="600" fill="#fff" letter-spacing="-2">${tspans}</text>
  <text x="80" y="595" font-family="JetBrains Mono" font-size="12" fill="rgba(255,255,255,0.55)" letter-spacing="2">VISION GO · ${post.date.split('-').reverse().join('.')} · ${post.read_min} MIN</text>
  <g transform="translate(1050, 70)">
    <path d="M0 0 L10 18 L14 11" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/>
    <path d="M28 0 L18 18 L14 11" stroke="${cat.accent}" stroke-width="2.4" stroke-linecap="round"/>
  </g>
  <text x="1095" y="80" font-family="Inter" font-size="14" fill="rgba(255,255,255,0.7)">Vision GO</text>
</svg>`;
}

function navFrag() {
  return `<header class="nav">
  <div class="container nav__inner">
    <a href="/" class="nav__brand"><span class="nav__brand-mark"><img src="/assets/logo.svg" alt=""/></span><span>Vision&nbsp;GO</span></a>
    <nav class="nav__links">
      <a class="nav__link" href="/">Studio</a>
      <a class="nav__link" href="/leistungen.html">Leistungen</a>
      <a class="nav__link" href="/projekte.html">Arbeiten</a>
      <a class="nav__link" href="/ueber-uns.html">Über</a>
      <a class="nav__link" href="/karriere.html">Karriere</a>
      <a class="nav__link" href="/kontakt.html">Kontakt</a>
    </nav>
    <a href="/kontakt.html" class="nav__cta"><span class="nav__cta-dot"></span>Projekt starten</a>
    <button class="nav__toggle" aria-label="Menü"><span></span><span></span></button>
  </div>
</header>`;
}

const FOOTER = `<footer class="footer">
  <div class="container">
    <div class="footer__top">
      <div class="footer__grid">
        <div class="footer__brand">
          <div class="footer__brand-mark">Vision GO</div>
          <div class="footer__brand-desc">Ihr Partner für digitale Transformation und innovative IT-Lösungen.</div>
          <address class="footer__brand-address">Vision GO GmbH<br/>Bäckerstraße 7/7<br/>1010 Wien · Österreich<br/><br/>Tel: <a href="tel:+436766440122" style="color:var(--ink-soft)">+43 676 6440122</a><br/><a href="mailto:info@visiongo.at" style="color:var(--ink-soft)">info@visiongo.at</a></address>
        </div>
        <div class="footer__col"><h4>Studio</h4><ul><li><a href="/leistungen.html">Leistungen</a></li><li><a href="/projekte.html">Arbeiten</a></li><li><a href="/ueber-uns.html">Über uns</a></li><li><a href="/karriere.html">Karriere</a></li><li><a href="/kontakt.html">Kontakt</a></li></ul></div>
        <div class="footer__col"><h4>Apps</h4><ul><li><a href="/projekte/megaradio.html">MegaRadio</a></li><li><a href="/projekte/scanup.html">ScanUp</a></li><li><a href="/projekte/esimfo.html">eSIMfo</a></li><li><a href="/projekte/taxihub.html">TaxiHub</a></li><li><a href="/projekte/snake-online.html">Online Snake</a></li></ul></div>
        <div class="footer__col"><h4>Lesen</h4><ul><li><a href="/blog/">Blog</a></li><li><a href="/blog/feed.xml">RSS</a></li></ul></div>
      </div>
    </div>
    <div class="footer__bottom">
      <span>© <span data-year>2026</span> Vision GO GmbH · FN 644224p · Handelsgericht Wien</span>
      <nav class="footer__legal"><a href="/impressum.html">Impressum</a><a href="/datenschutz.html">Datenschutz</a><a href="/sitemap.xml">Sitemap</a></nav>
    </div>
  </div>
</footer>

<script src="/assets/script.js" defer></script>`;

const ORG_LD = `<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://visiongo.at/#organization",
  "name": "Vision GO GmbH",
  "url": "https://visiongo.at/",
  "logo": "https://visiongo.at/assets/logo.svg",
  "address": { "@type": "PostalAddress", "streetAddress": "Bäckerstraße 7/7", "addressLocality": "Wien", "postalCode": "1010", "addressCountry": "AT" },
  "employee": [ { "@type": "Person", "name": "Muhammed Fatih Geyik", "jobTitle": "Head of IT" } ]
}
</script>`;

function renderPostPage(post, cat) {
  const url = `${SITE}/blog/${post.slug}.html`;
  const coverUrl = `${SITE}/assets/blog/post-${post.slug}.svg`;

  const blogPostLd = {
    '@context': 'https://schema.org',
    '@type': 'BlogPosting',
    '@id': url + '#article',
    headline: post.title,
    alternativeHeadline: post.subtitle,
    description: post.description,
    datePublished: post.date,
    dateModified: post.date,
    author: { '@id': 'https://visiongo.at/#organization' },
    publisher: { '@id': 'https://visiongo.at/#organization' },
    mainEntityOfPage: url,
    image: coverUrl,
    inLanguage: 'de-AT',
    articleSection: cat.name,
    keywords: post.tags.join(', '),
    timeRequired: `PT${post.read_min}M`,
    url,
  };

  const breadcrumbLd = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'Studio', item: SITE + '/' },
      { '@type': 'ListItem', position: 2, name: 'Blog', item: SITE + '/blog/' },
      { '@type': 'ListItem', position: 3, name: cat.name, item: `${SITE}/blog/kategorie/${cat.slug}.html` },
      { '@type': 'ListItem', position: 4, name: post.title, item: url },
    ],
  };

  let faqLd = '';
  if (post.faq && post.faq.length) {
    const faqEnt = post.faq.map(([q, a]) => ({ '@type': 'Question', name: q, acceptedAnswer: { '@type': 'Answer', text: a } }));
    faqLd = `<script type="application/ld+json">\n${JSON.stringify({ '@context': 'https://schema.org', '@type': 'FAQPage', mainEntity: faqEnt }, null, 2)}\n</script>`;
  }

  const faqHtml = post.faq && post.faq.length
    ? `
  <section class="faq-list">
    <div class="article-body" style="padding-top:0; padding-bottom:0;">
      <h3>Häufig gefragt</h3>
${post.faq.map(([q, a]) => `      <details>\n        <summary>${q}</summary>\n        <p>${a}</p>\n      </details>`).join('\n')}
    </div>
  </section>`
    : '';

  const tagsHtml = post.tags.map(t => `<span class="tag">${t}</span>`).join('');

  return `<!DOCTYPE html>
<html lang="de-AT">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>${post.title} · Vision GO Blog</title>
<meta name="description" content="${esc(post.description)}" />
<meta name="keywords" content="${esc(post.keywords)}" />
<meta name="author" content="Vision GO GmbH" />
<meta name="robots" content="index, follow, max-image-preview:large" />
<meta name="theme-color" content="${cat.color2}" />
<link rel="canonical" href="${url}" />
<meta property="og:type" content="article" />
<meta property="og:locale" content="de_AT" />
<meta property="og:site_name" content="Vision GO Blog" />
<meta property="og:url" content="${url}" />
<meta property="og:title" content="${esc(post.title)}" />
<meta property="og:description" content="${esc(post.description)}" />
<meta property="og:image" content="${coverUrl}" />
<meta property="article:published_time" content="${post.date}T09:00:00+02:00" />
<meta property="article:section" content="${cat.name}" />
${post.tags.map(t => `<meta property="article:tag" content="${t}" />`).join('\n')}
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="${esc(post.title)}" />
<meta name="twitter:description" content="${esc(post.description)}" />
<meta name="twitter:image" content="${coverUrl}" />
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg" />
<link rel="alternate" type="application/rss+xml" title="Vision GO Blog" href="/blog/feed.xml" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Fraunces:wght@400;500;600&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="/assets/styles.css" />
${ORG_LD}
<script type="application/ld+json">
${JSON.stringify(blogPostLd, null, 2)}
</script>
<script type="application/ld+json">
${JSON.stringify(breadcrumbLd, null, 2)}
</script>
${faqLd}
</head>
<body>
${navFrag()}
<main>
  <section class="article-hero">
    <div class="container container--tight">
      <p class="breadcrumb"><a href="/">Studio</a><span class="breadcrumb__sep">/</span><a href="/blog/">Blog</a><span class="breadcrumb__sep">/</span><a href="/blog/kategorie/${cat.slug}.html">${cat.name}</a></p>
      <div class="article-hero__meta">
        <span class="article-hero__cat">${cat.name}</span>
        <span>·</span>
        <time datetime="${post.date}">${fmtDate(post.date)}</time>
        <span>·</span>
        <span>${post.read_min} Min Lesezeit</span>
      </div>
      <h1 class="article-hero__title">${post.title}</h1>
      <p class="article-hero__sub">${post.subtitle}</p>
    </div>
    <div class="container container--tight">
      <div class="article-cover">
        <img src="/assets/blog/post-${post.slug}.svg" alt="${esc(post.title)}"/>
      </div>
    </div>
  </section>
  <article class="article-body">
${renderBody(post.body)}
    <div class="author-card">
      <div class="author-card__avatar">VG</div>
      <div>
        <div class="author-card__name">Vision GO Engineering</div>
        <div class="author-card__role">Software-Studio · Wien · Seit 2015</div>
      </div>
    </div>
  </article>
${faqHtml}
  <div class="article-footer">
    <div class="article-tags">${tagsHtml}</div>
  </div>
</main>
${FOOTER}
</body>
</html>
`;
}

// ============================================================
// MAIN
// ============================================================
async function main() {
  const today = new Date().toISOString().slice(0, 10);

  // Filter categories
  const selected = process.env.VG_CATEGORIES
    ? process.env.VG_CATEGORIES.split(',').map(s => s.trim())
    : CATEGORIES.map(c => c.slug);

  const cats = CATEGORIES.filter(c => selected.includes(c.slug));

  console.log(`\nVision GO Blog Generator · ${today}`);
  console.log(`Kategorien: ${cats.map(c => c.name).join(', ')}\n`);

  const created = [];

  for (const cat of cats) {
    try {
      const post = await generatePost(cat, today);
      post.date = today;
      post.category = cat.slug;

      // Write post HTML
      const html = renderPostPage(post, cat);
      const htmlPath = path.join(ROOT, 'blog', `${post.slug}.html`);
      await fs.writeFile(htmlPath, html, 'utf-8');

      // Write cover SVG
      const svg = postCoverSvg(post, cat);
      const svgPath = path.join(ROOT, 'assets', 'blog', `post-${post.slug}.svg`);
      await fs.writeFile(svgPath, svg, 'utf-8');

      console.log(`  ✓ ${post.slug}`);
      created.push({ post, cat });
    } catch (err) {
      console.error(`  ✗ ${cat.name}: ${err.message}`);
    }
  }

  // Rebuild blog index & feed (skipped here for brevity — call build_blog.py rebuilds)
  console.log(`\n${created.length} neue Artikel erstellt.`);
  console.log('Hinweis: blog/index.html und sitemap.xml manuell rebuilden mit:');
  console.log('  python3 tools/rebuild_index.py');
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
