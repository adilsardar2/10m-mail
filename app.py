from flask import Flask, render_template, request, redirect, url_for
import os
import uuid
import time
import json

app = Flask(__name__)
INBOX_DIR = "inbox"

# Ensure the inbox directory exists
if not os.path.exists(INBOX_DIR):
    os.makedirs(INBOX_DIR)

def generate_email():
    return f"{uuid.uuid4().hex[:12]}@10m-mail.com"

def get_inbox_messages():
    messages = []
    for fname in os.listdir(INBOX_DIR):
        with open(os.path.join(INBOX_DIR, fname), "r") as f:
            messages.append(json.load(f))
    return messages

@app.route("/")
def index():
    email = generate_email()
    return render_template("index.html", email=email, messages=get_inbox_messages(), expiry=600)

@app.route("/receive", methods=["POST"])
def receive_email():
    content = request.json
    filename = f"{int(time.time())}.json"
    with open(os.path.join(INBOX_DIR, filename), "w") as f:
        json.dump(content, f)
    return {"status": "received"}, 200

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
