from flask import Flask, render_template, session, redirect, url_for
import random, string

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def generate_email():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + "@10m-mail.com"

@app.route('/')
def index():
    if 'email' not in session:
        session['email'] = generate_email()
    return render_template('index.html', email=session['email'])

@app.route('/reset')
def reset():
    session.pop('email', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
