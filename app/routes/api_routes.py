from flask import Blueprint, jsonify, request
from app.models.recipe import Recipe
import random

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/recipes', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.order_by(db.func.random()).limit(9).all()
    return jsonify([{"id": r.id, "name": r.name} for r in recipes])

@bp.route('/shopping-list', methods=['POST'])
def save_shopping_list():
    try:
        data = request.get_json()
        items = data.get('items', [])
        
        # Hier später Shopping-List-Logik implementieren
        
        return jsonify({'message': 'Shopping list saved successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500