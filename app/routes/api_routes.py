from app import db
from flask import Blueprint, jsonify, request
from app.models.recipe import Recipe, RecipeIngredient, Ingredient
from app.models.shopping_list import ShoppingList
import random
from datetime import datetime

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/admin/shopping-list/clear', methods=['POST'])
def clear_shopping_list():
    try:
        ShoppingList.query.delete()
        db.session.commit()
        return jsonify({'message': 'Shopping list cleared successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

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

@bp.route('/shopping-list', methods=['GET'])
def get_shopping_list():
    try:
        shopping_items = ShoppingList.query.filter_by(is_active=True).all()
        consolidated = {}
        
        for item in shopping_items:
            recipe_ingredients = RecipeIngredient.query.filter_by(recipe_id=item.recipe_id).all()
            
            for ri in recipe_ingredients:
                ingredient = Ingredient.query.get(ri.ingredient_id)
                key = f"{ri.ingredient_id}_{ri.unit}"
                
                if key in consolidated:
                    consolidated[key]['amount'] += ri.amount * item.servings
                else:
                    consolidated[key] = {
                        'id': ri.ingredient_id,
                        'name': ingredient.name,
                        'amount': ri.amount * item.servings,
                        'unit': ri.unit,
                        'shopping_list_id': item.id
                    }
        
        return jsonify({
            'success': True,
            'ingredients': list(consolidated.values())
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    
@bp.route('/shopping-list/draft', methods=['GET'])
def get_draft():
    try:
        items = ShoppingList.query.filter_by(is_active=True).all()
        result = []
        for item in items:
            recipe = Recipe.query.get(item.recipe_id)
            if recipe:
                result.append({'id': recipe.id, 'name': recipe.name, 'servings': item.servings})
        return jsonify({'success': True, 'items': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/shopping-list/item', methods=['POST'])
def upsert_item():
    try:
        data = request.get_json()
        recipe_id = data.get('id')
        if not recipe_id:
            return jsonify({'error': 'Missing recipe id'}), 400
        item = ShoppingList.query.filter_by(recipe_id=recipe_id, is_active=True).first()
        if item:
            item.servings += 1
        else:
            db.session.add(ShoppingList(recipe_id=recipe_id, servings=1))
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/shopping-list/item/<int:recipe_id>/servings', methods=['PATCH'])
def update_servings(recipe_id):
    try:
        data = request.get_json()
        servings = data.get('servings')
        if not servings or servings <= 0:
            return jsonify({'error': 'Invalid servings'}), 400
        item = ShoppingList.query.filter_by(recipe_id=recipe_id, is_active=True).first()
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        item.servings = servings
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/shopping-list/item/<int:recipe_id>', methods=['DELETE'])
def delete_item(recipe_id):
    try:
        ShoppingList.query.filter_by(recipe_id=recipe_id, is_active=True).delete()
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/shopping-list/mark-bought', methods=['POST'])  # /api is already in the blueprint prefix
def mark_items_bought():
    try:
        # Mark all active items as bought
        items = ShoppingList.query.filter_by(is_active=True).all()
        print(f"Found {len(items)} active items") # Debug log
        
        for item in items:
            item.is_active = False
            item.bought_at = datetime.utcnow()
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'All items marked as bought'})
    except Exception as e:
        print(f"Error: {str(e)}") # Debug log
        db.session.rollback()
        return jsonify({'error': str(e)}), 500