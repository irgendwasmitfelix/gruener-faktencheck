#!/usr/bin/env node
/**
 * Setup Git Hooks
 * Arbeitet auf Windows, Mac und Linux
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const hookDir = path.join(__dirname, '.githooks');
const preCommitBash = path.join(hookDir, 'pre-commit');

console.log('📦 Richte Git Hooks ein...\n');

try {
  // Setze Git Hooks Path
  execSync('git config core.hooksPath .githooks', { 
    cwd: __dirname,
    stdio: 'pipe'
  });

  // Mache pre-commit auf Unix ausführbar
  if (fs.existsSync(preCommitBash)) {
    fs.chmodSync(preCommitBash, '755');
  }

  console.log('✅ Git Hooks konfiguriert!');
  console.log('\n📝 Setup abgeschlossen:');
  console.log('   • .githooks/pre-commit ist installiert');
  console.log('   • Automatische Generierung ist aktiviert\n');
  console.log('💡 Beim nächsten "git commit" werden automatisch:');
  console.log('   • Sitemap generiert');
  console.log('   • Static HTML erstellt');
  console.log('   • Dateien zum Commit hinzugefügt\n');
  console.log('🚀 Fertig! Probier einen Commit aus.\n');

} catch (error) {
  console.error('❌ Fehler beim Setup:', error.message);
  process.exit(1);
}
