@echo off
REM Setup Git Hooks für Windows

echo 📦 Richte Git Hooks ein...

REM Setze Git Hooks Path
git config core.hooksPath .githooks

REM Mache pre-commit.bat ausführbar (Windows braucht das nicht, aber zur Sicherheit)
echo ✅ Git Hooks konfiguriert!
echo.
echo 📝 Nächste Schritte:
echo 1. Öffne PowerShell als Administrator
echo 2. Führe aus: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
echo 3. Das war's! Hooks sind bereit.
echo.
echo 💡 Beim nächsten 'git commit' werden die Scripts automatisch ausgeführt.
