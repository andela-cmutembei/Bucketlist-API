from blst.api import db, bcrypt
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property


class User(db.Model):
    """ Defines the user model """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    _password = db.Column(db.String(128))

    # define a hybrid property with fns to be called on instance
    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    def verify_password(self, plaintext):
        return bcrypt.check_password_hash(self.password, plaintext)

    def __repr__(self):
        return '<User {0} : {1}>'.format(self.id, self.username)


class Bucketlist(db.Model):
    """ Defines the bucketlists model """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_modified = db.Column(
        db.DateTime,
        default=datetime.utcnow(),
        onupdate=datetime.utcnow()
    )
    items = db.relationship('Item')
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Bucketlist {0} : {1}>'.format(self.id, self.name)


class Item(db.Model):
    """ Defines the bucketlist items model """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_modified = db.Column(
        db.DateTime,
        default=datetime.utcnow(),
        onupdate=datetime.utcnow()
    )
    done = db.Column(db.Boolean, default=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlist.id'))

    def __repr__(self):
        return '<Item {0} : {1}>'.format(self.id, self.name)
