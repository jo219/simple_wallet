from app import app
from flask import request, jsonify
import app.utils as utils

from app.repositories import wallet_repositories

import uuid


# view balance

@app.route('/api/v1/wallet', methods=['GET'])
@utils.authenticate_token
def handle_view_balance_request(customer_xid):

    balance_data = wallet_repositories.Balance(
        owned_by=customer_xid
    ).get_balance_from_customer_xid(customer_xid)
    
    if not balance_data:
        response_data = {
            "status": "fail",
            "data": {
                "error": "Wallet disabled"
            }
        }    
        return jsonify(response_data), 400

    # Generate the response data
    response_data = {
        "status": "success",
        "data": {
            "wallet": {
                "id": balance_data.id,
                "owned_by": balance_data.owned_by,
                "status": balance_data.status,
                "enabled_at": balance_data.enabled_at,
                "balance": balance_data.balance
            }
        }
    }

    return jsonify(response_data), 200


# view transactions

@app.route('/api/v1/wallet/transactions', methods=['GET'])
@utils.authenticate_token
def handle_view_transactions_request(customer_xid):
    response_data = {
        "status": "success"
    }

    return jsonify(response_data), 200