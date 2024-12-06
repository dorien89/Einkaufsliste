from app import db
from datetime import datetime

class ShoppingList(db.Model):
    __tablename__ = 'shopping_list'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete="CASCADE"), nullable=False)
    servings = db.Column(db.Float, nullable=False)
    
    # Relationships (optional, for ORM convenience)
    recipe = db.relationship('Recipe', backref=db.backref('shopping_lists', cascade='all, delete-orphan'))
    
    def __repr__(self):
        return f"<ShoppingList(id={self.id}, recipe_id={self.recipe_id}, servings={self.servings})>"