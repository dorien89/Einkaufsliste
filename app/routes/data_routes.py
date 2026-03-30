from flask import Blueprint, render_template, jsonify, request, Response
from app import db
from app.models.recipe import Recipe, Ingredient, RecipeIngredient, Category
from app.models.shopping_list import ShoppingList
from app.models.week_plan import WeekPlan
from app.services.recipe_service import RecipeService
from datetime import datetime, timezone
import json

bp = Blueprint('data', __name__, url_prefix='/daten')

# ── Page ─────────────────────────────────────────────────────────────────────

@bp.route('/')
def data_page():
    return render_template('daten.html')

# ── Helpers ───────────────────────────────────────────────────────────────────

def _recipes_payload():
    recipes = Recipe.query.filter(Recipe.deleted_at == None).order_by(Recipe.name).all()
    ingredients = Ingredient.query.order_by(Ingredient.name).all()
    categories = Category.query.order_by(Category.name).all()
    return {
        'categories': [c.name for c in categories],
        'ingredients': [
            {'name': i.name, 'default_unit': i.default_unit or '', 'is_staple': i.is_staple, 'shop_category': i.shop_category}
            for i in ingredients
        ],
        'recipes': [
            {
                'name': r.name,
                'category': r.category or '',
                'description': r.description or '',
                'ingredients': [
                    {'name': Ingredient.query.get(ri.ingredient_id).name, 'amount': ri.amount, 'unit': ri.unit}
                    for ri in r.recipe_ingredients
                ]
            }
            for r in recipes
        ]
    }

def _backup_payload():
    payload = _recipes_payload()
    week_plans = WeekPlan.query.all()
    shopping = ShoppingList.query.filter_by(is_active=True).all()
    payload['week_plan'] = [
        {
            'week_start': str(wp.week_start),
            'day_index': wp.day_index,
            'slot_index': wp.slot_index,
            'recipe_name': Recipe.query.get(wp.recipe_id).name if wp.recipe_id else None,
            'servings': wp.servings,
            'is_bought': wp.is_bought
        }
        for wp in week_plans
    ]
    payload['shopping_list'] = [
        {
            'recipe_name': Recipe.query.get(s.recipe_id).name if s.recipe_id else None,
            'servings': s.servings,
            'is_active': s.is_active
        }
        for s in shopping
    ]
    return payload

# ── Export endpoints ──────────────────────────────────────────────────────────

@bp.route('/export/recipes.json')
def export_recipes_json():
    payload = _recipes_payload()
    payload['type'] = 'recipes'
    payload['version'] = 1
    payload['exported_at'] = datetime.now(timezone.utc).isoformat()
    data = json.dumps(payload, ensure_ascii=False, indent=2)
    return Response(data, mimetype='application/json',
                    headers={'Content-Disposition': 'attachment; filename="rezepte.json"'})

@bp.route('/export/backup.json')
def export_backup_json():
    payload = _backup_payload()
    payload['type'] = 'backup'
    payload['version'] = 1
    payload['exported_at'] = datetime.now(timezone.utc).isoformat()
    data = json.dumps(payload, ensure_ascii=False, indent=2)
    return Response(data, mimetype='application/json',
                    headers={'Content-Disposition': 'attachment; filename="backup.json"'})

@bp.route('/export/recipes.md')
def export_recipes_md():
    payload = _recipes_payload()
    lines = ['# Rezeptbuch', f'*Exportiert am {datetime.now().strftime("%d.%m.%Y")}*', '']
    for r in payload['recipes']:
        lines += [f'---', f'', f'## {r["name"]}']
        if r['category']:
            lines.append(f'**Kategorie:** {r["category"]}')
        if r['description']:
            lines += ['', r['description']]
        if r['ingredients']:
            lines += ['', '| Zutat | Menge | Einheit |', '|---|---|---|']
            for i in r['ingredients']:
                amt = int(i['amount']) if i['amount'] == int(i['amount']) else i['amount']
                lines.append(f'| {i["name"]} | {amt} | {i["unit"]} |')
        lines.append('')
    md = '\n'.join(lines)
    return Response(md, mimetype='text/markdown',
                    headers={'Content-Disposition': 'attachment; filename="rezepte.md"'})

# ── Import / Restore ──────────────────────────────────────────────────────────

