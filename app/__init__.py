# app.py
from flask import Flask

def create_app():
    app = Flask(__name__)

    # Import and register blueprints
    from .main_routes import main_bp
    from .test_routes import test_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(test_bp, url_prefix='/test')

    return app
