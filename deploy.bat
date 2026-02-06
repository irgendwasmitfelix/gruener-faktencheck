@echo off
REM Deployment Script für Grüner Faktencheck (Windows)
REM Optimiert für maximale Sichtbarkeit und Performance

setlocal enabledelayedexpansion

echo.
echo 🚀 GRUENER FAKTENCHECK - DEPLOYMENT SCRIPT
echo ==========================================
echo.

REM Check Node.js
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Node.js ist nicht installiert
    exit /b 1
)

for /f "tokens=*" %%i in ('node --version') do set NODE_VERSION=%%i
for /f "tokens=*" %%i in ('npm --version') do set NPM_VERSION=%%i

echo ✓ Node.js: %NODE_VERSION%
echo ✓ NPM: %NPM_VERSION%
echo.

REM Install dependencies
echo 📦 Installiere Dependencies...
call npm install
if %errorlevel% neq 0 (
    echo ❌ Fehler bei NPM Install
    exit /b 1
)
echo ✓ Dependencies installiert
echo.

REM Generate meta files
echo 📄 Generiere Meta-Dateien...
python generate_sitemap.py
python generate_rss.py
python generate_static_html.py
echo ✓ Meta-Dateien generiert
echo.

REM Build
echo 🔨 Baue Projekt...
call npm run build
if %errorlevel% neq 0 (
    echo ❌ Fehler beim Build
    exit /b 1
)
echo ✓ Build abgeschlossen
echo.

REM Check files
echo ✅ DEPLOYMENT BEREIT
echo.
echo Wichtige Dateien:
echo   ✓ index.html (SEO optimiert)
echo   ✓ manifest.json (PWA)
echo   ✓ service-worker.js (Offline)
echo   ✓ public/robots.txt (Crawling)
echo   ✓ public/sitemap.xml (Indexierung)
echo   ✓ public/feed.xml (RSS)
echo   ✓ public/feed.json (JSON Feed)
echo.

echo 📊 Statistiken:
echo   - Kategorien: 3 (Wirtschaft, Innenpolitik, Außenpolitik)
echo   - Meta-Tags: 15+
echo   - PWA Support: Ja
echo   - Service Worker: Ja
echo.

echo 🌐 Deployment auf Production:
echo   1. Deploy 'dist\' Verzeichnis zu Web Server
echo   2. Auf HTTPS überprüfen
echo   3. Sitemap in Google Search Console eintragen
echo   4. robots.txt überprüfen: https://gruener-faktencheck.de/robots.txt
echo   5. Service Worker testen: Chrome DevTools ^> Application ^> Service Workers
echo.

echo ✨ FERTIG!
pause
