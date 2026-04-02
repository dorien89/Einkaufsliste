from app import db
from datetime import datetime

class ManualShoppingItem(db.Model):
    __tablename__ = 'manual_shopping_items'

    id            = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name          = db.Column(db.String(200), nullable=False)
    amount        = db.Column(db.Float, nullable=True)
    unit          = db.Column(db.String(50), nullable=True)
    shop_category = db.Column(db.String(100), nullable=False, default='Sonstiges')
    created_at    = db.Column(db.DateTime, server_default=db.func.now())
