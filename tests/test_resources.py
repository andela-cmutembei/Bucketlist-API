from blst.api import app, db
from blst.config import config
from blst.models import User
import unittest
import json


class ResourcesTestCase(unittest.TestCase):

    def setUp(self):
        """method to initialize values used in testing"""
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
        """method to clearing values used in testing from DB"""
        db.session.remove()
        db.drop_all()

    def test_get_request_on_bucketlist_resource(self):
        """Checks status code for unauthenticated user on bucketlists resource"""

        response = self.client.get("/bucketlists/")
        self.assertEqual(response.status_code, 401)

    def test_getting_authentication_token_for_valid_user(self):
        """test for getting an authentication toke with valid user data"""

        response = self.client.post(
            "/auth/login",
            data=dict(username=self.test_user, password=self.test_password)
        )
        length = len(self.user_token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(self.user_token), unicode)
        self.assertGreater(length, 100)

    def test_failing_auth_token_for_invalid_user(self):
        """Test for failing to get auth token for invalid user credentials"""

        response = self.client.post(
            "/auth/login",
            data=dict(username='random_test_user', password='random_test_password')
        )
        self.assertEqual(response.status_code, 401)

    def test_list_all_bucektlists_for_authenticated_user(self):
        """Test for getting all bucketlists for authenticated users"""

        response = self.client.get(
            "/bucketlists/",
            headers={'Authorization': self.user_token}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, '[]\n')

    def test_creating_and_getting_a_bucketlist_for_authenticated_user(self):
        """Test for creating and getting bucketlist and constituent items"""

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
        self.assertEqual(created_item["name"], 'test_item')

        # test for deletion of bucketlist
        second_bucketlist = self.client.post(
            "/bucketlists/",
            data=dict(name='second_bucketlist'),
            headers={'Authorization': self.user_token}
        )

        bucketlist_two = json.loads(second_bucketlist.data)

        self.assertEqual(second_bucketlist.status_code, 200)
        self.assertEqual(bucketlist_two["name"], 'second_bucketlist')

        delete_response = self.client.delete(
            "/bucketlists/" + str(bucketlist_two["bucketlist_id"]) + "",
            headers={'Authorization': self.user_token}
        )

        deletion = json.loads(delete_response.data)

        self.assertEqual(delete_response.status_code, 200)
        self.assertEqual(deletion["message"], "Deleted")

        # test for deletion of an item in bucketlist
        delete_item = self.client.delete(
            "/bucketlists/" + str(bucketlist["bucketlist_id"]) + "/items/" + str(one_item["item_id"]) + "",
            headers={'Authorization': self.user_token}
        )

        item_deletion = json.loads(delete_item.data)

        self.assertEqual(delete_item.status_code, 200)
        self.assertEqual(item_deletion["message"], "Deleted")

        # test for updating of bucketlist
        self.bucketlist_id = bucketlist["bucketlist_id"]
        bucketlist_update = self.client.put(
            "/bucketlists/" + str(self.bucketlist_id) + "",
            data=dict(name='bucketlist_test'),
            headers={'Authorization': self.user_token}
        )

        updated_bucketlist = json.loads(bucketlist_update.data)

        self.assertEqual(bucketlist_update.status_code, 200)
        self.assertEqual(updated_bucketlist["name"], 'bucketlist_test')

        # test update of item in bucketlist
        item = self.client.post(
            "/bucketlists/" + str(self.bucketlist_id) + "/items/",
            data=dict(name="test_item"),
            headers={'Authorization': self.user_token}
        )

        one_item = json.loads(item.data)

        item_update = self.client.put(
            "/bucketlists/" + str(self.bucketlist_id) + "/items/"+ str(one_item["item_id"]) + "",
            data=dict(name="item_test"),
            headers={'Authorization': self.user_token}
        )

        updated_item = json.loads(item_update.data)
        # import ipdb; ipdb.set_trace()


        self.assertEqual(item_update.status_code, 200)
        self.assertEqual(updated_item["name"], 'item_test')


if __name__ == '__main__':
    unittest.main()