@bp.route('/import', methods=['POST'])
def import_data():
    try:
        file = request.files.get('file')
        if not file:
            return jsonify({'error': 'Keine Datei hochgeladen'}), 400

        payload = json.loads(file.read().decode('utf-8'))
        kind = payload.get('type')
        on_duplicate = request.form.get('on_duplicate', 'skip')  # 'skip' or 'overwrite'

        if kind not in ('recipes', 'backup'):
            return jsonify({'error': 'Unbekannter Dateityp. Bitte eine gültige Export- oder Backup-Datei wählen.'}), 400

        if kind == 'backup':
            _restore_backup(payload)
            return jsonify({'success': True, 'type': 'backup', 'message': 'Backup erfolgreich wiederhergestellt.'})
        else:
            stats = _import_recipes(payload, on_duplicate)
            return jsonify({'success': True, 'type': 'recipes', **stats})

    except (json.JSONDecodeError, KeyError) as e:
        return jsonify({'error': f'Ungültige Datei: {e}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


def _import_recipes(payload, on_duplicate):
    created_cats = 0
    updated_ings = 0
    created_recipes = 0
    skipped_recipes = 0
    overwritten_recipes = 0

    # Categories
    for cat_name in payload.get('categories', []):
        if not Category.query.filter_by(name=cat_name).first():
            db.session.add(Category(name=cat_name))
            created_cats += 1

    # Ingredient metadata
    for ing_data in payload.get('ingredients', []):
        ing = Ingredient.query.filter_by(name=ing_data['name']).first()
        if ing:
            if ing_data.get('default_unit'):
                ing.default_unit = ing_data['default_unit']
            if 'is_staple' in ing_data:
                ing.is_staple = ing_data['is_staple']
            if ing_data.get('shop_category'):
                ing.shop_category = ing_data['shop_category']
            updated_ings += 1

    db.session.flush()

    # Recipes
    for r in payload.get('recipes', []):
        existing = Recipe.query.filter(
            Recipe.name == r['name'], Recipe.deleted_at == None
        ).first()

        if existing and on_duplicate == 'skip':
            skipped_recipes += 1
            continue

        if existing and on_duplicate == 'overwrite':
            RecipeIngredient.query.filter_by(recipe_id=existing.id).delete()
            existing.category = r.get('category') or None
            existing.description = r.get('description') or None
            recipe = existing
            overwritten_recipes += 1
        else:
            recipe = Recipe(
                name=r['name'],
                category=r.get('category') or None,
                description=r.get('description') or None
            )
            db.session.add(recipe)
            db.session.flush()
            created_recipes += 1

        for i in r.get('ingredients', []):
            ing = Ingredient.query.filter_by(name=i['name']).first()
            if not ing:
                ing = Ingredient(name=i['name'])
                db.session.add(ing)
                db.session.flush()
            db.session.add(RecipeIngredient(
                recipe_id=recipe.id,
                ingredient_id=ing.id,
                amount=i['amount'],
                unit=i['unit']
            ))

    db.session.commit()
    return {
        'created_recipes': created_recipes,
        'overwritten_recipes': overwritten_recipes,
        'skipped_recipes': skipped_recipes,
        'created_categories': created_cats,
        'updated_ingredients': updated_ings,
        'message': f'{created_recipes} neu, {overwritten_recipes} überschrieben, {skipped_recipes} übersprungen.'
    }


def _restore_backup(payload):
    # Full wipe
    WeekPlan.query.delete()
    ShoppingList.query.delete()
    RecipeIngredient.query.delete()
    Recipe.query.delete()
    Ingredient.query.delete()
    Category.query.delete()
    db.session.flush()

    # Re-create categories
    for cat_name in payload.get('categories', []):
        db.session.add(Category(name=cat_name))
    db.session.flush()

    # Re-create ingredients
    for i in payload.get('ingredients', []):
        db.session.add(Ingredient(
            name=i['name'],
            default_unit=i.get('default_unit') or None,
            is_staple=i.get('is_staple', False),
            shop_category=i.get('shop_category', 'Sonstiges')
        ))
    db.session.flush()

    # Re-create recipes
    name_to_id = {}
    for r in payload.get('recipes', []):
        recipe = Recipe(
            name=r['name'],
            category=r.get('category') or None,
            description=r.get('description') or None
        )
        db.session.add(recipe)
        db.session.flush()
        name_to_id[r['name']] = recipe.id
        for i in r.get('ingredients', []):
            ing = Ingredient.query.filter_by(name=i['name']).first()
            if not ing:
                ing = Ingredient(name=i['name'])
                db.session.add(ing)
                db.session.flush()
            db.session.add(RecipeIngredient(
                recipe_id=recipe.id,
                ingredient_id=ing.id,
                amount=i['amount'],
                unit=i['unit']
            ))

    # Re-create week plan
    from datetime import date as date_type
    for wp in payload.get('week_plan', []):
        recipe_id = name_to_id.get(wp.get('recipe_name'))
        if not recipe_id:
            continue
        db.session.add(WeekPlan(
            week_start=date_type.fromisoformat(wp['week_start']),
            day_index=wp['day_index'],
            slot_index=wp['slot_index'],
            recipe_id=recipe_id,
            servings=wp.get('servings', 1),
            is_bought=wp.get('is_bought', False)
        ))

    # Re-create shopping list
    for s in payload.get('shopping_list', []):
        recipe_id = name_to_id.get(s.get('recipe_name'))
        if not recipe_id:
            continue
        db.session.add(ShoppingList(
            recipe_id=recipe_id,
            servings=s.get('servings', 1),
            is_active=s.get('is_active', True)
        ))

    db.session.commit()
