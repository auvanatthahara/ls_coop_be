from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from config import Config
from models.user import db
from routes import register_blueprints

jwt = JWTManager()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    Migrate(app, db)

    register_blueprints(app)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
