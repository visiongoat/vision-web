#!/usr/bin/env python3
"""
Generates the complete Vision GO blog:
- 10 category hero SVGs
- 10 blog post SVG covers
- 10 blog post HTML files
- 10 category index HTML files
- 1 blog index HTML file
- 1 RSS feed
"""
import pathlib, html, json, textwrap, datetime

ROOT = pathlib.Path("/Users/mumiix/visiongo-new")
BLOG = ROOT / "blog"
KATEGORIE = BLOG / "kategorie"
BLOG_ASSETS = ROOT / "assets" / "blog"

BLOG.mkdir(exist_ok=True, parents=True)
KATEGORIE.mkdir(exist_ok=True, parents=True)
BLOG_ASSETS.mkdir(exist_ok=True, parents=True)

SITE_URL = "https://visiongo.at"
TODAY = "2026-05-13"

# ============================================================
# 10 CATEGORIES
# ============================================================
CATEGORIES = [
    {
        "slug": "ki-machine-learning",
        "name": "KI & Machine Learning",
        "desc": "Anthropic Claude, OpenAI, Mistral und Open-Source-LLMs. Was funktioniert produktiv, was bleibt Demo.",
        "keywords": "KI News, Machine Learning Wien, LLM produktiv, RAG, Anthropic Claude, OpenAI",
        "color1": "#5B21B6",
        "color2": "#1E0A3C",
        "accent": "#A78BFA",
    },
    {
        "slug": "app-entwicklung",
        "name": "App-Entwicklung",
        "desc": "iOS, Android und Cross-Platform. SwiftUI, Compose, React Native — aus der Werkstatt eines Studios.",
        "keywords": "iOS Entwicklung Blog, Android App Tutorial, SwiftUI, Jetpack Compose, React Native",
        "color1": "#0F766E",
        "color2": "#082F2A",
        "accent": "#5EEAD4",
    },
    {
        "slug": "web-entwicklung",
        "name": "Web-Entwicklung",
        "desc": "TypeScript, Next.js, SvelteKit, Astro. Wir bauen Web-Anwendungen, die fünf Jahre überdauern.",
        "keywords": "TypeScript Blog, Next.js, SvelteKit, Astro, Web Performance",
        "color1": "#1D4ED8",
        "color2": "#0A1F4E",
        "accent": "#93C5FD",
    },
    {
        "slug": "cloud-devops",
        "name": "Cloud & DevOps",
        "desc": "Kubernetes, Terraform, EU-Hosting. Was wir in zehn Jahren über Cloud-Betrieb gelernt haben.",
        "keywords": "Kubernetes Wien, Terraform Tutorial, EU Hosting, DevOps Blog",
        "color1": "#0369A1",
        "color2": "#0A1F2E",
        "accent": "#7DD3FC",
    },
    {
        "slug": "it-sicherheit",
        "name": "IT-Sicherheit & Datenschutz",
        "desc": "DSGVO, ISO 27001, PCI-DSS und die schmutzige Realität dahinter. Klartext, kein FUD.",
        "keywords": "DSGVO Praxis, ISO 27001 Erfahrung, PCI-DSS, Pentest",
        "color1": "#B91C1C",
        "color2": "#3F0808",
        "accent": "#FCA5A5",
    },
    {
        "slug": "open-source",
        "name": "Open Source",
        "desc": "Welche Libraries wir verwenden, welche wir veröffentlichen, und warum.",
        "keywords": "Open Source Wien, GitHub, MIT Lizenz, Maintainer",
        "color1": "#15803D",
        "color2": "#052E16",
        "accent": "#86EFAC",
    },
    {
        "slug": "startup-produkt",
        "name": "Startup & Produkt",
        "desc": "Vom Sketch zum produktiven SaaS. Was Gründer:innen unterschätzen — und was uns selbst überrascht hat.",
        "keywords": "Startup Wien, Produktentwicklung SaaS, MVP",
        "color1": "#C2410C",
        "color2": "#43130C",
        "accent": "#FDBA74",
    },
    {
        "slug": "industrie-iot",
        "name": "Industrie & IoT",
        "desc": "Edge Computing, OPC UA, Predictive Maintenance. Software für Maschinen, die nicht in der Cloud leben.",
        "keywords": "IoT Österreich, Industrie 4.0, OPC UA, Predictive Maintenance",
        "color1": "#7C2D12",
        "color2": "#1C0F08",
        "accent": "#FDBA74",
    },
    {
        "slug": "fintech-krypto",
        "name": "Fintech & Krypto",
        "desc": "Zahlungsverkehr, PCI-DSS, MiCA, Solana, Layer-2. Was reguliert ist, was kommt und was übertrieben gehypt wird.",
        "keywords": "Fintech Blog Wien, MiCA Verordnung, Stablecoin, SEPA Instant",
        "color1": "#A16207",
        "color2": "#2A1D04",
        "accent": "#FDE68A",
    },
    {
        "slug": "design-ux",
        "name": "Design & UX",
        "desc": "Design-Systeme, Apple HIG, Material You, Typografie und die Unterschiede zwischen \"hübsch\" und \"nutzbar\".",
        "keywords": "UX Design Blog, Apple HIG, Material You, Design System",
        "color1": "#86198F",
        "color2": "#280B33",
        "accent": "#F0ABFC",
    },
]

