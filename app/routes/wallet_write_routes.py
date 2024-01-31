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

    # retrieve existing db
    balance_data = wallet_repositories.Balance(
        owned_by=customer_xid
    ).get_balance_from_customer_xid(customer_xid)


    # error checking

    error = ''

    if balance_data:
        if (request.method == 'POST') and (balance_data.status == 'enabled'):
            error = 'Already enabled'
        elif (request.method == 'PATCH') and (balance_data.status == 'disabled'):
            error = 'Already disabled'
    else:
        if request.method == 'PATCH':
            error = 'Wallet not found'
    
    if error != '':
        return jsonify({
            "status": "fail",
            "data": {
                "error": error
            }
        }), 400
    
    if balance_data:
        if (request.method == 'POST'):
            balance_data = balance_data.enable_wallet()
        elif (request.method == 'PATCH'):
            is_disabled = request.form.get('is_disabled')
            if not ((is_disabled is not None) and (is_disabled.lower() == 'true')):
                return jsonify({
                    "status": "fail",
                    "data": {
                        "error": "To disable, flag must be provided"
                    }
                }), 400

            balance_data = balance_data.disable_wallet()
    else:
        # initialize balance if record have not exist
        balance_data = wallet_repositories.Balance(
            id = uuid.uuid4(),
            owned_by = customer_xid,
            status = 'enabled',
            enabled_at = datetime.now(),
            disabled_at = None,
            balance = 0
        )
        balance_data.init_balance()

    wallet_data = {
        "id": balance_data.id,
        "owned_by": balance_data.owned_by,
        "status": balance_data.status,
        "balance": balance_data.balance
    }

    if (request.method == 'POST'):
        wallet_data["enabled_at"] = balance_data.enabled_at
    elif (request.method == 'PATCH'):
        wallet_data["disabled_at"] = balance_data.disabled_at

    response_data = {
        "status": "success",
        "data": {
            "wallet": wallet_data
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