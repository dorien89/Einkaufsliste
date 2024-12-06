import sqlite3

def populate_database():
    connection = sqlite3.connect('./database/einkaufsliste.db')
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
        ('Zitronensaft',),
        ('Zucchini',),  # Für Lasagne
        ('Aubergine',),  # Für Lasagne
        ('Quinoa',),  # Für Quinoa-Salat
        ('Avocado',),  # Für Quinoa-Salat
        ('Feta',),  # Für Quinoa-Salat
        ('Äpfel',),  # Für Pfannkuchen
        ('Zimt',),  # Für Pfannkuchen
        ('Mehl',),  # Für Pfannkuchen & Quiche
        ('Eier',),  # Für verschiedene Rezepte
        ('Nori-Blätter',),  # Für Sushi
        ('Wasabi',),  # Für Sushi
        ('Sojasauce',),  # Für Sushi
        ('Schokolade',),  # Für Fondue
        ('Erdbeeren',),  # Für Fondue
        ('Bananen',),  # Für Fondue
        ('Marshmallows',),  # Für Fondue
        ('Kartoffeln',),  # Für Kartoffelsuppe
        ('Speck',),  # Für Kartoffelsuppe & Carbonara
        ('Mozzarella',),  # Für Caprese
        ('Mascarpone',),  # Für Tiramisu
        ('Himbeeren',),  # Für Tiramisu
        ('Löffelbiskuits',),  # Für Tiramisu
        ('Kakao',),  # Für Tiramisu
        ('Milch',),  # Für verschiedene Rezepte
        ('Backpulver',)  # Für Pfannkuchen
    ]

    # Realistische Daten für die Tabelle "rezepte"
    rezepte_data = [
        ('Pasta mit Tomatensauce', 'Ein einfaches Pasta-Gericht mit frischer Tomatensauce.', 'Hauptgericht'),
        ('Hähnchen Curry mit Reis', 'Ein aromatisches Curry mit zartem Hähnchen und Reis.', 'Hauptgericht'),
        ('Tomaten-Risotto', 'Ein schmackhaftes Risotto mit frischen Tomaten und Parmesan.', 'Hauptgericht'),
        ('Cheeseburger', 'Ein saftiger Burger mit Cheddar-Käse, Salat und Tomate.', 'Snack'),
        ('Honig-Senf-Nudeln mit Rucola und Lachs', 'Nudeln in einer Honig-Senf-Sauce, serviert mit frischem Rucola und gegrilltem Lachs.', 'Hauptgericht'),
        ('Vegetarische Lasagne', 'Eine Lasagne mit Zucchini, Auberginen und einer cremigen Béchamelsauce.', 'Hauptgericht'),
        ('Quinoa-Salat mit Avocado und Feta', 'Ein leichter Salat mit Quinoa, cremiger Avocado und würzigem Feta.', 'Beilage'),
        ('Pfannkuchen mit Apfel und Zimt', 'Fluffige Pfannkuchen mit karamellisierten Äpfeln und einer Prise Zimt.', 'Dessert'),
        ('Sushi-Platte', 'Eine Auswahl an frischem Sushi, darunter Maki und Nigiri.', 'Snack'),
        ('Schokoladenfondue mit Früchten', 'Geschmolzene Schokolade zum Dippen mit Erdbeeren, Bananen und Marshmallows.', 'Dessert'),
        ('Kartoffelsuppe mit Speck', 'Eine cremige Suppe aus Kartoffeln, serviert mit knusprigem Speck.', 'Vorspeise'),
        ('Caprese-Salat', 'Ein erfrischender Salat mit Tomaten, Mozzarella und Basilikum.', 'Vorspeise'),
        ('Pasta Carbonara', 'Ein klassisches italienisches Nudelgericht mit Ei, Speck und Parmesan.', 'Hauptgericht'),
        ('Gemüse-Quiche', 'Eine Quiche mit Zwiebeln, Paprika und einer herzhaften Käsefüllung.', 'Hauptgericht'),
        ('Himbeer-Tiramisu', 'Ein sommerliches Tiramisu mit frischen Himbeeren und einer Mascarponecreme.', 'Dessert')
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
        (5, 19, 1, 'Prise'),   # Pfeffer: 1 Prise

        # Vegetarische Lasagne (ID: 6)
        (6, 30, 250, 'g'),  # Zucchini
        (6, 31, 250, 'g'),  # Aubergine
        (6, 7, 300, 'g'),  # Tomaten
        (6, 6, 2, 'Stück'),  # Zwiebeln
        (6, 5, 2, 'Zehen'),  # Knoblauch
        (6, 21, 200, 'ml'),  # Schlagsahne
        (6, 20, 50, 'g'),  # Parmesan
        (6, 16, 30, 'g'),  # Butter
        (6, 38, 2, 'Stück'),  # Eier

        # Quinoa-Salat (ID: 7)
        (7, 32, 200, 'g'),  # Quinoa
        (7, 33, 1, 'Stück'),  # Avocado
        (7, 34, 100, 'g'),  # Feta
        (7, 15, 50, 'g'),  # Rucola
        (7, 7, 200, 'g'),  # Tomaten
        (7, 17, 2, 'EL'),  # Olivenöl
        (7, 29, 2, 'EL'),  # Zitronensaft

        # Pfannkuchen (ID: 8)
        (8, 37, 200, 'g'),  # Mehl
        (8, 38, 2, 'Stück'),  # Eier
        (8, 53, 250, 'ml'),  # Milch
        (8, 16, 50, 'g'),  # Butter
        (8, 35, 2, 'Stück'),  # Äpfel
        (8, 36, 1, 'TL'),  # Zimt
        (8, 23, 2, 'EL'),  # Honig
        (8, 54, 1, 'TL'),  # Backpulver

        # Sushi-Platte (ID: 9)
        (9, 2, 300, 'g'),  # Reis
        (9, 4, 200, 'g'),  # Lachsfilet
        (9, 39, 5, 'Blatt'),  # Nori-Blätter
        (9, 40, 1, 'TL'),  # Wasabi
        (9, 41, 50, 'ml'),  # Sojasauce

        # Schokoladenfondue (ID: 10)
        (10, 42, 200, 'g'),  # Schokolade
        (10, 21, 100, 'ml'),  # Schlagsahne
        (10, 43, 200, 'g'),  # Erdbeeren
        (10, 44, 2, 'Stück'),  # Bananen
        (10, 45, 100, 'g'),  # Marshmallows

        # Kartoffelsuppe (ID: 11)
        (11, 46, 500, 'g'),  # Kartoffeln
        (11, 47, 100, 'g'),  # Speck
        (11, 6, 2, 'Stück'),  # Zwiebeln
        (11, 21, 200, 'ml'),  # Schlagsahne
        (11, 16, 30, 'g'),  # Butter

        # Caprese-Salat (ID: 12)
        (12, 7, 400, 'g'),  # Tomaten
        (12, 48, 200, 'g'),  # Mozzarella
        (12, 14, 30, 'g'),  # Basilikum
        (12, 17, 3, 'EL'),  # Olivenöl

        # Pasta Carbonara (ID: 13)
        (13, 1, 400, 'g'),  # Pasta
        (13, 47, 150, 'g'),  # Speck
        (13, 38, 3, 'Stück'),  # Eier
        (13, 20, 100, 'g'),  # Parmesan
        (13, 5, 2, 'Zehen'),  # Knoblauch

        # Gemüse-Quiche (ID: 14)
        (14, 37, 250, 'g'),  # Mehl
        (14, 16, 125, 'g'),  # Butter
        (14, 38, 4, 'Stück'),  # Eier
        (14, 21, 200, 'ml'),  # Schlagsahne
        (14, 6, 2, 'Stück'),  # Zwiebeln
        (14, 8, 2, 'Stück'),  # Paprika
        (14, 20, 50, 'g'),  # Parmesan

        # Himbeer-Tiramisu (ID: 15)
        (15, 49, 250, 'g'),  # Mascarpone
        (15, 21, 200, 'ml'),  # Schlagsahne
        (15, 50, 300, 'g'),  # Himbeeren
        (15, 51, 200, 'g'),  # Löffelbiskuits
        (15, 52, 2, 'EL'),  # Kakao
        (15, 38, 3, 'Stück')  # Eier
    ]

    # Tabellen mit Daten befüllen
    try:
        # Zutaten einfügen
        cursor.executemany('INSERT OR IGNORE INTO ingredients (name) VALUES (?)', zutaten_data)

        # Rezepte einfügen
        cursor.executemany('INSERT INTO recipes (name, description, category) VALUES (?, ?, ?)', rezepte_data)

        # Rezeptliste einfügen
        cursor.executemany('INSERT INTO recipe_ingredients (recipe_id, ingredient_id, amount, unit) VALUES (?, ?, ?, ?)', rezeptliste_data)

        connection.commit()
        print("Tabellen erfolgreich mit realistischen Testdaten befüllt.")
    except sqlite3.Error as e:
        print("Fehler beim Einfügen der Daten:", e)
    finally:
        connection.close()

# Funktion aufrufen
populate_database()
