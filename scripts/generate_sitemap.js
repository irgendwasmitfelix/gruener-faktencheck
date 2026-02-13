const fs = require('fs');
const path = require('path');
const vm = require('vm');

const SRC = path.join(__dirname, '..', 'src', 'articles-enhanced.js');
const OUT = path.join(__dirname, '..', 'public', 'sitemap.xml');
const DOMAIN = 'https://gruener-faktencheck.de';

function loadArticles() {
  const src = fs.readFileSync(SRC, 'utf8');
  // Remove "export" and wrap in an object for evaluation
  const transformed = src.replace(/^\s*export\s+const\s+articles\s*=\s*/m, 'const articles = ');
  // Execute safely in VM
  const sandbox = {};
  vm.createContext(sandbox);
  try {
    vm.runInContext(transformed + '\n;globalThis.__ARTICLES__ = articles;', sandbox, { timeout: 1000 });
    return sandbox.__ARTICLES__;
  } catch (err) {
    console.error('Failed to parse articles file:', err.message);
    process.exit(1);
  }
}

function buildUrls(articles) {
  const urls = new Set();
  // static pages
  ['/', '/aussenpolitik.html', '/energie.html', '/innenpolitik.html', '/wirtschaft.html'].forEach(p => urls.add(DOMAIN + p));

  // categories
  Object.keys(articles).forEach(cat => {
    const slug = cat.toLowerCase().replace(/ä/g,'ae').replace(/ö/g,'oe').replace(/ü/g,'ue').replace(/ß/g,'ss').replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');
    urls.add(`${DOMAIN}/category/${slug}`);
    // article links (external) are included as outbound sources, but do not include external links in sitemap
  });

  return Array.from(urls);
}

function writeSitemap(list) {
  const lines = [];
  lines.push('<?xml version="1.0" encoding="UTF-8"?>');
  lines.push('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">');
  const now = new Date().toISOString().split('T')[0];
  list.forEach(loc => {
    lines.push('  <url>');
    lines.push(`    <loc>${loc}</loc>`);
    lines.push(`    <lastmod>${now}</lastmod>`);
    lines.push('    <changefreq>weekly</changefreq>');
    lines.push('    <priority>0.8</priority>');
    lines.push('  </url>');
  });
  lines.push('</urlset>');

  fs.writeFileSync(OUT, lines.join('\n'));
  console.log('Wrote sitemap to', OUT);
}

function main() {
  const articles = loadArticles();
  const urls = buildUrls(articles);
  writeSitemap(urls);
}

if (require.main === module) main();
