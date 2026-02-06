import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Helmet } from 'react-helmet';
import { articles } from './articles-enhanced';

function ArticleDetail() {
  const { category } = useParams();
  const [categoryArticles, setCategoryArticles] = useState([]);

  useEffect(() => {
    if (category && articles[category]) {
      setCategoryArticles(articles[category]);
    }
  }, [category]);

  const canonicalUrl = `https://grüner-faktencheck.de/category/${category}`;
  
  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": `${category} - Grüner Faktencheck`,
    "description": `Alle ${category} Artikel mit kritischen Analysen zur Grünen Partei Deutschland`,
    "url": canonicalUrl,
    "mainEntity": {
      "@type": "ItemList",
      "itemListElement": categoryArticles.map((article, idx) => ({
        "@type": "NewsArticle",
        "position": idx + 1,
        "headline": article.title,
        "description": article.description || article.title,
        "keywords": article.keywords,
        "url": article.url
      }))
    }
  };

  return (
    <div className="article-collection">
      <Helmet>
        <title>{category} - Grüner Faktencheck 2026 | Unabhängige Analyse</title>
        <meta name="description" content={`Alle ${category} Artikel: Kritische Analysen zur Grünen Partei Deutschland mit Fokus auf Habeck, Baerbock und aktuelle Skandale.`} />
        <meta name="keywords" content={`${category}, Grüne Partei, Faktencheck, Kritik, Deutschland Politik 2026`} />
        <link rel="canonical" href={canonicalUrl} />
        <meta property="og:title" content={`${category} - Grüner Faktencheck`} />
        <meta property="og:description" content={`Faktencheck-Artikel zu Grüner ${category}`} />
        <meta property="og:url" content={canonicalUrl} />
        <meta property="og:type" content="website" />
        <script type="application/ld+json">{JSON.stringify(jsonLd)}</script>
      </Helmet>
      
      <h1>{category} - Grüner Faktencheck</h1>
      <p className="category-description">
        Lesen Sie {categoryArticles.length} kritische Artikel zur {category.toLowerCase()} der Grünen Partei
      </p>
      
      {categoryArticles.map((article, idx) => (
        <article key={article.url || idx} className="article-item">
          <h2>{article.title}</h2>
          {article.description && (
            <p className="article-description">{article.description}</p>
          )}
          {article.keywords && (
            <p className="article-tags">
              <strong>Tags:</strong> {article.keywords}
            </p>
          )}
          <a href={article.url} target="_blank" rel="noopener noreferrer" className="read-more">
            Artikel lesen
          </a>
        </article>
      ))}
    </div>
  );
}

export default ArticleDetail;
