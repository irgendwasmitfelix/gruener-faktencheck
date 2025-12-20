import React, { useState, useEffect, useMemo } from "react";
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
  
  // Auto Dark Mode Detection
  const [darkmode, setDarkmode] = useState(() => {
    if (typeof window !== "undefined") {
      const saved = localStorage.getItem("darkmode");
      if (saved !== null) return saved === "true";
      return window.matchMedia("(prefers-color-scheme: dark)").matches;
    }
    return false;
  });
  
  const [showScrollTop, setShowScrollTop] = useState(false);
  const [search, setSearch] = useState("");
  
  const categoryArticles = articles[category] || [];
  const year = new Date().getFullYear();
  
  // Filter articles from ALL categories by search term
  const filteredArticles = useMemo(() => 
    Object.fromEntries(
      Object.entries(articles).map(([cat, list]) => [
        cat,
        list.filter(article =>
          article.title.toLowerCase().includes(search.toLowerCase())
        ),
      ])
    ), [search]
  );
  
  const hasResults = Object.values(filteredArticles).some(list => list.length > 0);
  
  // Darkmode Toggle mit LocalStorage
  useEffect(() => {
    localStorage.setItem("darkmode", darkmode);
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

      <div style={{ display: "flex", justifyContent: "center", marginBottom: "2em" }}>
        <label htmlFor="category-search" style={{ display: "none" }}>Suche Artikel</label>
        <input
          id="category-search"
          type="text"
          placeholder="Suche Artikel..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          style={{
            width: "100%",
            maxWidth: "400px",
            padding: "0.7em",
            fontSize: "1em",
            borderRadius: "6px",
            border: "1px solid #ddd",
            boxSizing: "border-box"
          }}
        />
      </div>

      {hasResults ? (
        Object.entries(filteredArticles).map(([cat, list]) =>
          list.length > 0 ? (
            <div className="category-box" key={cat} style={{ marginTop: "2em" }}>
              <h2>{cat}</h2>
              {list.map((article, idx) => (
                <div className="article-teaser" key={`${cat}-${article.url}-${idx}`}>
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
          ) : null
        )
      ) : search.trim() !== "" ? (
        <div style={{ textAlign: "center", color: "#888", margin: "2em 0", fontSize: "1.1em" }}>
          <p>Keine Treffer gefunden für „{search}"</p>
        </div>
      ) : null}

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
