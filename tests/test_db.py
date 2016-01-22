from blst.api import app, db
from blst.config import config
from blst.models import User
import unittest


class DBTestCase(unittest.TestCase):

    def setUp(self):
        """method to initialize values used in testing"""

        app.config.from_object(config['testing'])
        db.create_all()

    def tearDown(self):
        """method to clearing values used in testing from DB"""
        db.session.remove()
        db.drop_all()

    def test_user_not_in_db_before_addition(self):
        """Queries the user table to ensure user is not in db already"""

        username = 'testuser'
        user = User.query.filter_by(username=username).first()
        self.assertTrue(user.__str__(), None)

    def test_add_new_user_to_db(self):
        """Confirms addition of a user to the db """

        test_user = 'test_first_user'
        test_password = 'liamNees0n_T4k3n'
        user_object = User(username=test_user, password=test_password)
        db.session.add(user_object)
        db.session.commit()
        self.assertEqual(user_object.username, 'test_first_user')

if __name__ == '__main__':
    unittest.main()
