from blst.api import app, db
from blst.config import config
import unittest


class ResourcesTestCase(unittest.TestCase):

    def setUp(self):
        app.config.from_object(config['testing'])
        db.create_all()

        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_request_on_bucketlist_resource(self):
        """Checks status code for unauthenticated user on bucketlists resource"""

        response = self.client.get("/bucketlists/")
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
