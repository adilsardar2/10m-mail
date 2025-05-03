
import os
import random
import string
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'
MAILBOX_PATH = "mailbox"
EMAIL_EXPIRY_SECONDS = 600

def generate_email():
    local = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    domain = "10m-mail.com"
    return f"{local}@{domain}"

@app.route("/")
def home():
    if 'email' not in session:
        session['email'] = generate_email()
    return render_template("index.html", email=session['email'], expiry=EMAIL_EXPIRY_SECONDS)

@app.route("/inbox")
def inbox():
    email = session.get('email', '')
    path = os.path.join(MAILBOX_PATH, email)
    messages = []
    if os.path.exists(path):
        for file in sorted(os.listdir(path), reverse=True):
            with open(os.path.join(path, file)) as f:
                messages.append(f.read())
    return jsonify(messages)

@app.route("/receive", methods=["POST"])
def receive():
    email = request.form.get("to")
    subject = request.form.get("subject", "")
    content = request.form.get("text", "")
    sender = request.form.get("from", "")
    full_message = f"From: {sender}\nSubject: {subject}\n\n{content}"
    folder = os.path.join(MAILBOX_PATH, email)
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    with open(os.path.join(folder, f"{timestamp}.txt"), "w") as f:
        f.write(full_message)
    return "OK", 200

@app.route("/reset")
def reset():
    session.pop('email', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
