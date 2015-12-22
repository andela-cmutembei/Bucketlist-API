#! /usr/bin/env python

from blst.app import create_app
from blst.models import db
from flask.ext.script import Manager
import os

app = create_app(os.environ.get('BLST_CONFIG', 'default'))
manager = Manager(app)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db)


if __name__ == '__main__':
    manager.run()
