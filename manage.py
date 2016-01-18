#! /usr/bin/env python

from blst.api import app, db
from blst.models import User
from flask.ext.script import Server, Manager
from getpass import getpass
import coloredlogs
import logging
import sys
import unittest


# declare script manager and server configuration
manager = Manager(app)
manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    host='0.0.0.0'
    )
)

# configure logging
coloredlogs.install(level='DEBUG')
logger = logging.getLogger(__file__)


# custom script command to add users
@manager.command
def adduser(username):
    """ Registers a new user. """
    password = getpass()
    confirm_password = getpass(prompt='Confirm: ')
    if password != confirm_password:
        sys.exit(logger.error('Error: passwords do not match.'))
    db.create_all()
    if not User.query.filter_by(username=username).first():
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        logger.debug('Success: {0} was registered.'.format(username))
        return User.query.filter_by(username=username).first()
    else:
        logger.error('Error: username already taken, try another')


# custom script command to run unit tests
@manager.command
def test():
    test_loader = unittest.defaultTestLoader
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_suite = test_loader.discover('tests')
    test_runner.run(test_suite)


if __name__ == '__main__':
    manager.run()
