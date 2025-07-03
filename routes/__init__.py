from flask import Flask
from routes.user_routes import user_bp
from routes.auth_routes import auth_bp


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
