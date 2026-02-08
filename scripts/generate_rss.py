#!/usr/bin/env python3
"""
RSS Feed Generator für Grüner Faktencheck
Liest articles-enhanced.js und generiert feed.xml
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path

def escape_xml(text):
    """Escapiert XML Special Characters korrekt (& ZUERST!)"""
    if not isinstance(text, str):
        text = str(text)
    # Reihenfolge ist wichtig: & muss ZUERST escapiert werden!
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&apos;')
    return text

def parse_articles_js(file_path):
    """Parst articles-enhanced.js mit Regex und extrahiert die Artikel-Daten"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    articles_data = {}
    
    # Finde alle Kategorien mit ihren Arrays
    category_pattern = r'"(\w+)"\s*:\s*\[(.*?)\n  \]'
    categories = re.finditer(category_pattern, content, re.DOTALL)
    
    for cat_match in categories:
        category_name = cat_match.group(1)
        array_content = cat_match.group(2)
        
        # Extrahiere alle Artikel in dieser Kategorie
        articles_list = []
        
        # Finde alle {title: ..., url: ...} Objekte mit allen Fields
        article_pattern = r'\{\s*(?:")?title(?:")?\s*:\s*"(.*?)(?<!\\)"\s*,.*?(?:")?url(?:")?\s*:\s*"(.*?)(?<!\\)"\s*,.*?\}'
        articles = re.finditer(article_pattern, array_content, re.DOTALL)
        
        for art_match in articles:
            title = art_match.group(1).strip()
            url = art_match.group(2).strip()
            articles_list.append({'title': title, 'url': url})
        
        if articles_list:
            articles_data[category_name] = articles_list
    
    return articles_data

def generate_rss_feed(articles_data, output_path):
    """Generiert RSS Feed aus Artikel-Daten"""
    
    # RSS Header
    rss = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Grüner Faktencheck - RSS Feed</title>
    <link>https://gruener-faktencheck.de/</link>
    <description>Unabhängige Artikel und Links zur Grünen Partei Deutschland</description>
    <language>de-de</language>
    <lastBuildDate>{}</lastBuildDate>
    <generator>RSS Generator v1.0</generator>
'''
    
    # Aktuelle Zeit im RFC 822 Format
    now = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S +0000')
    rss = rss.format(now)
    
    # Items pro Kategorie
    item_count = 0
    for category, articles in articles_data.items():
        for article in articles:
            title = article.get('title', 'Unbekannter Titel')
            url = article.get('url', '')
            
            # Sichere Escape-Funktionen für XML mit korrekter Reihenfolge
            title_safe = escape_xml(title)
            url_safe = escape_xml(url)
            
            # Unique GUID basierend auf URL und Kategorie
            guid = f"{url}#{category}"
            guid_safe = escape_xml(guid)
            
            item = f'''    <item>
      <title>{title_safe}</title>
      <link>{url_safe}</link>
      <description>{title_safe} - Kategorie: {category}</description>
      <category>{category}</category>
      <guid isPermaLink="false">{guid_safe}</guid>
      <pubDate>{now}</pubDate>
    </item>
'''
            rss += item
            item_count += 1
    
    # RSS Footer
    rss += '''  </channel>
</rss>'''
    
    # Schreibe RSS Datei
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(rss)
    
    print("[OK] RSS Feed generiert: " + str(output_file))
    print("     " + str(item_count) + " Artikel enthalten")

if __name__ == '__main__':
    articles_path = Path(__file__).parent.parent / 'src' / 'articles-enhanced.js'
    output_path = Path(__file__).parent.parent / 'public' / 'feed.xml'
    
    if articles_path.exists():
        articles = parse_articles_js(articles_path)
        if articles:
            generate_rss_feed(articles, output_path)
        else:
            print("[ERROR] Keine Artikel gefunden in articles-enhanced.js")
    else:
        print("[ERROR] Datei nicht gefunden: " + str(articles_path))
