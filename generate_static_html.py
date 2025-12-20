"""
Static HTML Generator für Grüner Faktencheck
Generiert separate HTML-Seiten für jede Kategorie zur SEO-Optimierung
Läuft unabhängig und beeinflusst nicht die React-App
"""

import os
import json
from datetime import datetime
from pathlib import Path

# ========== ARTIKELDATEN ==========
# Diese sollten aus deiner articles.js kommen
# Für jetzt hardcodiert, später von API laden oder aus JS-Datei parsen

ARTICLES = {
    "Wirtschaft": [
        {"title": "Staatsanwaltschaft Dresden führt Ermittlungsverfahren gegen Robert Habeck", "url": "https://www.medienservice.sachsen.de/medien/news/1088002"},
        {"title": "Habeck-Enthüllung und das Versagen der Medien", "url": "https://www.nius.de/kommentar/news/keine-silbe-in-der-tagesschau-die-habeck-enthuellung-und-das-gewaltige-versagen-der-medien/b15a84e4-8f20-4072-9681-8067f1acda7f"},
    ],
    "Energie": [
        {"title": "Windkraft in Deutschland", "url": "https://example.com"},
    ],
    # Weitere Kategorien folgen...
}

# ========== HTML TEMPLATE ==========
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Grüner Faktencheck – {category}</title>
    <meta name="description" content="Grüner Faktencheck - {category} Artikel: Unabhängige Analyse und Faktenchecks zur Grünen Partei. Artikel, Quellen und kritische Bewertung von Grünen-Politik in Deutschland.">
    <meta name="keywords" content="Grüne Partei, {category}, Faktencheck, Faktenfinder, Deutschland Politik, Habeck, Baerbock">
    <link rel="canonical" href="https://grüner-faktencheck.de/{category_slug}">
    
    <!-- Open Graph -->
    <meta property="og:title" content="Grüner Faktencheck – {category}">
    <meta property="og:description" content="{category} Artikel - Faktencheck zur Grünen Partei Deutschland">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://grüner-faktencheck.de/{category_slug}">
    <meta property="og:image" content="https://grüner-faktencheck.de/og-image.jpg">
    
    <!-- JSON-LD Schema -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Grüner Faktencheck - {category}",
        "url": "https://grüner-faktencheck.de/{category_slug}",
        "description": "{category} Artikel zum Grünen Faktencheck. Kritische Analyse und Faktenüberprüfung.",
        "mainEntity": {{
            "@type": "ItemList",
            "itemListElement": {items_json}
        }}
    }}
    </script>
    
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; line-height: 1.6; }}
        h1 {{ color: #217c3b; border-bottom: 3px solid #217c3b; padding-bottom: 10px; }}
        .article {{ border: 1px solid #ddd; padding: 15px; margin: 15px 0; border-radius: 6px; }}
        .article h2 {{ margin-top: 0; }}
        a {{ color: #217c3b; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .meta {{ color: #666; font-size: 0.9em; }}
        .back-link {{ margin-bottom: 20px; }}
        footer {{ border-top: 1px solid #ddd; padding-top: 20px; margin-top: 40px; color: #666; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="back-link">
        <a href="/">← Zurück zur Startseite</a>
    </div>
    
    <h1>Grüner Faktencheck – {category}</h1>
    <p class="meta">Kritische Analyse und Faktenüberprüfung zur Grünen Partei Deutschland</p>
    
    <div class="articles">
        {articles_html}
    </div>
    
    <footer>
        <p>Erstellt von: <a href="https://www.youtube.com/@reallifemitfelix" target="_blank">Felix H.</a> | 
        <a href="https://paypal.me/Sparky512" target="_blank">Trinkgeld via PayPal</a></p>
        <p>&copy; 2025 Grüner Faktencheck. Letzte Aktualisierung: {timestamp}</p>
    </footer>
</body>
</html>"""

# ========== FUNKTIONEN ==========

def get_domain(url):
    """Extrahiert Domain aus URL"""
    try:
        from urllib.parse import urlparse
        domain = urlparse(url).netloc.replace("www.", "")
        return domain
    except:
        return url

def generate_article_html(article):
    """Generiert HTML für einen Artikel"""
    return f"""
    <div class="article">
        <h2>{article['title']}</h2>
        <a href="{article['url']}" target="_blank" rel="noopener noreferrer">
            Weiterlesen auf {get_domain(article['url'])}
        </a>
    </div>
    """

def generate_json_ld_items(articles):
    """Generiert JSON-LD ItemList für Schema.org"""
    items = []
    for idx, article in enumerate(articles, 1):
        items.append({
            "@type": "ListItem",
            "position": idx,
            "name": article['title'],
            "url": article['url']
        })
    return json.dumps(items)

def generate_category_page(category, articles_list):
    """Generiert statische HTML-Seite für eine Kategorie"""
    
    category_slug = category.lower()
    
    # Artikel HTML generieren
    articles_html = "".join([generate_article_html(a) for a in articles_list])
    
    # JSON-LD Items generieren
    items_json = generate_json_ld_items(articles_list)
    
    # Template mit Daten füllen
    html = HTML_TEMPLATE.format(
        category=category,
        category_slug=category_slug,
        articles_html=articles_html,
        items_json=items_json,
        timestamp=datetime.now().strftime("%d.%m.%Y %H:%M")
    )
    
    return html, category_slug

def save_html_files(output_dir="./static_pages"):
    """Speichert alle Kategorie-Seiten als HTML-Dateien"""
    
    # Output-Verzeichnis erstellen
    Path(output_dir).mkdir(exist_ok=True)
    
    generated_files = []
    
    for category, articles_list in ARTICLES.items():
        if articles_list:  # Nur Kategorien mit Artikeln
            html, slug = generate_category_page(category, articles_list)
            
            filename = f"{output_dir}/{slug}.html"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html)
            
            generated_files.append({
                "category": category,
                "slug": slug,
                "file": filename,
                "articles": len(articles_list)
            })
            
            print(f"✓ Generiert: {filename} ({len(articles_list)} Artikel)")
    
    return generated_files

def upload_to_hostinger(local_dir="./static_pages", remote_dir="/public_html/"):
    """
    Lädt HTML-Dateien zu Hostinger hoch (über SFTP)
    WICHTIG: Benötigt paramiko library: pip install paramiko
    """
    
    try:
        import paramiko
    except ImportError:
        print("⚠ paramiko nicht installiert. Installiere mit: pip install paramiko")
        print("Datein wurden lokal gespeichert, aber nicht hochgeladen.")
        return False
    
    # Deine Hostinger-Credentials (ACHTUNG: In Produktion in Env-Variable speichern!)
    SFTP_HOST = "your-hostinger-sftp-server.com"
    SFTP_USER = "your-sftp-username"
    SFTP_PASS = "your-sftp-password"
    
    try:
        # SFTP-Verbindung aufbauen
        transport = paramiko.Transport((SFTP_HOST, 22))
        transport.connect(username=SFTP_USER, password=SFTP_PASS)
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        # Alle HTML-Dateien hochladen
        for file in Path(local_dir).glob("*.html"):
            remote_path = f"{remote_dir}{file.name}"
            sftp.put(str(file), remote_path)
            print(f"✓ Hochgeladen: {remote_path}")
        
        sftp.close()
        transport.close()
        print("✓ Upload zu Hostinger abgeschlossen!")
        return True
        
    except Exception as e:
        print(f"✗ Upload fehlgeschlagen: {e}")
        return False

# ========== HAUPTFUNKTION ==========

def main():
    """Hauptfunktion - führt alles aus"""
    
    print("=" * 50)
    print("Grüner Faktencheck - Static HTML Generator")
    print("=" * 50)
    
    # 1. HTML-Dateien generieren
    print("\n1. Generiere statische HTML-Seiten...")
    generated = save_html_files()
    print(f"\n✓ {len(generated)} Kategorien generiert!")
    
    # 2. Optional: Zu Hostinger hochladen (deaktiviert bis Credentials eingegeben)
    # print("\n2. Lade Dateien zu Hostinger hoch...")
    # upload_to_hostinger()
    
    print("\n" + "=" * 50)
    print("Fertig! Die HTML-Seiten sind unter ./static_pages/ verfügbar.")
    print("\nNächste Schritte:")
    print("1. Ergänze deine Hostinger-SFTP-Credentials in der upload_to_hostinger() Funktion")
    print("2. Richte einen Cron-Job auf PythonAnywhere ein (siehe unten)")
    print("\nCron-Job auf PythonAnywhere:")
    print("  - Zeitplan: Täglich um 02:00 Uhr (oder deine Vorliebe)")
    print("  - Befehl: python /home/username/generate_static_html.py")
    print("=" * 50)

if __name__ == "__main__":
    main()
