from blst.api import app, db
from blst.config import config
from blst.models import User
import unittest
import json


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

        request_token = self.client.post(
            "/auth/login",
            data=dict(username=self.test_user, password=self.test_password)
        )
        data = json.loads(request_token.data)
        self.user_token = data['token']

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
        length = len(self.user_token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(self.user_token), unicode)
        self.assertGreater(length, 100)

    def test_failing_auth_token_for_invalid_user(self):

        response = self.client.post(
            "/auth/login",
            data=dict(username='random_test_user', password='random_test_password')
        )
        self.assertEqual(response.status_code, 401)

    def test_list_all_bucektlists_for_authenticated_user(self):

        response = self.client.get(
            "/bucketlists/",
            headers={'Authorization': self.user_token}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, '[]\n')

    def test_creating_and_getting_a_bucketlist_for_authenticated_user(self):

        # test all bucketlists
        response = self.client.post(
            "/bucketlists/",
            data=dict(name='test_bucketlist'),
            headers={'Authorization': self.user_token}
        )
        bucketlist = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(bucketlist["name"], 'test_bucketlist')

        # test single bucketlist
        self.bucketlist_id = bucketlist["bucketlist_id"]
        single_bucketlist = self.client.get(
            "/bucketlists/" + str(self.bucketlist_id) + "",
            headers={'Authorization': self.user_token}
        )

        one_bucketlist = json.loads(single_bucketlist.data)

        self.assertEqual(single_bucketlist.status_code, 200)
        self.assertEqual(one_bucketlist["name"], 'test_bucketlist')

        # test all items in bucketlist
        item = self.client.post(
            "/bucketlists/" + str(self.bucketlist_id) + "/items/",
            data=dict(name="test_item"),
            headers={'Authorization': self.user_token}
        )

        one_item = json.loads(item.data)

        self.assertEqual(item.status_code, 200)
        self.assertEqual(one_item["name"], 'test_item')


        # test single item in bucketlist
        self.item_id = one_item["item_id"]
        single_item = self.client.get(
            "/bucketlists/" + str(self.bucketlist_id) + "/items/" + str(self.item_id) + "",
            headers={'Authorization': self.user_token}
        )

        created_item = json.loads(single_item.data)

        self.assertEqual(single_item.status_code, 200)
        self.assertEqual(one_item["name"], 'test_item')
if __name__ == '__main__':
    unittest.main()