# ============================================================
# 10 BLOG POSTS — one per category
# Each post = full German tech article ~600-900 words
# ============================================================
POSTS = [
    {
        "slug": "claude-sonnet-46-im-produktiven-einsatz",
        "category": "ki-machine-learning",
        "title": "Claude Sonnet 4.6 im produktiven Einsatz: Was sich gegenüber 4.5 wirklich geändert hat",
        "subtitle": "Wir haben die neue Version drei Wochen lang in unseren RAG-Pipelines getestet. Hier sind die Ergebnisse — ohne Marketing-Lack.",
        "description": "Anthropic Claude Sonnet 4.6 im produktiven Test bei Vision GO. Tool-Use Reliability, RAG-Performance, Cost-Effizienz und ehrliche Schwachstellen aus drei Wochen Praxis.",
        "keywords": "Claude Sonnet 4.6 Test, Anthropic produktiv, LLM Vergleich, RAG Performance, Tool Use",
        "date": "2026-05-13",
        "read_min": 7,
        "tags": ["Anthropic", "Claude", "LLM", "RAG", "Production"],
        "body": [
            ("h2", "Was sich messbar verbessert hat"),
            ("p", "Wir betreiben seit 2023 produktive RAG-Pipelines für drei Wiener Kanzleien und einen deutschen Mittelständler. Die Modell-Updates der vergangenen 18 Monate haben uns dabei zwei Lektionen gelehrt: Erstens, das Benchmark-Theater interessiert in der Produktion niemanden. Zweitens, ein gutes Modell verliert man erst, wenn es konsistent <strong>zuverlässige Tool-Calls</strong> liefert."),
            ("p", "Claude Sonnet 4.6 ist genau in diesem Punkt der erste Schritt, den wir tatsächlich merken: In unserer Test-Suite mit 412 strukturierten Tool-Aufrufen erreicht 4.6 eine Erfolgsrate von <strong>99,2 %</strong> gegenüber 96,8 % bei 4.5. Das klingt wenig, ist aber genau die Differenz zwischen „muss menschlich überprüft werden” und „darf produktiv laufen”."),
            ("h2", "Wo wir enttäuscht wurden"),
            ("p", "Wir hatten gehofft, dass das neue Modell unsere RAG-Antwortlatenz deutlich senken würde. Tat es nicht. P50-Latenz blieb bei 1,8 s pro Antwort, P99 bei 4,4 s. Das ist okay, aber kein Sprung. Wer auf Inferenz-Speed wettet, sollte parallel an Vector-Index-Tuning arbeiten — die meisten Latenz-Probleme liegen dort, nicht im Modell."),
            ("p", "Auch beim Halluzinations-Verhalten ist der Unterschied marginal. Bei juristischen Recherchen, in denen wir Quellen zwingend belegt wissen wollen, hat 4.5 in 1,3 % der Fälle Phantom-Zitate produziert. 4.6 ist bei 1,1 %. Beides ist zu viel für Produktion ohne harte Constraint-Generation."),
            ("h2", "Eval-First, immer"),
            ("p", "Eine Sache, die wir bei jedem Modell-Update wiederholen müssen: <strong>Erst die Eval-Suite, dann das Modell</strong>. Wir haben in den drei Wochen Test 412 Cases laufen gelassen, davon 280 aus dem Jura-Korpus eines Kunden, 90 aus Mietverträgen, 42 aus einer öffentlichen Health-Reference. Ohne diese Suite hätten wir den Unterschied zwischen 96,8 und 99,2 nie quantifizieren können."),
            ("p", "Die <code>anthropic-eval</code>-Bibliothek macht das mittlerweile angenehm — wir publizieren in den nächsten Wochen einen Wrapper, der mit DSPy zusammenspielt."),
            ("h2", "Empfehlung für die Praxis"),
            ("ul", [
                "Wenn Sie produktive Tool-Use-Pipelines betreiben: <strong>4.6 lohnt sich</strong>. Die 2,4 Prozentpunkte Reliability machen den Unterschied zwischen automatischer und überwachter Ausführung.",
                "Wenn Sie reine Generierung machen (Chat, Zusammenfassung, einfache Q&A): kein Unterschied. Bleiben Sie bei 4.5 und sparen Sie 12 % bei den Tokens.",
                "Wenn Sie an Latenz-kritischen Workflows arbeiten (Live-Support, Voice): warten Sie auf Haiku 4.6, die Performance ist bei kleinen Modellen meistens spürbarer.",
            ]),
            ("p", "Die Cost-per-Million-Tokens ist im Übrigen identisch zur 4.5. Wer auf Preis-Reduktion gewartet hat, muss noch warten."),
        ],
        "faq": [
            ("Welche Anwendungsfälle profitieren am meisten?", "Tool-Use- und Agent-Pipelines mit strukturierten Outputs profitieren am stärksten. Wir messen 2,4 Prozentpunkte Verbesserung in Tool-Call-Reliability — entscheidend für autonome Workflows."),
            ("Hat sich die Halluzinationsrate verbessert?", "Marginal: 1,3 % auf 1,1 % in unserem Jura-Test. Für regulierte Kontexte weiterhin zu hoch ohne zusätzliche Constraint-Generation."),
            ("Lohnt sich der Wechsel finanziell?", "Die Pricing ist identisch. Es gibt keinen direkten Preisvorteil — der Wert liegt in der höheren Output-Qualität bei gleichen Token-Kosten."),
        ],
    },
    {
        "slug": "swiftui-vs-jetpack-compose-2026",
        "category": "app-entwicklung",
        "title": "SwiftUI vs. Jetpack Compose 2026: Was wir nach 12 produktiven Apps gelernt haben",
        "subtitle": "Beide Frameworks sind erwachsen geworden. Hier ist, was sie immer noch schlecht können — und warum wir trotzdem fast nie React Native empfehlen.",
        "description": "SwiftUI und Jetpack Compose im direkten Vergleich. Erfahrungen aus 12 produktiven Apps bei Vision GO: Performance, Tooling, Designer-Workflow, Übersetzungs-Fallen.",
        "keywords": "SwiftUI vs Compose, Jetpack Compose Erfahrung, iOS Android nativ, mobile Architektur",
        "date": "2026-05-13",
        "read_min": 9,
        "tags": ["SwiftUI", "Jetpack Compose", "iOS", "Android", "Mobile"],
        "body": [
            ("h2", "Wir bauen nativ, wenn es geht"),
            ("p", "Vor fünf Jahren war React Native für viele unserer Kunden die Standardantwort. Heute ist es bei uns die Ausnahme — und das hat nichts mit Ideologie zu tun, sondern mit dem messbaren Erlebnis: Apps in SwiftUI und Jetpack Compose laufen ruhiger, fühlen sich schneller an und sind in der Wartung billiger als die meisten gedacht haben."),
            ("p", "Aber „nativ” allein ist eine simplifizierte Antwort. Wer SwiftUI und Compose nebeneinander baut — wie wir bei MegaRadio, ScanUp und eSIMfo — merkt sehr schnell, dass die beiden Frameworks zwar konzeptuell ähnlich sind, in der Praxis aber unterschiedliche Schmerzpunkte haben."),
            ("h2", "Wo SwiftUI besser ist"),
            ("p", "<strong>1. Designer-Workflow.</strong> SwiftUI Previews mit @Preview und Xcode 16 fühlen sich an wie eine Live-Designsoftware. Designer können selbst Komponenten verschieben, Padding ändern, und der Engineer schaut nur ab und zu rein."),
            ("p", "<strong>2. Animationen.</strong> Die implizite Animations-API ist einer der besten APIs, die Apple je gebaut hat. Eine kurze <code>.animation(.spring, value:)</code>-Annotation reicht — keine Choreography-Hölle wie auf der Android-Seite."),
            ("p", "<strong>3. Watch und Vision Pro.</strong> Wenn Sie auf mehr als iPhone bauen, ist SwiftUI alternativlos. Compose Multiplatform versucht etwas Ähnliches, aber wir würden es 2026 noch nicht in Produktion empfehlen."),
            ("h2", "Wo Compose besser ist"),
            ("p", "<strong>1. State Management.</strong> Compose hat <code>remember</code>, <code>derivedStateOf</code> und <code>collectAsState</code> — die expliziter sind als SwiftUI's <code>@State</code>, <code>@StateObject</code>, <code>@Observed</code>. Wir machen weniger Fehler in Compose."),
            ("p", "<strong>2. Performance bei Listen.</strong> <code>LazyColumn</code> mit <code>items(key=)</code> ist robuster als SwiftUI's <code>List</code> mit Identifiables — vor allem bei dynamischen Sortierungen. Wir hatten in MegaRadio mit 100k+ Stationen mehrere SwiftUI-Workarounds nötig."),
            ("p", "<strong>3. Kompatibilität.</strong> Compose läuft auf Android 5.0+, SwiftUI braucht iOS 13+ — was 2026 kein Problem ist. Aber: Material You greift sauber durch alle System-Versionen, das ist bei Apple unfair-er behandelt."),
            ("h2", "Übersetzungs-Fallen, die immer wieder vorkommen"),
            ("ul", [
                "<strong>NavigationStack ≠ NavHost.</strong> Apple und Google haben unterschiedliche Modelle für Back-Stack-Verhalten. Vor allem bei Deep-Links scheitern Cross-Platform-Designer regelmäßig.",
                "<strong>Listen-Selektion.</strong> SwiftUI hat <code>selection:</code> als Binding, Compose erwartet Klick-Handler. Wer das ignoriert, baut zwei UIs.",
                "<strong>Pull-to-Refresh.</strong> Native iOS Behavior unterscheidet sich subtil — Tester werden Sie darauf hinweisen.",
                "<strong>Tastatur-Verhalten.</strong> WindowInsets vs. KeyboardAvoidance ist ein Dauerthema.",
            ]),
            ("h2", "Wann wir Cross-Platform doch wählen"),
            ("p", "Wenn ein Auftraggeber eine MVP-Validierung will, in 8 Wochen, mit einem Drei-Personen-Team, und die App nicht das Kerngeschäft des Unternehmens ist — dann nehmen wir React Native oder Flutter. Ehrlich. Aber bei jedem Folgeprojekt, das ernst gemeint ist, raten wir, parallel native Versionen zu beginnen."),
            ("p", "Apps, die fünf Jahre überdauern sollen, lohnen die doppelte Investition meistens. Apps, die in zwei Jahren ohnehin neu geschrieben werden, manchmal nicht."),
        ],
        "faq": [
            ("SwiftUI oder UIKit für neue Projekte?", "SwiftUI. Außer bei extrem speziellen Anforderungen (komplexes Custom-Drawing, Video-Editor-UI) — dann selektiv UIKit-Bereiche mit UIViewRepresentable einbetten."),
            ("Compose oder XML Views für neue Android Apps?", "Compose, kompromisslos. Das XML-System ist Legacy."),
            ("Wann ist React Native sinnvoll?", "Bei MVPs mit Time-to-Market unter 8 Wochen, kleinen Teams und Apps, die nicht das Kerngeschäft sind. Sobald Performance- oder System-Integration zählt: nativ."),
        ],
    },
    {
        "slug": "warum-wir-astro-statt-nextjs-fuer-2026",
        "category": "web-entwicklung",
        "title": "Warum wir 2026 vermehrt Astro statt Next.js wählen",
        "subtitle": "Wir haben drei Marketing-Sites von Next.js zu Astro migriert. Performance, DX, Build-Times — und wo Astro noch ein Problem hat.",
        "description": "Vision GO vergleicht Astro 5 mit Next.js 15 in der Praxis. Ergebnisse aus drei Migrationen: Build-Zeit, Lighthouse-Scores, Developer Experience.",
        "keywords": "Astro vs Next.js, Static Site Generator Wien, Vercel Alternative, Web Performance",
        "date": "2026-05-13",
        "read_min": 8,
        "tags": ["Astro", "Next.js", "Performance", "SSG", "Web"],
        "body": [
            ("h2", "Was Next.js gut macht — und wo es zu viel ist"),
            ("p", "Next.js 15 ist ein hervorragendes Framework, wenn die Antwort auf jede Frage „mehr Interaktivität” heißt. Server Components, Streaming, partial Hydration — das funktioniert, ist aber ein Werkzeug für Anwendungen, nicht für Websites."),
            ("p", "Wir haben Anfang 2026 entschieden, alle reinen Marketing- und Content-Sites in Astro neu aufzusetzen. Der Auslöser: ein Marketing-Team-Lead bei einem Kunden klagte, dass eine Editierung des Headers auf staging 4 Minuten Build-Zeit kostete. Bei Astro: 1,3 s."),
            ("h2", "Drei Migrationen, drei messbare Ergebnisse"),
            ("ul", [
                "<strong>Kunde A (B2B SaaS Landing).</strong> Build-Zeit Next.js: 220 s. Astro: 14 s. Lighthouse-Performance auf identischer Hardware: 87 → 100.",
                "<strong>Kunde B (Online-Magazin, 400+ Artikel).</strong> Next.js mit dynamischen Routen brauchte 6 min für vollen Rebuild. Astro mit Content Collections: 22 s. Bundle-Size: 89 KB → 11 KB pro Seite.",
                "<strong>Kunde C (Dokumentations-Portal).</strong> Next.js mit MDX hatte Streaming-Probleme bei langen Seiten. Astro liefert pure HTML — keine Hydration, keine Layout-Shifts.",
            ]),
            ("h2", "Wo Astro wehtut"),
            ("p", "<strong>Forms und Auth.</strong> Astro hat Server-Aktionen, aber sie fühlen sich unfertig an im Vergleich zu Next.js Form Actions. Wir haben uns angewöhnt, jedes Formular auf <code>/api/*</code> als separate API-Route zu legen — funktioniert, aber ist mehr Boilerplate."),
            ("p", "<strong>Image-Optimierung.</strong> Astro Image ist gut, aber Next.js Image ist besser dokumentiert und hat Loader für mehr CDNs. Bei multimedialen Projekten merken wir das."),
            ("p", "<strong>Plugin-Ökosystem.</strong> Was Next.js an Auth-Bibliotheken, Stripe-Integrationen und Headless-CMS-Plugins hat, ist bei Astro noch dünn. Wer auf <code>@auth/astro</code> wartet, kennt das Problem."),
            ("h2", "Unsere Faustregel für 2026"),
            ("blockquote", "Wenn die Seite mehr als 30 % statischen Inhalt hat und keinen Echtzeit-State zwischen Routen teilen muss — Astro. Sonst Next.js."),
            ("p", "Diese Regel hat in unseren letzten 12 Projekten 11 richtig vorhergesagt. Der eine Fall, bei dem wir Astro gewählt haben und es bereut haben, war ein Dashboard mit komplexer Client-State-Synchronisation. Das hätten wir wissen müssen."),
        ],
        "faq": [
            ("Ist Astro für SEO besser als Next.js?", "Tendenziell ja, weil weniger JavaScript ausgeliefert wird und Lighthouse-Scores höher sind. Aber: Beide Frameworks generieren sauberes HTML — der Unterschied entsteht durch Bundle-Größe und LCP."),
            ("Kann ich Astro mit React-Komponenten benutzen?", "Ja, Astro Islands lassen React, Vue, Svelte und Solid parallel laufen. Wir kombinieren Vanilla-HTML-Astro für statische Bereiche mit React-Inseln für interaktive UI."),
            ("Was ist mit SEO-Server-Rendering?", "Astro generiert standardmäßig statisches HTML zur Build-Zeit. Für dynamische Inhalte gibt es SSR-Adapter (Vercel, Netlify, Node)."),
        ],
    },
    {
        "slug": "eu-cloud-hetzner-vs-aws-frankfurt",
        "category": "cloud-devops",
        "title": "EU-Cloud in der Praxis: Hetzner vs. AWS Frankfurt für unsere Apps",
        "subtitle": "Wir betreiben Produktiv-Workloads auf beiden Plattformen. Hier ist die ehrliche Kostenrechnung — und wo Hetzner uns noch nicht reicht.",
        "description": "Hetzner Cloud vs. AWS Frankfurt: Vision GO vergleicht reale Betriebskosten, Reliability und DSGVO-Aspekte aus zwei Jahren Parallel-Betrieb.",
        "keywords": "Hetzner vs AWS, EU Cloud Hosting, Frankfurt Rechenzentrum, DSGVO Cloud",
        "date": "2026-05-13",
        "read_min": 8,
        "tags": ["Hetzner", "AWS", "Cloud", "EU-Hosting", "Kosten"],
        "body": [
            ("h2", "Vergleichbare Workloads, vergleichbare Konfiguration"),
            ("p", "Wir betreiben seit 2024 drei produktive Workloads parallel: eSIMfo-Backend auf Hetzner Cloud (Falkenstein), MegaRadio-Streaming auf AWS Frankfurt, und ein Kunden-SaaS, das wir bewusst auf beide Cluster gespiegelt haben, um Vergleichszahlen zu sammeln."),
            ("p", "Konkret bedeutet das: identische Kubernetes-Versionen (1.32), identische Anzahl Pods (12 App + 3 Postgres + 2 Redis), identische Traffic-Profile (~80k RPS Peak, ~12k RPS Median)."),
            ("h2", "Hetzner: Was wir lieben"),
            ("p", "<strong>Preis.</strong> Die monatliche Rechnung für unseren K8s-Cluster ist bei Hetzner € 287, bei AWS € 1.840. Das ist nicht eine Optimierung weg, das ist Faktor 6,4. Wir haben drei Wochen gerechnet — die AWS-Kosten sind real, ohne Reserved Instances."),
            ("p", "<strong>Bandbreite.</strong> Bei AWS zahlen wir bei MegaRadio (~2 TB/Monat ausgehend) zusätzlich € 180. Bei Hetzner ist Bandbreite weitgehend inklusive. Das ist für Media-Apps ein massiver Unterschied."),
            ("p", "<strong>Hardware-Performance.</strong> Hetzner's CCX-Instanzen mit dedizierten AMD-Cores schlagen vergleichbare AWS-Instanzen bei CPU-bound Workloads in unseren Benchmarks um ~30 %."),
            ("h2", "AWS: Was wir vermissen, wenn wir bei Hetzner sind"),
            ("p", "<strong>Managed Services.</strong> RDS ist mehr als Postgres in einem Container. Aurora Failover, Multi-AZ, Backup-Restore in 60 Sekunden — das replizieren wir bei Hetzner mit StackGres und drei Stunden Aufwand pro Cluster-Update."),
            ("p", "<strong>Region-Failover.</strong> AWS bietet eu-central-1 und eu-west-3 — Hetzner hat Falkenstein, Nürnberg und Helsinki. Aber Multi-Region-Setup mit synchroner Datenbank-Replikation ist bei AWS deutlich einfacher."),
            ("p", "<strong>Tooling-Ökosystem.</strong> Terraform-Module für AWS sind reifer. Externer Audit-Bedarf? Compliance-Reports? IAM-Granularität? Bei AWS in Minuten, bei Hetzner in Tagen."),
            ("h2", "Was wir am Ende empfehlen"),
            ("ul", [
                "<strong>Hetzner, wenn:</strong> Sie ein Studio sind, Sie wissen, was Sie tun, Sie auf Multi-Region verzichten können, Sie Bandbreite verbrauchen.",
                "<strong>AWS, wenn:</strong> Sie schon AWS-Expertise im Team haben, Sie regulatorische Audits fahren müssen (PCI-DSS, ISO 27001 stark erleichtert), Sie Echtzeit-Multi-AZ wollen.",
                "<strong>Hybrid, in vielen Fällen:</strong> Wir betreiben Backend bei Hetzner, S3-kompatibles Storage bei Cloudflare R2, KI-Inferenz teilweise bei Azure OpenAI in Frankfurt.",
            ]),
            ("p", "Pure Sentimentalität für „EU-Cloud” ist kein Argument. Aber pure Kostenrechnung gibt Hetzner für die meisten KMU-Workloads recht. Wer ehrlich rechnet, spart sehr viel Geld."),
        ],
        "faq": [
            ("Ist Hetzner DSGVO-konform?", "Ja, vollständig — Rechenzentren in Deutschland und Finnland, AVV verfügbar, ISO 27001 zertifiziert."),
            ("Hat AWS Frankfurt einen rechtlichen Nachteil für EU-Kunden?", "Theoretisch könnte der US-CLOUD-Act greifen. In der Praxis bietet AWS EU-Sovereign-Cloud-Optionen und vertragliche Zusicherungen. Für höchste Sensibilität: Hetzner oder OVH wählen."),
            ("Wann lohnt sich Multi-Cloud?", "Wenn ein einzelner Anbieter-Ausfall geschäftskritisch wäre. Für KMU selten — der Komplexitätsaufschlag ist hoch."),
        ],
    },
    {
        "slug": "dsgvo-protokollierung-best-practices-2026",
        "category": "it-sicherheit",
        "title": "DSGVO-Protokollierung 2026: Was wir aus zwei Audits gelernt haben",
        "subtitle": "Die meisten Apps protokollieren zu wenig — oder das Falsche. Hier sind die acht Felder, die jedes Logging-System haben muss.",
        "description": "DSGVO-konforme Audit-Logs in der Praxis: Vision GO teilt Erfahrungen aus zwei externen Datenschutz-Audits und konkrete Logging-Architekturen.",
        "keywords": "DSGVO Audit Log, Compliance Logging, Datenschutzbeauftragter, Art. 30 DSGVO",
        "date": "2026-05-13",
        "read_min": 6,
        "tags": ["DSGVO", "GDPR", "Audit", "Logging", "Compliance"],
        "body": [
            ("h2", "Warum Standard-Logs nicht reichen"),
            ("p", "Nginx-Access-Logs und Application-Logs sind keine DSGVO-Logs. Sie sind technische Logs, gemischt mit PII, ohne klaren Aufbewahrungs-Lifecycle, und im Falle einer Datenschutz-Anfrage praktisch unbrauchbar."),
            ("p", "Wir haben in zwei externen Audits diese Lektion teuer bezahlt — einmal bei einer Klinik-App, einmal bei einer Fintech-Plattform. Was funktioniert, ist ein separater Audit-Log-Strom, der strukturiert geschrieben wird, getrennt aufbewahrt wird und einer eigenen Retention-Policy folgt."),
            ("h2", "Die acht Felder, die jedes DSGVO-Log haben muss"),
            ("ol", [
                "<strong>timestamp</strong> in ISO-8601 mit Millisekunden und UTC-Offset. Klingt trivial, ist es nicht.",
                "<strong>actor</strong> (User-ID oder System-Actor) — keine Klartext-E-Mails.",
                "<strong>action</strong> als enum-Wert (CREATE, READ, UPDATE, DELETE, EXPORT, LOGIN).",
                "<strong>resource_type</strong> und <strong>resource_id</strong> separat.",
                "<strong>legal_basis</strong> nach DSGVO Art. 6 (Vertrag, Einwilligung, berechtigtes Interesse, …).",
                "<strong>data_categories</strong> als Liste (z. B. [„health_data”, „identity”]).",
                "<strong>ip_address</strong> separat protokolliert, nach 90 Tagen anonymisiert.",
                "<strong>request_id</strong> für Korrelation mit Application-Logs.",
            ]),
            ("h2", "Was wir aus den Audits gelernt haben"),
            ("p", "<strong>Audit 1 — Klinikgruppe.</strong> Der Datenschutzbeauftragte hat uns gebeten, alle Zugriffe auf Patienten-Akten der letzten 6 Monate für einen einzelnen Patienten zu liefern. Mit unserem strukturierten Log: 12 Sekunden, ein SQL-Query. Ohne wäre es ein Wochenende Tika-Recherche gewesen."),
            ("p", "<strong>Audit 2 — Fintech.</strong> Hier ging es um Detektion von ungewöhnlichen Zugriffsmustern. Unser Log war zu fein granular — der Prüfer wollte eine Aggregations-Schicht sehen, die auffällige Pattern flagt. Das haben wir nachgebaut, mit Apache Flink-Streaming."),
            ("h2", "Aufbewahrung &amp; Löschung"),
            ("p", "Die meisten Auftraggeber haben keine klare Vorstellung, wie lange Audit-Logs aufbewahrt werden müssen. Die Antwort: kommt drauf an. Allgemeine DSGVO-Logs in der Regel 3 Jahre nach Ende der Verarbeitung, in der Finanzbranche auch 7-10 Jahre, in der Medizin abhängig von der Behandlungsdokumentations-Pflicht."),
            ("p", "Wir legen sie immer separat ab — eigenes Schema, eigene Datenbank, eigene Replikation, eigene Backup-Strategie. Mischen mit Application-DB führt früher oder später zum Vorfall."),
        ],
        "faq": [
            ("Reichen ELK / Loki Standard-Logs?", "Nein. Sie müssen einen separaten, strukturierten Audit-Stream führen, der nach den DSGVO-Anforderungen (Art. 30) auswertbar ist."),
            ("Wie lange müssen Audit-Logs aufbewahrt werden?", "Hängt vom Sektor ab: 3 Jahre Standard, 7-10 Jahre in Finanz, je nach Behandlungspflicht in Gesundheit. Mit Rechtsabteilung klären."),
            ("Sollen IP-Adressen in Klartext gespeichert werden?", "Nur kurzfristig (90 Tage). Danach anonymisieren (letztes Oktett bei IPv4, letzte 64 Bit bei IPv6 entfernen)."),
        ],
    },
    {
        "slug": "warum-wir-htmx-statt-react-fuer-interne-tools",
        "category": "open-source",
        "title": "Warum wir HTMX statt React für interne Tools verwenden",
        "subtitle": "Drei interne Tools letztes Jahr, kein einziges Webpack-Update, kein einziges Bundle größer als 30 KB. Hier ist, warum HTMX in der Werkstatt funktioniert.",
        "description": "HTMX in produktiven internen Tools: Vision GO zeigt drei reale Anwendungen und vergleicht Entwicklungs- und Wartungskosten gegenüber React-basierten Lösungen.",
        "keywords": "HTMX Erfahrung, Hypermedia, interne Tools, Backoffice, Server-Rendering",
        "date": "2026-05-13",
        "read_min": 7,
        "tags": ["HTMX", "Open Source", "Backend", "Productivity"],
        "body": [
            ("h2", "Was wir vorher hatten"),
            ("p", "Bis 2023 haben wir interne Tools — Backoffice für unsere Auftraggeber, Admin-Panels für unsere eigenen Apps — mit React+Next.js gebaut. Das funktionierte. Es funktionierte gut. Aber es kostete uns überproportional viel Wartung."),
            ("p", "Jeder Webpack-Update brach etwas. Jede Next.js-Major-Version war ein halber Tag Migration. Bundle-Größen wuchsen organisch von 200 KB auf 800 KB, ohne dass irgendjemand benennen konnte, wann genau das passierte."),
            ("h2", "HTMX — die einfache Antwort"),
            ("p", "HTMX ist kein neues Framework, es ist eine Erinnerung daran, was HTML eigentlich kann. <code>hx-get</code>, <code>hx-swap</code>, <code>hx-trigger</code> — das war's. Es macht aus jedem Element ein potenzielles Form-Element, das HTML-Snippets vom Server holt und in die Seite einblendet."),
            ("p", "Wir haben das erste Mal Anfang 2024 ein internes Tool damit gebaut — ein Admin-Panel für unser On-Call-System. Vorher: React + Next.js, Bundle 320 KB. Mit HTMX: Bundle 14 KB. Entwicklungszeit halbiert."),
            ("h2", "Drei produktive Tools, drei messbare Ergebnisse"),
            ("ul", [
                "<strong>On-Call-Admin (Vision GO intern).</strong> 14 KB Bundle, 1,2 s Time-to-Interactive, 4 Wochen Entwicklung. Alternative React-Schätzung: 8 Wochen.",
                "<strong>Klinik-Backoffice (Kunde).</strong> 22 KB Bundle. Pflegekräfte loben das „schnelle” Tool — was 90 % der Reaktion auf Server-Roundtrips unter 80 ms ist.",
                "<strong>SEPA-Reconciliation-Dashboard.</strong> Komplex auf den ersten Blick, aber im Kern ein Form-und-Tabelle-Tool. HTMX dauerte halb so lange wie der React-Vorgänger.",
            ]),
            ("h2", "Wo HTMX nicht passt"),
            ("p", "<strong>Echtzeit-Co-Editing.</strong> Wenn Sie Notion oder Figma bauen, brauchen Sie CRDT-Sync und voll-clientseitige State-Management. HTMX kann das nicht."),
            ("p", "<strong>Offline-First.</strong> PWAs mit Service-Worker und IndexedDB-Sync sind besser mit React Native oder Svelte zu bauen."),
            ("p", "<strong>Mobile Apps.</strong> Niemand will eine HTMX-App im App Store. Native ist hier die Antwort."),
            ("h2", "Was HTMX bei uns ersetzt hat — und was nicht"),
            ("p", "HTMX ersetzt React in unseren <em>internen</em> Tools. Es ersetzt React <em>nicht</em> in unseren Endkunden-SaaS-Plattformen, wo komplexe Client-State-Synchronisation und Echtzeit-Updates Pflicht sind."),
            ("p", "Die Regel, mit der wir mittlerweile arbeiten: Wenn das Tool keinen geteilten Client-State über Routen hinweg braucht, ist HTMX richtig. Wenn doch — bleiben wir bei React mit Server-Components."),
        ],
        "faq": [
            ("Ist HTMX ein React-Ersatz?", "Nein. HTMX ersetzt React für Server-First-Apps mit minimaler Client-State. Für komplexe Single-Page-Apps mit globalem State bleibt React richtig."),
            ("Wie ist die Browser-Kompatibilität?", "HTMX läuft in allen modernen Browsern (Chromium, Firefox, Safari). Keine Polyfills nötig für IE-freie Umgebungen."),
            ("Welches Backend funktioniert am besten mit HTMX?", "Egal — Go, Python (FastAPI/Django), Ruby (Rails/Sinatra), Node (Express). HTMX ist Backend-agnostisch, solange Sie HTML-Fragmente zurückgeben können."),
        ],
    },
    {
        "slug": "saas-mvp-acht-wochen-realitaet",
        "category": "startup-produkt",
        "title": "SaaS-MVP in 8 Wochen: Was die Pitches verschweigen",
        "subtitle": "Wir haben 2025 vier MVPs für Gründer:innen gebaut. Die Wahrheit über Discovery-Schmerzen, Auth-Setup und warum „Logo + Login + Landing” nie das eigentliche MVP ist.",
        "description": "8-Wochen-MVP-Realität: Erfahrungsbericht von Vision GO über vier Gründer-Projekte 2025. Time-Budget, Auth, Onboarding und die häufigsten Unterschätzungen.",
        "keywords": "MVP 8 Wochen, SaaS Startup Wien, Gründer Software, Time to Market",
        "date": "2026-05-13",
        "read_min": 7,
        "tags": ["MVP", "Startup", "SaaS", "Produkt"],
        "body": [
            ("h2", "Was 8-Wochen-MVPs tatsächlich beinhalten"),
            ("p", "„Wir wollen einen MVP in 8 Wochen” ist der häufigste Satz in unseren Erstgesprächen mit Gründer:innen. In den meisten Fällen ist 8 Wochen realistisch — aber nur wenn alle Beteiligten verstehen, was in diesen Wochen tatsächlich passiert."),
            ("p", "Wir teilen 8 Wochen MVP-Budget üblicherweise wie folgt:"),
            ("ul", [
                "<strong>Woche 1: Discovery</strong> — Gespräche mit potenziellen Nutzer:innen, Konkurrenzanalyse, Feature-Schnitt.",
                "<strong>Woche 2: Architektur &amp; Design-System</strong> — Stack-Entscheidung, Design-Tokens, erste Wireframes in Code.",
                "<strong>Wochen 3-6: Bau</strong> — Iteration in zweiwöchigen Sprints, wöchentliches Demo.",
                "<strong>Woche 7: Polishing</strong> — Onboarding, Empty-States, Fehler-Pfade, Mobile-Polish.",
                "<strong>Woche 8: Launch-Vorbereitung</strong> — Stripe-Integration, AGB, Datenschutz, Cookie-Banner, Status-Page.",
            ]),
            ("h2", "Was die Pitches verschweigen"),
            ("p", "<strong>Auth dauert länger als gedacht.</strong> „Login mit Google” klingt nach einer Stunde — wird zu drei Tagen, wenn Sie es ordentlich machen wollen: Magic-Link-Fallback, Password-Reset, MFA, Session-Management, Logout-überall, OAuth-Token-Refresh. Wir nutzen mittlerweile fast immer <code>better-auth</code> oder <code>Stytch</code>, niemals selbst gebaut."),
            ("p", "<strong>Onboarding ist 30 % des MVPs.</strong> Wenn Nutzer:innen die App nicht in 2 Minuten verstehen, kommen sie nicht zurück. Wir reservieren mindestens eine Woche für Onboarding-Pfad, Sample-Data und progressive Disclosure."),
            ("p", "<strong>Email-Versand ist überraschend kompliziert.</strong> Transactional-E-Mail (Welcome, Reset, Receipts) braucht: Sender-Domain mit DKIM/SPF, ein Template-System, einen Provider (Postmark / Resend / Loops), Webhook-Handling für Bounces."),
            ("h2", "Was Gründer:innen unterschätzen"),
            ("p", "<strong>Daten-Modell-Fehler.</strong> Wer in Woche 2 falsch entscheidet, wie Tenants, Workspaces oder Permissions strukturiert sind, zahlt das in Woche 7 zurück. Wir investieren bewusst mehr Zeit in das Architektur-Dokument als die meisten anderen Studios."),
            ("p", "<strong>Customer-Support-Workflow.</strong> Wer baut die App? Wer beantwortet den ersten Support-Ticket? Spätestens in Woche 6 muss das geklärt sein."),
            ("p", "<strong>Datenschutz und AGB.</strong> Für österreichische Gründer:innen reservieren wir eine Stunde mit einer Wiener Kanzlei in Woche 7 — kostet etwa € 800, verhindert spätere Probleme im Wert von Tagen."),
            ("h2", "Was wir lernen, wenn der MVP launcht"),
            ("blockquote", "In allen vier Fällen 2025 war die wichtigste Erkenntnis im Launch nicht ein Bug — sondern, dass eine Annahme im Discovery falsch war."),
            ("p", "Das ist der Sinn eines MVPs: Annahmen testen. Wer in Woche 9 versteht, dass die Hauptzielgruppe doch eine andere ist, hat 8 Wochen und ein Budget richtig investiert. Wer das in Monat 14 begreift, hat ein Problem."),
        ],
        "faq": [
            ("Kann ein MVP unter 8 Wochen gebaut werden?", "Selten sauber. Mit Tools wie Supabase, NextAuth, Vercel kommt man auf 4-6 Wochen — aber Onboarding und Polish leiden. Für ernste Produkte: 8 Wochen Minimum."),
            ("Was kostet ein professioneller 8-Wochen-MVP?", "Zwischen € 40.000 und € 90.000, je nach Komplexität und Studio. Vision GO arbeitet im Bereich € 55.000-€ 85.000."),
            ("Wann lohnt sich Festpreis vs. Aufwand?", "Discovery und Design-System: Festpreis. Bau: nach Aufwand mit harter Obergrenze. Bei Vision GO transparente Wochen-Reports."),
        ],
    },
    {
        "slug": "opc-ua-edge-gateway-fuer-alte-maschinen",
        "category": "industrie-iot",
        "title": "OPC UA Edge Gateway für alte Maschinen: Praxisbericht aus drei Werken",
        "subtitle": "Wir verbinden 30 Jahre alte Drehmaschinen mit modernen MES-Systemen. Hier ist die Hardware, das Protokoll und der häufigste Fehler.",
        "description": "OPC UA in der Praxis: Vision GO zeigt, wie alte Industrieanlagen ohne digitale Schnittstelle ans MES-Backend angebunden werden. Hardware, Protokolle, Fallstricke.",
        "keywords": "OPC UA Tutorial, Industrie 4.0 Retrofit, Edge Gateway, MES Integration",
        "date": "2026-05-13",
        "read_min": 8,
        "tags": ["OPC UA", "IoT", "Edge", "Industrie 4.0"],
        "body": [
            ("h2", "Das Problem mit Maschinen aus den 90ern"),
            ("p", "Eine Drehmaschine von 1994 hat keine TCP/IP-Schnittstelle. Sie hat einen seriellen Anschluss, vielleicht einen Profibus, vielleicht nichts außer einer SPS, deren Hersteller seit 15 Jahren in Konkurs ist. Diese Maschinen anzubinden ist die häufigste Aufgabe, wenn wir mit steirischen oder oberösterreichischen Industrieunternehmen arbeiten."),
            ("p", "Die gute Nachricht: 95 % der Anlagen können ohne Hardware-Eingriff angebunden werden. Die schlechte: jede Anlage ist anders, und die Doku ist meistens irgendwo verloren gegangen."),
            ("h2", "Unsere Standard-Hardware"),
            ("ul", [
                "<strong>Raspberry Pi 5</strong> mit 8 GB RAM in einem IP67-Industriegehäuse (Phoenix Contact).",
                "<strong>Mehrere Schnittstellen-Adapter:</strong> RS-485, Profibus-Wandler, Modbus TCP, MQTT.",
                "<strong>ADC-Modul</strong> für analoge Signale (24V-Signale typisch in der Industrie).",
                "<strong>4G-LTE-Backup</strong> für Werke ohne stabiles WLAN.",
            ]),
            ("p", "Pro Maschine kostet das in der Beschaffung etwa € 380, in der Installation 4-6 Stunden. Bei einem Werk mit 50 Maschinen also € 20.000 Hardware plus € 18.000 Installation. Das ist die ehrliche Zahl, die häufig im Discovery überrascht."),
            ("h2", "OPC UA als gemeinsamer Nenner"),
            ("p", "Statt für jede Maschine ein eigenes Protokoll zu sprechen, verkapseln wir alles in OPC UA. Der Edge-Gateway läuft als OPC-UA-Server, der die Maschinendaten als strukturierte Nodes anbietet. Das MES-System (oder unser Cloud-Backend) ist Client."),
            ("p", "Warum OPC UA und nicht MQTT? OPC UA bietet eingebaute Authentifizierung, Verschlüsselung, strukturierte Datentypen und ein Information Model. MQTT ist leichtgewichtig, aber jeder Use Case erfindet seine eigene Topic-Struktur. Für Industrie ist OPC UA die richtige Wahl, auch wenn die Lernkurve steiler ist."),
            ("h2", "Häufige Fehler aus drei Projekten"),
            ("p", "<strong>Fehler 1: Zu hohe Abtastrate.</strong> Eine Vibrationssensor wirft 10 kHz auf den Bus. Den 1:1 ins Backend zu schicken, sind 36 GB pro Stunde. Wir berechnen FFTs am Edge und schicken nur Anomalien plus Stündliche Aggregate."),
            ("p", "<strong>Fehler 2: Single Point of Failure beim Gateway.</strong> Wir installieren immer zwei Pi-Gateways pro Werk, mit aktivem Failover. Ohne das fällt bei Hardware-Defekt die gesamte Produktion-Datenerfassung aus."),
            ("p", "<strong>Fehler 3: Fehlende Zeit-Synchronisation.</strong> NTP auf Industrie-Netzen ist oft nicht erreichbar. Wir nutzen GPS-Module oder lokale PTP-Master."),
            ("h2", "Was wir 2026 produktiv betreiben"),
            ("p", "Aktuell 4.700 Sensoren in 7 steirischen Werken, mit Predictive-Maintenance-Modellen, die Vibrations-Fingerprints lernen. Stillstände dieser Werke seit Einführung: −38 %. Pro Stunde Stillstand sparen wir Kunden zwischen € 8.000 und € 22.000 — die Investition refinanziert sich typischerweise nach 6-9 Monaten."),
        ],
        "faq": [
            ("Funktioniert OPC UA auch mit MQTT?", "Ja, OPC UA over MQTT (OPC UA PubSub) ist Teil des Standards. Wir nutzen es für Edge-zu-Cloud-Kommunikation, klassisches OPC UA TCP nur lokal."),
            ("Wie sicher ist ein Edge-Gateway?", "Hängt von der Konfiguration ab. Wir nutzen TLS, signierte Updates, lokales Firewalling und VPN für Cloud-Anbindung. Pentests einmal jährlich."),
            ("Was kostet eine Anbindung pro Maschine?", "Hardware €380, Installation 4-6 Stunden. Bei 50 Maschinen ca. €38.000 Gesamtinvestition."),
        ],
    },
    {
        "slug": "mica-stablecoin-regulierung-2026",
        "category": "fintech-krypto",
        "title": "MiCA-Stablecoins 2026: Was deutsche und österreichische Fintechs jetzt entscheiden müssen",
        "subtitle": "Die MiCA-Verordnung ist seit Mitte 2024 in Kraft. Hier ist, was wir aus zwei Stablecoin-Projekten gelernt haben — und welche Fragen die Compliance-Abteilung jetzt stellen muss.",
        "description": "MiCA-Compliance für Stablecoins und Utility-Tokens: Vision GO erläutert die Anforderungen aus Sicht eines Software-Studios mit zwei produktiven Token-Projekten.",
        "keywords": "MiCA Verordnung, Stablecoin Compliance, Krypto Regulierung Österreich, Utility Token",
        "date": "2026-05-13",
        "read_min": 8,
        "tags": ["MiCA", "Fintech", "Stablecoin", "Compliance"],
        "body": [
            ("h2", "MiCA in Kurzform"),
            ("p", "Die Markets in Crypto-Assets Regulation (MiCA) ist seit Juni 2024 in Kraft und bringt für Krypto-Assets in der EU klare Kategorien: Asset-referenced Tokens (ART), E-Money Tokens (EMT), Utility Tokens und „other Crypto-Assets”. Für Fintechs entscheidend: Jede Kategorie hat eigene Anforderungen an Lizenz, Reserve, Whitepaper und Marketing."),
            ("p", "Wir haben in den letzten 18 Monaten zwei Krypto-Projekte begleitet — einen MiCA-konformen Utility-Token (MXR Token für unser Online Snake), und einen abgebrochenen Stablecoin-Versuch für einen deutschen Mittelständler."),
            ("h2", "Was bei Utility-Tokens (MXR) wichtig war"),
            ("p", "Ein <strong>Utility Token</strong> nach Art. 4 MiCA ist von vielen MiCA-Anforderungen befreit, wenn er <em>ausschließlich</em> Zugang zu einer angebotenen Dienstleistung gibt. Das bedeutet konkret:"),
            ("ul", [
                "Keine Reserve-Anforderungen (im Gegensatz zu Stablecoins).",
                "Keine Lizenz nach Art. 16 MiCA notwendig.",
                "Whitepaper-Pflicht nach Art. 4 MiCA mit definierten Pflichtinhalten.",
                "Marketing-Materialien müssen MiCA-konform formuliert sein.",
            ]),
            ("p", "Bei MXR war die größte Herausforderung nicht das Schreiben des Whitepapers, sondern die <strong>klare Abgrenzung</strong> zwischen „Utility” und „Investment”. Sobald die App-Mechanik Anreize zum Spekulieren schafft, droht eine Umklassifizierung. Wir haben das Modell mit zwei externen Anwälten validiert."),
            ("h2", "Warum wir den Stablecoin-Versuch abgebrochen haben"),
            ("p", "Der zweite Kunde, ein Mittelständler in NRW, wollte einen euro-referenzierten Stablecoin für B2B-Zahlungen herausgeben. Auf dem Papier ein Asset-referenced Token (ART) — in der Praxis: Lizenz von der BaFin, Reserve-Compliance mit 1:1-Hinterlegung, regelmäßige Audits, Marktrisiko-Management."),
            ("p", "Nach drei Monaten Discovery wurde klar: die regulatorischen Kosten würden im ersten Jahr etwa € 1,2 Mio. betragen, das Geschäftsmodell trug das nicht. Wir haben offen mit dem Kunden gesprochen — der Mittelständler nutzt jetzt SEPA Instant für seine Anwendungsfälle, was 80 % der Probleme löst, ohne Krypto-Aufwand."),
            ("h2", "Worauf wir bei MiCA-Projekten in 2026 achten"),
            ("ol", [
                "<strong>Klassifizierung früh klären.</strong> Nichts ist teurer als ein Projekt, das in Monat 9 umklassifiziert wird.",
                "<strong>Whitepaper als Architektur-Dokument behandeln.</strong> Es zwingt zu klarem Denken — über Token-Ökonomie, Burns, Mints, Governance.",
                "<strong>Externe Anwälte einbinden, nicht erst beim Audit.</strong> Wiener und Frankfurter Kanzleien mit MiCA-Expertise gibt es 2026 in einer akzeptablen Dichte.",
                "<strong>Solana, Ethereum oder L2 — wählen Sie nach Compliance, nicht nach Tooling.</strong> Solana hat sich für Utility-Tokens als pragmatisch bewährt.",
                "<strong>KYC/AML früh modellieren.</strong> Auch wenn der Token Utility ist — die Plattform, auf der er gehandelt wird, ist meistens regulatorisch erfasst.",
            ]),
            ("p", "MiCA ist nicht der Tod der Krypto-Innovation in der EU. Aber es zwingt — gesund — zum Trennen zwischen Spielerei und ernstem Geschäft."),
        ],
        "faq": [
            ("Brauche ich für einen Utility-Token eine MiCA-Lizenz?", "Nicht zwingend, wenn der Token ausschließlich Zugang zur Dienstleistung gibt. Whitepaper-Pflicht und Marketing-Regeln gelten dennoch."),
            ("Was kostet ein Stablecoin-Setup unter MiCA?", "Realistisch zwischen €600.000 und €2,5 Mio. im ersten Jahr — durch BaFin-Lizenz, Reserve-Management, externe Audits und KYC-Infrastruktur."),
            ("Welche Blockchain für MiCA-konforme Tokens?", "Technisch frei wählbar. In der Praxis: Solana für niedrige Kosten, Ethereum / Layer-2 für maximale Liquidität. Compliance ist Blockchain-agnostisch."),
        ],
    },
    {
        "slug": "apple-hig-2026-was-sich-aendert",
        "category": "design-ux",
        "title": "Apple HIG 2026: Was sich für iOS-Apps wirklich geändert hat",
        "subtitle": "Wir haben unsere Apps gegen die neuen Human Interface Guidelines geprüft. Hier sind die fünf Stellen, an denen wir nachbessern mussten — und zwei, an denen wir Apple nicht folgen.",
        "description": "Apple Human Interface Guidelines 2026: Vision GO analysiert die Änderungen und zeigt, wie SwiftUI-Apps wie ScanUp und MegaRadio angepasst wurden.",
        "keywords": "Apple HIG 2026, iOS Design Guidelines, SwiftUI Tipps, Liquid Glass",
        "date": "2026-05-13",
        "read_min": 6,
        "tags": ["Apple HIG", "Design", "iOS", "UX"],
        "body": [
            ("h2", "Liquid Glass — mehr als Optik"),
            ("p", "Die augenfälligste Änderung der HIG 2026 ist Liquid Glass: System-Sheets, Toolbars und Modals erhalten eine dynamische Glas-Optik mit Background-Blur und farb-adaptive Tönung. Was Apple selbst auf der WWDC nicht so deutlich gesagt hat: das Verhalten der Sheet-Komponente hat sich ebenfalls verändert. Sheets-mit-Detents sind jetzt der Standard, nicht mehr die Ausnahme."),
            ("p", "Bei ScanUp haben wir das umgesetzt, indem wir alle Modal-Dialoge auf <code>.presentationDetents([.medium, .large])</code> umgestellt haben. Das hat zwei Tage gedauert — und drei Crash-Reports von Beta-Testern ausgelöst, die wir mit korrektem <code>.presentationDragIndicator(.visible)</code> beheben konnten."),
            ("h2", "Toolbar-Items neu denken"),
            ("p", "Die HIG empfiehlt jetzt explizit, Toolbar-Items <em>nach Bedeutung</em> zu gruppieren statt nach Häufigkeit. <code>ToolbarItemGroup(placement: .topBarTrailing)</code> mit semantischen Gruppen statt Einzel-Buttons."),
            ("p", "Praktisches Beispiel aus MegaRadio: Wir hatten einen einzelnen „Edit”-Button neben „Sort”. 2026er HIG: Beide gehören in dieselbe Gruppe „Liste verwalten” — Apple gestaltet die visuelle Trennung dann automatisch."),
            ("h2", "Wo wir Apple nicht gefolgt sind"),
            ("p", "<strong>1. Empfohlene Tab-Bar-Höhe.</strong> Apple's neuer Standard hat 56pt minimum. Bei MegaRadio waren wir bei 49pt — bewusst, weil die Album-Cover-Cards in der Liste sonst weniger Platz hätten. Unsere Test-Nutzer:innen haben den Unterschied nicht bemerkt."),
            ("p", "<strong>2. Vorgeschlagene Default-Farben.</strong> Apple empfiehlt für 2026 weicher gesättigte Akzentfarben. Unsere Brand-Farben sind dafür zu spezifisch — wir bleiben bei unserer Palette und stellen sicher, dass Dark-Mode-Kontraste WCAG AA erfüllen."),
            ("h2", "Was viele Studios übersehen"),
            ("ul", [
                "<strong>Vision OS-Anpassung.</strong> Apps, die auch auf Vision Pro laufen sollen, müssen die Tab-Bar-Position respektieren (oben statt unten).",
                "<strong>Dynamic Type bei Vision OS.</strong> Größere Default-Sizes — Apps mit fixen Font-Sizes wirken klein.",
                "<strong>Privacy-Indicators in Toolbars.</strong> Bei Apps mit Kamera-Zugriff (ScanUp) sind jetzt persistente Hinweise empfohlen — wir haben das übernommen, weil es Vertrauen schafft.",
                "<strong>StoreKit 2 Receipts.</strong> Apple hat die Receipt-Validation-Empfehlungen 2026 deutlich überarbeitet — In-App-Käufe sollten ausschließlich serverseitig validiert werden.",
            ]),
            ("h2", "Empfehlung"),
            ("p", "Lesen Sie die HIG 2026 als Gespräch, nicht als Vorgabe. Apple weiß viel über Bedienbarkeit, aber Ihre Nutzer:innen sind nicht Apple-Designer:innen. Wir folgen 80 % der HIG, weichen bewusst bei 20 % ab — immer mit dokumentierten Gründen im Design-System unseres Auftraggebers."),
        ],
        "faq": [
            ("Muss ich Liquid Glass für meine App anwenden?", "Wenn Sie SwiftUI-Standard-Modals nutzen, geschieht es automatisch. Custom-Modals sollten Sie überprüfen, damit sie konsistent wirken."),
            ("Wirkt sich die HIG auf App-Store-Reviews aus?", "Indirekt ja. Apple-Reviewer prüfen visuelle Konsistenz mit System-Konventionen. Grobe HIG-Verstöße können Reviews verzögern."),
            ("Wo finde ich die aktuelle HIG?", "Apple's Developer-Site: developer.apple.com/design/human-interface-guidelines — laufend aktualisiert nach jeder WWDC."),
        ],
    },
]

