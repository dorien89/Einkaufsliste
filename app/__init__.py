from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/einkaufsliste.db'
    
    db.init_app(app)
    
    # Blueprints importieren und registrieren
    from app.routes.main_routes import bp as main_bp
    from app.routes.recipe_routes import bp as recipe_bp
    from app.routes.api_routes import bp as api_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(recipe_bp)
    app.register_blueprint(api_bp)
    
    return app