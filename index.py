import requests, re
from bs4 import BeautifulSoup

from flask import Flask, jsonify, request

app = Flask(__name__)

# Die URL der Wikipedia-Seite
url = "https://de.wikipedia.org/wiki/One_Piece_(Anime)/Episodenliste"

# Die Anfrage an die URL senden und den HTML-Inhalt abrufen
response = requests.get(url)
html_content = response.content

# BeautifulSoup verwenden, um das HTML zu parsen
soup = BeautifulSoup(html_content, 'html.parser')

# Ein leeres Dictionary erstellen, um die Kapitel- und Episodendaten zu speichern
chapters_dict = {}
episode_count = 0

# Durch jede Tabelle iterieren
for wikitable in soup.find_all('table', class_='wikitable'):
    # Den Namen des Kapitels extrahieren
    chapter_name = wikitable.find_previous('h2').text.strip().replace('[Bearbeiten | Quelltext bearbeiten]','')

    # Diese Tabellen sollen ignoriert werden
    if re.search("Übersicht|Einzelnachweise|TV-Specials", chapter_name):
      continue
    
    # Ein leeres Dictionary für die Episoden dieses Kapitels erstellen
    episodes_dict = {}
    
    # Durch die Zeilen der Tabelle iterieren, beginnend ab der zweiten Zeile (die erste Zeile enthält Überschriften)
    for row in wikitable.find_all('tr')[1:]:
        columns = row.find_all('td')

        if len(columns) >= 3:
            episode_number = columns[0].text.strip()
            title = columns[1].text.strip()
            air_date = columns[2].text.strip()

            # Die Episodendaten diesem Kapitel hinzufügen
            episodes_dict[episode_number] = air_date

            # Episoden hochzählen
            episode_count += 1
    
    # Die Episoden diesem Kapitel im Kapitel-Dictionary zuordnen
    chapters_dict[chapter_name] = episodes_dict

# Es werden die Episoden zurueck gegeben
@app.route('/api/episodes', methods=['GET'])
def get_episodes():
    chapter_state = request.args.get('chapter')
    episode_number = request.args.get('number')
    episode_title = request.args.get('title')

    episodes = {}
    for episode_dict in chapters_dict.values():
        episodes.update(episode_dict)

    if chapter_state and chapter_state == 'false':
        return jsonify(episodes)
    
    elif episode_number:
        if episode_number in episodes:
            return jsonify({episode_number: episodes[episode_number]})
        else:
            response = jsonify(message="Episode not found")
            response.status_code = 404
            return response
    
    elif episode_title:
        for key, value in episodes.items():
            if re.search(episode_title, value):
                return jsonify({key: value})
        
        response = jsonify(message="Episode not found")
        response.status_code = 404
        return response


    else:
        return jsonify(chapters_dict)

# Es werden nur die einzelnen Chapter zurück gegeben
@app.route('/api/chapters', methods=['GET'])
def get_chapters():
    return jsonify(list(chapters_dict.keys()))

if __name__ == '__main__':
    print(f" Load Episodes {episode_count}")
    app.run(debug=True, host="0.0.0.0")