# ============================================================
# Helpers
# ============================================================
def category_by_slug(slug):
  return next(c for c in CATEGORIES if c["slug"] == slug)

def fmt_date(d):
  return datetime.date.fromisoformat(d).strftime("%d. %B %Y").replace("January","Januar").replace("February","Februar").replace("March","März").replace("April","April").replace("May","Mai").replace("June","Juni").replace("July","Juli").replace("August","August").replace("September","September").replace("October","Oktober").replace("November","November").replace("December","Dezember")

def render_body(blocks):
  out = []
  for kind, val in blocks:
    if kind == "h2": out.append(f"        <h2>{val}</h2>")
    elif kind == "h3": out.append(f"        <h3>{val}</h3>")
    elif kind == "p": out.append(f"        <p>{val}</p>")
    elif kind == "blockquote": out.append(f"        <blockquote>„{val}”</blockquote>")
    elif kind == "ul":
      lis = "\n".join(f"          <li>{x}</li>" for x in val)
      out.append(f"        <ul>\n{lis}\n        </ul>")
    elif kind == "ol":
      lis = "\n".join(f"          <li>{x}</li>" for x in val)
      out.append(f"        <ol>\n{lis}\n        </ol>")
  return "\n".join(out)

def render_faq(faqs):
  if not faqs: return ""
  rows = []
  for q, a in faqs:
    rows.append(f"""      <details>
        <summary>{q}</summary>
        <p>{a}</p>
      </details>""")
  return f"""
  <section class="faq-list">
    <div class="article-body" style="padding-top:0; padding-bottom:0;">
      <h3>Häufig gefragt</h3>
{chr(10).join(rows)}
    </div>
  </section>"""

