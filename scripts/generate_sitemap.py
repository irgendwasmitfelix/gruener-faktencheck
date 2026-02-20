#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generates a dynamic sitemap.xml from articles-enhanced.js
Run this whenever you add new articles to automatically update the sitemap
SEO-optimized with proper priorities and change frequencies
"""

import sys
import re
import json
import subprocess
from shutil import which
sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None
from datetime import datetime
from pathlib import Path
import glob
import unicodedata

# Use ASCII/Punycode site domain for sitemap and ping URLs
SITE_DOMAIN = "https://xn--grner-faktencheck-32b.de"

def category_to_slug(category):
    """Create SEO slug for category paths."""
    return (
        category.strip()
        .replace("Ä", "Ae")
        .replace("Ö", "Oe")
        .replace("Ü", "Ue")
        .replace("ä", "ae")
        .replace("ö", "oe")
        .replace("ü", "ue")
        .replace("ß", "ss")
        .lower()
        .replace(" ", "-")
    )

def extract_static_pages():
    """Extract static HTML pages from static_pages directory"""
    static_pages_dir = Path(__file__).parent.parent / "static_pages"
    static_pages = {}
    
    if static_pages_dir.exists():
        for html_file in static_pages_dir.glob("*.html"):
            # Extract category name from filename (e.g., aussenpolitik.html -> Außenpolitik)
            name = html_file.stem
            # Map to proper category names
            category_map = {
                "aussenpolitik": "Außenpolitik",
                "energie": "Energie",
                "innenpolitik": "Innenpolitik",
                "wirtschaft": "Wirtschaft"
            }
            if name in category_map:
                static_pages[category_map[name]] = f"/{name}.html"
    
    return static_pages

def extract_categories_and_articles_from_js():
    """Extract category names and article count from articles-enhanced.js.

    Prefer using Node helper `scripts/parse_articles.js` for robust parsing.
    Falls Node nicht vorhanden oder Fehler auftritt, wird ein Regex‑Fallback verwendet.
    """
    scripts_dir = Path(__file__).parent
    node_helper = scripts_dir / 'parse_articles.js'

    # Try Node helper first
    if which('node') and node_helper.exists():
        try:
            proc = subprocess.run(['node', str(node_helper)], capture_output=True, text=True, timeout=5)
            if proc.returncode == 0 and proc.stdout:
                parsed = json.loads(proc.stdout)
                # Build categories dict with counts
                return {k: len(v) for k, v in parsed.items()}
            else:
                print('[WARN] Node parser failed, falling back to regex.', file=sys.stderr)
        except Exception as e:
            print(f'[WARN] Node parser error: {e}, falling back to regex.', file=sys.stderr)

    # Regex fallback (older behaviour)
    articles_file = Path(__file__).parent.parent / "src" / "articles-enhanced.js"

    with open(articles_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract category names and article counts
    categories = {}
    for match in re.finditer(r'"([^"]+)":\s*\[', content):
        cat_name = match.group(1)
        # Count articles in this category by counting title fields
        start = match.end()
        # Find next category or end
        next_match = re.search(r'},\s*"([^"]+)":\s*\[', content[start:])
        if next_match:
            end = start + next_match.start()
        else:
            end = len(content)

        cat_content = content[start:end]
        article_count = cat_content.count('"title":')
        categories[cat_name] = article_count

    return categories

def generate_sitemap(categories, static_pages, domain=SITE_DOMAIN):
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
    
    # Add static pages
    for category_name, url_path in static_pages.items():
        static_url = f"{domain}{url_path}"
        sitemap_lines.append('  <url>')
        sitemap_lines.append(f'    <loc>{static_url}</loc>')
        sitemap_lines.append(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
        sitemap_lines.append('    <changefreq>weekly</changefreq>')
        sitemap_lines.append('    <priority>0.9</priority>')
        sitemap_lines.append('  </url>')

    # Add individual article pages if they exist under static_pages/articles
    articles_dir = Path(__file__).parent.parent / 'static_pages' / 'articles'
    if articles_dir.exists():
        project_root = Path(__file__).parent.parent
        for article_file in sorted(articles_dir.glob('*.html')):
            rel_path = article_file.relative_to(project_root).as_posix()
            # Entferne führendes static_pages/ damit URLs wie /articles/... oder /aussenpolitik.html entstehen
            if rel_path.startswith('static_pages/'):
                rel_path = rel_path[len('static_pages/'):]
            article_url = f"{domain}/{rel_path}"
            sitemap_lines.append('  <url>')
            sitemap_lines.append(f'    <loc>{article_url}</loc>')
            sitemap_lines.append(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
            sitemap_lines.append('    <changefreq>monthly</changefreq>')
            sitemap_lines.append('    <priority>0.60</priority>')
            sitemap_lines.append('  </url>')
    
    # Add category pages with dynamic priority based on article count
    max_articles = max(categories.values()) if categories else 1
    
    for category, article_count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        category_slug = category_to_slug(category)
        category_url = f"{domain}/category/{category_slug}"
        
        # Priority based on article count (more articles = higher priority)
        priority = round(0.7 + (article_count / max_articles) * 0.25, 2)
        
        sitemap_lines.append('  <url>')
        sitemap_lines.append(f'    <loc>{category_url}</loc>')
        sitemap_lines.append(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
        sitemap_lines.append('    <changefreq>weekly</changefreq>')
        sitemap_lines.append(f'    <priority>{priority}</priority>')
        sitemap_lines.append('  </url>')
        # Also add the collection page URL that lists all articles for this category
        collection_url = f"{domain}/category/{category_slug}/articles"
        sitemap_lines.append('  <url>')
        sitemap_lines.append(f'    <loc>{collection_url}</loc>')
        sitemap_lines.append(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
        sitemap_lines.append('    <changefreq>weekly</changefreq>')
        sitemap_lines.append(f'    <priority>{round(max(0.6, priority - 0.05), 2)}</priority>')
        sitemap_lines.append('  </url>')
    
    sitemap_lines.append('</urlset>')
    
    return '\n'.join(sitemap_lines), categories, static_pages

if __name__ == "__main__":
    try:
        categories = extract_categories_and_articles_from_js()
        static_pages = extract_static_pages()
        sitemap_content, cat_data, static_data = generate_sitemap(categories, static_pages)
        
        sitemap_path = Path(__file__).parent.parent / "public" / "sitemap.xml"
        with open(sitemap_path, 'w', encoding='utf-8') as f:
            f.write(sitemap_content)
        
            print(f"[OK] Sitemap generated: {sitemap_path}")
            # Try to ping Google and Bing so they fetch the updated sitemap faster
            try:
                import urllib.request
                sitemap_domain = SITE_DOMAIN
                google_ping = f"https://www.google.com/ping?sitemap={sitemap_domain}/sitemap.xml"
                bing_ping = f"https://www.bing.com/webmaster/ping.aspx?siteMap={sitemap_domain}/sitemap.xml"
                for url in (google_ping, bing_ping):
                    try:
                        resp = urllib.request.urlopen(url, timeout=10)
                        print(f"[OK] Pinged: {url} -> {resp.getcode()}")
                    except Exception as pe:
                        print(f"[WARN] Ping failed: {url} -> {pe}")
            except Exception as e:
                print(f"[WARN] Ping skipped: {e}")
        print(f"[OK] Kategorien mit Artikel-Zahl:")
        for cat, count in sorted(cat_data.items(), key=lambda x: x[1], reverse=True):
            print(f"     - {cat}: {count} Artikel")
        print(f"[OK] Statische Seiten:")
        for cat, url in static_data.items():
            print(f"     - {cat}: {url}")
        print(f"[OK] Sitemap URL: {SITE_DOMAIN}/sitemap.xml")
        print(f"\n[INFO] NÄCHSTE SCHRITTE:")
        print(f"1. Gehen Sie zu: https://search.google.com/search-console")
        print(f"2. Registrieren Sie Ihre Domain (falls noch nicht getan)")
        print(f"3. Gehen Sie zu: Sitemaps")
        print(f"4. Tragen Sie ein: {SITE_DOMAIN}/sitemap.xml")
        print(f"5. Klicken Sie: 'Absenden'")
        print(f"\n[DONE] Das war's! Google wird Ihre Artikel jetzt regelmäßig crawlen.")
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        exit(1)
