#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generates a dynamic sitemap.xml from articles-enhanced.js
Run this whenever you add new articles to automatically update the sitemap
SEO-optimized with proper priorities and change frequencies
"""

import sys
import re
sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None
from datetime import datetime
from pathlib import Path

def extract_categories_and_articles_from_js():
    """Extract category names and article count from articles-enhanced.js"""
    articles_file = Path(__file__).parent.parent / "src" / "articles-enhanced.js"
    
    with open(articles_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract category names and article counts
    categories = {}
    category_pattern = r'"([^"]+)":\s*\[([\s\S]*?)\](?:,\s*"([^"]+)"|\])'
    
    current_pos = 0
    for match in re.finditer(r'"([^"]+)":\s*\[', content):
        cat_name = match.group(1)
        # Count articles in this category by counting title fields
        start = match.end()
        # Find next category or end
        next_match = re.search(r'},\s*"([^"]+)":\s*\[', content[start:])
        if next_match:
            end = start + next_match.start()
        else:
            end = content.rfind('}\n];', start)
        
        cat_content = content[start:end]
        article_count = cat_content.count('"title":')
        categories[cat_name] = article_count
    
    return categories

def generate_sitemap(categories, domain="https://grüner-faktencheck.de"):
    """Generate sitemap XML content with SEO optimization"""
    sitemap_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
        '  <url>',
        f'    <loc>{domain}/</loc>',
        f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>',
        '    <changefreq>weekly</changefreq>',
        '    <priority>1.0</priority>',
        '  </url>',
    ]
    
    # Add category pages with dynamic priority based on article count
    max_articles = max(categories.values()) if categories else 1
    
    for category, article_count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        category_slug = category.lower().replace(" ", "-")
        category_url = f"{domain}/category/{category_slug}"
        
        # Priority based on article count (more articles = higher priority)
        priority = round(0.7 + (article_count / max_articles) * 0.25, 2)
        
        sitemap_lines.append('  <url>')
        sitemap_lines.append(f'    <loc>{category_url}</loc>')
        sitemap_lines.append(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
        sitemap_lines.append('    <changefreq>weekly</changefreq>')
        sitemap_lines.append(f'    <priority>{priority}</priority>')
        sitemap_lines.append('  </url>')
    
    sitemap_lines.append('</urlset>')
    
    return '\n'.join(sitemap_lines), categories

if __name__ == "__main__":
    try:
        categories = extract_categories_and_articles_from_js()
        sitemap_content, cat_data = generate_sitemap(categories)
        
        sitemap_path = Path(__file__).parent.parent / "public" / "sitemap.xml"
        with open(sitemap_path, 'w', encoding='utf-8') as f:
            f.write(sitemap_content)
        
        print(f"[OK] Sitemap generated: {sitemap_path}")
        print(f"[OK] Kategorien mit Artikel-Zahl:")
        for cat, count in sorted(cat_data.items(), key=lambda x: x[1], reverse=True):
            print(f"     - {cat}: {count} Artikel")
        print(f"[OK] Sitemap URL: https://grüner-faktencheck.de/sitemap.xml")
        print(f"\n[INFO] NÄCHSTE SCHRITTE:")
        print(f"1. Gehen Sie zu: https://search.google.com/search-console")
        print(f"2. Registrieren Sie Ihre Domain (falls noch nicht getan)")
        print(f"3. Gehen Sie zu: Sitemaps")
        print(f"4. Tragen Sie ein: https://grüner-faktencheck.de/sitemap.xml")
        print(f"5. Klicken Sie: 'Absenden'")
        print(f"\n[DONE] Das war's! Google wird Ihre Artikel jetzt regelmäßig crawlen.")
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        exit(1)
