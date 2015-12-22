from datetime import datetime
from . import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_modified = db.Column(
        db.DateTime,
        default=datetime.now(),
        onupdate=datetime.now()
    )