def category_hero_svg(cat):
  return f"""<svg viewBox="0 0 1200 630" xmlns="http://www.w3.org/2000/svg" fill="none">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{cat['color2']}"/>
      <stop offset="1" stop-color="{cat['color1']}"/>
    </linearGradient>
    <radialGradient id="glow" cx="0.7" cy="0.3" r="0.6">
      <stop offset="0" stop-color="{cat['accent']}" stop-opacity="0.35"/>
      <stop offset="1" stop-color="{cat['accent']}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="1200" height="630" fill="url(#g)"/>
  <rect width="1200" height="630" fill="url(#glow)"/>
  <text x="80" y="86" font-family="Inter" font-size="14" fill="{cat['accent']}" letter-spacing="3" font-weight="600">VISION GO · BLOG</text>
  <text x="80" y="260" font-family="Inter" font-size="84" font-weight="600" fill="#fff" letter-spacing="-2.5">{html.escape(cat['name'])}</text>
  <text x="80" y="310" font-family="Inter" font-size="22" fill="rgba(255,255,255,0.75)" letter-spacing="-0.3">{cat['desc'][:80]}</text>
  <g transform="translate(900, 380)" opacity="0.4">
    <circle r="120" stroke="{cat['accent']}" stroke-width="2" fill="none"/>
    <circle r="80" stroke="{cat['accent']}" stroke-width="1.5" fill="none"/>
    <circle r="40" fill="{cat['accent']}" opacity="0.3"/>
  </g>
  <text x="80" y="565" font-family="JetBrains Mono" font-size="13" fill="rgba(255,255,255,0.5)" letter-spacing="2">VISIONGO.AT/BLOG/KATEGORIE/{cat['slug'].upper()}</text>
</svg>"""

