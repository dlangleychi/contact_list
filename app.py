from flask import (
    Flask,
    redirect,
    render_template,
    request,
    url_for,
)

import json
import os

import uuid

app = Flask(__name__)
app.secret_key = 'secret'

def get_contact_filepath():
    if app.config['TESTING']:
        return os.path.join(os.path.dirname(__file__), 'tests', 'contacts.json')
    else:
        return os.path.join(os.path.dirname(__file__), 'contact_list', 'contacts.json')

def load_contacts():
    json_path = get_contact_filepath()
    try:
        with open(json_path, 'r') as file:
            contacts = json.load(file)
            return contacts
    except:
        return []
    
def save_contacts(contacts):
    json_path = get_contact_filepath()
    with open(json_path, 'w') as file:
        json.dump(contacts, file, indent=4)

@app.route('/')
def index():
    # return render_template('index.html')
    return redirect(url_for('get_contacts'))

@app.route('/contacts')
def get_contacts():
    contacts = load_contacts()
    return render_template('contacts.html',
                           contacts=contacts)

@app.route('/contacts/new')
def add_contact():
    return render_template('new_contact.html')

@app.route('/contacts', methods=['POST'])
def create_contact():
    contacts = load_contacts()

    name = request.form['name'].strip()
    phone = request.form['phone'].strip()
    email = request.form['email'].strip()
    category = request.form['category'].strip()

    contacts.append(
        {
            'id': uuid.uuid4().hex,
            'name': name,
            'phone': phone,
            'email': email,
            'category': category
        }
    )
    save_contacts(contacts)

    return redirect(url_for('get_contacts'))

@app.route('/contacts/<contact_id>/delete', methods=['POST'])
def delete_contact(contact_id):
    contacts = load_contacts()
    contacts = [contact for contact in contacts if contact['id'] != contact_id]
    save_contacts(contacts)
    return redirect(url_for('get_contacts'))

if __name__ == '__main__':
    app.run(debug=True, port=5003)