#!/usr/bin/env python3
"""
Generates a dynamic sitemap.xml from articles.js
Run this whenever you add new articles to automatically update the sitemap
"""

import re
from datetime import datetime
from pathlib import Path

def extract_categories_from_js():
    """Extract category names from articles.js"""
    articles_file = Path(__file__).parent / "src" / "articles.js"
    
    with open(articles_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract category names using regex
    categories = re.findall(r'"([^"]+)":\s*\[', content)
    return list(dict.fromkeys(categories))  # Remove duplicates, keep order

def generate_sitemap(categories, domain="https://grüner-faktencheck.de"):
    """Generate sitemap XML content"""
    sitemap_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        '  <url>',
        f'    <loc>{domain}/</loc>',
        f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>',
        '    <changefreq>weekly</changefreq>',
        '    <priority>1.0</priority>',
        '  </url>',
    ]
    
    # Add category pages
    for category in categories:
        category_slug = category.lower().replace(" ", "-")
        category_url = f"{domain}/category/{category_slug}"
        sitemap_lines.append('  <url>')
        sitemap_lines.append(f'    <loc>{category_url}</loc>')
        sitemap_lines.append(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
        sitemap_lines.append('    <changefreq>weekly</changefreq>')
        sitemap_lines.append('    <priority>0.8</priority>')
        sitemap_lines.append('  </url>')
    
    sitemap_lines.append('</urlset>')
    
    return '\n'.join(sitemap_lines)

if __name__ == "__main__":
    try:
        categories = extract_categories_from_js()
        sitemap_content = generate_sitemap(categories)
        
        sitemap_path = Path(__file__).parent / "public" / "sitemap.xml"
        with open(sitemap_path, 'w', encoding='utf-8') as f:
            f.write(sitemap_content)
        
        print(f"✓ Sitemap generated: {sitemap_path}")
        print(f"✓ Categories added: {', '.join(categories)}")
        print(f"✓ Sitemap URL: https://grüner-faktencheck.de/sitemap.xml")
        print(f"\n📌 NÄCHSTE SCHRITTE:")
        print(f"1. Gehen Sie zu: https://search.google.com/search-console")
        print(f"2. Registrieren Sie Ihre Domain (falls noch nicht getan)")
        print(f"3. Gehen Sie zu: Sitemaps")
        print(f"4. Tragen Sie ein: https://grüner-faktencheck.de/sitemap.xml")
        print(f"5. Klicken Sie: 'Absenden'")
        print(f"\n⚡ Das war's! Google wird Ihre Artikel jetzt regelmäßig crawlen.")
    except Exception as e:
        print(f"✗ Error: {e}")
        exit(1)
