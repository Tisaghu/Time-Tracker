from flask import Flask

def create_app():
    app = Flask(__name__)

    #import and register Blueprints
    from app.routes.timer_routes import timer_bp
    from app.routes.log_routes import log_bp
    from app.routes.core_routes import core_bp
    from app.routes.category_routes import category_bp
    from .test_routes import test_bp

    app.register_blueprint(timer_bp, url_prefix='/timer')
    app.register_blueprint(log_bp, url_prefix='/logs')
    app.register_blueprint(test_bp, url_prefix='/test')
    app.register_blueprint(category_bp, url_prefix='/category')
    app.register_blueprint(core_bp)

    return app
