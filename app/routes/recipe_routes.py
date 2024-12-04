from flask import Blueprint, render_template, request, redirect, url_for
from app.services.recipe_service import RecipeService

bp = Blueprint('recipe', __name__, url_prefix='/recipe')

@bp.route('/')
def list_recipes():
    recipes = RecipeService.get_all_recipes()
    return render_template('recipes.html', recipes=recipes)

@bp.route('/add', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        ingredients_data = [
            {
                'ingredient_id': ing_id,
                'amount': float(amount),
                'unit': unit
            }
            for ing_id, amount, unit in zip(
                request.form.getlist('ingredients[]'),
                request.form.getlist('amounts[]'),
                request.form.getlist('units[]')
            )
        ]
        RecipeService.create_recipe(
            name=request.form['name'],
            description=request.form['description'],
            category=request.form['category'],
            ingredients_data=ingredients_data
        )
        return redirect(url_for('recipe.list_recipes'))

@bp.route('/delete/<int:recipe_id>', methods=['POST'])
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for('recipe.list_recipes'))

@bp.route('/ingredients/<int:recipe_id>', methods=['GET'])
def get_ingredients(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    ingredients_html = '<ul>'
    for ri in recipe.ingredients:
        ingredient = Ingredient.query.get(ri.ingredient_id)
        ingredients_html += f'<li>{ingredient.name}: {ri.amount} {ri.unit}</li>'
    ingredients_html += '</ul>'
    return ingredients_html

@bp.route('/calculate/<int:recipe_id>', methods=['GET', 'POST'])
def calculate_ingredients(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    
    if request.method == 'POST':
        portions = int(request.form['portions'])
        calculated_ingredients = []
        for ri in recipe.ingredients:
            ingredient = Ingredient.query.get(ri.ingredient_id)
            calculated_ingredients.append({
                'name': ingredient.name,
                'amount': ri.amount * portions,
                'unit': ri.unit
            })
        return render_template('calculated_ingredients.html', 
                             ingredients=calculated_ingredients, 
                             portions=portions)
    
    return render_template('input_portions.html', recipe_id=recipe_id)