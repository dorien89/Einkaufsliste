from flask import Blueprint, jsonify, request
from app.models.recipe import Recipe
import random

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/recipes')
def get_random_recipes():
    # Hier holen wir 3 zufällige Rezepte aus der Datenbank
    recipes = Recipe.get_random(limit=9)  # Diese Methode müssen Sie in Ihrem Recipe-Model implementieren
    return jsonify([{
        'id': recipe.id,
        'name': recipe.name
    } for recipe in recipes])


@bp.route('/shopping-list', methods=['POST'])
def save_shopping_list():
    try:
        data = request.get_json()
        items = data.get('items', [])
        
        # Hier später Shopping-List-Logik implementieren
        
        return jsonify({'message': 'Shopping list saved successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500