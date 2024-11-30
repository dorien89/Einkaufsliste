import sqlite3

def populate_database():
    connection = sqlite3.connect('einkaufsliste.db')
    cursor = connection.cursor()

    # Realistische Daten für die Tabelle "zutaten"
    zutaten_data = [
        ('Pasta',),
        ('Reis',),
        ('Hähnchenbrust',),
        ('Lachsfilet',),
        ('Knoblauch',),
        ('Zwiebel',),
        ('Tomaten',),
        ('Paprika',),
        ('Brokkoli',),
        ('Kokosmilch',),
        ('Currypaste',),
        ('Chili',),
        ('Kreuzkümmel',),
        ('Basilikum',),
        ('Rucola',),
        ('Butter',),
        ('Olivenöl',),
        ('Salz',),
        ('Pfeffer',),
        ('Parmesan',),
        ('Schlagsahne',),
        ('Senf',),
        ('Honig',),
        ('Brot',),
        ('Cheddar',),
        ('Salat',),
        ('Ketchup',),
        ('Mayonnaise',),
        ('Zitronensaft',)
    ]

    # Realistische Daten für die Tabelle "rezepte"
    rezepte_data = [
        ('Pasta mit Tomatensauce', 'Ein einfaches Pasta-Gericht mit frischer Tomatensauce.', 'Hauptgericht'),
        ('Hähnchen Curry mit Reis', 'Ein aromatisches Curry mit zartem Hähnchen und Reis.', 'Hauptgericht'),
        ('Tomaten-Risotto', 'Ein schmackhaftes Risotto mit frischen Tomaten und Parmesan.', 'Hauptgericht'),
        ('Cheeseburger', 'Ein saftiger Burger mit Cheddar-Käse, Salat und Tomate.', 'Snack'),
        ('Honig-Senf-Nudeln mit Rucola und Lachs', 'Nudeln in einer Honig-Senf-Sauce, serviert mit frischem Rucola und gegrilltem Lachs.', 'Hauptgericht')
    ]

    # Realistische Daten für die Tabelle "rezeptliste"
    rezeptliste_data = [
        # Pasta mit Tomatensauce
        (1, 1, 100, 'g'),  # Pasta: 100g
        (1, 7, 150, 'g'),  # Tomaten: 150g
        (1, 6, 1, 'Stück'),  # Zwiebel: 1
        (1, 15, 2, 'EL'),  # Olivenöl: 2 EL
        (1, 18, 1, 'Prise'),  # Salz: 1 Prise
        (1, 19, 1, 'Prise'),  # Pfeffer: 1 Prise
        (1, 20, 30, 'g'),  # Parmesan: 30g

        # Hähnchen Curry mit Reis
        (2, 3, 150, 'g'),  # Hähnchenbrust: 150g
        (2, 2, 100, 'g'),  # Reis: 100g
        (2, 5, 1, 'Zehe'),  # Knoblauch: 1 Zehe
        (2, 10, 50, 'ml'),  # Kokosmilch: 50ml
        (2, 11, 1, 'EL'),  # Currypaste: 1 EL
        (2, 14, 1, 'EL'),  # Basilikum: 1 EL
        (2, 18, 1, 'Prise'),  # Salz: 1 Prise
        (2, 19, 1, 'Prise'),  # Pfeffer: 1 Prise
        (2, 13, 1, 'Prise'),  # Kreuzkümmel: 1 Prise

        # Tomaten-Risotto
        (3, 1, 100, 'g'),  # Reis: 100g
        (3, 7, 150, 'g'),  # Tomaten: 150g
        (3, 5, 1, 'Zehe'),  # Knoblauch: 1 Zehe
        (3, 6, 1, 'Stück'),  # Zwiebel: 1
        (3, 15, 2, 'EL'),  # Olivenöl: 2 EL
        (3, 20, 30, 'g'),  # Parmesan: 30g
        (3, 18, 1, 'Prise'),  # Salz: 1 Prise
        (3, 19, 1, 'Prise'),  # Pfeffer: 1 Prise

        # Cheeseburger
        (4, 24, 1, 'Stück'),  # Burger-Brötchen: 1
        (4, 23, 100, 'g'),  # Cheddar: 100g
        (4, 15, 1, 'EL'),  # Mayonnaise: 1 EL
        (4, 7, 2, 'Scheiben'),  # Tomate: 2 Scheiben
        (4, 22, 50, 'g'),  # Salat: 50g
        (4, 21, 1, 'Stück'),  # Ketchup: 1 EL

        # Honig-Senf-Nudeln mit Rucola und Lachs
        (5, 1, 100, 'g'),  # Nudeln: 100g
        (5, 15, 1, 'EL'),  # Olivenöl: 1 EL
        (5, 16, 1, 'TL'),  # Senf: 1 TL
        (5, 17, 1, 'EL'),  # Honig: 1 EL
        (5, 14, 30, 'g'),  # Rucola: 30g
        (5, 4, 150, 'g'),  # Lachsfilet: 150g
        (5, 18, 1, 'Prise'),  # Salz: 1 Prise
        (5, 19, 1, 'Prise')   # Pfeffer: 1 Prise
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
        print("Tabellen erfolgreich mit realistischen Testdaten befüllt.")
    except sqlite3.Error as e:
        print("Fehler beim Einfügen der Daten:", e)
    finally:
        connection.close()

# Funktion aufrufen
populate_database()
