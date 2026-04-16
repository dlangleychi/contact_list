from flask import (
    Flask,
    redirect,
    render_template,
    url_for,
)

app = Flask(__name__)

@app.route('/')
def index():
    # return render_template('index.html')
    return redirect(url_for('get_contacts'))

@app.route('/contacts')
def get_contacts():
    contacts = ['a', 'b', 'c']
    return render_template('contacts.html',
                           contacts=contacts)

if __name__ == '__main__':
    app.run(debug=True, port=5003)