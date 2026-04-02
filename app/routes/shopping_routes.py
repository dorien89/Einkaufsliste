# app/routes/shopping_routes.py
from flask import Blueprint, render_template
from app import db
from app.models.manual_shopping_item import ManualShoppingItem
from app.routes.api_routes import get_shopping_list, _cleanup_past_shopping_list

bp = Blueprint('shopping-list', __name__, url_prefix='/shopping-list')

@bp.route('/', methods=['GET'])
def view_shopping_list():
    _cleanup_past_shopping_list()
    db.session.commit()
    result = get_shopping_list()
    response = result[0] if isinstance(result, tuple) else result
    data = response.get_json()

    manual_items = ManualShoppingItem.query.order_by(ManualShoppingItem.created_at).all()

    if data.get('success'):
        return render_template('shopping_list.html',
                               ingredients=data.get('ingredients', []),
                               manual_items=manual_items)
    else:
        return render_template('shopping_list.html',
                               error=data.get('error', 'Unknown error'),
                               manual_items=manual_items)