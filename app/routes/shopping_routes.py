# app/routes/shopping_routes.py
from flask import Blueprint, render_template
from app.routes.api_routes import get_shopping_list

bp = Blueprint('shopping-list', __name__, url_prefix='/shopping-list')

@bp.route('/', methods=['GET'])
def view_shopping_list():
    # Get data directly from API function
    response = get_shopping_list()
    
    # Since response is a JSONified response, we need to get the json data
    if hasattr(response, 'json'):
        data = response.json
        if data.get('success'):
            ingredients = data.get('ingredients', [])
            # Sort ingredients by name
            ingredients.sort(key=lambda x: x['name'])
            return render_template('shopping_list.html', ingredients=ingredients)
    
    return render_template('shopping_list.html', error="Could not load shopping list")