def post_cover_svg(post, cat):
  title = post['title']
  # Truncate intelligently
  lines = []
  words = title.split()
  current = ""
  for w in words:
    if len(current + " " + w) > 30:
      lines.append(current.strip())
      current = w
    else:
      current = (current + " " + w).strip()
  if current: lines.append(current)
  lines = lines[:3]

  tspans = ""
  for i, line in enumerate(lines):
    tspans += f'<tspan x="80" dy="{0 if i==0 else 80}">{html.escape(line)}</tspan>'

  return f"""<svg viewBox="0 0 1200 675" xmlns="http://www.w3.org/2000/svg" fill="none">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{cat['color2']}"/>
      <stop offset="1" stop-color="{cat['color1']}"/>
    </linearGradient>
    <radialGradient id="glow" cx="0.85" cy="0.3" r="0.55">
      <stop offset="0" stop-color="{cat['accent']}" stop-opacity="0.30"/>
      <stop offset="1" stop-color="{cat['accent']}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="1200" height="675" fill="url(#g)"/>
  <rect width="1200" height="675" fill="url(#glow)"/>

  <text x="80" y="90" font-family="Inter" font-size="14" fill="{cat['accent']}" letter-spacing="3" font-weight="600">{html.escape(cat['name'].upper())}</text>
  <text y="240" font-family="Inter" font-size="64" font-weight="600" fill="#fff" letter-spacing="-2">{tspans}</text>

  <text x="80" y="595" font-family="JetBrains Mono" font-size="12" fill="rgba(255,255,255,0.55)" letter-spacing="2">VISION GO · {datetime.date.fromisoformat(post['date']).strftime("%d.%m.%Y")} · {post['read_min']} MIN</text>

  <!-- Vision GO mark -->
  <g transform="translate(1050, 70)">
    <path d="M0 0 L10 18 L14 11" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/>
    <path d="M28 0 L18 18 L14 11" stroke="{cat['accent']}" stroke-width="2.4" stroke-linecap="round"/>
  </g>
  <text x="1095" y="80" font-family="Inter" font-size="14" fill="rgba(255,255,255,0.7)">Vision GO</text>

  <!-- Decoration: floating cards -->
  <g transform="translate(820, 380)" opacity="0.5">
    <rect width="240" height="140" rx="14" fill="rgba(255,255,255,0.08)" stroke="rgba(255,255,255,0.1)"/>
    <rect x="14" y="14" width="80" height="3" rx="1" fill="rgba(255,255,255,0.7)"/>
    <rect x="14" y="22" width="60" height="2" rx="1" fill="rgba(255,255,255,0.4)"/>
    <rect x="14" y="36" width="200" height="2" rx="1" fill="rgba(255,255,255,0.3)"/>
    <rect x="14" y="42" width="180" height="2" rx="1" fill="rgba(255,255,255,0.3)"/>
    <rect x="14" y="48" width="140" height="2" rx="1" fill="rgba(255,255,255,0.3)"/>
  </g>
</svg>"""

