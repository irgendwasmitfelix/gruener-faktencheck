import React, { useState, useEffect } from 'react';
import { Link, useParams } from 'react-router-dom';
import { Helmet } from 'react-helmet';
import { articles } from './articles-enhanced';
import { categoryToSlug, resolveCategoryKey } from './category-seo';

function ArticleDetail() {
  const { category: categoryParam } = useParams();
  const resolvedCategory = resolveCategoryKey(categoryParam, articles);
  const category = resolvedCategory || categoryParam;
  const categorySlug = categoryToSlug(category || "");
  const [categoryArticles, setCategoryArticles] = useState([]);

  useEffect(() => {
    if (resolvedCategory && articles[resolvedCategory]) {
      setCategoryArticles(articles[resolvedCategory]);
    } else {
      setCategoryArticles([]);
    }
  }, [resolvedCategory]);

  const canonicalUrl = `https://grüner-faktencheck.de/category/${categorySlug}/articles`;
  
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

  if (!resolvedCategory) {
    return (
      <div className="article-collection">
        <h1>Kategorie "{categoryParam}" nicht gefunden</h1>
        <p>Diese Kategorie existiert nicht oder hat keine Artikel.</p>
        <Link to="/" style={{ textDecoration: "none", color: "#217c3b" }}>
          ← Zurück zur Startseite
        </Link>
      </div>
    );
  }

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
          <a href={article.url} target="_blank" rel="noopener noreferrer" className="read-more">
            Artikel lesen
          </a>
        </article>
      ))}
    </div>
  );
}

export default ArticleDetail;
