#!/bin/bash
# Setup Git Hooks für Unix/Linux/Mac

echo "📦 Richte Git Hooks ein..."

# Setze Git Hooks Path
git config core.hooksPath .githooks

# Mache pre-commit ausführbar
chmod +x .githooks/pre-commit

echo "✅ Git Hooks konfiguriert!"
echo ""
echo "💡 Beim nächsten 'git commit' werden die Scripts automatisch ausgeführt."
