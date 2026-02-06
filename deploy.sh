#!/bin/bash
# Deployment Script für Grüner Faktencheck
# Optimiert für maximale Sichtbarkeit und Performance

set -e  # Exit on error

echo "🚀 GRÜNER FAKTENCHECK - DEPLOYMENT SCRIPT"
echo "=========================================="
echo ""

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js ist nicht installiert"
    exit 1
fi

echo "✓ Node.js: $(node --version)"
echo "✓ NPM: $(npm --version)"
echo ""

# Install dependencies
echo "📦 Installiere Dependencies..."
npm install
echo "✓ Dependencies installiert"
echo ""

# Generate meta files
echo "📄 Generiere Meta-Dateien..."
python generate_sitemap.py
python generate_rss.py
python generate_static_html.py
echo "✓ Meta-Dateien generiert"
echo ""

# Build
echo "🔨 Baue Projekt..."
npm run build
echo "✓ Build abgeschlossen"
echo ""

# Check files
echo "✅ DEPLOYMENT BEREIT"
echo ""
echo "Wichtige Dateien:"
echo "  ✓ index.html (SEO optimiert)"
echo "  ✓ manifest.json (PWA)"
echo "  ✓ service-worker.js (Offline)"
echo "  ✓ public/robots.txt (Crawling)"
echo "  ✓ public/sitemap.xml (Indexierung)"
echo "  ✓ public/feed.xml (RSS)"
echo "  ✓ public/feed.json (JSON Feed)"
echo ""

echo "📊 Statistiken:"
echo "  - Artikel: $(grep -o '"title":' src/articles-enhanced.js | wc -l)"
echo "  - Kategorien: 3 (Wirtschaft, Innenpolitik, Außenpolitik)"
echo "  - Meta-Tags: 15+"
echo ""

echo "🌐 Deployment auf Production:"
echo "  1. Deploy 'dist/' Verzeichnis zu Web Server"
echo "  2. Auf HTTPS überprüfen"
echo "  3. Sitemap in Google Search Console eintragen"
echo "  4. robots.txt überprüfen: https://grüner-faktencheck.de/robots.txt"
echo "  5. Service Worker testen: Chrome DevTools > Application > Service Workers"
echo ""

echo "✨ FERTIG!"
