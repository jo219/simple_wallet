from app import app
from flask import request, jsonify

import app.utils as utils

from app.repositories import wallet_repositories

import uuid
from datetime import datetime


# (dis/en)able wallet

@app.route('/api/v1/wallet', methods=['POST', 'PATCH'])
@utils.authenticate_token
def handle_activate_wallet_request(customer_xid):

    balance_data = wallet_repositories.Balance(
        owned_by=customer_xid
    ).get_balance_from_customer_xid(customer_xid)

    if balance_data and (balance_data.status == 'enabled'):
        response_data = {
            "status": "success",
            "data": {
                "error": "Already enabled"
            }
        }

        return jsonify(response_data), 400
    
    # initialize balance if record have not exist
    if not balance_data:
        balance_data = wallet_repositories.Balance(
            id = uuid.uuid4(),
            owned_by = customer_xid,
            status = 'enabled',
            enabled_at = datetime.now(),
            disabled_at = None,
            balance = 0
        )
        balance_data.init_balance()

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

    return jsonify(response_data), 201
        

# deposits

@app.route('/api/v1/wallet/deposits', methods=['POST'])
@utils.authenticate_token
def handle_deposits_wallet_request(customer_xid):
    response_data = {
        "status": "success"
    }

    return jsonify(response_data), 200


# withdrawals

@app.route('/api/v1/wallet/withdrawals', methods=['POST'])
@utils.authenticate_token
def handle_withdrawals_wallet_request(customer_xid):
    response_data = {
        "status": "success"
    }

    return jsonify(response_data), 200