from flask import (
    Flask,
    redirect,
    render_template,
    session,
    url_for,
)

app = Flask(__name__)
app.secret_key = 'secret'

@app.before_request
def initialize_session():
    if 'contacts' not in session:
        session['contacts'] = ['apple', 'banana', 'corn']

@app.route('/')
def index():
    # return render_template('index.html')
    return redirect(url_for('get_contacts'))

@app.route('/contacts')
def get_contacts():
    contacts = session['contacts']
    return render_template('contacts.html',
                           contacts=contacts)

@app.route('/contacts/new')
def add_contact():
    return render_template('new_contact.html')

@app.route('/contacts', methods=['POST'])
def create_contact():
    return redirect(url_for('get_contacts'))

if __name__ == '__main__':
    app.run(debug=True, port=5003)