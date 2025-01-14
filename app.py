from flask import Flask, render_template
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

app = Flask(__name__)

@app.route('/')
def index():
    # Artikel-Daten
    articles = {
        "Politik und Gesellschaft": [
            {
                "title": "Klimaschutzprojekte in China: Milliardenbetrug in Ölbranche?",
                "url": "https://www.zdf.de/nachrichten/politik/deutschland/china-klimabetrug-mineraloel-ermittlungen-umweltausschuss-lemke-100.html",
                "date": "13.01.2025"
            },
            {
                "title": "Vorwürfe gegen Berliner Grünen-Politiker",
                "url": "https://www.rbb24.de/politik/beitrag/2024/12/gelbhaar-vorwuerfe-belaestigung-gruene-berlin-pankow.html",
                "date": "12.12.2024"
            },
            {
                "title": "Berliner Grüne wollen externe Meldestelle für Fälle sexueller Belästigung",
                "url": "https://www.tagesschau.de/inland/regional/berlin/rbb-nach-vorwuerfen-gegen-bundestagsabgeordneten-berliner-gruene-wollen-externe-meldestelle-fuer-faelle-sexueller-belaestigung-100.html",
                "date": "11.12.2024"
            },
            {
                "title": "Vorwürfe gegen Andreas Ewald: Wo bleibt der Staatsanwalt?",
                "url": "https://www.msn.com/de-de/nachrichten/politik/vorw%C3%BCrfe-gegen-andreas-ewald-wo-bleibt-der-staatsanwalt/ar-BB1rgQbW",
                "date": "10.12.2024"
            },
            {
                "title": 'Göring-Eckardt relativiert Hausdurchsuchung wegen "Schwachkopf"-Meme',
                "url": "https://apollo-news.net/das-geht-jetzt-nicht-mehr-goering-eckardt-relativiert-hausdurchsuchung-wegen-schwachkopf-meme/",
                "date": "09.12.2024"
            }
        ],
        "Wirtschaft und Politik (Habeck)": [
            {
                "title": "Die Habeck-Enthüllung und das Versagen der Medien",
                "url": "https://www.nius.de/kommentar/news/keine-silbe-in-der-tagesschau-die-habeck-enthuellung-und-das-gewaltige-versagen-der-medien/b15a84e4-8f20-4072-9681-8067f1acda7f",
                "date": "08.12.2024"
            },
            {
                "title": "Deutschland beim Wirtschaftswachstum auf dem letzten Platz",
                "url": "https://jungefreiheit.de/wirtschaft/2023/wachstum-deutschland-letzter/",
                "date": "07.12.2024"
            },
            {
                'title': 'Habeck feiert sich für freche, piratige Aktion',
                'url': 'https://apollo-news.net/illegale-siegestor-projektion-habeck-feiert-sich-fuer-freche-piratige-aktion/',
                'date': '06.12.2024'
            },
            {
                'title': 'Habeck-Behörde droht Facebook wegen Abschaffung von Zensoren',
                'url': 'https://jungefreiheit.de/politik/deutschland/2025/habeck-behoerde-droht-facebook-wegen-abschaffung-von-zensoren/',
                'date': '05.12.2024'
            },
            {
                'title': '600 Euro Strafe wegen Emoji: Habeck stellt Strafantrag',
                'url': 'https://www.nius.de/politik/news/600-euro-strafe-wegen-emoji-der-zeuge-habeck-fuehlt-sich-durch-in-seiner-ehre-verletzt-und-stellt-strafantrag/b0addc8c-ca2e-497c-8919-38f0e45083ad',
                'date': '04.12.2024'
            },
            {
                'title': 'NRW: Fünf Meldestellen gegen Hetze kosten 900.000 Euro pro Jahr',
                'url': 'https://www.bild.de/politik/inland/nrw-fuenf-meldestellen-gegen-hetze-kosten-900000-euro-pro-jahr',
                'date': '03.12.2024'
            },
            {
                'title': '90 Prozent aller Anzeigen von Bundestagsabgeordneten, stammen von Habeck und Bärbock',
                'url': 'https://www.focus.de/politik/deutsche-bundesminister-im-vergleich-mehr-als-90-prozent-der-anzeigen-gegen-buerger-stammen-von-habeck-und-baerbock_id_260500296.html',
                'date': '24.11.2024'
            },
            {
                'title': 'Cafe auf Rügen benennt sich wegen Habeck um - wollen nichts mit ihm zutun haben',
                'url': 'https://www.bild.de/regional/mecklenburg-vorpommern/news-inland/ruegen-caf-benennt-sich-um-name-habeck-war-schlecht-fuers-geschaeft-85091870.bild.html?',
                'date': '18.08.2023'
            },
        ],
        "Außenpolitik und Diplomatie (Baerbock)": [
            {
                'title': 'Baerbocks treffen mit Syrischen Islamisten',
                'url': 'https://www.bild.de/politik/ausland-und-internationales/annalena-baerbock-auf-fotos-in-syrien-von-islamisten-zensiert-677943390195b908c189a674',
                'date': '05.01.2025'
            },
            {
                'title': 'Baerbocks EM-Kurzstreckenflug und weitere Ministrecken-Flüge',
                'url': 'https://www.welt.de/politik/deutschland/article252604396/Auf-Baerbocks-EM-Kurzstreckenflug-folgtennochweitere-Ministrecken-Fluege.html',
                'date': '02.12.2024'
            },
            {
                'title': 'Nachtflug der Ampel-Regierung zum Fußball',
                'url': 'https://www.merkur.de/politik/nachtflugampel-regierung-fussball-frankfurt-annalenabaerbock-grueneolafscholz-flugzeug93165061.html',
                'date': '01.12.2024'
            },
            {
                'title': 'Facebook schmeißt Corrective Faktenchecker raus',
                'url': 'https://www.nius.de/medien/news/facebook-schmeisst-correctiv-und-alle-faktenchecker-raus/0ffc2f9c-b625-4906-9817-38ffe0dbc56e',
                'date': '07.01.2025'
            },
        ]
    }

    # Aktuelles Jahr für den Footer
    current_year = datetime.now().year

    return render_template('index.html', articles=articles, year=current_year)

if __name__ == '__main__':
    app.run(debug=True)
