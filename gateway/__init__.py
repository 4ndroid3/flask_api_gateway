import os
from flask import Flask
from flask_jwt_extended import JWTManager

from gateway import auth
from gateway import main
from gateway.config import limiter


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY="dev")

    app.config.from_pyfile("config.py", silent=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    jwt = JWTManager(app)
    limiter.init_app(app=app)

    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(main.main_bp)

    return app
