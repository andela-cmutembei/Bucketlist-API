from flask import Flask
from flask.ext.restful import Api
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt

from config import config
import os

app = Flask(__name__)
api = Api(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

# Set the config for app
config_name = os.environ.get('BLST_CONFIG', 'default')
app.config.from_object(config[config_name])


if __name__ == '__main__':
    app.run()