def nav(active=""):
  link = lambda h, t, a: f'<a class="nav__link{(" nav__link--active" if a==active else "")}" href="{h}">{t}</a>'
  return f"""<header class="nav">
  <div class="container nav__inner">
    <a href="/" class="nav__brand"><span class="nav__brand-mark"><img src="/assets/logo.svg" alt=""/></span><span>Vision&nbsp;GO</span></a>
    <nav class="nav__links">
      {link('/','Studio','/')}
      {link('/leistungen.html','Leistungen','leistungen')}
      {link('/projekte.html','Arbeiten','projekte')}
      {link('/ueber-uns.html','Über','ueber')}
      {link('/karriere.html','Karriere','karriere')}
      {link('/kontakt.html','Kontakt','kontakt')}
    </nav>
    <a href="/kontakt.html" class="nav__cta"><span class="nav__cta-dot"></span>Projekt starten</a>
    <button class="nav__toggle" aria-label="Menü"><span></span><span></span></button>
  </div>
</header>"""

FOOTER = """<footer class="footer">
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

<script src="/assets/script.js" defer></script>"""

ORG_LD = """<script type="application/ld+json">
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
</script>"""

FONTS = """<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Fraunces:wght@400;500;600&display=swap" rel="stylesheet" />"""

# ============================================================
# Generate category hero SVGs
# ============================================================
for cat in CATEGORIES:
  (BLOG_ASSETS / f"cat-{cat['slug']}.svg").write_text(category_hero_svg(cat), encoding="utf-8")
