from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        name = request.form['name']
        beschreibung = request.form['beschreibung']
        kategorie = request.form['kategorie']
        zutaten = request.form.getlist('zutaten[]')
        mengen = request.form.getlist('mengen[]')
        einheiten = request.form.getlist('einheiten[]')

        connection = sqlite3.connect('einkaufsliste.db')
        cursor = connection.cursor()

        # Rezept speichern
        cursor.execute('INSERT INTO rezepte (name, beschreibung, kategorie) VALUES (?, ?, ?)',
                       (name, beschreibung, kategorie))
        rezept_id = cursor.lastrowid

        # Zutaten speichern
        for zutat, menge, einheit in zip(zutaten, mengen, einheiten):
            cursor.execute('INSERT INTO zutaten (rezept_id, name, menge, einheit) VALUES (?, ?, ?, ?)',
                           (rezept_id, zutat, menge, einheit))

        connection.commit()
        connection.close()

        return redirect(url_for('list_recipes'))

    return render_template('add_recipe.html')

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




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
