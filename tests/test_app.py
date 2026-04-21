import unittest
from app import app, get_contact_filepath
import os

class ContactList(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.json_path = get_contact_filepath()
        with open(self.json_path, 'w') as f:
            pass

    def tearDown(self):
        os.remove(self.json_path)


    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        follow_response = self.client.get(response.headers['Location'])
        self.assertIn('no contacts', follow_response.get_data(as_text=True))

    def test_new_contact_page(self):
        pass

    def test_create_contact(self):
        response = self.client.post('/contacts',
                                    data={
                                        'name': 'John',
                                        'phone': '123',
                                        'email': 'john@test.com',
                                        'category': 'personal'
                                    },
                                    follow_redirects=True)
        self.assertIn('John', response.get_data(as_text=True))
        self.assertIn('123', response.get_data(as_text=True))
        self.assertIn('john@test.com', response.get_data(as_text=True))
        self.assertIn('personal', response.get_data(as_text=True))

    def test_edit(self):
        pass

    def test_delete(self):
        pass

if __name__ == '__main__':
    unittest.main()