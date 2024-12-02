import sqlite3

def initialize_database():
    connection = sqlite3.connect('einkaufsliste.db')
    cursor = connection.cursor()

    # Tabellen erstellen
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS zutaten (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rezepte (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        beschreibung TEXT,
        kategorie TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rezeptliste (
        rezept_id INTEGER NOT NULL,
        zutat_id INTEGER NOT NULL,
        menge REAL NOT NULL,
        einheit TEXT NOT NULL,
        PRIMARY KEY (rezept_id, zutat_id),
        FOREIGN KEY (rezept_id) REFERENCES rezepte(id) ON DELETE CASCADE,
        FOREIGN KEY (zutat_id) REFERENCES zutaten(id) ON DELETE CASCADE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS einkaufsliste (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rezept_id INTEGER NOT NULL,
        portionen REAL NOT NULL,
        status INTEGER NOT NULL,
        FOREIGN KEY (rezept_id) REFERENCES rezepte(id) ON DELETE CASCADE
    )
    ''')

    # Verbindung schließen
    connection.commit()
    connection.close()
    print("Datenbank erfolgreich initialisiert.")

# Initialisieren der Datenbank
initialize_database()
