from app import app
from flask import jsonify

@app.route('/ping')
def ping():
    response_data = {
        "message": "pong"
    }

    return jsonify(response_data), 200