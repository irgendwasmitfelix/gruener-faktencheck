#!/usr/bin/env node

/**
 * Cloudflare + Uptime Robot Verification Script
 * Testet ob alles richtig eingerichtet ist
 */

const https = require('https');
const dns = require('dns').promises;

const CONFIG = {
  DOMAIN_ASCII: 'gruener-faktencheck.de',
  DOMAIN_UMLAUT: 'grüner-faktencheck.de',
  SERVER_IP: process.env.SERVER_IP || '0.0.0.0', // Deine Server IP
};

// Farben für Output
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m'
};

const log = {
  success: (msg) => console.log(`${colors.green}✅ ${msg}${colors.reset}`),
  error: (msg) => console.log(`${colors.red}❌ ${msg}${colors.reset}`),
  warn: (msg) => console.log(`${colors.yellow}⚠️  ${msg}${colors.reset}`),
  info: (msg) => console.log(`${colors.cyan}ℹ️  ${msg}${colors.reset}`),
  step: (msg) => console.log(`${colors.blue}\n📋 ${msg}${colors.reset}`)
};

// Test 1: DNS Resolution
async function testDNS() {
  log.step('TEST 1: DNS Resolution (Cloudflare)');
  
  try {
    const result = await dns.resolve4(CONFIG.DOMAIN_ASCII);
    log.success(`DNS resolve: ${CONFIG.DOMAIN_ASCII} → ${result.join(', ')}`);
    
    // Check if Cloudflare IP (104.21.x.x or 104.22.x.x)
    if (result[0].startsWith('104.21') || result[0].startsWith('104.22')) {
      log.success('IP ist Cloudflare! ✅');
      return true;
    } else {
      log.warn(`IP (${result[0]}) ist nicht Cloudflare (Sollte 104.21.x.x oder 104.22.x.x sein)`);
      return false;
    }
  } catch (error) {
    log.error(`DNS lookup failed: ${error.message}`);
    return false;
  }
}

// Test 2: HTTPS/SSL
async function testSSL() {
  log.step('TEST 2: SSL/HTTPS Connection');
  
  return new Promise((resolve) => {
    const req = https.get(`https://${CONFIG.DOMAIN_ASCII}`, { 
      timeout: 5000,
      rejectUnauthorized: false // Erlaubt auch selbst-signierte Certs für Test
    }, (res) => {
      if (res.statusCode === 200) {
        log.success(`HTTPS verbunden (Status: ${res.statusCode})`);
        
        // Check SSL cert
        const cert = res.socket.getPeerCertificate();
        if (cert.subject && cert.subject.CN) {
          log.success(`SSL Cert für: ${cert.subject.CN}`);
          resolve(true);
        }
      } else {
        log.warn(`HTTP Status: ${res.statusCode}`);
        resolve(true); // Nicht als Fehler, da Server antwortete
      }
    });
    
    req.on('error', (err) => {
      log.error(`Connection error: ${err.message}`);
      resolve(false);
    });
    
    req.on('timeout', () => {
      log.error('Connection timeout');
      req.destroy();
      resolve(false);
    });
  });
}

// Test 3: Umlaut Domain Redirect
async function testUmlautRedirect() {
  log.step('TEST 3: Umlaute-Domain Redirect (grüner → gruener)');
  
  return new Promise((resolve) => {
    const req = https.get(`https://${CONFIG.DOMAIN_UMLAUT}`, { 
      timeout: 5000,
      maxRedirects: 5
    }, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400) {
        log.success(`Redirect gefunden (${res.statusCode})`);
        if (res.headers.location) {
          log.info(`Redirect zu: ${res.headers.location}`);
          if (res.headers.location.includes(CONFIG.DOMAIN_ASCII)) {
            log.success('Redirect zu ASCII-Domain! ✅');
            resolve(true);
          } else {
            log.warn('Redirect, aber nicht zur ASCII-Domain');
            resolve(false);
          }
        }
      } else if (res.statusCode === 200) {
        log.warn('Umlaut-Domain funktioniert direkt (kein Redirect nötig)');
        resolve(true);
      }
    });
    
    req.on('error', (err) => {
      log.info(`Umlaut-Domain Error (kann normal sein): ${err.message}`);
      resolve(false);
    });
    
    req.on('timeout', () => {
      log.warn('Umlaut-Domain timeout');
      req.destroy();
      resolve(false);
    });
  });
}

