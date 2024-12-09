import sqlite3
from difflib import SequenceMatcher

def similar(a, b, threshold=0.6):
    """Prüft die Ähnlichkeit zweier Strings"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio() > threshold

def check_similar_recipes(cursor, recipe_name):
    """Prüft ob ähnliche Rezepte existieren"""
    cursor.execute('SELECT name FROM recipes')
    existing_recipes = cursor.fetchall()
    similar_recipes = []
    
    for (existing_name,) in existing_recipes:
        if similar(recipe_name, existing_name):
            similar_recipes.append(existing_name)
    
    return similar_recipes

def import_recipe():
    connection = sqlite3.connect('./database/einkaufsliste.db')
    cursor = connection.cursor()
    
    try:
        recipe_name = "Fettuccine mit Lachs und getrockneten Tomaten in Honig-Balsamic-Sauce"
        
        # 1. Prüfe auf exakte und ähnliche Rezepte
        cursor.execute('SELECT id FROM recipes WHERE name = ?', (recipe_name,))
        if cursor.fetchone():
            print(f"Warnung: Rezept '{recipe_name}' existiert bereits exakt so in der Datenbank!")
            return
        
        similar_recipes = check_similar_recipes(cursor, recipe_name)
        if similar_recipes:
            print("\nWarnung: Ähnliche Rezepte gefunden:")
            for recipe in similar_recipes:
                print(f"- {recipe}")
            user_input = input("\nMöchten Sie trotzdem fortfahren? (j/n): ")
            if user_input.lower() != 'j':
                print("Import abgebrochen.")
                return
        
        # 2. Füge Rezept hinzu
        recipe_data = (
            recipe_name,
            "Pasta mit Lachs, getrockneten Tomaten und einer süß-sauren Honig-Balsamico-Sauce",
            "Hauptgericht"
        )
        
        cursor.execute('''
            INSERT INTO recipes (name, description, category)
            VALUES (?, ?, ?)
        ''', recipe_data)
        
        recipe_id = cursor.lastrowid
        
        # 3. Zutaten-Daten
        ingredients_data = [
            ('Zwiebel', 0.5, 'Stück'),
            ('Rucola', 15, 'g'),
            ('Schlagsahne', 75, 'g'),
            ('Lachsfilet', 100, 'g'),
            ('Pasta', 90, 'g'),
            ('Tomaten (getrocknet, in Öl)', 15, 'g'),
            ('Pfeffer', 1, 'Prise'),
            ('Salz', 1, 'Prise'),
            ('Honig', 0.5, 'TL'),
            ('Senf', 0.5, 'TL'),
            ('Knoblauch', 0.5, 'Zehe'),
            ('Balsamico-Essig', 1, 'EL')
        ]
        
        for ing_name, amount, unit in ingredients_data:
            # Prüfe ob Zutat existiert
            cursor.execute('SELECT id FROM ingredients WHERE name = ?', (ing_name,))
            result = cursor.fetchone()
            
            if result is None:
                # Zutat existiert nicht - füge sie hinzu
                cursor.execute('INSERT INTO ingredients (name) VALUES (?)', (ing_name,))
                ingredient_id = cursor.lastrowid
                print(f"Neue Zutat hinzugefügt: {ing_name}")
            else:
                ingredient_id = result[0]
                print(f"Vorhandene Zutat verwendet: {ing_name}")
            
            # Füge Rezept-Zutat hinzu
            cursor.execute('''
                INSERT INTO recipe_ingredients (recipe_id, ingredient_id, amount, unit)
                VALUES (?, ?, ?, ?)
            ''', (recipe_id, ingredient_id, amount, unit))
        
        connection.commit()
        print("\nRezept erfolgreich importiert!")
        
    except Exception as e:
        print(f"Fehler: {e}")
        connection.rollback()
    finally:
        connection.close()

if __name__ == '__main__':
    import_recipe()