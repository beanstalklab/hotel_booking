from datetime import timedelta
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config")
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
    register_blueprints(app)
    return app

def register_blueprints(app):
    from app.auth import auth_blp
    from app.view import main_blp
    from app.admin import admin_blp 
    app.register_blueprint(main_blp)
    app.register_blueprint(auth_blp)
    app.register_blueprint(admin_blp)