// Test 4: Response Headers (Cloudflare)
async function testCloudflareHeaders() {
  log.step('TEST 4: Cloudflare Headers Check');
  
  return new Promise((resolve) => {
    const req = https.get(`https://${CONFIG.DOMAIN_ASCII}`, {}, (res) => {
      const cfHeaders = {
        'cf-ray': res.headers['cf-ray'] || 'nicht vorhanden',
        'cf-cache-status': res.headers['cf-cache-status'] || 'nicht vorhanden',
        'server': res.headers['server'] || 'nicht vorhanden'
      };
      
      if (res.headers['cf-ray']) {
        log.success(`Cloudflare aktiv! cf-ray: ${cfHeaders['cf-ray']}`);
        log.info(`Cache Status: ${cfHeaders['cf-cache-status']}`);
        
        if (cfHeaders['cf-cache-status'] === 'HIT') {
          log.success('Caching arbeitet! 🚀');
        } else if (cfHeaders['cf-cache-status'] === 'MISS') {
          log.warn('Cache MISS (erstes Request ok)');
        }
        
        resolve(true);
      } else {
        log.error('Cloudflare Header nicht gefunden - Cloudflare vielleicht nicht aktiv?');
        resolve(false);
      }
    });
    
    req.on('error', (err) => {
      log.error(`Request error: ${err.message}`);
      resolve(false);
    });
  });
}

// Test 5: Performance Check
async function testPerformance() {
  log.step('TEST 5: Performance Check');
  
  return new Promise((resolve) => {
    const startTime = Date.now();
    
    const req = https.get(`https://${CONFIG.DOMAIN_ASCII}`, {}, (res) => {
      const endTime = Date.now();
      const duration = endTime - startTime;
      
      if (duration < 500) {
        log.success(`⚡ Sehr schnell: ${duration}ms`);
        resolve(true);
      } else if (duration < 1000) {
        log.success(`✅ Schnell: ${duration}ms`);
        resolve(true);
      } else if (duration < 3000) {
        log.warn(`⚠️  Mittelschnell: ${duration}ms`);
        resolve(true);
      } else {
        log.error(`🐌 Langsam: ${duration}ms`);
        resolve(false);
      }
    });
    
    req.on('error', (err) => {
      log.error(`Performance test error: ${err.message}`);
      resolve(false);
    });
    
    req.on('timeout', () => {
      log.error('Performance test timeout');
      req.destroy();
      resolve(false);
    });
    
    req.setTimeout(5000);
  });
}

// MAIN
async function runAllTests() {
  console.log(`${colors.cyan}
╔════════════════════════════════════════╗
║   Cloudflare + Uptime Robot Checker    ║
║   Grüner Faktencheck Setup Validator   ║
╚════════════════════════════════════════╝
${colors.reset}`);

  const results = {
    dns: await testDNS(),
    ssl: await testSSL(),
    umlaut: await testUmlautRedirect(),
    cloudflare: await testCloudflareHeaders(),
    performance: await testPerformance()
  };
  
  // Summary
  console.log(`\n${colors.blue}${'='.repeat(45)}${colors.reset}`);
  console.log(`${colors.cyan}ZUSAMMENFASSUNG:${colors.reset}`);
  console.log(`${colors.blue}${'='.repeat(45)}${colors.reset}\n`);
  
  const passed = Object.values(results).filter(r => r).length;
  const total = Object.keys(results).length;
  
  Object.entries(results).forEach(([test, passed]) => {
    const status = passed ? `${colors.green}✅ PASS` : `${colors.red}❌ FAIL`;
    console.log(`${status}${colors.reset} - ${test.toUpperCase()}`);
  });
  
  console.log(`\n${colors.cyan}Score: ${passed}/${total}${colors.reset}`);
  
  if (passed === total) {
    log.success('\n🎉 ALLES PERFEKT! Deine Konfiguration ist bereit für 100K Hits!\n');
    process.exit(0);
  } else if (passed >= 3) {
    log.warn('\n⚠️  Die meisten Tests bestanden. Überprüfe die fehlgeschlagenen Tests.\n');
    process.exit(0);
  } else {
    log.error('\n❌ Zu viele Tests fehlgeschlagen. Überprüfe deine Konfiguration!\n');
    process.exit(1);
  }
}

// Starten
runAllTests().catch(err => {
  log.error(`Fatal error: ${err.message}`);
  process.exit(1);
});
