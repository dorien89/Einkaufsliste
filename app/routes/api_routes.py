from app import db
from flask import Blueprint, jsonify, request
from app.models.recipe import Recipe, RecipeIngredient, Ingredient
from app.models.shopping_list import ShoppingList
from app.services.recipe_service import RecipeService
import random
from datetime import datetime

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/ingredients', methods=['GET'])
def search_ingredients():
    q = request.args.get('q', '').strip()
    query = Ingredient.query
    if q:
        query = query.filter(Ingredient.name.ilike(f'%{q}%'))
    ingredients = query.order_by(Ingredient.name).all()
    return jsonify([{'id': i.id, 'name': i.name, 'default_unit': i.default_unit or ''} for i in ingredients])

@bp.route('/ingredients', methods=['POST'])
def create_ingredient():
    data = request.get_json()
    name = data.get('name', '').strip()
    if not name:
        return jsonify({'error': 'Name required'}), 400
    existing = Ingredient.query.filter(Ingredient.name.ilike(name)).first()
    if existing:
        return jsonify({'id': existing.id, 'name': existing.name, 'default_unit': existing.default_unit or ''})
    ingredient = Ingredient(name=name)
    db.session.add(ingredient)
    db.session.commit()
    return jsonify({'id': ingredient.id, 'name': ingredient.name, 'default_unit': ''}), 201

@bp.route('/ingredients/<int:ingredient_id>', methods=['PUT'])
def update_ingredient(ingredient_id):
    ingredient = Ingredient.query.get_or_404(ingredient_id)
    data = request.get_json()
    name = data.get('name', '').strip()
    if not name:
        return jsonify({'error': 'Name required'}), 400
    ingredient.name = name
    if 'default_unit' in data:
        ingredient.default_unit = data['default_unit'].strip() or None
    db.session.commit()
    return jsonify({'id': ingredient.id, 'name': ingredient.name, 'default_unit': ingredient.default_unit or ''})

@bp.route('/ingredients/<int:ingredient_id>', methods=['DELETE'])
def delete_ingredient(ingredient_id):
    ingredient = Ingredient.query.get_or_404(ingredient_id)
    in_use = RecipeIngredient.query.filter_by(ingredient_id=ingredient_id).first()
    if in_use:
        return jsonify({'error': 'Ingredient is used in recipes'}), 400
    db.session.delete(ingredient)
    db.session.commit()
    return jsonify({'success': True})

@bp.route('/recipe/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    ingredients = []
    for ri in recipe.recipe_ingredients:
        ingredient = Ingredient.query.get(ri.ingredient_id)
        ingredients.append({
            'ingredient_id': ri.ingredient_id,
            'name': ingredient.name,
            'amount': ri.amount,
            'unit': ri.unit
        })
    return jsonify({
        'id': recipe.id,
        'name': recipe.name,
        'description': recipe.description or '',
        'category': recipe.category or '',
        'ingredients': ingredients
    })

@bp.route('/recipe', methods=['POST'])
def create_recipe_api():
    data = request.get_json()
    try:
        recipe = RecipeService.save_recipe(
            None, data['name'], data.get('description', ''), data.get('category', ''), data['ingredients']
        )
        return jsonify({'id': recipe.id, 'name': recipe.name}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/recipe/<int:recipe_id>', methods=['PUT'])
def update_recipe_api(recipe_id):
    data = request.get_json()
    try:
        recipe = RecipeService.save_recipe(
            recipe_id, data['name'], data.get('description', ''), data.get('category', ''), data['ingredients']
        )
        return jsonify({'id': recipe.id, 'name': recipe.name})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/recipe/<int:recipe_id>', methods=['DELETE'])
def delete_recipe_api(recipe_id):
    try:
        RecipeService.delete_recipe(recipe_id)
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/admin/shopping-list/clear', methods=['POST'])
def clear_shopping_list():
    try:
        ShoppingList.query.delete()
        db.session.commit()
        return jsonify({'message': 'Shopping list cleared successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/recipes/all')
def get_all_recipes():
    recipes = Recipe.query.order_by(Recipe.name).all()
    return jsonify([{'id': r.id, 'name': r.name, 'category': r.category} for r in recipes])

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