// Merge script: Combine articles.js (correct URLs) with articles-enhanced.js (SEO metadata)
const fs = require('fs');

// Read both files
const articlesOriginal = require('./src/articles.js').articles;
const articlesEnhanced = require('./src/articles-enhanced.js').articles;

// Helper function to find SEO metadata for an article
function findEnhancedMetadata(title, url, category) {
  if (articlesEnhanced[category]) {
    const enhanced = articlesEnhanced[category].find(art => 
      art.title.toLowerCase().replace(/[^a-z0-9]/g, '') === 
      title.toLowerCase().replace(/[^a-z0-9]/g, '')
    );
    if (enhanced) {
      return {
        description: enhanced.description || "",
        keywords: enhanced.keywords || ""
      };
    }
  }
  return {
    description: "",
    keywords: ""
  };
}

// Merge articles: Use URLs from articles.js, add SEO from articles-enhanced.js
const mergedArticles = {};

for (const category in articlesOriginal) {
  mergedArticles[category] = articlesOriginal[category].map(article => {
    const seo = findEnhancedMetadata(article.title, article.url, category);
    return {
      title: article.title,
      url: article.url,
      description: seo.description,
      keywords: seo.keywords
    };
  });
}

// Generate JavaScript export
const output = `export const articles = ${JSON.stringify(mergedArticles, null, 2)};
`;

// Write merged file
fs.writeFileSync('./src/articles-enhanced.js', output);

console.log('✅ Merged articles:');
for (const category in mergedArticles) {
  console.log(`  ${category}: ${mergedArticles[category].length} articles with correct URLs`);
}
console.log('\n✅ File updated: src/articles-enhanced.js');
