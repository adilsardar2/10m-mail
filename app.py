
from flask import Flask, render_template
import os
import random
import string

app = Flask(__name__)
INBOX_DIR = 'inbox'

def generate_email():
    prefix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
    return f"{prefix}@10m-mail.com"

@app.route('/')
def index():
    email = generate_email()
    return render_template('index.html', email=email)

if __name__ == "__main__":
    if not os.path.exists(INBOX_DIR):
        os.makedirs(INBOX_DIR)
    app.run(host='0.0.0.0', port=10000)
