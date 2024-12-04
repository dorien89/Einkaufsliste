from app import db

class Recipe(db.Model):
    __tablename__ = 'rezepte'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    ingredients = db.relationship('RecipeIngredient', backref='recipe', lazy=True)

class Ingredient(db.Model):
    __tablename__ = 'zutaten'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class RecipeIngredient(db.Model):
    __tablename__ = 'rezeptliste'
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('rezepte.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('zutaten.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)