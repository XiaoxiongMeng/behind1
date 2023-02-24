from flask import Flask
from flask_cors import CORS
from user import user
from search import search
from history import history

app = Flask(__name__)
app.register_blueprint(user)
app.register_blueprint(search)
app.register_blueprint(history)
CORS(app, supports_credentials=True)
nowuser = ''


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    print(app.url_map)
    app.run(host='0.0.0.0', port=8000, debug=True)
