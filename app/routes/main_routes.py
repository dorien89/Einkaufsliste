from flask import Blueprint, render_template, jsonify
from app.models.recipe import Recipe

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/planen/')
def planen():
    return render_template('planen.html')

@bp.route('/wochenplan/')
def wochenplan():
    return render_template('wochenplan.html')

