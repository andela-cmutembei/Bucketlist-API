from blst.api import db, bcrypt, app
from datetime import datetime
from flask.ext.login import UserMixin
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer)
from sqlalchemy.ext.hybrid import hybrid_property


class User(db.Model, UserMixin):
    """ Defines the user model """

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    _password = db.Column(db.String(128))
    logged_in = db.Column(db.Boolean, default=False)

    # define a hybrid property with fns to be called on instance
    @hybrid_property
    def password(self):
        """Assigns the hashed password to user"""

        return self._password

    @password.setter
    def _set_password(self, plaintext):
        """Hashes a password from plaintext to ciphertext"""

        self._password = bcrypt.generate_password_hash(plaintext)

    def verify_password(self, plaintext):
        """Checks the entered paintext against the hashed password"""

        return bcrypt.check_password_hash(self.password, plaintext)

    def generate_auth_token(self, expiration=6000):
        """Generates a authentication token from user data"""

        user_data = [self.user_id, self.username, self.password]
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps(user_data)

    def invalidate_token(self):
        """Makes an existing token invalid by logging out a user"""

        self.logged_in = False

    def __repr__(self):
        """Represents the user object"""
        return '<User {0} : {1}>'.format(self.user_id, self.username)


class Bucketlist(db.Model):
    """ Defines the bucketlists model """

    bucketlist_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    date_modified = db.Column(
        db.DateTime,
        default=datetime.utcnow(),
        onupdate=datetime.utcnow()
    )
    items = db.relationship('Item', cascade="all, delete-orphan")
    created_by = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def __repr__(self):
        """Represents the bucketlist object"""
        return '<Bucketlist {0} : {1}>'.format(self.bucketlist_id, self.name)


class Item(db.Model):
    """ Defines the bucketlist items model """

    item_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    date_modified = db.Column(
        db.DateTime,
        default=datetime.utcnow(),
        onupdate=datetime.utcnow()
    )
    done = db.Column(db.Boolean, default=False)
    parent_bucketlist = db.Column(db.Integer, db.ForeignKey('bucketlist.bucketlist_id'))

    def __repr__(self):
        """Represents the item object"""
        return '<Item {0} : {1}>'.format(self.item_id, self.name)
