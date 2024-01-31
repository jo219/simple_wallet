from app import app
from flask import request, jsonify
import app.utils as utils


# view balance

@app.route('/api/v1/wallet', methods=['GET'])
@utils.authenticate_token
def handle_view_balance_request(customer_xid):

    # dummy id
    wallet_id = "6ef31ed3-f396-4b6c-8049-674ddede1b16"

    # Generate the response data
    response_data = {
        "status": "success",
        "data": {
            "wallet": {
                "id": wallet_id,
                "owned_by": customer_xid,
                "status": "enabled",
                "enabled_at": "1994-11-05T08:15:30-05:00",
                "balance": 0
            }
        }
    }

    return jsonify(response_data), 200


# view transactions

@app.route('/api/v1/wallet/transactions', methods=['GET'])
def handle_view_transactions_request():
    response_data = {
        "status": "success"
    }

    return jsonify(response_data), 200