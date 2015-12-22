from config import config
from flask import Flask
from models import db


def create_app(config_name):
    app = Flask(__name__)
    loaded_config = config[config_name]
    app.config.from_object(loaded_config)

    db.init_app(app)

    from blst.api_v1 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/v1')

    @app.route('/')
    def index():
        return "Hello World"

    return app
