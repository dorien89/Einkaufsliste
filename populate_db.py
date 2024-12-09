import sqlite3
from datetime import datetime, timedelta

def populate_database():
    connection = sqlite3.connect('./database/einkaufsliste.db')
    cursor = connection.cursor()

    # Testdaten für die Tabelle "zutaten"
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
        ('Zucchini',),
        ('Aubergine',),
        ('Quinoa',),
        ('Avocado',),
        ('Feta',),
        ('Äpfel',),
        ('Zimt',),
        ('Mehl',),
        ('Eier',),
        ('Nori-Blätter',),
        ('Wasabi',),
        ('Sojasauce',),
        ('Schokolade',),
        ('Erdbeeren',),
        ('Bananen',),
        ('Marshmallows',),
        ('Kartoffeln',),
        ('Speck',),
        ('Mozzarella',),
        ('Mascarpone',),
        ('Himbeeren',),
        ('Löffelbiskuits',),
        ('Kakao',),
        ('Milch',),
        ('Backpulver',)
    ]

    # Testdaten für die Tabelle "rezepte"
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
        ('Himbeer-Tiramisu', 'Ein sommerliches Tiramisu mit frischen Himbeeren und einer Mascarponecreme.', 'Dessert'),
    ]

    rezeptliste_data = [
        # Pasta mit Tomatensauce (ID: 1)
        (1, 1, 100, 'g'),  # Pasta
        (1, 7, 150, 'g'),  # Tomaten
        (1, 6, 1, 'Stück'),  # Zwiebel
        (1, 17, 2, 'EL'),  # Olivenöl
        (1, 18, 1, 'Prise'),  # Salz
        (1, 19, 1, 'Prise'),  # Pfeffer
        (1, 20, 30, 'g'),  # Parmesan

        # Hähnchen Curry mit Reis (ID: 2)
        (2, 3, 150, 'g'),  # Hähnchenbrust
        (2, 2, 100, 'g'),  # Reis
        (2, 5, 1, 'Zehe'),  # Knoblauch
        (2, 10, 50, 'ml'),  # Kokosmilch
        (2, 11, 1, 'EL'),  # Currypaste
        (2, 14, 1, 'EL'),  # Basilikum
        (2, 18, 1, 'Prise'),  # Salz
        (2, 19, 1, 'Prise'),  # Pfeffer
        (2, 13, 1, 'Prise'),  # Kreuzkümmel

        # Tomaten-Risotto (ID: 3)
        (3, 2, 100, 'g'),  # Reis
        (3, 7, 150, 'g'),  # Tomaten
        (3, 5, 1, 'Zehe'),  # Knoblauch
        (3, 6, 1, 'Stück'),  # Zwiebel
        (3, 17, 2, 'EL'),  # Olivenöl
        (3, 20, 30, 'g'),  # Parmesan
        (3, 18, 1, 'Prise'),  # Salz
        (3, 19, 1, 'Prise'),  # Pfeffer

        # Cheeseburger (ID: 4)
        (4, 24, 1, 'Stück'),  # Burger-Brötchen
        (4, 25, 100, 'g'),  # Cheddar
        (4, 28, 1, 'EL'),  # Mayonnaise
        (4, 7, 2, 'Scheiben'),  # Tomate
        (4, 26, 50, 'g'),  # Salat
        (4, 27, 1, 'EL'),  # Ketchup

        # Honig-Senf-Nudeln mit Rucola und Lachs (ID: 5)
        (5, 1, 100, 'g'),   # Nudeln
        (5, 17, 1, 'EL'),   # Olivenöl
        (5, 22, 1, 'TL'),   # Senf
        (5, 23, 1, 'EL'),   # Honig
        (5, 15, 30, 'g'),   # Rucola
        (5, 4, 150, 'g'),   # Lachsfilet
        (5, 18, 1, 'Prise'), # Salz
        (5, 19, 1, 'Prise'), # Pfeffer

        # Vegetarische Lasagne (ID: 6)
        (6, 30, 250, 'g'),  # Zucchini
        (6, 31, 250, 'g'),  # Aubergine
        (6, 7, 300, 'g'),   # Tomaten
        (6, 6, 2, 'Stück'), # Zwiebeln
        (6, 5, 2, 'Zehen'), # Knoblauch
        (6, 21, 200, 'ml'), # Schlagsahne
        (6, 20, 50, 'g'),   # Parmesan
        (6, 16, 30, 'g'),   # Butter
        (6, 38, 2, 'Stück'), # Eier

        # Quinoa-Salat (ID: 7)
        (7, 32, 200, 'g'),  # Quinoa
        (7, 33, 1, 'Stück'), # Avocado
        (7, 34, 100, 'g'),  # Feta
        (7, 15, 50, 'g'),   # Rucola
        (7, 7, 200, 'g'),   # Tomaten
        (7, 17, 2, 'EL'),   # Olivenöl
        (7, 29, 2, 'EL'),   # Zitronensaft

        # Pfannkuchen (ID: 8)
        (8, 37, 200, 'g'),  # Mehl
        (8, 38, 2, 'Stück'), # Eier
        (8, 53, 250, 'ml'), # Milch
        (8, 16, 50, 'g'),   # Butter
        (8, 35, 2, 'Stück'), # Äpfel
        (8, 36, 1, 'TL'),   # Zimt
        (8, 23, 2, 'EL'),   # Honig
        (8, 54, 1, 'TL'),   # Backpulver

        # Sushi-Platte (ID: 9)
        (9, 2, 300, 'g'),   # Reis
        (9, 4, 200, 'g'),   # Lachsfilet
        (9, 39, 5, 'Blatt'), # Nori-Blätter
        (9, 40, 1, 'TL'),   # Wasabi
        (9, 41, 50, 'ml'),  # Sojasauce

        # Schokoladenfondue (ID: 10)
        (10, 42, 200, 'g'), # Schokolade
        (10, 21, 100, 'ml'), # Schlagsahne
        (10, 43, 200, 'g'), # Erdbeeren
        (10, 44, 2, 'Stück'), # Bananen
        (10, 45, 100, 'g'), # Marshmallows

        # Kartoffelsuppe (ID: 11)
        (11, 46, 500, 'g'), # Kartoffeln
        (11, 47, 100, 'g'), # Speck
        (11, 6, 2, 'Stück'), # Zwiebeln
        (11, 21, 200, 'ml'), # Schlagsahne
        (11, 16, 30, 'g'),  # Butter

        # Caprese-Salat (ID: 12)
        (12, 7, 400, 'g'),  # Tomaten
        (12, 48, 200, 'g'), # Mozzarella
        (12, 14, 30, 'g'),  # Basilikum
        (12, 17, 3, 'EL'),  # Olivenöl

        # Pasta Carbonara (ID: 13)
        (13, 1, 400, 'g'),  # Pasta
        (13, 47, 150, 'g'), # Speck
        (13, 38, 3, 'Stück'), # Eier
        (13, 20, 100, 'g'), # Parmesan
        (13, 5, 2, 'Zehen'), # Knoblauch

        # Gemüse-Quiche (ID: 14)
        (14, 37, 250, 'g'), # Mehl
        (14, 16, 125, 'g'), # Butter
        (14, 38, 4, 'Stück'), # Eier
        (14, 21, 200, 'ml'), # Schlagsahne
        (14, 6, 2, 'Stück'), # Zwiebeln
        (14, 8, 2, 'Stück'), # Paprika
        (14, 20, 50, 'g'),  # Parmesan

        # Himbeer-Tiramisu (ID: 15)
        (15, 49, 250, 'g'), # Mascarpone
        (15, 21, 200, 'ml'), # Schlagsahne
        (15, 50, 300, 'g'), # Himbeeren
        (15, 51, 200, 'g'), # Löffelbiskuits
        (15, 52, 2, 'EL'),  # Kakao
        (15, 38, 3, 'Stück') # Eier
    ]

    # Beispiel-Einkaufsliste mit verschiedenen Stati
    shopping_list_data = [
        # Aktive Einkäufe
        (1, 2.0, 1, datetime.now(), None),  # Pasta für 2 Portionen
        (2, 4.0, 1, datetime.now(), None),  # Curry für 4 Portionen
        (3, 3.0, 1, datetime.now(), None),  # Risotto für 3 Portionen
        
        # Bereits gekaufte Artikel (Beispielhistorie)
        (4, 2.0, 0, datetime.now() - timedelta(days=2), datetime.now() - timedelta(days=1)),  # Cheeseburger
        (1, 3.0, 0, datetime.now() - timedelta(days=3), datetime.now() - timedelta(days=2)),  # Pasta
        (2, 2.0, 0, datetime.now() - timedelta(days=4), datetime.now() - timedelta(days=3))   # Curry
    ]

    try:
        # Zutaten einfügen
        cursor.executemany('INSERT OR IGNORE INTO ingredients (name) VALUES (?)', zutaten_data)

        # Rezepte einfügen
        cursor.executemany('INSERT INTO recipes (name, description, category) VALUES (?, ?, ?)', rezepte_data)

        # Rezeptliste einfügen
        cursor.executemany('''
            INSERT INTO recipe_ingredients 
            (recipe_id, ingredient_id, amount, unit) 
            VALUES (?, ?, ?, ?)
        ''', rezeptliste_data)

        # Einkaufsliste einfügen
        cursor.executemany('''
            INSERT INTO shopping_list 
            (recipe_id, servings, is_active, created_at, bought_at) 
            VALUES (?, ?, ?, ?, ?)
        ''', shopping_list_data)

        connection.commit()
        print("Tabellen erfolgreich mit Testdaten befüllt.")
        
    except sqlite3.Error as e:
        print("Fehler beim Einfügen der Daten:", e)
        connection.rollback()
    finally:
        connection.close()

if __name__ == "__main__":
    populate_database()