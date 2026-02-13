const fs = require('fs');
const path = require('path');
const vm = require('vm');

const SRC = path.join(__dirname, '..', 'src', 'articles-enhanced.js');

function loadArticles() {
  const src = fs.readFileSync(SRC, 'utf8');
  const transformed = src.replace(/^\s*export\s+const\s+articles\s*=\s*/m, 'const articles = ');
  const sandbox = {};
  vm.createContext(sandbox);
  try {
    vm.runInContext(transformed + '\n;globalThis.__ARTICLES__ = articles;', sandbox, { timeout: 2000 });
    return sandbox.__ARTICLES__ || {};
  } catch (err) {
    console.error('PARSE_ERROR:', err && err.message ? err.message : err);
    process.exit(2);
  }
}

function main() {
  const articles = loadArticles();
  // Simplify output to only what's needed (category -> list of {title, url})
  const output = {};
  Object.keys(articles).forEach(cat => {
    output[cat] = (articles[cat] || []).map(a => ({ title: a.title || '', url: a.url || '' }));
  });
  console.log(JSON.stringify(output));
}

if (require.main === module) main();
