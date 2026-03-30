from flask import Blueprint, render_template, request, redirect, url_for
from app.services.recipe_service import RecipeService
from app.models.recipe import Ingredient, Category

bp = Blueprint('recipe', __name__, url_prefix='/recipe')

@bp.route('/')
def list_recipes():
    recipes = RecipeService.get_all_recipes()
    return render_template('recipes.html', recipes=recipes)

@bp.route('/<int:recipe_id>/calculate', methods=['GET', 'POST'])
def calculate_ingredients(recipe_id):
    if request.method == 'POST':
        portions = float(request.form['portions'])
        ingredients = RecipeService.calculate_portions(recipe_id, portions)
        return render_template('calculated_ingredients.html', ingredients=ingredients, portions=portions)
    return render_template('input_portions.html')

@bp.route('/<int:recipe_id>/delete', methods=['POST'])
def delete_recipe(recipe_id):
    RecipeService.delete_recipe(recipe_id)
    return redirect(url_for('recipe.list_recipes'))

@bp.route('/ingredients')
def manage_ingredients():
    ingredients = Ingredient.query.order_by(Ingredient.name).all()
    return render_template('ingredients.html', ingredients=ingredients)

@bp.route('/categories')
def manage_categories():
    categories = Category.query.order_by(Category.name).all()
    return render_template('categories.html', categories=categories)

@bp.route('/bin')
def recipe_bin():
    return render_template('recipe_bin.html')

