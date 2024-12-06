from flask import Blueprint, render_template, request, redirect, url_for
from app.services.recipe_service import RecipeService

bp = Blueprint('recipe', __name__, url_prefix='/recipe')

@bp.route('/')
def list_recipes():
    recipes = RecipeService.get_all_recipes()
    return render_template('recipes.html', recipes=recipes)

