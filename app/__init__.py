import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Absoluten Pfad zur Datenbank erstellen
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    db_path = os.path.join(basedir, 'database', 'einkaufsliste.db')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
   
    db.init_app(app)
   
    # Blueprints importieren und registrieren
    from app.routes.main_routes import bp as main_bp
    from app.routes.recipe_routes import bp as recipe_bp
    from app.routes.api_routes import bp as api_bp
    from app.routes.kiosk_routes import bp as kiosk_bp
   
    app.register_blueprint(main_bp)
    app.register_blueprint(recipe_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(kiosk_bp)
   
    return app