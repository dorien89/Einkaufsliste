import sqlite3
from datetime import datetime, timedelta

def populate_database():
    connection = sqlite3.connect('./database/einkaufsliste.db')
    cursor = connection.cursor()

    zutaten_data = [
        'Pasta', 'Reis', 'Hähnchenbrust', 'Lachsfilet', 'Knoblauch',
        'Zwiebel', 'Tomaten', 'Paprika', 'Brokkoli', 'Kokosmilch',
        'Currypaste', 'Chili', 'Kreuzkümmel', 'Basilikum', 'Rucola',
        'Butter', 'Olivenöl', 'Salz', 'Pfeffer', 'Parmesan',
        'Schlagsahne', 'Senf', 'Honig', 'Brot', 'Cheddar',
        'Salat', 'Ketchup', 'Mayonnaise', 'Zitronensaft', 'Zucchini',
        'Aubergine', 'Quinoa', 'Avocado', 'Feta', 'Äpfel',
        'Zimt', 'Mehl', 'Eier', 'Nori-Blätter', 'Wasabi',
        'Sojasauce', 'Schokolade', 'Erdbeeren', 'Bananen', 'Marshmallows',
        'Kartoffeln', 'Speck', 'Mozzarella', 'Mascarpone', 'Himbeeren',
        'Löffelbiskuits', 'Kakao', 'Milch', 'Backpulver',
    ]

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

    # Recipe ingredients defined by name instead of hardcoded IDs
    rezeptliste_data = [
        # Pasta mit Tomatensauce
        ('Pasta mit Tomatensauce', 'Pasta', 100, 'g'),
        ('Pasta mit Tomatensauce', 'Tomaten', 150, 'g'),
        ('Pasta mit Tomatensauce', 'Zwiebel', 1, 'Stück'),
        ('Pasta mit Tomatensauce', 'Olivenöl', 2, 'EL'),
        ('Pasta mit Tomatensauce', 'Salz', 1, 'Prise'),
        ('Pasta mit Tomatensauce', 'Pfeffer', 1, 'Prise'),
        ('Pasta mit Tomatensauce', 'Parmesan', 30, 'g'),

        # Hähnchen Curry mit Reis
        ('Hähnchen Curry mit Reis', 'Hähnchenbrust', 150, 'g'),
        ('Hähnchen Curry mit Reis', 'Reis', 100, 'g'),
        ('Hähnchen Curry mit Reis', 'Knoblauch', 1, 'Zehe'),
        ('Hähnchen Curry mit Reis', 'Kokosmilch', 50, 'ml'),
        ('Hähnchen Curry mit Reis', 'Currypaste', 1, 'EL'),
        ('Hähnchen Curry mit Reis', 'Basilikum', 1, 'EL'),
        ('Hähnchen Curry mit Reis', 'Salz', 1, 'Prise'),
        ('Hähnchen Curry mit Reis', 'Pfeffer', 1, 'Prise'),
        ('Hähnchen Curry mit Reis', 'Kreuzkümmel', 1, 'Prise'),

        # Tomaten-Risotto
        ('Tomaten-Risotto', 'Reis', 100, 'g'),
        ('Tomaten-Risotto', 'Tomaten', 150, 'g'),
        ('Tomaten-Risotto', 'Knoblauch', 1, 'Zehe'),
        ('Tomaten-Risotto', 'Zwiebel', 1, 'Stück'),
        ('Tomaten-Risotto', 'Olivenöl', 2, 'EL'),
        ('Tomaten-Risotto', 'Parmesan', 30, 'g'),
        ('Tomaten-Risotto', 'Salz', 1, 'Prise'),
        ('Tomaten-Risotto', 'Pfeffer', 1, 'Prise'),

        # Cheeseburger
        ('Cheeseburger', 'Brot', 1, 'Stück'),
        ('Cheeseburger', 'Cheddar', 100, 'g'),
        ('Cheeseburger', 'Mayonnaise', 1, 'EL'),
        ('Cheeseburger', 'Tomaten', 2, 'Scheiben'),
        ('Cheeseburger', 'Salat', 50, 'g'),
        ('Cheeseburger', 'Ketchup', 1, 'EL'),

        # Honig-Senf-Nudeln mit Rucola und Lachs
        ('Honig-Senf-Nudeln mit Rucola und Lachs', 'Pasta', 100, 'g'),
        ('Honig-Senf-Nudeln mit Rucola und Lachs', 'Olivenöl', 1, 'EL'),
        ('Honig-Senf-Nudeln mit Rucola und Lachs', 'Senf', 1, 'TL'),
        ('Honig-Senf-Nudeln mit Rucola und Lachs', 'Honig', 1, 'EL'),
        ('Honig-Senf-Nudeln mit Rucola und Lachs', 'Rucola', 30, 'g'),
        ('Honig-Senf-Nudeln mit Rucola und Lachs', 'Lachsfilet', 150, 'g'),
        ('Honig-Senf-Nudeln mit Rucola und Lachs', 'Salz', 1, 'Prise'),
        ('Honig-Senf-Nudeln mit Rucola und Lachs', 'Pfeffer', 1, 'Prise'),

        # Vegetarische Lasagne
        ('Vegetarische Lasagne', 'Zucchini', 250, 'g'),
        ('Vegetarische Lasagne', 'Aubergine', 250, 'g'),
        ('Vegetarische Lasagne', 'Tomaten', 300, 'g'),
        ('Vegetarische Lasagne', 'Zwiebel', 2, 'Stück'),
        ('Vegetarische Lasagne', 'Knoblauch', 2, 'Zehen'),
        ('Vegetarische Lasagne', 'Schlagsahne', 200, 'ml'),
        ('Vegetarische Lasagne', 'Parmesan', 50, 'g'),
        ('Vegetarische Lasagne', 'Butter', 30, 'g'),
        ('Vegetarische Lasagne', 'Eier', 2, 'Stück'),

        # Quinoa-Salat mit Avocado und Feta
        ('Quinoa-Salat mit Avocado und Feta', 'Quinoa', 200, 'g'),
        ('Quinoa-Salat mit Avocado und Feta', 'Avocado', 1, 'Stück'),
        ('Quinoa-Salat mit Avocado und Feta', 'Feta', 100, 'g'),
        ('Quinoa-Salat mit Avocado und Feta', 'Rucola', 50, 'g'),
        ('Quinoa-Salat mit Avocado und Feta', 'Tomaten', 200, 'g'),
        ('Quinoa-Salat mit Avocado und Feta', 'Olivenöl', 2, 'EL'),
        ('Quinoa-Salat mit Avocado und Feta', 'Zitronensaft', 2, 'EL'),

        # Pfannkuchen mit Apfel und Zimt
        ('Pfannkuchen mit Apfel und Zimt', 'Mehl', 200, 'g'),
        ('Pfannkuchen mit Apfel und Zimt', 'Eier', 2, 'Stück'),
        ('Pfannkuchen mit Apfel und Zimt', 'Milch', 250, 'ml'),
        ('Pfannkuchen mit Apfel und Zimt', 'Butter', 50, 'g'),
        ('Pfannkuchen mit Apfel und Zimt', 'Äpfel', 2, 'Stück'),
        ('Pfannkuchen mit Apfel und Zimt', 'Zimt', 1, 'TL'),
        ('Pfannkuchen mit Apfel und Zimt', 'Honig', 2, 'EL'),
        ('Pfannkuchen mit Apfel und Zimt', 'Backpulver', 1, 'TL'),

        # Sushi-Platte
        ('Sushi-Platte', 'Reis', 300, 'g'),
        ('Sushi-Platte', 'Lachsfilet', 200, 'g'),
        ('Sushi-Platte', 'Nori-Blätter', 5, 'Blatt'),
        ('Sushi-Platte', 'Wasabi', 1, 'TL'),
        ('Sushi-Platte', 'Sojasauce', 50, 'ml'),

        # Schokoladenfondue mit Früchten
        ('Schokoladenfondue mit Früchten', 'Schokolade', 200, 'g'),
        ('Schokoladenfondue mit Früchten', 'Schlagsahne', 100, 'ml'),
        ('Schokoladenfondue mit Früchten', 'Erdbeeren', 200, 'g'),
        ('Schokoladenfondue mit Früchten', 'Bananen', 2, 'Stück'),
        ('Schokoladenfondue mit Früchten', 'Marshmallows', 100, 'g'),

        # Kartoffelsuppe mit Speck
        ('Kartoffelsuppe mit Speck', 'Kartoffeln', 500, 'g'),
        ('Kartoffelsuppe mit Speck', 'Speck', 100, 'g'),
        ('Kartoffelsuppe mit Speck', 'Zwiebel', 2, 'Stück'),
        ('Kartoffelsuppe mit Speck', 'Schlagsahne', 200, 'ml'),
        ('Kartoffelsuppe mit Speck', 'Butter', 30, 'g'),

        # Caprese-Salat
        ('Caprese-Salat', 'Tomaten', 400, 'g'),
        ('Caprese-Salat', 'Mozzarella', 200, 'g'),
        ('Caprese-Salat', 'Basilikum', 30, 'g'),
        ('Caprese-Salat', 'Olivenöl', 3, 'EL'),

        # Pasta Carbonara
        ('Pasta Carbonara', 'Pasta', 400, 'g'),
        ('Pasta Carbonara', 'Speck', 150, 'g'),
        ('Pasta Carbonara', 'Eier', 3, 'Stück'),
        ('Pasta Carbonara', 'Parmesan', 100, 'g'),
        ('Pasta Carbonara', 'Knoblauch', 2, 'Zehen'),

        # Gemüse-Quiche
        ('Gemüse-Quiche', 'Mehl', 250, 'g'),
        ('Gemüse-Quiche', 'Butter', 125, 'g'),
        ('Gemüse-Quiche', 'Eier', 4, 'Stück'),
        ('Gemüse-Quiche', 'Schlagsahne', 200, 'ml'),
        ('Gemüse-Quiche', 'Zwiebel', 2, 'Stück'),
        ('Gemüse-Quiche', 'Paprika', 2, 'Stück'),
        ('Gemüse-Quiche', 'Parmesan', 50, 'g'),

        # Himbeer-Tiramisu
        ('Himbeer-Tiramisu', 'Mascarpone', 250, 'g'),
        ('Himbeer-Tiramisu', 'Schlagsahne', 200, 'ml'),
        ('Himbeer-Tiramisu', 'Himbeeren', 300, 'g'),
        ('Himbeer-Tiramisu', 'Löffelbiskuits', 200, 'g'),
        ('Himbeer-Tiramisu', 'Kakao', 2, 'EL'),
        ('Himbeer-Tiramisu', 'Eier', 3, 'Stück'),
    ]

    try:
        # Insert ingredients
        for name in zutaten_data:
            cursor.execute('INSERT OR IGNORE INTO ingredients (name) VALUES (?)', (name,))

        # Build ingredient name -> id lookup
        cursor.execute('SELECT id, name FROM ingredients')
        ingredient_ids = {name: id for id, name in cursor.fetchall()}

        # Insert recipes
        for name, description, category in rezepte_data:
            cursor.execute('INSERT INTO recipes (name, description, category) VALUES (?, ?, ?)',
                           (name, description, category))

        # Build recipe name -> id lookup
        cursor.execute('SELECT id, name FROM recipes')
        recipe_ids = {name: id for id, name in cursor.fetchall()}

        # Insert recipe ingredients using looked-up IDs
        for recipe_name, ingredient_name, amount, unit in rezeptliste_data:
            cursor.execute('''
                INSERT INTO recipe_ingredients (recipe_id, ingredient_id, amount, unit)
                VALUES (?, ?, ?, ?)
            ''', (recipe_ids[recipe_name], ingredient_ids[ingredient_name], amount, unit))

        connection.commit()
        print("Tabellen erfolgreich mit Testdaten befüllt.")

    except sqlite3.Error as e:
        print("Fehler beim Einfügen der Daten:", e)
        connection.rollback()
    finally:
        connection.close()

if __name__ == "__main__":
    populate_database()
