# this is my implementation of a contact list app with a database

import secrets

from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    url_for,
)

import json
import os

from contact_list.database_persistence import DatabasePersistence

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

def get_contact_filepath():
    if app.config['TESTING']:
        return os.path.join(os.path.dirname(__file__), 'tests', 'contacts.json')
    else:
        return os.path.join(os.path.dirname(__file__), 'contact_list', 'contacts.json')
    
@app.before_request
def load_db():
    g.storage = DatabasePersistence()

def load_contacts():
    json_path = get_contact_filepath()
    try:
        with open(json_path, 'r') as file:
            contacts = json.load(file)
            return contacts
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
    except:
        return []
    
def save_contacts(contacts):
    json_path = get_contact_filepath()
    with open(json_path, 'w') as file:
        json.dump(contacts, file, indent=4)

def get_contact(contact_id, contacts):
    for contact in contacts:
        if contact['id'] == contact_id:
            return contact
    return None

@app.route('/')
def index():
    return redirect(url_for('get_contacts'))

@app.route('/contacts')
def get_contacts():
    contacts = g.storage.all_contacts()
    return render_template('contacts.html',
                           contacts=contacts)
@app.route('/contacts/new')
def add_contact():
    return render_template('new_contact.html')

@app.route('/contacts', methods=['POST'])
def create_contact():
    name = request.form['name'].strip()
    phone = request.form['phone'].strip()
    email = request.form['email'].strip()
    category = request.form['category'].strip()

    g.storage.create_new_contact(name, phone, email, category)

    return redirect(url_for('get_contacts'))

@app.route('/contacts/<int:contact_id>/delete', methods=['POST'])
def delete_contact(contact_id):
    g.storage.delete_contact(contact_id)
    return redirect(url_for('get_contacts'))

@app.route('/contacts/<int:contact_id>/edit')
def edit_contact(contact_id):
    contact = g.storage.find_contact(contact_id)

    if contact:
        return render_template('update_contact.html', contact=contact)
    
    return redirect(url_for('get_contacts'))

@app.route('/contacts/<int:contact_id>/update', methods=['POST'])
def update_contact(contact_id):
    contact = g.storage.find_contact(contact_id)
    
    if contact:
        name = request.form['name'].strip()
        phone = request.form['phone'].strip()
        email = request.form['email'].strip()
        category = request.form['category'].strip()

        g.storage.update_contact(contact_id, name, phone, email, category)

        return redirect(url_for('get_contacts'))

    return redirect(url_for('get_contacts'))

if __name__ == '__main__':
    app.run(debug=True, port=5003)