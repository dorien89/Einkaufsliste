from flask import Blueprint, render_template, jsonify
from app.models.recipe import Recipe

bp = Blueprint('kiosk', __name__, url_prefix='/kiosk')

@bp.route('/')
def run_kiosk():
    return render_template('kiosk.html')

