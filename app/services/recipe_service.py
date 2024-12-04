from app import db
from app.models.recipe import Recipe, Ingredient, RecipeIngredient

class RecipeService:
    @staticmethod
    def get_all_recipes():
        return Recipe.query.all()
    
    @staticmethod
    def create_recipe(name, description, category, ingredients_data):
        recipe = Recipe(name=name, description=description, category=category)
        db.session.add(recipe)
        
        for ing_data in ingredients_data:
            recipe_ingredient = RecipeIngredient(
                recipe=recipe,
                ingredient_id=ing_data['ingredient_id'],
                amount=ing_data['amount'],
                unit=ing_data['unit']
            )
            db.session.add(recipe_ingredient)
        
        db.session.commit()
        return recipe
    
    @staticmethod
    def delete_recipe(recipe_id):
        recipe = Recipe.query.get_or_404(recipe_id)
        db.session.delete(recipe)
        db.session.commit()
    
    @staticmethod
    def calculate_portions(recipe_id, portions):
        recipe = Recipe.query.get_or_404(recipe_id)
        calculated = []
        for ri in recipe.ingredients:
            ingredient = Ingredient.query.get(ri.ingredient_id)
            calculated.append({
                'name': ingredient.name,
                'amount': ri.amount * portions,
                'unit': ri.unit
            })
        return calculated