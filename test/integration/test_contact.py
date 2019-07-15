import uuid
import json
import requests
from .config import *
from pprint import pprint as pp
import unittest
PASSWORD = "1234"
FIRST_NAME = "Jeff"
LAST_NAME = "Johnson"
EMAIL = "{}test@testmail.com".format(uuid.uuid4())
TOKEN = None
CONTACT_ID = None


class TestContact(unittest.TestCase):
    def test_101_create_account(self):
        global TOKEN
        r = requests.post(
            url="{}/{}/{}".format(API_HOST, API_VERSION, 'user'),
            data={'email': EMAIL,
                  'first_name': FIRST_NAME,
                  'last_name': LAST_NAME,
                  'password': PASSWORD})
        data = r.json()
        pp(data)
        self.assertTrue(data['data'].get('data'))
        TOKEN = data['data']['data']['token']

    def test_102_create_contact(self):
        global TOKEN, CONTACT_ID
        url = "{}/{}/{}".format(API_HOST, API_VERSION, 'contact')
        headers = {'content-type': 'application/json', 'API-Token': TOKEN}
        post_data = {
            "first_name": "Sandy",
            "email": EMAIL,
        }
        r = requests.post(url=url, headers=headers, data=json.dumps(post_data))
        data = r.json()
        pp(data)
        self.assertTrue(data['data'].get('data'))
        self.assertEqual(data['data']['data']['first_name'], post_data['first_name'])
        self.assertEqual(data['data']['data']['email'], post_data['email'])
        CONTACT_ID = data['data']['data']['_id']

    def test_103_contact_edit(self):
        global TOKEN, CONTACT_ID
        url = "{}/{}/{}/{}".format(API_HOST, API_VERSION, 'contact', CONTACT_ID)
        headers = {'content-type': 'application/json', 'API-Token': TOKEN}

        post_data = {
            "last_name": "Rosa",
            "first_name": "Anabel"
        }
        r = requests.put(url=url, headers=headers, data=json.dumps(post_data))
        data = r.json()
        pp(data)
        self.assertTrue(data['data'].get('data'))
        self.assertEqual(data['data']['data']['first_name'], post_data['first_name'])
        self.assertEqual(data['data']['data']['last_name'], post_data['last_name'])

    def test_104_delete_contact(self):
        global TOKEN, CONTACT_ID
        url = "{}/{}/{}/{}".format(API_HOST, API_VERSION, 'contact', CONTACT_ID)
        headers = {'content-type': 'application/json', 'API-Token': TOKEN}

        r = requests.delete(url=url, headers=headers)
        data = r.json()
        pp(data)
        self.assertTrue(data['data'].get('data'))
        self.assertTrue(data['data']['data']['_id'] == CONTACT_ID)
        self.assertTrue(data['data']['data']['is_deleted'])


if __name__ == '__main__':
    unittest.main()
