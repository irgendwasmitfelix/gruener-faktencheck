import React, { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { articles } from "./articles";
import { Helmet } from "react-helmet";

function getDomain(url) {
  try {
    return new URL(url).hostname.replace("www.", "");
  } catch {
    return url;
  }
}

function CategoryPage() {
  const { category } = useParams();
  const [darkmode, setDarkmode] = useState(false);
  const [showScrollTop, setShowScrollTop] = useState(false);
  
  const categoryArticles = articles[category] || [];
  const year = new Date().getFullYear();
  
  // Darkmode Toggle
  useEffect(() => {
    if (darkmode) {
      document.body.classList.add("darkmode");
    } else {
      document.body.classList.remove("darkmode");
    }
  }, [darkmode]);

  // Scroll-Button
  useEffect(() => {
    const onScroll = () => setShowScrollTop(window.scrollY > 300);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  // JSON-LD für Kategorie-Seite
  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": `Grüner Faktencheck - ${category}`,
    "url": `https://grüner-faktencheck.de/${category.toLowerCase()}`,
    "description": `Alle ${category}-Artikel zum Grünen Faktencheck. Kritische Analyse und Quellen.`
  };

  if (categoryArticles.length === 0) {
    return (
      <div className="container">
        <Link to="/" style={{ textDecoration: "none", color: "#217c3b", marginTop: "1em", display: "inline-block" }}>
          ← Zurück zur Startseite
        </Link>
        <h1>Kategorie "{category}" nicht gefunden</h1>
        <p>Diese Kategorie existiert nicht oder hat keine Artikel.</p>
      </div>
    );
  }

  return (
    <div className="container">
      <Helmet>
        <title>Grüner Faktencheck - {category}</title>
        <meta name="description" content={`${category} Artikel - Grüner Faktencheck: Unabhängige Analyse und Faktenchecks zur Grünen Partei.`} />
        <script type="application/ld+json">{JSON.stringify(jsonLd)}</script>
      </Helmet>

      <div className="hero-section">
        <h1>Grüner Faktencheck</h1>
        <p className="tagline">{category} - Unabhängige Faktenchecks zur Grünen Partei</p>
      </div>

      <div className="theme-toggle-container">
        <button
          onClick={() => setDarkmode(!darkmode)}
          className="theme-toggle-btn"
        >
          {darkmode ? "Light Mode" : "Dark Mode"}
        </button>
      </div>

      <Link to="/" style={{ textDecoration: "none", color: "#217c3b", marginBottom: "1em", display: "inline-block", fontSize: "1.1em" }}>
        ← Alle Kategorien
      </Link>

      <div className="category-box" style={{ marginTop: "2em" }}>
        <h2>{category}</h2>
        {categoryArticles.map((article, idx) => (
          <div className="article-teaser" key={article.url || idx}>
            <h3>{article.title}</h3>
            {(article.date || article.source) && (
              <p className="article-meta">
                {article.date && <span>{article.date}</span>}
                {article.date && article.source && <span className="meta-separator"> • </span>}
                {article.source && <span>{article.source}</span>}
              </p>
            )}
            <a href={article.url} target="_blank" rel="noopener noreferrer" className="article-link">
              Weiterlesen auf {getDomain(article.url)}
            </a>
          </div>
        ))}
      </div>

      {showScrollTop && (
        <button
          style={{
            position: "fixed",
            bottom: 30,
            right: 30,
            background: "#217c3b",
            color: "#fff",
            border: "none",
            borderRadius: "50%",
            width: 48,
            height: 48,
            fontSize: 28,
            cursor: "pointer",
            boxShadow: "0 2px 8px rgba(0,0,0,0.15)",
            zIndex: 1000
          }}
          aria-label="Nach oben"
          onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
        >
          ⬆
        </button>
      )}

      <footer>
        <p>
          Erstellt von:{" "}
          <a href="https://www.youtube.com/@reallifemitfelix" target="_blank" rel="noopener noreferrer">
            Felix H.
          </a>{" "}
          |{" "}
          <a href="https://paypal.me/Sparky512" target="_blank" rel="noopener noreferrer">
            Trinkgeld via PayPal
          </a>
        </p>
        <p>&copy; {year}</p>
      </footer>
    </div>
  );
}

export default CategoryPage;
