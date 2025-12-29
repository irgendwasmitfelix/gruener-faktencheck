@echo off
REM Pre-commit hook für Windows: Generiert Sitemap und Static HTML vor dem Commit

echo 🔄 Generiere Sitemap und Static HTML...

REM Prüfe ob Python installiert ist
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python nicht gefunden! Bitte Python installieren.
    exit /b 1
)

REM Führe Scripts aus
python generate_sitemap.py
if %errorlevel% neq 0 (
    echo ❌ generate_sitemap.py fehlgeschlagen!
    exit /b 1
)

python generate_static_html.py
if %errorlevel% neq 0 (
    echo ❌ generate_static_html.py fehlgeschlagen!
    exit /b 1
)

REM Füge generierte Dateien zum Commit hinzu
git add public/sitemap.xml
git add static/ 2>nul

echo ✅ Sitemap und Static HTML aktualisiert!
exit /b 0
