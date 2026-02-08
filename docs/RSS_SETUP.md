# RSS Feed Setup für Grüner Faktencheck

## 📡 RSS Feed ist jetzt aktiv!

Der RSS Feed wird automatisch bei jedem Build generiert und liegt unter:
```
https://grüner-faktencheck.de/feed.xml
```

## 🔄 Wie es funktioniert

1. **Automatische Generierung**: Mit jedem `npm run build` oder `npm run generate` wird `generate_rss.py` ausgeführt
2. **Datenquelle**: Alle Artikel aus `src/articles.js` werden automatisch ins RSS-Format konvertiert
3. **Kategorisierung**: Jeder Artikel wird mit seiner Kategorie (Wirtschaft, Innenpolitik, etc.) getaggt
4. **Unique GUIDs**: Jeder Artikel hat eine eindeutige ID basierend auf URL + Kategorie

## 🔗 RSS Feed mit n8n verwenden

### In n8n HTTP Request Node:
```
URL: https://grüner-faktencheck.de/feed.xml
Method: GET
Response format: XML (oder auto-detect)
```

### Mit CRON-Trigger:
```json
{
  "trigger": "Schedule",
  "interval": "0 */6 * * *",  // Alle 6 Stunden
  "nodes": [
    {
      "type": "n8n-nodes-base.httpRequest",
      "url": "https://grüner-faktencheck.de/feed.xml"
    },
    // Verarbeite die neuen Artikel hier
  ]
}
```

### RSS zu Datenbank (Beispiel):
```json
{
  "workflows": [
    {
      "HTTP Request (feed.xml)",
      "XML Parse",
      "Loop über items",
      "Database Insert/Update"
    }
  ]
}
```

## 📋 RSS Feed Struktur

Jeder Item enthält:
- `title`: Artikeltitel
- `link`: Vollständige URL zum Artikel
- `description`: Titel + Kategorie
- `category`: Die Kategorie (Wirtschaft, Innenpolitik, Außenpolitik)
- `guid`: Eindeutige Identifikation (nicht veränderbar)
- `pubDate`: Zeitstempel der Generierung

**Beispiel-Item:**
```xml
<item>
  <title>Parteispitze zu Freihandelsabkommen...</title>
  <link>https://taz.de/...</link>
  <description>Parteispitze zu Freihandelsabkommen... - Kategorie: Wirtschaft</description>
  <category>Wirtschaft</category>
  <guid isPermaLink="false">https://taz.de/.../#Wirtschaft</guid>
  <pubDate>Sun, 01 Feb 2026 18:07:18 +0000</pubDate>
</item>
```

## 🎯 n8n Anwendungsbeispiele

### Beispiel 1: Neue Artikel in Telegram posten
```
HTTP Request (Feed) 
→ XML Parse 
→ Filter (neue Items seit letztem Run)
→ Loop & Format
→ Telegram Send
```

### Beispiel 2: Artikel in Datenbank speichern
```
HTTP Request (Feed)
→ XML Parse
→ Loop über items
→ Check if exists in DB
→ Insert/Update in Database
```

### Beispiel 3: Feed zu RSS-Aggregator
```
HTTP Request (Feed)
→ Forward zu anderem RSS-Tool
```

## 🛠️ Manuell generieren

```bash
npm run generate     # Generiert Sitemap, RSS Feed und Static HTML
# oder nur RSS:
python generate_rss.py
```

## ✨ Zusätzliche Infos

- **Update-Frequenz**: Jedes Mal wenn du `npm run build` ausführst
- **Feed-URL**: `https://grüner-faktencheck.de/feed.xml`
- **Format**: RSS 2.0 (Standard)
- **Content-Type**: `application/rss+xml`
- **Encoding**: UTF-8

Die Feed-Datei wird bei jedem Build komplett neu generiert - alte Items werden nicht "erinnert". Wenn du nur neue/geänderte Items tracken möchtest, speichere die Feed-Datei in n8n und vergleiche.

## 📌 Hinweis für n8n

Falls n8n die XML nicht richtig parst, konvertiere zu JSON:
```json
{
  "node": "XML to JSON",
  "input": "feed.xml",
  "output": "JSON mit array von items"
}
```
