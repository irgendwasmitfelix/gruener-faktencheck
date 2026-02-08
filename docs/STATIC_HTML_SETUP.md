# Static HTML Generator - Setup Guide

## Was macht das Script?

Das `generate_static_html.py` Script:
- ✅ Generiert für **jede Kategorie** eine separate HTML-Seite
- ✅ Optimiert für SEO (Schema.org JSON-LD, Canonical URLs, Meta-Tags)
- ✅ Lädt Seiten automatisch zu Hostinger hoch (optional)
- ✅ Kann als Cron-Job täglich/wöchentlich laufen

**Wichtig:** Das Script läuft **komplett unabhängig** von der React-App und beeinflusst **NICHT** die Performance!

---

## Setup auf PythonAnywhere

### 1. Script hochladen

1. Geh zu https://www.pythonanywhere.com/
2. Login in dein Account
3. Geh zu "Files" → `/home/dein-username/`
4. Lade die `generate_static_html.py` hoch

### 2. Credentials eintragen

In der Datei `generate_static_html.py` findest du:

```python
SFTP_HOST = "your-hostinger-sftp-server.com"
SFTP_USER = "your-sftp-username"
SFTP_PASS = "your-sftp-password"
```

**Wie du deine Hostinger-SFTP-Daten findest:**
1. Login bei Hostinger → Hosting → Mein Konto
2. Geh zu "FTP-Konten" oder "SSH/SFTP"
3. Kopiere Host, Username, Password

**ACHTUNG:** Speichere Credentials **NICHT** im Code! Verwende stattdessen Environment-Variablen:

```python
import os
SFTP_HOST = os.getenv("SFTP_HOST")
SFTP_USER = os.getenv("SFTP_USER")
SFTP_PASS = os.getenv("SFTP_PASS")
```

Auf PythonAnywhere: Geh zu "Web" → Bearbeite deine Web-App → "Environment Variables"

### 3. Dependencies installieren

Auf PythonAnywhere Terminal:
```bash
pip install paramiko
```

### 4. Cron-Job einrichten

1. Geh zu https://www.pythonanywhere.com/
2. "Tasks" oder "Scheduled tasks"
3. Neue Task hinzufügen:
   - **Zeit:** Z.B. täglich um 02:00 Uhr
   - **Befehl:** `python /home/dein-username/generate_static_html.py`

---

## Artikel-Daten aktualisieren

Das Script hat die Artikel aktuell hardcodiert. Um es dynamisch zu machen:

### Option A: Aus React-App importieren (BESTE LÖSUNG)

```python
# Statt hardcodierte ARTICLES, aus articles.js laden
import json

def load_articles_from_react():
    """Lädt articles.js und parsed sie"""
    # Du könntest auch eine API-Endpoint machen, die articles.js serviert
    with open("path/to/articles.json") as f:
        return json.load(f)

ARTICLES = load_articles_from_react()
```

### Option B: API-Endpoint

```python
import requests

def load_articles_from_api():
    response = requests.get("https://grüner-faktencheck.de/api/articles")
    return response.json()

ARTICLES = load_articles_from_api()
```

---

## Testing lokal

1. Lokal im Terminal testen:
```bash
python generate_static_html.py
```

2. Schau in den `./static_pages/` Ordner - dort sind die HTML-Dateien

---

## FAQ

**F: Wird die React-App verlangsamt?**
A: Nein! Das Script lädt nur nachts/geplant. Die React-App bleibt auf 807ms. ✅

**F: Was wenn die Credentials falsch sind?**
A: Script zeigt einen Error. Überprüf deine Hostinger-SFTP-Daten.

**F: Wie oft sollte das Script laufen?**
A: Empfohlen: **1x täglich** um 02:00 Uhr (nachts, wenig Traffic)

**F: Beeinflussen die statischen Seiten die React-App?**
A: Nein. Die liegen in einem separaten Ordner (`/public_html/`) und sind komplett unabhängig.

**F: Wie sieht die URL aus?**
A: Z.B. `https://grüner-faktencheck.de/wirtschaft.html`

---

## SEO-Bonus durch statische HTML

Mit statischen HTML-Seiten:
- ✅ Google indexiert schneller
- ✅ Bessere Core Web Vitals
- ✅ Featured Snippets möglich
- ✅ Höhere Rankings für spezifische Keywords pro Kategorie

---

## Support

Wenn es Probleme gibt, schau in die PythonAnywhere Logs:
1. "Web" → "Error log"
2. Oder "Tasks" → Task-Historie

