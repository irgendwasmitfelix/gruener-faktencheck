import React, { useState, useEffect } from "react";
import { articles } from "./articles";

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

  // Darkmode nur im Browser aktivieren
  useEffect(() => {
    document.body.classList.toggle("darkmode");
  }, []);

  // Toggle-Funktion
  const toggleCategory = (category) => {
    setOpenCategories((prev) => ({
      ...prev,
      [category]: !prev[category],
    }));
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
  }, [search, filteredArticles]);

  return (
    <div className="container">
      <h1>Grüner Faktencheck</h1>
      <div style={{ display: "flex", justifyContent: "center", marginBottom: "2em" }}>
        <input
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
            border: "1px solid #217c3b",
          }}
        />
      </div>
      {Object.entries(filteredArticles).map(([category, list]) =>
        list.length > 0 ? (
          <div className="category-box" key={category}>
            <h2
              style={{ cursor: "pointer", userSelect: "none" }}
              onClick={() => toggleCategory(category)}
            >
              {category} {openCategories[category] ? "▲" : "▼"}
            </h2>
            {openCategories[category] &&
              list.map((article, idx) => (
                <div className="article-teaser" key={idx}>
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