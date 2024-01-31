from app import app
from flask import request, jsonify


# view balance

@app.route('/api/v1/wallet', methods=['GET'])
def handle_view_balance_request():
    response_data = {
        "status": "success"
    }

    return jsonify(response_data), 200


# view transactions

@app.route('/api/v1/wallet/transactions', methods=['GET'])
def handle_view_transactions_request():
    response_data = {
        "status": "success"
    }

    return jsonify(response_data), 200