from app import db

class Recipe(db.Model):
    __tablename__ = 'recipes'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String)
    
    @classmethod
    def get_random(cls, limit=3):
        return cls.query.order_by(db.func.random()).limit(limit).all()

    def __repr__(self):
        return f"<Recipe(id={self.id}, name={self.name}, category={self.category})>"

class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)
    
    def __repr__(self):
        return f"<Ingredient(id={self.id}, name={self.name})>"

class RecipeIngredient(db.Model):
    __tablename__ = 'recipe_ingredients'
    
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete="CASCADE"), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id', ondelete="CASCADE"), primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String, nullable=False)
    
    # Relationships (optional, for ORM convenience)
    recipe = db.relationship('Recipe', backref=db.backref('recipe_ingredients', cascade='all, delete-orphan'))
    ingredient = db.relationship('Ingredient', backref=db.backref('recipe_ingredients', cascade='all, delete-orphan'))
    
    def __repr__(self):
        return (f"<RecipeIngredient(recipe_id={self.recipe_id}, ingredient_id={self.ingredient_id}, "
                f"amount={self.amount}, unit={self.unit})>")