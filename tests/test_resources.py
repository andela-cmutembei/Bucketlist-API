from blst.api import app, db
from blst.config import config
from blst.models import User
import unittest


class ResourcesTestCase(unittest.TestCase):

    def setUp(self):
        app.config.from_object(config['testing'])
        db.create_all()

        self.client = app.test_client()

        self.test_user = 'test_first_user'
        self.test_password = 'liamNees0n_T4k3n'
        self.user_object = User(username=self.test_user, password=self.test_password)
        db.session.add(self.user_object)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_request_on_bucketlist_resource(self):
        """Checks status code for unauthenticated user on bucketlists resource"""

        response = self.client.get("/bucketlists/")
        self.assertEqual(response.status_code, 401)

    def test_getting_authentication_token_for_valid_user(self):

        response = self.client.post(
            "/auth/login",
            data=dict(username=self.test_user, password=self.test_password)
        )
        self.assertEqual(response.status_code, 200)

    def test_failing_auth_token_for_invalid_user(self):

        response = self.client.post(
            "/auth/login",
            data=dict(username='random_test_user', password='random_test_password')
        )
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
