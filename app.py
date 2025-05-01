# Flask app entry point

from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return '10m-mail is live!'

if __name__ == '__main__':
    app.run(debug=True)