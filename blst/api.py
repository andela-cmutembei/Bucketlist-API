from flask import Flask
from flask.ext.bcrypt import Bcrypt
from flask.ext.restful import Api
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


from config import config
import os

app = Flask(__name__)
api = Api(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


# Set the config for app
config_name = os.environ.get('BLST_CONFIG', 'default')
app.config.from_object(config[config_name])


auth_serializer = Serializer(app.config['SECRET_KEY'])

from blst.models import *


@login_manager.request_loader
def authenticate_user(request):
    """Require token for authentication to allow view"""
    token = request.headers.get('Authorization')
    if token:
        try:
            data = auth_serializer.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query.get(data[0])
        return user
    return None



from resources import AllBucketlists, SingleBucketlists, AllBucketlistItems, SingleBucketlistItem, Login

# API resources
api.add_resource(Login, '/auth/login')
api.add_resource(AllBucketlists, '/bucketlists/')
api.add_resource(SingleBucketlists, '/bucketlists/<id>')
api.add_resource(AllBucketlistItems, '/bucketlists/<id>/items/')
api.add_resource(SingleBucketlistItem, '/bucketlists/<id>/items/<item_id>')

if __name__ == '__main__':
    app.run()
