import sqlite3

def initialize_database():
    # Verbindung zur Datenbank herstellen (erstellt die Datei, falls sie nicht existiert)
    connection = sqlite3.connect('einkaufsliste.db')
    cursor = connection.cursor()

    # Tabelle für Einkaufsartikel erstellen
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS artikel (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            menge INTEGER DEFAULT 1,
            kategorie TEXT DEFAULT 'Sonstiges',
            erledigt BOOLEAN DEFAULT 0
        )
    ''')

    # Änderungen speichern und Verbindung schließen
    connection.commit()
    connection.close()
    print("Datenbank erfolgreich initialisiert.")

def initialize_recipe_database():
    connection = sqlite3.connect('einkaufsliste.db')
    cursor = connection.cursor()

    # Tabelle für Rezepte
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rezepte (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            beschreibung TEXT,
            kategorie TEXT
        )
    ''')

    # Tabelle für Zutaten
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS zutaten (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rezept_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            menge REAL NOT NULL,
            einheit TEXT NOT NULL,
            FOREIGN KEY (rezept_id) REFERENCES rezepte (id)
        )
    ''')

    connection.commit()
    connection.close()
    print("Datenbank für Rezepte erfolgreich initialisiert.")

if __name__ == "__main__":
    initialize_database()
    initialize_recipe_database()
