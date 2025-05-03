from flask import Flask, render_template, request, redirect, url_for
import os
import uuid

app = Flask(__name__)
INBOX_DIR = "inbox"

if not os.path.exists(INBOX_DIR):
    os.makedirs(INBOX_DIR)

@app.route('/')
def index():
    email = f"{uuid.uuid4().hex[:10]}@10m-mail.com"
    expires = 600
    messages = get_inbox_messages()
    return render_template("index.html", email=email, expires=expires, messages=messages)

def get_inbox_messages():
    messages = []
    for fname in os.listdir(INBOX_DIR):
        if fname.endswith(".txt"):
            with open(os.path.join(INBOX_DIR, fname)) as f:
                content = f.read()
                messages.append(content)
    return messages

@app.route('/receive', methods=['POST'])
def receive():
    subject = request.form.get('subject')
    body = request.form.get('body')
    filename = f"{uuid.uuid4().hex}.txt"
    with open(os.path.join(INBOX_DIR, filename), "w") as f:
        f.write(f"Subject: {subject}\n{body}")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()