# app/__init__.py
from flask import Flask

def create_app():
    
    app = Flask(__name__)
    from app.filters import b64encode
    app.jinja_env.filters['b64encode'] = b64encode

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app

