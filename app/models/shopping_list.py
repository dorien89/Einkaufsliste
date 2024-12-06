from app import db
from datetime import datetime

class ShoppingList(db.Model):
    __tablename__ = 'shopping_list'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete="CASCADE"), nullable=False)
    servings = db.Column(db.Float, nullable=False)
    is_active = db.Column(db.Boolean, server_default='1', nullable=False)  # Sets default in DB
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    bought_at = db.Column(db.DateTime, nullable=True)