from app import app
from flask import request, jsonify


# de/activate wallet

@app.route('/api/v1/wallet', methods=['POST', 'PATCH'])
def handle_activate_wallet_request():
    response_data = {
        "status": "success"
    }

    return jsonify(response_data), 200
        

# deposits

@app.route('/api/v1/wallet/deposits', methods=['POST'])
def handle_deposits_wallet_request():
    response_data = {
        "status": "success"
    }

    return jsonify(response_data), 200


# withdrawals

@app.route('/api/v1/wallet/withdrawals', methods=['POST'])
def handle_withdrawals_wallet_request():
    response_data = {
        "status": "success"
    }

    return jsonify(response_data), 200