// Verify that all URLs from articles.js match articles-enhanced.js
const articlesOriginal = require('./src/articles.js').articles;
const articlesEnhanced = require('./src/articles-enhanced.js').articles;

let errors = [];
let matches = 0;
let total = 0;

for (const category in articlesOriginal) {
  const originalCount = articlesOriginal[category].length;
  const enhancedCount = articlesEnhanced[category] ? articlesEnhanced[category].length : 0;
  
  console.log(`\n📋 Kategorie: ${category}`);
  console.log(`   Original: ${originalCount} Artikel`);
  console.log(`   Enhanced: ${enhancedCount} Artikel`);
  
  if (originalCount !== enhancedCount) {
    errors.push(`❌ ${category}: Unterschiedliche Anzahl (${originalCount} vs ${enhancedCount})`);
  }
  
  // Check each article
  articlesOriginal[category].forEach((origArticle, index) => {
    total++;
    const enhancedArticle = articlesEnhanced[category] ? 
      articlesEnhanced[category][index] : null;
    
    if (!enhancedArticle) {
      errors.push(`❌ ${category}[${index}]: Artikel fehlt in enhanced`);
      return;
    }
    
    // Compare URLs
    if (origArticle.url === enhancedArticle.url) {
      matches++;
    } else {
      errors.push(`❌ ${category}[${index}]: URL unterschiedlich`);
      console.log(`   Original: ${origArticle.url}`);
      console.log(`   Enhanced: ${enhancedArticle.url}`);
    }
  });
}

console.log(`\n${'='.repeat(60)}`);
console.log(`✅ VERIFIKATIONSERGEBNIS:`);
console.log(`   Insgesamt geprüft: ${total} Artikel`);
console.log(`   URLs korrekt: ${matches}/${total}`);
console.log(`    Match-Rate: ${((matches/total)*100).toFixed(1)}%`);
console.log(`${'='.repeat(60)}\n`);

if (errors.length > 0) {
  console.log(`⚠️  FEHLER GEFUNDEN (${errors.length}):`);
  errors.forEach(err => console.log(`   ${err}`));
  process.exit(1);
} else {
  console.log(`✅ ALLE LINKS SIND IDENTISCH! Alle URLs wurden korrekt übernommen.`);
  process.exit(0);
}
