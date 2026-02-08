#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import sys

try:
    tree = ET.parse('public/feed.xml')
    root = tree.getroot()
    items = root.findall('.//item')
    print("[OK] RSS feed is valid XML")
    print(f"     Items: {len(items)}")
    
    # Check for common issues
    has_errors = False
    for i, item in enumerate(items):
        title = item.find('title')
        if title is None or not title.text:
            print(f"[WARNING] Item {i+1} has no title")
            has_errors = True
    
    if not has_errors:
        print("[OK] All items have titles")
    
    sys.exit(0)
except ET.ParseError as e:
    print(f"[ERROR] XML Parse Error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"[ERROR] {e}")
    sys.exit(1)
