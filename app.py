from flask import Flask, request, render_template, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    connection = sqlite3.connect('einkaufsliste.db')
    cursor = connection.cursor()
    
    # Zutaten aus der Datenbank abrufen (Name und zutat_id)
    cursor.execute('SELECT id, name FROM zutaten')
    zutaten_liste = cursor.fetchall()
    connection.close()

    # Wenn das Formular abgesendet wurde, Rezept speichern
    if request.method == 'POST':
        name = request.form['name']
        beschreibung = request.form['beschreibung']
        kategorie = request.form['kategorie']
        zutaten_ids = request.form.getlist('zutaten[]')  # Enthält die zutat_id
        mengen = request.form.getlist('mengen[]')
        einheiten = request.form.getlist('einheiten[]')

        connection = sqlite3.connect('einkaufsliste.db')
        cursor = connection.cursor()

        # Rezept speichern
        cursor.execute('INSERT INTO rezepte (name, beschreibung, kategorie) VALUES (?, ?, ?)',
                       (name, beschreibung, kategorie))
        rezept_id = cursor.lastrowid

        # Zutaten in die rezeptliste-Tabelle speichern
        for zutat_id, menge, einheit in zip(zutaten_ids, mengen, einheiten):
            cursor.execute('INSERT INTO rezeptliste (rezept_id, zutat_id, menge, einheit) VALUES (?, ?, ?, ?)',
                           (rezept_id, zutat_id, menge, einheit))

        connection.commit()
        connection.close()
        return redirect(url_for('list_recipes'))

    return render_template('add_recipe.html', zutaten_liste=zutaten_liste)


@app.route('/get_ingredients/<int:rezept_id>', methods=['GET'])
def get_ingredients(rezept_id):
    connection = sqlite3.connect('einkaufsliste.db')
    cursor = connection.cursor()

    # Zutaten für das Rezept abrufen
    cursor.execute('SELECT z.name, r.menge, r.einheit '
                   'FROM rezeptliste r JOIN zutaten z ON r.zutat_id = z.id '
                   'WHERE r.rezept_id = ?', (rezept_id,))
    zutaten = cursor.fetchall()
    connection.close()

    # Zutaten als HTML-Liste zurückgeben
    if zutaten:
        zutaten_html = '<ul>'
        for zutat in zutaten:
            zutaten_html += f'<li>{zutat[0]}: {zutat[1]} {zutat[2]}</li>'
        zutaten_html += '</ul>'
        return zutaten_html
    else:
        return '<p>Keine Zutaten gefunden.</p>'



@app.route('/delete_recipe/<int:rezept_id>', methods=['POST'])
def delete_recipe(rezept_id):
    connection = sqlite3.connect('einkaufsliste.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM rezeptliste WHERE rezept_id = ?', (rezept_id,))
    rows = cursor.fetchall()
    print(rows)  # Sollte Ergebnisse zeigen, wenn die ID vorhanden ist

    # Rezept aus der Datenbank löschen
    cursor.execute('DELETE FROM rezepte WHERE id = ?', (rezept_id,))
    cursor.execute('DELETE FROM rezeptliste WHERE rezept_id = ?', (rezept_id,))

    # Änderungen speichern und Verbindung schließen
    connection.commit()
    connection.close()


    # Zur Liste der Rezepte zurückkehren
    return redirect(url_for('list_recipes'))



@app.route('/recipes', methods=['GET'])
def list_recipes():
    connection = sqlite3.connect('einkaufsliste.db')
    cursor = connection.cursor()

    # Rezepte abrufen (nur ID, Name und Kategorie)
    cursor.execute('SELECT id, name, kategorie FROM rezepte')
    rezepte = cursor.fetchall()

    connection.close()

    # Rezepte an das Template übergeben
    return render_template('recipes.html', rezepte=rezepte)



@app.route('/calculate_ingredients/<int:rezept_id>', methods=['GET', 'POST'])
def calculate_ingredients(rezept_id):
    if request.method == 'POST':
        portionen = int(request.form['portionen'])

        connection = sqlite3.connect('einkaufsliste.db')
        cursor = connection.cursor()

        # Zutaten für das Rezept abrufen
        cursor.execute('SELECT name, menge, einheit FROM zutaten WHERE rezept_id = ?', (rezept_id,))
        zutaten = cursor.fetchall()

        # Mengen anpassen
        berechnete_zutaten = [
            {'name': z[0], 'menge': z[1] * portionen, 'einheit': z[2]} for z in zutaten
        ]

        connection.close()
        return render_template('calculated_ingredients.html', zutaten=berechnete_zutaten, portionen=portionen)

    return render_template('input_portions.html', rezept_id=rezept_id)



# Datenbankverbindung herstellen
def get_db_connection():
    conn = sqlite3.connect('einkaufsliste.db')
    conn.row_factory = sqlite3.Row
    return conn

# Rezepte abrufen
@app.route('/api/rezepte', methods=['GET'])
def get_rezepte():
    conn = get_db_connection()
    rezepte = conn.execute('SELECT * FROM rezepte').fetchall()
    conn.close()
    return jsonify([dict(row) for row in rezepte])

# Einkaufsdaten speichern
@app.route('/api/einkaufsliste', methods=['POST'])
def save_einkaufsliste():
    data = request.json
    conn = get_db_connection()
    for item in data['items']:
        conn.execute(
            'INSERT INTO einkaufsliste (rezept_id, portionen, status) VALUES (?, ?, ?)',
            (item['rezept_id'], item['portionen'], 0)
        )
    conn.commit()
    conn.close()
    return jsonify({"message": "Einkaufsliste aktualisiert"})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