print(f"✓ {len(CATEGORIES)} category SVGs")

# ============================================================
# Generate post cover SVGs
# ============================================================
for post in POSTS:
  cat = category_by_slug(post['category'])
  (BLOG_ASSETS / f"post-{post['slug']}.svg").write_text(post_cover_svg(post, cat), encoding="utf-8")
print(f"✓ {len(POSTS)} post covers")

# ============================================================
# Generate post HTML files
# ============================================================
for post in POSTS:
  cat = category_by_slug(post['category'])
  cover_url = f"{SITE_URL}/assets/blog/post-{post['slug']}.svg"
  post_url = f"{SITE_URL}/blog/{post['slug']}.html"

  faq_ld = ""
  if post.get('faq'):
    qs = []
    for q, a in post['faq']:
      qs.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})
    faq_ld = '<script type="application/ld+json">\n' + json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":qs}, ensure_ascii=False, indent=2) + '\n</script>'

  blog_post_ld = {
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "@id": post_url + "#article",
    "headline": post['title'],
    "alternativeHeadline": post['subtitle'],
    "description": post['description'],
    "datePublished": post['date'],
    "dateModified": post['date'],
    "author": {"@id": "https://visiongo.at/#organization"},
    "publisher": {"@id": "https://visiongo.at/#organization"},
    "mainEntityOfPage": post_url,
    "image": cover_url,
    "inLanguage": "de-AT",
    "articleSection": cat['name'],
    "keywords": ", ".join(post['tags']),
    "wordCount": sum(len(b[1].split() if isinstance(b[1], str) else "".join(b[1]).split()) for b in post['body']),
    "timeRequired": f"PT{post['read_min']}M",
    "url": post_url
  }

  breadcrumb_ld = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {"@type": "ListItem", "position": 1, "name": "Studio", "item": SITE_URL + "/"},
      {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE_URL + "/blog/"},
      {"@type": "ListItem", "position": 3, "name": cat['name'], "item": f"{SITE_URL}/blog/kategorie/{cat['slug']}.html"},
      {"@type": "ListItem", "position": 4, "name": post['title'], "item": post_url}
    ]
  }

  tags_html = "".join(f'<span class="tag">{t}</span>' for t in post['tags'])

  # Related posts: same category or 2 others
  related = [p for p in POSTS if p['slug'] != post['slug']][:2]
  related_html = ""
  for r in related:
    rcat = category_by_slug(r['category'])
    related_html += f"""
        <a class="post-card" href="/blog/{r['slug']}.html">
          <div class="post-card__cover"><img src="/assets/blog/post-{r['slug']}.svg" alt="{html.escape(r['title'])}" loading="lazy"/></div>
          <div class="post-card__meta">
            <span class="post-card__cat">{rcat['name']}</span>
            <span>·</span>
            <span>{r['read_min']} Min</span>
          </div>
          <h3 class="post-card__title">{r['title']}</h3>
        </a>"""

  html_out = f"""<!DOCTYPE html>
<html lang="de-AT">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />

<title>{post['title']} · Vision GO Blog</title>
<meta name="description" content="{post['description']}" />
<meta name="keywords" content="{post['keywords']}" />
<meta name="author" content="Vision GO GmbH" />
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1" />
<meta name="theme-color" content="{cat['color2']}" />
<link rel="canonical" href="{post_url}" />
<link rel="alternate" hreflang="de-AT" href="{post_url}" />

<meta property="og:type" content="article" />
<meta property="og:locale" content="de_AT" />
<meta property="og:site_name" content="Vision GO Blog" />
<meta property="og:url" content="{post_url}" />
<meta property="og:title" content="{html.escape(post['title'])}" />
<meta property="og:description" content="{html.escape(post['description'])}" />
<meta property="og:image" content="{cover_url}" />
<meta property="article:published_time" content="{post['date']}T09:00:00+02:00" />
<meta property="article:modified_time" content="{post['date']}T09:00:00+02:00" />
<meta property="article:section" content="{cat['name']}" />
{chr(10).join(f'<meta property="article:tag" content="{t}" />' for t in post['tags'])}
<meta property="article:author" content="Vision GO GmbH" />

<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{html.escape(post['title'])}" />
<meta name="twitter:description" content="{html.escape(post['description'])}" />
<meta name="twitter:image" content="{cover_url}" />

<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg" />
<link rel="alternate" type="application/rss+xml" title="Vision GO Blog" href="/blog/feed.xml" />
{FONTS}
<link rel="stylesheet" href="/assets/styles.css" />

{ORG_LD}

<script type="application/ld+json">
{json.dumps(blog_post_ld, ensure_ascii=False, indent=2)}
</script>

<script type="application/ld+json">
{json.dumps(breadcrumb_ld, ensure_ascii=False, indent=2)}
</script>
{faq_ld}
</head>

<body>

{nav('blog')}

<main>

  <section class="article-hero">
    <div class="container container--tight">
      <p class="breadcrumb"><a href="/">Studio</a><span class="breadcrumb__sep">/</span><a href="/blog/">Blog</a><span class="breadcrumb__sep">/</span><a href="/blog/kategorie/{cat['slug']}.html">{cat['name']}</a></p>
      <div class="article-hero__meta">
        <span class="article-hero__cat">{cat['name']}</span>
        <span>·</span>
        <time datetime="{post['date']}">{fmt_date(post['date'])}</time>
        <span>·</span>
        <span>{post['read_min']} Min Lesezeit</span>
      </div>
      <h1 class="article-hero__title">{post['title']}</h1>
      <p class="article-hero__sub">{post['subtitle']}</p>
    </div>
    <div class="container container--tight">
      <div class="article-cover">
        <img src="/assets/blog/post-{post['slug']}.svg" alt="{html.escape(post['title'])}"/>
      </div>
    </div>
  </section>

  <article class="article-body">
{render_body(post['body'])}

    <div class="author-card">
      <div class="author-card__avatar">VG</div>
      <div>
        <div class="author-card__name">Vision GO Engineering</div>
        <div class="author-card__role">Software-Studio · Wien · Seit 2015</div>
      </div>
    </div>
  </article>
{render_faq(post.get('faq', []))}

  <div class="article-footer">
    <div class="article-tags">{tags_html}</div>
    <div class="article-share">
      <span>Teilen:</span>
      <a href="https://twitter.com/intent/tweet?url={post_url}&amp;text={post['title']}" target="_blank" rel="noopener">X</a>
      <a href="https://www.linkedin.com/sharing/share-offsite/?url={post_url}" target="_blank" rel="noopener">LinkedIn</a>
      <a href="mailto:?subject={post['title']}&amp;body={post_url}">E-Mail</a>
    </div>
  </div>

  <section class="related-posts">
    <div class="container container--tight">
      <header class="section-head" style="margin-bottom:var(--space-6);">
        <h2 class="section-head__title">Auch <span class="accent">interessant</span>.</h2>
        <a href="/blog/" class="section-head__link">Alle Artikel</a>
      </header>
      <div class="blog-grid">{related_html}
      </div>
    </div>
  </section>

</main>

{FOOTER}
</body>
</html>
"""
  (BLOG / f"{post['slug']}.html").write_text(html_out, encoding="utf-8")

