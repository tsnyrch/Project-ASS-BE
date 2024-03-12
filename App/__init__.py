from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Registrujte blueprint pro routy
    from .routes import api
    app.register_blueprint(api)

    return app