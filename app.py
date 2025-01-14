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
            },
            {
                "title": "Vorwürfe gegen Berliner Grünen-Politiker",
                "url": "https://www.rbb24.de/politik/beitrag/2024/12/gelbhaar-vorwuerfe-belaestigung-gruene-berlin-pankow.html",
            },
            {
                "title": "Berliner Grüne wollen externe Meldestelle für Fälle sexueller Belästigung",
                "url": "https://www.tagesschau.de/inland/regional/berlin/rbb-nach-vorwuerfen-gegen-bundestagsabgeordneten-berliner-gruene-wollen-externe-meldestelle-fuer-faelle-sexueller-belaestigung-100.html",
            },
            {
                "title": "Vorwürfe gegen Andreas Ewald: Wo bleibt der Staatsanwalt?",
                "url": "https://www.msn.com/de-de/nachrichten/politik/vorw%C3%BCrfe-gegen-andreas-ewald-wo-bleibt-der-staatsanwalt/ar-BB1rgQbW",
            },
            {
                "title": 'Göring-Eckardt relativiert Hausdurchsuchung wegen "Schwachkopf"-Meme',
                "url": "https://apollo-news.net/das-geht-jetzt-nicht-mehr-goering-eckardt-relativiert-hausdurchsuchung-wegen-schwachkopf-meme/",
            },
             {
                "title": 'Alptraum Asylheim - Islamisten unkontrolliert ins Land gelassen?',
                "url": "https://archive.ph/hbENt",
            },
        ],
        "Wirtschaft und Politik (Habeck)": [
            {
                "title": "Die Habeck-Enthüllung und das Versagen der Medien",
                "url": "https://www.nius.de/kommentar/news/keine-silbe-in-der-tagesschau-die-habeck-enthuellung-und-das-gewaltige-versagen-der-medien/b15a84e4-8f20-4072-9681-8067f1acda7f",
            },
            {
                "title": "Deutschland beim Wirtschaftswachstum auf dem letzten Platz",
                "url": "https://jungefreiheit.de/wirtschaft/2023/wachstum-deutschland-letzter/",
            },
            {
                'title': 'Habeck feiert sich für freche, piratige Aktion',
                'url': 'https://apollo-news.net/illegale-siegestor-projektion-habeck-feiert-sich-fuer-freche-piratige-aktion/',
            },
            {
                'title': 'Habeck-Behörde droht Facebook wegen Abschaffung von Zensoren',
                'url': 'https://jungefreiheit.de/politik/deutschland/2025/habeck-behoerde-droht-facebook-wegen-abschaffung-von-zensoren/',
            },
            {
                'title': '600 Euro Strafe wegen Emoji: Habeck stellt Strafantrag',
                'url': 'https://www.nius.de/politik/news/600-euro-strafe-wegen-emoji-der-zeuge-habeck-fuehlt-sich-durch-in-seiner-ehre-verletzt-und-stellt-strafantrag/b0addc8c-ca2e-497c-8919-38f0e45083ad',
            },
            {
                'title': 'NRW: Fünf Meldestellen gegen Hetze kosten 900.000 Euro pro Jahr',
                'url': 'https://www.bild.de/politik/inland/nrw-fuenf-meldestellen-gegen-hetze-kosten-900000-euro-pro-jahr',
            },
            {
                'title': '90 Prozent aller Anzeigen von Bundestagsabgeordneten, stammen von Habeck und Bärbock',
                'url': 'https://www.focus.de/politik/deutsche-bundesminister-im-vergleich-mehr-als-90-prozent-der-anzeigen-gegen-buerger-stammen-von-habeck-und-baerbock_id_260500296.html',
            },
            {
                'title': 'Cafe auf Rügen benennt sich wegen Habeck um - wollen nichts mit ihm zutun haben',
                'url': 'https://www.bild.de/regional/mecklenburg-vorpommern/news-inland/ruegen-caf-benennt-sich-um-name-habeck-war-schlecht-fuers-geschaeft-85091870.bild.html?',
            },
        ],
        "Außenpolitik und Diplomatie (Baerbock)": [
            {
                'title': 'Baerbocks treffen mit Syrischen Islamisten',
                'url': 'https://www.bild.de/politik/ausland-und-internationales/annalena-baerbock-auf-fotos-in-syrien-von-islamisten-zensiert-677943390195b908c189a674',
            },
            {
                'title': 'Baerbocks EM-Kurzstreckenflug und weitere Ministrecken-Flüge',
                'url': 'https://www.welt.de/politik/deutschland/article252604396/Auf-Baerbocks-EM-Kurzstreckenflug-folgtennochweitere-Ministrecken-Fluege.html',
            },
            {
                'title': 'Nachtflug der Ampel-Regierung zum Fußball',
                'url': 'https://www.merkur.de/politik/nachtflugampel-regierung-fussball-frankfurt-annalenabaerbock-grueneolafscholz-flugzeug93165061.html',
            },
            {
                'title': 'Facebook schmeißt Corrective Faktenchecker raus',
                'url': 'https://www.nius.de/medien/news/facebook-schmeisst-correctiv-und-alle-faktenchecker-raus/0ffc2f9c-b625-4906-9817-38ffe0dbc56e',
            },
            {
                'title': 'Bärbock fordert Ausnahme für Heimatbesuche von Syrern',
                'url': 'https://www.welt.de/politik/deutschland/article255097076/Annalena-Baerbock-fordert-Ausnahmen-fuer-Heimatbesuche-von-Syrern.html',
            },
            {
                'title': 'Bärbock kündigt 8 Millionen Euro Hilfe für Islamisten an.',
                'url': 'https://apollo-news.net/baerbock-kndigt-acht-millionen-euro-hilfe-und-zusammenarbeit-mit-islamisten-terrormiliz-an/',
            },
            {
                'title': 'Bärbock hält Bundeswehr Einsatz von Deutschen Soldaten in der Ukraine für möglich.',
                'url': 'https://www.focus.de/politik/deutsche-rueckendeckung-baerbock-haelt-einsatz-der-bundeswehr-in-der-ukraine-fuer-moeglich_id_260534717.html',
            },
              {
                'title': 'Afghanistan-Programm: Baerbock will Tausende nach Deutschland einfliegen',
                'url': 'https://www.tichyseinblick.de/daili-es-sentials/afghanistan-programm-baerbock/',
            },
        ]
    }

    # Aktuelles Jahr für den Footer
    current_year = datetime.now().year

    return render_template('index.html', articles=articles, year=current_year)

if __name__ == '__main__':
    app.run(debug=True)
