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

from contact_list.database_persistence import DatabasePersistence

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
    
@app.before_request
def load_db():
    g.storage = DatabasePersistence()

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