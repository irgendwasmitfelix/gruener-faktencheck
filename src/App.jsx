import React, { useState, useEffect } from "react";
import { articles } from "./articles";
import { Helmet } from "react-helmet";

function getDomain(url) {
  try {
    return new URL(url).hostname.replace("www.", "");
  } catch {
    return url;
  }
}

function App() {
  const year = new Date().getFullYear();
  const [search, setSearch] = useState("");
  const [openCategories, setOpenCategories] = useState({});
  const [showScrollTop, setShowScrollTop] = useState(false);
  const [darkmode, setDarkmode] = useState(false);

  // Darkmode Toggle mit State
  useEffect(() => {
    if (darkmode) {
      document.body.classList.add("darkmode");
    } else {
      document.body.classList.remove("darkmode");
    }
  }, [darkmode]);

  // Toggle-Funktion
  const toggleCategory = (category) => {
    setOpenCategories((prev) => ({
      ...prev,
      [category]: !prev[category],
    }));
  };

  // Tastaturbedienung für Kategorie-Reiter
  const handleCategoryKey = (e, category) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      toggleCategory(category);
    }
  };

  // Filtert alle Artikel nach Suchbegriff (in Titel)
  const filteredArticles = Object.fromEntries(
    Object.entries(articles).map(([category, list]) => [
      category,
      list.filter(article =>
        article.title.toLowerCase().includes(search.toLowerCase())
      ),
    ])
  );

  // Kategorien mit Treffern automatisch öffnen, wenn gesucht wird, sonst zuklappen
 // Kategorien mit Treffern automatisch öffnen, wenn gesucht wird, sonst zuklappen
  useEffect(() => {
  if (search.trim() !== "") {
    const open = {};
    for (const [category, list] of Object.entries(filteredArticles)) {
      if (list.length > 0) open[category] = true;
    }
    setOpenCategories(open);
  } else {
    setOpenCategories({});
  }
}, [search]); // NUR search als Abhängigkeit, NICHT filteredArticles!

  // Scroll-Button anzeigen
  useEffect(() => {
    const onScroll = () => setShowScrollTop(window.scrollY > 300);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  // Strukturierte Daten (JSON-LD)
  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "Grüner Faktencheck",
    "url": "https://grüner-faktencheck.de/",
    "description": "Unabhängige Analyse und Faktenchecks zur Grünen Partei Deutschland",
    "potentialAction": {
      "@type": "SearchAction",
      "target": "https://grüner-faktencheck.de/?search={search_term_string}",
      "query-input": "required name=search_term_string"
    }
  };

  const hasResults = Object.values(filteredArticles).some(list => list.length > 0);

  return (
    <div className="container">
      <Helmet>
        <script type="application/ld+json">{JSON.stringify(jsonLd)}</script>
      </Helmet>
      <h1>Grüner Faktencheck</h1>
      
      {/* Darkmode Toggle Button */}
      <div style={{ textAlign: "center", marginBottom: "1.5em" }}>
        <button
          onClick={() => setDarkmode(!darkmode)}
          style={{
            padding: "0.5em 1em",
            borderRadius: "6px",
            border: "1px solid #217c3b",
            background: darkmode ? "#333" : "#eafbe7",
            color: darkmode ? "#fff" : "#217c3b",
            cursor: "pointer",
            fontSize: "0.9em",
            fontWeight: "bold",
            transition: "all 0.3s"
          }}
        >
          {darkmode ? "☀️ Light Mode" : "🌙 Dark Mode"}
        </button>
      </div>

      <div style={{ display: "flex", justifyContent: "center", marginBottom: "2em" }}>
        <label htmlFor="search" style={{ display: "none" }}>Suche Artikel</label>
        <input
          id="search"
          type="text"
          placeholder="Suche Artikel..."
          value={search}
          autoFocus
          onChange={e => setSearch(e.target.value)}
          style={{
            width: "100%",
            maxWidth: "400px",
            padding: "0.7em",
            fontSize: "1em",
            borderRadius: "6px",
            border: "1px solid #217c3b",
          }}
        />
      </div>

      {hasResults ? (
        Object.entries(filteredArticles).map(([category, list]) =>
          list.length > 0 ? (
            <div className="category-box" key={category}>
              <h2
                style={{ cursor: "pointer", userSelect: "none" }}
                tabIndex={0}
                onClick={() => toggleCategory(category)}
                onKeyDown={e => handleCategoryKey(e, category)}
                aria-expanded={!!openCategories[category]}
                role="button"
              >
                {category} {openCategories[category] ? "▲" : "▼"}
              </h2>
              {openCategories[category] &&
                list.map((article, idx) => (
                  <div className="article-teaser" key={article.url || idx}>
                    <h3>{article.title}</h3>
                    {(article.date || article.source) && (
                      <p style={{ fontSize: "0.95em", color: "#666", margin: "0 0 0.3em 0" }}>
                        {article.date && <span>{article.date}</span>}
                        {article.date && article.source && <span> &middot; </span>}
                        {article.source && <span>{article.source}</span>}
                      </p>
                    )}
                    <a href={article.url} target="_blank" rel="noopener noreferrer">
                      {getDomain(article.url)}
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
          ↑
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

export default App;