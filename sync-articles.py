#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Synchronisiert articles.js mit articles-enhanced.js
Erstellt articles.js aus der erweiterten Version (ohne description/keywords)
"""

import re
import sys
from pathlib import Path

def sync_articles():
    """Liest articles-enhanced.js und generiert articles.js"""
    
    enhanced_file = Path(__file__).parent / "src" / "articles-enhanced.js"
    articles_file = Path(__file__).parent / "src" / "articles.js"
    
    # Lese enhanced
    with open(enhanced_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse Kategorien und Artikel mit Regex
    categories = {}
    
    # Finde alle Kategorien - pattern: "CategoryName": [ ... ],
    cat_starts = [(m.start(), m.group(1)) for m in re.finditer(r'"([^"]+)":\s*\[', content)]
    
    for idx, (start, cat_name) in enumerate(cat_starts):
        # Finde das Ende dieser Kategorie (nächste ] oder Ende der Datei)
        next_cat_start = cat_starts[idx + 1][0] if idx + 1 < len(cat_starts) else len(content)
        
        # Finde die passende schließende Klammer
        bracket_count = 1
        pos = content.find('[', start) + 1
        end = pos
        
        while bracket_count > 0 and pos < next_cat_start:
            if content[pos] == '[':
                bracket_count += 1
            elif content[pos] == ']':
                bracket_count -= 1
            pos += 1
        
        end = pos - 1
        cat_content = content[start:end]
        
        articles = []
        # Finde alle Artikel: "title": "...", "url": "..."
        article_pattern = r'"title":\s*"([^"]*(?:\\"[^"]*)*)",\s*"url":\s*"([^"]*(?:\\"[^"]*)*)"'
        
        for match in re.finditer(article_pattern, cat_content):
            title = match.group(1)
            url = match.group(2)
            
            # Unescape
            title = title.replace('\\"', '"')
            url = url.replace('\\"', '"')
            
            articles.append({"title": title, "url": url})
        
        if articles:
            categories[cat_name] = articles
    
    # Generiere articles.js Format (einfach, nur title + url)
    output_lines = ["export const articles = {"]
    
    cat_list = list(categories.keys())
    for i, cat in enumerate(cat_list):
        output_lines.append(f'  "{cat}": [')
        
        articles = categories[cat]
        for j, article in enumerate(articles):
            title = article['title'].replace('\\', '\\\\').replace('"', '\\"')
            url = article['url'].replace('\\', '\\\\').replace('"', '\\"')
            
            spacing = "    " if j < len(articles) - 1 else "    "
            line = f'{spacing}{{\n{spacing}  title: "{title}",\n{spacing}  url: "{url}"\n{spacing}}}'
            
            if j < len(articles) - 1:
                line += ','
            
            output_lines.append(line)
        
        if i < len(cat_list) - 1:
            output_lines.append('  ],')
        else:
            output_lines.append('  ]')
    
    output_lines.append("};")
    
    # Schreibe articles.js
    output = '\n'.join(output_lines)
    
    with open(articles_file, 'w', encoding='utf-8') as f:
        f.write(output)
    
    total_articles = sum(len(categories[cat]) for cat in categories)
    print(f"✅ articles.js synchronisiert!")
    print(f"   Kategorien: {', '.join(cat_list)}")
    print(f"   Insgesamt Artikel: {total_articles}")
    
    return True

if __name__ == "__main__":
    try:
        sync_articles()
        sys.exit(0)
    except Exception as e:
        print(f"❌ Fehler beim Synchronisieren: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
