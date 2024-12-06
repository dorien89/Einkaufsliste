from app import db
from flask import Blueprint, jsonify, request
from app.models.recipe import Recipe, RecipeIngredient, Ingredient
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

@bp.route('/shopping-list', methods=['GET'])
def get_shopping_list():
    try:
        
        print("\n=== Checking Database State ===")
        
        # Check recipe_ingredients table
        all_recipe_ingredients = RecipeIngredient.query.all()
        print(f"\nTotal recipe_ingredients entries: {len(all_recipe_ingredients)}")
        print("\nSample of recipe_ingredients:")
        for ri in all_recipe_ingredients[:5]:  # Show first 5
            print(f"Recipe {ri.recipe_id}: {ri.ingredient.name}, {ri.amount} {ri.unit}")
            
        
        print("\n=== Starting shopping list calculation ===")
        
        # Get all shopping list entries
        shopping_items = ShoppingList.query.all()
        print(f"\nShopping List Items:")
        for item in shopping_items:
            print(f"ID: {item.id}, Recipe ID: {item.recipe_id}, Servings: {item.servings}")
        
        consolidated = {}

        for item in shopping_items:
            print(f"\n--- Processing Recipe ID {item.recipe_id} ---")
            
            # Debug: Check if recipe exists
            recipe = Recipe.query.get(item.recipe_id)
            if recipe:
                print(f"Recipe found: {recipe}")
            else:
                print(f"WARNING: Recipe {item.recipe_id} not found!")
            
            # Get all ingredients for this recipe
            recipe_ingredients = RecipeIngredient.query.filter_by(recipe_id=item.recipe_id).all()
            print(f"Ingredients found for recipe {item.recipe_id}:")
            for ri in recipe_ingredients:
                print(f"  - ID: {ri.ingredient_id}, Amount: {ri.amount} {ri.unit}")
            
            for ri in recipe_ingredients:
                key = f"{ri.ingredient_id}_{ri.unit}"
                scaled_amount = ri.amount * item.servings
                
                # Debug: Print ingredient details
                print(f"\nProcessing ingredient:")
                print(f"  Key: {key}")
                print(f"  Name: {ri.ingredient.name}")
                print(f"  Original amount: {ri.amount}")
                print(f"  Scaled amount: {scaled_amount}")
                print(f"  Unit: {ri.unit}")
                
                if key in consolidated:
                    old_amount = consolidated[key]['amount']
                    consolidated[key]['amount'] += scaled_amount
                    print(f"  Updated amount from {old_amount} to {consolidated[key]['amount']}")
                else:
                    consolidated[key] = {
                        'name': ri.ingredient.name,
                        'amount': scaled_amount,
                        'unit': ri.unit
                    }
                    print(f"  Added new ingredient to consolidated list")

        print("\n=== Final consolidated ingredients ===")
        for key, value in consolidated.items():
            print(f"Key: {key}")
            print(f"  Name: {value['name']}")
            print(f"  Amount: {value['amount']} {value['unit']}")
        
        return jsonify({
            'success': True,
            'ingredients': list(consolidated.values())
        })

    except Exception as e:
        print(f"ERROR in get_shopping_list: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500