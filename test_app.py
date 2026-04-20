import unittest
from app import app

class ContactList(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        follow_response = self.client.get(response.headers['Location'])

if __name__ == '__main__':
    unittest.main()