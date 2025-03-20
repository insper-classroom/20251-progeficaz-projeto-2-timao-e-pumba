from flask import Flask
from config import Config
from app import routes
from app.database import db

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(Config[config_name])

    db.init_app(app)

    app.register_blueprint(routes.bp)

    return app