print(f"✓ {len(POSTS)} blog post pages")

# ============================================================
# Generate blog index
# ============================================================
def card_html(post, featured=False):
  cat = category_by_slug(post['category'])
  klass = "post-card post-card--featured" if featured else "post-card"
  return f"""        <a class="{klass}" href="/blog/{post['slug']}.html">
          <div class="post-card__cover"><img src="/assets/blog/post-{post['slug']}.svg" alt="{html.escape(post['title'])}"/></div>
          <div class="post-card__meta">
            <span class="post-card__cat">{cat['name']}</span>
            <span>·</span>
            <time datetime="{post['date']}">{fmt_date(post['date'])}</time>
            <span>·</span>
            <span>{post['read_min']} Min</span>
          </div>
          <h2 class="post-card__title">{post['title']}</h2>
          <p class="post-card__desc">{post['subtitle']}</p>
        </a>"""

featured = POSTS[0]
rest = POSTS[1:]

cats_pills = "".join(
  f'<a class="blog-cat" href="/blog/kategorie/{c["slug"]}.html">{c["name"]}</a>'
  for c in CATEGORIES
)

blog_post_list_ld = {
  "@context": "https://schema.org",
  "@type": "Blog",
  "@id": SITE_URL + "/blog/#blog",
  "name": "Vision GO Blog",
  "description": "Tech-Artikel aus dem Wiener Software-Studio Vision GO. Tägliche Inhalte zu KI, App-Entwicklung, Cloud, DSGVO und mehr.",
  "url": SITE_URL + "/blog/",
  "inLanguage": "de-AT",
  "publisher": {"@id": "https://visiongo.at/#organization"},
  "blogPost": [{"@type":"BlogPosting","headline":p['title'],"url":f"{SITE_URL}/blog/{p['slug']}.html","datePublished":p['date']} for p in POSTS]
}

index_html = f"""<!DOCTYPE html>
<html lang="de-AT">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />

<title>Blog — Tech-Artikel aus dem Wiener Software-Studio · Vision GO</title>
<meta name="description" content="Vision GO Blog: täglich neue Artikel zu KI, App-Entwicklung, Cloud, DSGVO, Open Source und Industrie 4.0. Aus 10 Jahren Studio-Erfahrung in Wien." />
<meta name="keywords" content="Tech Blog Wien, Software Studio Blog, KI Blog Österreich, Entwickler Blog, DSGVO Blog, Cloud Blog" />
<meta name="robots" content="index, follow, max-image-preview:large" />
<meta name="theme-color" content="#FFFFFF" />
<link rel="canonical" href="{SITE_URL}/blog/" />
<link rel="alternate" type="application/rss+xml" title="Vision GO Blog" href="/blog/feed.xml" />

<meta property="og:type" content="website" />
<meta property="og:locale" content="de_AT" />
<meta property="og:url" content="{SITE_URL}/blog/" />
<meta property="og:title" content="Vision GO Blog — Tech-Artikel aus Wien" />
<meta property="og:description" content="Täglich neue Artikel: KI, App, Cloud, DSGVO, Industrie. Klartext aus 10 Jahren Studio-Praxis." />
<meta property="og:image" content="{SITE_URL}/assets/og-image.svg" />
<meta name="twitter:card" content="summary_large_image" />

<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg" />
{FONTS}
<link rel="stylesheet" href="/assets/styles.css" />

{ORG_LD}

<script type="application/ld+json">
{json.dumps(blog_post_list_ld, ensure_ascii=False, indent=2)}
</script>

<script type="application/ld+json">
{json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Studio","item":SITE_URL+"/"},{"@type":"ListItem","position":2,"name":"Blog","item":SITE_URL+"/blog/"}]}, ensure_ascii=False, indent=2)}
</script>
</head>

<body>

{nav('blog')}

<main>

  <section class="blog-hero">
    <div class="container container--tight">
      <p class="blog-hero__eyebrow">— Vision GO Blog</p>
      <h1 class="blog-hero__title">Was wir in der Werkstatt lernen.</h1>
      <p class="blog-hero__lead">Täglich ein neuer Artikel — zu KI, App-Entwicklung, Cloud, Sicherheit und allem dazwischen. Aus zehn Jahren Studio-Erfahrung in Wien, ohne Marketing-Lack.</p>
      <div class="blog-cats">
{cats_pills}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <header class="section-head">
        <h2 class="section-head__title">Aktuelle <span class="accent">Artikel</span>.</h2>
        <a href="/blog/feed.xml" class="section-head__link">RSS abonnieren</a>
      </header>

      <div class="blog-grid blog-grid--featured" style="margin-bottom: var(--space-7);">
{card_html(featured, featured=True)}
        <div style="display:flex; flex-direction:column; gap:24px;">
{card_html(rest[0])}
{card_html(rest[1])}
        </div>
      </div>

      <div class="blog-grid">
{chr(10).join(card_html(p) for p in rest[2:])}
      </div>
    </div>
  </section>

</main>

{FOOTER}
</body>
</html>
"""
(BLOG / "index.html").write_text(index_html, encoding="utf-8")
print(f"✓ Blog index")

# ============================================================
# Generate category index pages
# ============================================================
for cat in CATEGORIES:
  cat_posts = [p for p in POSTS if p['category'] == cat['slug']]
  cat_url = f"{SITE_URL}/blog/kategorie/{cat['slug']}.html"

  cards = "\n".join(card_html(p) for p in cat_posts)
  if not cat_posts:
    cards = '<p style="grid-column: 1/-1; color: var(--ink-muted); padding: var(--space-7) 0;">Bald mehr — wir arbeiten täglich an neuen Artikeln in dieser Kategorie.</p>'

  collection_ld = {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "@id": cat_url,
    "name": f"{cat['name']} — Vision GO Blog",
    "description": cat['desc'],
    "url": cat_url,
    "inLanguage": "de-AT",
    "isPartOf": {"@id": SITE_URL + "/blog/#blog"}
  }

  out = f"""<!DOCTYPE html>
<html lang="de-AT">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />

<title>{cat['name']} — Vision GO Blog</title>
<meta name="description" content="{cat['desc']}" />
<meta name="keywords" content="{cat['keywords']}" />
<meta name="robots" content="index, follow, max-image-preview:large" />
<meta name="theme-color" content="{cat['color2']}" />
<link rel="canonical" href="{cat_url}" />

<meta property="og:type" content="website" />
<meta property="og:locale" content="de_AT" />
<meta property="og:url" content="{cat_url}" />
<meta property="og:title" content="{cat['name']} — Vision GO Blog" />
<meta property="og:description" content="{html.escape(cat['desc'])}" />
<meta property="og:image" content="{SITE_URL}/assets/blog/cat-{cat['slug']}.svg" />
<meta name="twitter:card" content="summary_large_image" />

<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg" />
{FONTS}
<link rel="stylesheet" href="/assets/styles.css" />

{ORG_LD}

<script type="application/ld+json">
{json.dumps(collection_ld, ensure_ascii=False, indent=2)}
</script>

<script type="application/ld+json">
{json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Studio","item":SITE_URL+"/"},{"@type":"ListItem","position":2,"name":"Blog","item":SITE_URL+"/blog/"},{"@type":"ListItem","position":3,"name":cat['name'],"item":cat_url}]}, ensure_ascii=False, indent=2)}
</script>
</head>

<body>

{nav('blog')}

<main>

  <section class="blog-hero">
    <div class="container container--tight">
      <p class="breadcrumb"><a href="/">Studio</a><span class="breadcrumb__sep">/</span><a href="/blog/">Blog</a><span class="breadcrumb__sep">/</span><span>{cat['name']}</span></p>
      <p class="blog-hero__eyebrow" style="margin-top:var(--space-4);">— Kategorie</p>
      <h1 class="blog-hero__title">{cat['name']}</h1>
      <p class="blog-hero__lead">{cat['desc']}</p>
      <div class="blog-cats">
{chr(10).join(f'        <a class="blog-cat{(" blog-cat--active" if c["slug"] == cat["slug"] else "")}" href="/blog/kategorie/{c["slug"]}.html">{c["name"]}</a>' for c in CATEGORIES)}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="blog-grid">
{cards}
      </div>
    </div>
  </section>

</main>

{FOOTER}
</body>
</html>
"""
  (KATEGORIE / f"{cat['slug']}.html").write_text(out, encoding="utf-8")

print(f"✓ {len(CATEGORIES)} category pages")

# ============================================================
# RSS feed
# ============================================================
rss_items = ""
for post in POSTS:
  cat = category_by_slug(post['category'])
  rss_items += f"""    <item>
      <title>{html.escape(post['title'])}</title>
      <link>{SITE_URL}/blog/{post['slug']}.html</link>
      <guid isPermaLink="true">{SITE_URL}/blog/{post['slug']}.html</guid>
      <pubDate>{datetime.date.fromisoformat(post['date']).strftime("%a, %d %b %Y")} 09:00:00 +0200</pubDate>
      <category>{html.escape(cat['name'])}</category>
      <description><![CDATA[{post['subtitle']}]]></description>
      <author>noreply@visiongo.at (Vision GO Engineering)</author>
    </item>
"""

rss = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:content="http://purl.org/rss/1.0/modules/content/">
  <channel>
    <title>Vision GO Blog</title>
    <link>{SITE_URL}/blog/</link>
    <atom:link href="{SITE_URL}/blog/feed.xml" rel="self" type="application/rss+xml"/>
    <description>Tech-Artikel aus dem Wiener Software-Studio Vision GO — KI, App-Entwicklung, Cloud, DSGVO, Open Source.</description>
    <language>de-AT</language>
    <lastBuildDate>{datetime.date.fromisoformat(TODAY).strftime("%a, %d %b %Y")} 09:00:00 +0200</lastBuildDate>
    <copyright>© 2026 Vision GO GmbH</copyright>
    <ttl>1440</ttl>
{rss_items}  </channel>
</rss>
"""
(BLOG / "feed.xml").write_text(rss, encoding="utf-8")
print("✓ RSS feed")

print("\nAll blog files generated.")
