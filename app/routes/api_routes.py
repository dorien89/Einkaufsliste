from app import db
from flask import Blueprint, jsonify, request
from app.models.recipe import Recipe
from app.models.shopping_list import ShoppingList
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
        # Log incoming request data
        data = request.get_json()
        print("Incoming request data:", data)
        
        # Validate incoming data
        if not data or 'items' not in data:
            return jsonify({'error': 'No items provided'}), 400

        items = data['items']
        
        if not isinstance(items, list) or not all(isinstance(item, dict) for item in items):
            return jsonify({'error': 'Invalid format for items'}), 400
        
        # Create shopping list entries
        for item in items:
            if 'id' not in item or 'servings' not in item:
                return jsonify({'error': f"Invalid item format: {item}"}), 400

            shopping_list_item = ShoppingList(
                recipe_id=item['id'],
                servings=item['servings']
            )
            db.session.add(shopping_list_item)
        
        # Commit transaction
        db.session.commit()
        
        # Return success response
        return jsonify({
            'message': 'Shopping list saved successfully',
            'items_saved': len(items)
        }), 201
    
    except Exception as e:
        print(f"Error in save_shopping_list: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

