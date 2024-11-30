import sqlite3

def populate_database():
    connection = sqlite3.connect('einkaufsliste.db')
    cursor = connection.cursor()

    # Beispiel-Daten für die Tabelle "zutaten"
    zutaten_data = [
        ('Mehl',),
        ('Zucker',),
        ('Eier',),
        ('Milch',),
        ('Butter',),
        ('Tomaten',),
        ('Käse',),
        ('Hefe',),
        ('Salz',)
    ]

    # Beispiel-Daten für die Tabelle "rezepte"
    rezepte_data = [
        ('Pfannkuchen', 'Leckere Pfannkuchen aus der Pfanne.', 'Dessert'),
        ('Pizza', 'Klassische italienische Pizza.', 'Hauptgericht'),
        ('Kuchen', 'Ein einfacher Kuchen.', 'Dessert')
    ]

    # Beispiel-Daten für die Tabelle "rezeptliste"
    rezeptliste_data = [
        (1, 1, 200, 'g'),  # Pfannkuchen: 200g Mehl
        (1, 2, 50, 'g'),   # Pfannkuchen: 50g Zucker
        (1, 3, 2, 'Stück'), # Pfannkuchen: 2 Eier
        (1, 4, 250, 'ml'),  # Pfannkuchen: 250ml Milch
        (2, 1, 300, 'g'),  # Pizza: 300g Mehl
        (2, 6, 200, 'g'),  # Pizza: 200g Tomaten
        (2, 7, 150, 'g'),  # Pizza: 150g Käse
        (2, 8, 1, 'Päckchen'),  # Pizza: 1 Päckchen Hefe
        (2, 9, 1, 'TL'),   # Pizza: 1 TL Salz
        (3, 1, 200, 'g'),  # Kuchen: 200g Mehl
        (3, 2, 100, 'g'),  # Kuchen: 100g Zucker
        (3, 3, 3, 'Stück'), # Kuchen: 3 Eier
        (3, 5, 100, 'g')   # Kuchen: 100g Butter
    ]

    # Tabellen mit Daten befüllen
    try:
        # Zutaten einfügen
        cursor.executemany('INSERT OR IGNORE INTO zutaten (name) VALUES (?)', zutaten_data)

        # Rezepte einfügen
        cursor.executemany('INSERT INTO rezepte (name, beschreibung, kategorie) VALUES (?, ?, ?)', rezepte_data)

        # Rezeptliste einfügen
        cursor.executemany('INSERT INTO rezeptliste (rezept_id, zutat_id, menge, einheit) VALUES (?, ?, ?, ?)', rezeptliste_data)

        connection.commit()
        print("Tabellen erfolgreich mit Beispiel-Daten befüllt.")
    except sqlite3.Error as e:
        print("Fehler beim Einfügen der Daten:", e)
    finally:
        connection.close()

# Funktion aufrufen
populate_database()
