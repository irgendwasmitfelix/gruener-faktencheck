#!/usr/bin/env python3
"""
Generate JSON Feed for optimal distribution and sharing
Supports integration with social media, podcasts, and news aggregators
"""

import json
from datetime import datetime
from pathlib import Path

def generate_json_feed():
    """Generate JSON Feed 1.1 format for maximum distribution"""
    
    articles_data = {
        "Wirtschaft": [
            {
                "title": "Grüne Liga Brandenburg klagt gegen Bebauungsplan für Werk von Red Bull",
                "description": "Umweltaktivisten der Grünen Liga klagen gegen Industrieprojekte",
                "url": "https://www.ariva.de/aktien/tesla-inc-aktie/news/gruene-liga-brandenburg-klagt-gegen-bebauungsplan-fuer-werk-11892363"
            }
        ]
    }
    
    feed = {
        "version": "https://jsonfeed.org/version/1.1",
        "title": "Grüner Faktencheck - Kritische Analysen der Grünen Partei",
        "description": "Unabhängige Faktenchecks, Analysen und kritische Bewertung der Grünen Partei Deutschland",
        "home_page_url": "https://gruener-faktencheck.de",
        "feed_url": "https://gruener-faktencheck.de/feed.json",
        "icon": "https://gruener-faktencheck.de/favicon.ico",
        "favicon": "https://gruener-faktencheck.de/favicon.ico",
        "language": "de",
        "authors": [
            {
                "name": "Grüner Faktencheck",
                "url": "https://gruener-faktencheck.de"
            }
        ],
        "hubs": [
            {
                "type": "WebSub",
                "url": "https://pubsubhubbub.appspot.com/"
            }
        ]
    }
    
    items = []
    article_id = 1
    
    for category, articles_list in articles_data.items():
        for article in articles_list:
            item = {
                "id": f"https://gruener-faktencheck.de/article/{article_id}",
                "url": article["url"],
                "external_url": article["url"],
                "title": article["title"],
                "summary": article["description"],
                "content_html": f"""
                    <h3>{article['title']}</h3>
                    <p>{article['description']}</p>
                    <p><strong>Kategorie:</strong> {category}</p>
                    <a href="{article['url']}" target="_blank">Artikel lesen</a>
                """,
                "tags": ["grüne-partei", "faktencheck", category.lower()],
                "date_published": datetime.now().isoformat(),
                "date_modified": datetime.now().isoformat(),
                "image": "https://gruener-faktencheck.de/og-image.jpg"
            }
            items.append(item)
            article_id += 1
    
    feed["items"] = items
    
    # Write to file
    output_path = Path("public/feed.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(feed, f, ensure_ascii=False, indent=2)
    
    print(f"✓ JSON Feed generated: {output_path}")
    print(f"  - Total articles: {len(items)}")
    print(f"  - Feed URL: https://gruener-faktencheck.de/feed.json")


if __name__ == "__main__":
    generate_json_feed()
