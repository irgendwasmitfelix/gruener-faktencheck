import React from "react";
import { articles } from "./articles";

function App() {
  const year = new Date().getFullYear();

  return (
    <div className="container">
      <h1>Grüner Faktencheck</h1>
      {Object.entries(articles).map(([category, list]) => (
        <div className="category-box" key={category}>
          <h2>{category}</h2>
          {list.map((article, idx) => (
            <div className="article-teaser" key={idx}>
              <h3>{article.title}</h3>
              {/* Datum und Quelle falls vorhanden */}
              {(article.date || article.source) && (
                <p style={{ fontSize: "0.95em", color: "#666", margin: "0 0 0.3em 0" }}>
                  {article.date && <span>{article.date}</span>}
                  {article.date && article.source && <span> &middot; </span>}
                  {article.source && <span>{article.source}</span>}
                </p>
              )}
              <a href={article.url} target="_blank" rel="noopener noreferrer">
                Artikel lesen
              </a>
            </div>
          ))}
        </div>
      ))}
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