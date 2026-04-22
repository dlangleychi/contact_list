# these are the unit tests

import unittest
from app import app, get_contact_filepath
import os
import json

class ContactList(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.json_path = get_contact_filepath()
        with open(self.json_path, 'w') as f:
            pass

    def tearDown(self):
        os.remove(self.json_path)


    def test_index_redirect(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/contacts', response.headers['Location'])

    def test_empty_contacts(self):
        response = self.client.get('/contacts')
        self.assertIn('no contacts', response.get_data(as_text=True))

    def test_new_contact(self):
        response = self.client.get('/contacts/new')
        self.assertIn('Name', response.get_data(as_text=True))
        self.assertIn('Phone', response.get_data(as_text=True))
        self.assertIn('Email', response.get_data(as_text=True))
        self.assertIn('Category', response.get_data(as_text=True))

    def test_create_contact(self):
        response = self.client.post('/contacts',
                                    data={
                                        'name': 'John',
                                        'phone': '123',
                                        'email': 'john@test.com',
                                        'category': 'personal'
                                    },
                                    follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('John', response.get_data(as_text=True))
        self.assertIn('123', response.get_data(as_text=True))
        self.assertIn('john@test.com', response.get_data(as_text=True))
        self.assertIn('personal', response.get_data(as_text=True))

    def test_delete_contact(self):
        response = self.client.post('/contacts',
                                    data={
                                        'name': 'John',
                                        'phone': '123',
                                        'email': 'john@test.com',
                                        'category': 'personal'
                                    },
                                    follow_redirects=True)
        
        with open(self.json_path, 'r') as file:
            contacts = json.load(file)

        id = contacts.pop()['id']
        delete_response = self.client.post(f'/contacts/{id}/delete',
                                           follow_redirects=True)
        self.assertEqual(delete_response.status_code, 200)
        self.assertIn('no contacts', delete_response.get_data(as_text=True))

    def test_edit_contact(self):
        response = self.client.post('/contacts',
                                    data={
                                        'name': 'John',
                                        'phone': '123',
                                        'email': 'john@test.com',
                                        'category': 'personal'
                                    },
                                    follow_redirects=True)
        
        with open(self.json_path, 'r') as file:
            contacts = json.load(file)

        id = contacts[0]['id']
        edit_response = self.client.get(f'/contacts/{id}/edit',
                                           follow_redirects=True)
        self.assertEqual(edit_response.status_code, 200)
        self.assertIn('John', edit_response.get_data(as_text=True))
        self.assertIn('Name', edit_response.get_data(as_text=True))

    def test_update_contact(self):
        response = self.client.post('/contacts',
                                    data={
                                        'name': 'John',
                                        'phone': '123',
                                        'email': 'john@test.com',
                                        'category': 'personal'
                                    },
                                    follow_redirects=True)
        
        with open(self.json_path, 'r') as file:
            contacts = json.load(file)

        id = contacts[0]['id']
        update_response = self.client.post(f'/contacts/{id}/update',
                                           data={
                                                'name': 'John',
                                                'phone': '987',
                                                'email': 'john@test.com',
                                                'category': 'personal'
                                            },
                                           follow_redirects=True)
        self.assertEqual(update_response.status_code, 200)
        self.assertIn('John', update_response.get_data(as_text=True))
        self.assertIn('987', update_response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()