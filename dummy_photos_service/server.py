import json
from flask import Flask


app = Flask(__name__)

@app.route('/')
def index():
    return json.dumps({'msg': "success"})

@app.route('/<id>')
def single_user(id):
    response = {
        "thumbnailUrl": "https://via.placeholder.com/150/24f355"
    }
    return json.dumps(response)


app.run(host='0.0.0.0', port=80, debug=True)