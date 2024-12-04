import sqlite3

def initialize_database():
   connection = sqlite3.connect('./database/einkaufsliste.db')
   cursor = connection.cursor()
   
   # Create tables
   cursor.execute('''
   CREATE TABLE IF NOT EXISTS ingredients (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       name TEXT NOT NULL UNIQUE
   )
   ''')
   
   cursor.execute('''
   CREATE TABLE IF NOT EXISTS recipes (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       name TEXT NOT NULL,
       description TEXT,
       category TEXT
   )
   ''')
   
   cursor.execute('''
   CREATE TABLE IF NOT EXISTS recipe_ingredients (
       recipe_id INTEGER NOT NULL,
       ingredient_id INTEGER NOT NULL,
       amount REAL NOT NULL,
       unit TEXT NOT NULL,
       PRIMARY KEY (recipe_id, ingredient_id),
       FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
       FOREIGN KEY (ingredient_id) REFERENCES ingredients(id) ON DELETE CASCADE
   )
   ''')
   
   cursor.execute('''
   CREATE TABLE IF NOT EXISTS shopping_list (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       recipe_id INTEGER NOT NULL,
       servings REAL NOT NULL,
       FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
   )
   ''')
   
   # Close connection
   connection.commit()
   connection.close()
   print("Database successfully initialized.")

# Initialize the database
if __name__ == '__main__':
   initialize_database()