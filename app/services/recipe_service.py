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
    def save_recipe(recipe_id, name, description, category, ingredients_data):
        """Create or update a recipe. Pass recipe_id=None to create."""
        if recipe_id:
            recipe = Recipe.query.get_or_404(recipe_id)
            recipe.name = name
            recipe.description = description
            recipe.category = category
            RecipeIngredient.query.filter_by(recipe_id=recipe_id).delete()
        else:
            recipe = Recipe(name=name, description=description, category=category)
            db.session.add(recipe)
            db.session.flush()

        for ing_data in ingredients_data:
            ingredient_id = ing_data.get('ingredient_id')
            if not ingredient_id:
                existing = Ingredient.query.filter(Ingredient.name.ilike(ing_data['name'].strip())).first()
                if existing:
                    ingredient_id = existing.id
                else:
                    ingredient = Ingredient(name=ing_data['name'].strip())
                    db.session.add(ingredient)
                    db.session.flush()
                    ingredient_id = ingredient.id
            ri = RecipeIngredient(
                recipe_id=recipe.id,
                ingredient_id=ingredient_id,
                amount=ing_data['amount'],
                unit=ing_data['unit']
            )
            db.session.add(ri)

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